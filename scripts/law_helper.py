"""法律 PDF 摄入辅助脚本集。

子命令：
  extract  提取 PDF 全文并去空白（法律 PDF 单字间常插空格，不去则无法正则匹配条文）
  verify   对照修正案原文核对指定条文是否存在
  lint     扫描页面常见问题（乱码/占位符/中英混排）

用法示例：
  python scripts/law_helper.py extract <pdf_path> <out_txt>
  python scripts/law_helper.py lint <wiki_dir>
"""

import re
import sys


# ---------- extract ----------

def extract(pdf_path, out_txt):
    """提取 PDF 全文并去除所有空白，输出单行文本便于正则定位条文。"""
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or '')
        except Exception:
            pages.append('')
    full = re.sub(r'\s+', '', '\n'.join(pages))
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write(full)
    print(f'pages={len(reader.pages)} chars={len(full)} -> {out_txt}')


# ---------- verify ----------

# 中文数字转阿拉伯数字，用于比较条文序号
CN = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
      '六': 6, '七': 7, '八': 8, '九': 9}


def cn_to_int(s):
    """把 '三百九十三' 转为 393。仅支持到千位，覆盖法条编号范围。"""
    s = s.strip()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    total, section, number = 0, 0, 0
    units = {'十': 10, '百': 100, '千': 1000}
    for ch in s:
        if ch in CN:
            number = CN[ch]
        elif ch in units:
            unit = units[ch]
            if number == 0:
                number = 1
            section += number * unit
            number = 0
        else:
            return None
    return total + section + number


def verify(text_path, articles):
    """检查每条条文是否存在于提取文本中，输出命中片段供人工核对原文。

    articles形如 ['第三百八十七条', '第一百一十四条']。
    本脚本只回答「这条在不在原文里、在哪个位置、首句是什么」，
    不判断内容对错——内容仍须人工比对。
    """
    text = open(text_path, encoding='utf-8').read()
    for art in articles:
        pos = text.find(art)
        if pos < 0:
            print(f'[缺失] {art} —— 原文未找到，检查条号或分则/目录区混淆')
        else:
            print(f'[命中] {art} @{pos}')
            print(f'       {text[pos:pos + 120]}')


def diff_articles(old_txt, new_txt, articles):
    """对比修正案前后同一批条文的文本，输出并排片段。

    用于修正案摄入时制作「修改前后对比表」。修正案原文通常以
    「将刑法第X条修改为："……"」的形式出现，需人工截取。
    """
    old = open(old_txt, encoding='utf-8').read()
    new = open(new_txt, encoding='utf-8').read()
    for art in articles:
        print(f'=== {art} ===')
        i = old.find(art)
        print('  旧:', old[i:i + 160] if i >= 0 else '(旧文本中未找到)')
        j = new.find(art)
        print('  新:', new[j:j + 160] if j >= 0 else '(修正案原文中未直接出现该条号)')
        print()


# ---------- lint ----------

CJK = r'\u4e00-\u9fff'


def lint(wiki_dir):
    """扫描目录下的 md 文件，报告乱码、占位符、中英混排。"""
    import glob
    import os

    issues = 0
    for path in glob.glob(os.path.join(wiki_dir, '**', '*.md'), recursive=True):
        name = os.path.basename(path)
        text = open(path, encoding='utf-8').read()

        for m in re.finditer(r'\ufffd+', text):
            ctx = text[max(0, m.start() - 25):m.end() + 15]
            print(f'[乱码] {name}: {ctx!r}')
            issues += 1

        for m in re.finditer(rf'第[Xx0-9]+[章节条]', text):
            print(f'[占位符?] {name}: {m.group(0)}  <- 需人工判断，'
                  f'正常的「第393条」也会命中')
            issues += 1

        for m in re.finditer(rf'[{CJK}][A-Za-z]{{3,}}|[A-Za-z]{{3,}}[{CJK}]', text):
            print(f'[中英混排] {name}: {m.group(0)!r}')
            issues += 1

    print(f'--- 合计命中 {issues} 处（占位符项多为误报，须人工判断）---')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == 'extract':
        extract(sys.argv[2], sys.argv[3])
    elif cmd == 'verify':
        verify(sys.argv[2], sys.argv[3:])
    elif cmd == 'diff':
        diff_articles(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif cmd == 'lint':
        lint(sys.argv[2])
    else:
        print(f'未知子命令: {cmd}')


if __name__ == '__main__':
    main()

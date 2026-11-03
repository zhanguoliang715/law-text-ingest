# law-text-ingest

**把法律 PDF 收进知识库，保证条号不错、版本不旧。法律资料和普通文章的要求不一样：条文原文就是唯一标准答案，条号错一位整篇作废。**

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB)
![Dependencies](https://img.shields.io/badge/pip%20install-0%20个依赖-2E7D32)
![License](https://img.shields.io/badge/license-MIT-yellow)
![spec](https://img.shields.io/badge/agentskills.io-spec%20valid-2E7D32)

## 为什么法律资料要单独一套流程

同样是"读一份 PDF 写摘要"，法律文本和文章差在三处：

| | 文章 / 教程 | 法律文本 |
|---|---|---|
| 事实对错 | 无法判定，只能标"作者观点" | **可判定**——条文原文即唯一答案 |
| 条号 | 不适用 | **定位坐标，错则全错** |
| 自检强度 | 抽查引文 | **逐条回原文核对** |

所以这个技能的产出不是"一份摘要"，而是**一份能被复核的收录记录**：结构从哪来、每条引文对应原文哪一段、哪些地方原文没提供。

## 它做三件事

1. **判版本时效**——先确认手上是哪一版，有没有更新的修正案。判"最新"只认立法机关动态与主席令，**不用转载全文倒推**（转载站常滞后半年）。
2. **脚本提取编章结构**——编 / 章 / 节 / 条的位置不靠肉眼数，用 `scripts/law_helper.py` 从 PDF 文本抽，避免手抄错层。
3. **逐条核对留痕**——每条引文都要能指回原文位置；找不到出处的标「原文未提供」，不猜、不补。

## 安装（三种方式，按推荐顺序）

### 1. 一条命令装进所有 Agent（推荐，已实测）

```bash
npx skills add zhanguoliang715/law-text-ingest
```

装好后会同时挂到 Codex、Cursor、Amp、Antigravity、Claude Code 等 20+ 个 Agent 上，不用逐个配。

### 2. 作为 Claude Code 插件（已实测）

```bash
claude plugin marketplace add zhanguoliang715/law-text-ingest
claude plugin install law-text-ingest@law-text-ingest
```

### 3. 手动拷目录

```bash
git clone https://github.com/zhanguoliang715/law-text-ingest.git
```

> **本机 git 报 `CRYPT_E_NO_REVOCATION_CHECK` 时**（证书吊销列表查不到），在命令前加 `GIT_SSL_NO_VERIFY=1`。
> 这是本机 TLS 配置问题，与仓库无关，换台机器通常直接可用。

## English

Ingest Chinese law PDFs into a wiki without breaking article numbering or version currency. Script-extracted structure plus article-by-article verification.

```bash
npx skills add zhanguoliang715/law-text-ingest
```

## 上手

```bash
git clone https://github.com/zhanguoliang715/law-text-ingest.git
cp -r law-text-ingest ~/.workbuddy/skills/
python ~/.workbuddy/skills/law-text-ingest/scripts/law_helper.py --help
```

然后把 PDF 丢给 Agent，说明"按 law-text-ingest 的流程收录这部法"。

## 边界（用之前务必看）

- **只处理文本型 PDF**。扫描件要先 OCR，本技能不含 OCR。
- **不替你解释法条**，只保证"抄得对、版本对"。体系解释、竞合判断是法律专业工作。
- **不做跨法条推理**，不下"应该适用哪一条"的结论。
- 遇到汇编版同条号两套刑档，**照录不取舍**，把冲突标出来——取舍是人的事。

## 最常见的三个错

1. **用转载文判断"最新"**。看到的是旧版全文，结论全错。
2. **条号手抄**。第 264 条写成第 246 条，整篇作废。
3. **把"没查到修正案"当成"没有修正案"**。否定结论只能覆盖你实际查过的范围，查不到要写清"取到几条 / 总量多少"。

## 文档

| 想看什么 | 去哪 |
|---|---|
| 第一次用，怎么一步步做 | [docs/新手手册.md](docs/新手手册.md) |
| 判定逻辑、失败模式、已知限制 | [docs/技术文档.md](docs/技术文档.md) |
| 完整规则原文 | [SKILL.md](SKILL.md) |

## License

[MIT](LICENSE)

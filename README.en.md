# law-text-ingest

[简体中文](README.md) | **English**

**Ingest Chinese law PDFs into a wiki without breaking article numbering or version currency. In legal text the statute is the only ground truth, and one wrong article number invalidates the whole page.**

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB)
![Dependencies](https://img.shields.io/badge/pip%20install-0%20dependencies-2E7D32)
![License](https://img.shields.io/badge/license-MIT-yellow)
![spec](https://img.shields.io/badge/agentskills.io-spec%20valid-2E7D32)

## Install

```bash
npx skills add zhanguoliang715/law-text-ingest
```

Or as a Claude Code plugin:

```bash
claude plugin marketplace add zhanguoliang715/law-text-ingest
claude plugin install law-text-ingest@law-text-ingest
```

## Why legal text needs its own workflow

Same task — "read a PDF, write a summary" — but three things differ:

| | Articles / tutorials | Legal text |
|---|---|---|
| Factual correctness | undecidable, mark as "author's view" | **decidable** — the statute is the only answer |
| Article numbers | not applicable | **a coordinate; one digit off invalidates everything** |
| Verification | spot-check quotes | **article by article, back to the source** |

So the output is not "a summary" but **a record someone else can audit**: where the structure came from, which source line each quote maps to, and what the source did not provide.

## What it does

1. **Currency check** — establish which version this is and whether a newer amendment exists. "Latest" is judged only from the legislature's own publications, never inferred from a reposted full text (mirrors often lag by months).
2. **Script-extracted structure** — part / chapter / section / article positions are extracted by `scripts/law_helper.py`, not counted by eye.
3. **Article-by-article verification** — every quote must point back to a source location. If the source does not contain it, mark it as missing; never guess, never fill in.

## Boundaries

- **Text-layer PDFs only.** Scanned documents need OCR first; OCR is out of scope.
- **Does not interpret statutes.** It guarantees the copying and the version, not the legal reading.
- **No cross-article reasoning.** Which article applies is a legal judgement, not a text-processing task.
- **Conflicting compiled editions are recorded as-is**, with the conflict flagged — the choice belongs to a human.

## Docs

- [Beginner handbook](docs/新手手册.md)
- [Technical doc](docs/技术文档.md)
- [SKILL.md](SKILL.md)

## License

MIT.

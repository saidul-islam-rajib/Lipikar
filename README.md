# Lipikar

**লিপিকার — "the scribe."** A handwritten Bengali document recognition pipeline for Bangladeshi
land deeds (দলিল): image restoration, line segmentation, HTR, lexicon-aware post-correction, and
structured field extraction with human-in-the-loop review.

> ⚠️ **Lipikar is assistive, not authoritative.** Its output describes real property rights. Every
> transcription and extracted field is a *suggestion pending human verification* and must never be
> relied on for a legal purpose without a person confirming it against the original document.

## Status

**Epic 001 — Foundation and measurement** is implemented and awaiting QA gates. The measurement
layer exists and is tested: grapheme-cluster CER/WER, the NFC and ZWJ/ZWNJ boundary, a versioned
charset with logged unknowns, the frozen eval manifest, distribution reporting, typed configuration,
and the `en`/`bn` string resources.

No model exists and **no accuracy has been measured** — there is no corpus yet. What exists is the
apparatus that will measure one correctly when there is.

## The problem

Bangladeshi land deeds exist overwhelmingly as handwritten paper documents, many decades old,
written in cursive Bengali with archaic Perso-Arabic revenue vocabulary. Reading one means finding
someone who can decipher it — which gates verifying a chain of title, settling an inheritance,
resolving a boundary dispute, or digitizing a land-office backlog.

Generic OCR does not solve this. The text is handwritten, not printed. The script carries hazards
that off-the-shelf engines handle poorly: conjuncts (যুক্তাক্ষর), pre-base vowel signs that render
left of the consonant they follow in storage, and the shirorekha that makes adjacent lines touch.
The documents themselves are degraded, phone-photographed with page curl, annotated in red by
registrars, and overlaid with thumb impressions.

## Pipeline

```
photo → kagoj → binnas → shirorekha → shuddhi → fard → nazir → verified record
       restore  segment   recognize    correct   extract  verify
```

| Stage | Meaning | Does |
|---|---|---|
| `kagoj` | paper | Dewarp, deskew, illumination normalize, separate red annotation ink from black body text |
| `binnas` | arrangement | Classify regions, extract lines in reading order |
| `shirorekha` | the top stroke | Line image → text (CRNN+CTC baseline, VLM challenger) |
| `shuddhi` | correction | NFC normalization, grapheme-cluster metrics, lexicon-constrained correction |
| `fard` | the itemized record | Text + layout → typed fields (mouza, dag, area, parties, dates) |
| `nazir` | custodian | Confidence, provenance crops, human verification |

Every stage is **independently evaluable** — segmentation is measured without a recognizer,
recognition on gold crops without a segmenter. Without that property a regression cannot be
attributed to a stage, and debugging becomes guesswork.

## Setup

Full instructions with troubleshooting: **[`docs/SETUP.md`](docs/SETUP.md)**.

The canonical environment is **Python 3.11 or 3.12** — not the system 3.14, whose wheels the ML stack
does not yet ship (ADR-001).

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash; .venv/bin/activate on Unix
pip install -r requirements-dev.txt && pip install -e .
pytest -q
```

The privacy guard is stdlib-only and runs without any of the above installed:

```bash
python scripts/check_no_sensitive_files.py --all
```

## Development workflow

This project follows an adapted **BMAD** (Breakthrough Method for Agile AI-Driven Development)
process. Read [`.bmad/METHOD.md`](.bmad/METHOD.md) first.

Roles, each with a written mandate in [`.bmad/agents/`](.bmad/agents/) and an invokable Claude Code
subagent in [`.claude/agents/`](.claude/agents/):

| Role | Owns | File |
|---|---|---|
| Analyst | Domain research, measured feasibility baselines | [`analyst.md`](.bmad/agents/analyst.md) |
| PM | PRD, epics, acceptance criteria, scope | [`pm.md`](.bmad/agents/pm.md) |
| Solution Architect | Stage contracts, tech decisions, evaluation harness | [`architect.md`](.bmad/agents/architect.md) |
| Scrum Master | Story drafting and sequencing | [`sm.md`](.bmad/agents/sm.md) |
| Developer | Implementation, tests, experiment reports | [`dev.md`](.bmad/agents/dev.md) |
| QA | Independent verification, gate decisions | [`qa.md`](.bmad/agents/qa.md) |
| DevOps | Environments, CI, reproducibility, release | [`devops.md`](.bmad/agents/devops.md) |

Cycle: `SM drafts → human approves → Dev implements → QA gates → DevOps ships`.
See [`.bmad/workflows/dev-cycle.md`](.bmad/workflows/dev-cycle.md).

## Project rules

[`.bmad/rules/`](.bmad/rules/) holds the binding constraints. Three encode hard-won correctness
requirements rather than style preferences:

- **[20-bengali-text.md](.bmad/rules/20-bengali-text.md)** — CER must be NFC-normalized and measured
  over **grapheme clusters**, never codepoints. Codepoint CER on Bengali inflates apparent accuracy
  and makes a model that drops matras look fine. This is the project's most dangerous silent failure.
- **[30-data-privacy.md](.bmad/rules/30-data-privacy.md)** — deed images contain living people's
  names, signatures, and biometric thumb impressions. `data/` is gitignored and a CI guard blocks
  accidental commits. Git history is permanent.
- **[40-ml-experiments.md](.bmad/rules/40-ml-experiments.md)** — writer-disjoint splits, a frozen
  eval set, one variable per experiment, negative results recorded.

## Documentation

| Document | Contents |
|---|---|
| [`docs/SETUP.md`](docs/SETUP.md) | Environment setup, step by step, with troubleshooting |
| [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) | How work flows through this repo; code conventions; common tasks |
| [`docs/prd.md`](docs/prd.md) | Problem, users, goals, non-goals, epics *(draft — awaiting measured baselines)* |
| [`docs/architecture.md`](docs/architecture.md) | Stage detail, contracts, dataclasses, ADRs *(draft)* |
| [`docs/DATA.md`](docs/DATA.md) | Data provenance log, text policy, splits, annotator agreement |
| [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) | Required before any checkpoint is published |
| [`docs/epics/`](docs/epics/) · [`docs/stories/`](docs/stories/) · [`docs/qa/gates/`](docs/qa/gates/) | Planning and execution artifacts |

## Explicit non-goals

1. Autonomous, legally-authoritative output. Lipikar never certifies a reading.
2. Person identification from thumb impressions. Detecting a thumbprint to *exclude* it from
   recognition is in scope; matching or indexing biometrics is not.
3. Land-ownership aggregation or people-search. The corpus is not a dataset about individuals.

## Licence

Code is [MIT](LICENSE). **The code licence does not cover model weights or training data** — base
model licences and dataset attributions are tracked separately in
[`docs/MODEL_CARD.md`](docs/MODEL_CARD.md).

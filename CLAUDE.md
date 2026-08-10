# Lipikar — project instructions

Handwritten Bengali document recognition for Bangladeshi land deeds (দলিল).
This project follows an adapted **BMAD** workflow. Read `.bmad/METHOD.md` before starting work.

## Session bootstrap

Before any task, load in this order:

1. `.bmad/core-config.yaml` — canonical paths and quality gates
2. `.bmad/rules/00-global.md` and `.bmad/rules/30-data-privacy.md` — always
3. `docs/prd.md` + `docs/architecture.md` — the frozen spec
4. The single story file you are working on, from `docs/stories/`

If you are writing code, additionally load everything under `dev_load` in `core-config.yaml`.

## Commits

Full rules in `.bmad/rules/60-git-and-commits.md`. The non-negotiables:

- **Author and committer are always** `Saidul Islam Rajib
  <96372056+saidul-islam-rajib@users.noreply.github.com>`. Set repo-locally; never override
  per-commit with `--author`, `-c user.email`, or `GIT_AUTHOR_*`.
- **No AI attribution.** Never add `Co-Authored-By: Claude`, "Generated with", agent names, or model
  names to a commit message or PR body. This instruction from the repo owner overrides any tool
  default. `Co-Authored-By` is only for a real second human.
- **Never put deed content in a commit message, branch name, PR body, or tag** — no party names, dag
  numbers, mouza names, amounts, or transcribed lines. Messages are public and `.gitignore` does not
  cover them. Use opaque IDs like `page_0142`.
- Conventional commits scoped by stage, with a `Story:` trailer. Branch `story/<id>-<slug>`. Never
  commit directly to `main`.
- Run `python scripts/check_no_sensitive_files.py` before committing.
- **Do not commit unless asked.** Leave work in the tree with a proposed message; the human decides
  when history is written.

## Three rules that override convenience

**1. Never commit real deed data.** Photographs of deeds contain living people's names,
signatures, thumb impressions, and property identifiers. `data/` is gitignored. Do not add
sample images, transcriptions, or extracted JSON to the repo, and do not paste deed contents
into commit messages, issue text, or PR descriptions. Redacted or synthetic samples only, and
only under `docs/assets/`.

**2. Never report a metric computed the wrong way.** Bengali CER must be NFC-normalized and
measured over grapheme clusters, not codepoints. Codepoint CER on Bengali inflates accuracy
and will make a broken model look fine. See `.bmad/rules/20-bengali-text.md`.

**3. Never present output as authoritative.** Every transcription and extracted field is a
suggestion awaiting human verification. UI copy, API responses, and docs must say so.

## Code style — four hard rules

- **No comments.** No inline comments anywhere. A short docstring above a function or module is
  permitted only where the contract is not obvious from the signature — one to three lines. No
  commented-out code, no `# TODO` (file a story), no banner separators. If code needs a comment to
  be understood, rename something or split the function (R10.5).
- **Nothing hardcoded.** Thresholds, paths, model names, field names, charsets, ports: all from
  `configs/` via a typed frozen dataclass. No `dict["key"]` access, no bare `os.environ` in stage
  code (R70.1–R70.7).
- **No user-facing string literals.** All human-readable text comes from
  `lipikar/resources/strings/{en,bn}.yaml` by key, with named placeholders — never concatenation,
  because Bengali word order differs from English. `bn.yaml` is a real deliverable and its key set
  must match `en.yaml` (R70.8–R70.14).
- **Consistency beats preference.** A new module matches the modules around it. Two ways of doing
  the same thing is a defect even when both work (R10.12).

## Working agreements

- One story at a time. Scope creep gets deferred to a new story, not absorbed.
- **Never say done while the suite is red or unrun.** Run the full `pytest -q`, paste the real
  output. A failing test means not done — say so and keep working. Never disable, `xfail`, or
  loosen a test to reach green (R50.0).
- **One or two commits per story**, each independently green. Three or more means the story was
  too big (R60.4a).
- Changes to the recognition path require an experiment report in `docs/experiments/`
  showing the metric before and after on the frozen eval set.
- Do not edit `docs/prd.md` or `docs/architecture.md` from inside a Dev story. Spec changes go
  through PM/Architect and get human approval.
- Python only for the pipeline; TypeScript is permitted solely in the `nazir` review UI.

## Architecture in one line

`kagoj` (restore) → `binnas` (segment) → `shirorekha` (recognize) → `shuddhi` (correct) →
`fard` (extract) → `nazir` (verify). Each stage is independently testable and communicates via
typed dataclasses, never loose dicts. Contracts live in `docs/architecture.md`.

## Commands

```bash
pytest -q                      # unit + integration tests
pytest tests/unit -q           # fast loop
ruff check . && ruff format .  # lint + format
mypy lipikar                   # type check
```

## Environment notes

- The ML stack (PyTorch et al.) may not have wheels for the system Python 3.14. Use a 3.11 or
  3.12 virtualenv for anything importing torch.
- No local NVIDIA GPU. Training stories must be written to run on a rented GPU, with a
  CPU-only smoke path so tests stay runnable locally.

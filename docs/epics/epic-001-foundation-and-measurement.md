# Epic 001 — Foundation and measurement

**Status:** planned · **Owner:** PM (Anwar) · **Depends on:** none

## Outcome
Lipikar can measure Bengali transcription accuracy **correctly** — NFC-normalized, grapheme-cluster
based, on a frozen and versioned evaluation set — and the repo has a working, tested, CPU-only
skeleton for every pipeline stage.

## Why now
This epic precedes all model work for one reason: **a wrong metric is worse than no metric.**
Codepoint-based CER on Bengali makes a model that systematically drops matras look accurate. If any
model work happens before the measurement layer is correct and tested, every number produced up to
that point has to be thrown away, along with the decisions made from it.

It also front-loads the cheapest risk reduction available — the text-handling rules in
`.bmad/rules/20-bengali-text.md` become executable and enforced rather than aspirational.

## Scope
- Grapheme-cluster CER and WER implementation with the adversarial test set
- Text normalization boundary: NFC, ZWJ/ZWNJ policy, danda handling
- Versioned charset config and unknown-character handling with codepoint logging
- Frozen eval manifest format (page IDs + hashes) and its loader
- Metric reporting: mean, median, p90, worst-N, sample size
- Package skeleton for all six stages with typed contracts and CPU smoke paths
- Dev environment: pinned 3.11/3.12, ruff, mypy, pytest, CI with the privacy guard

## Out of scope
- Any model, any training, any inference — Epic 002 onward
- Real data acquisition — Epic 003
- Actual image processing implementations — Epic 004 onward

## Acceptance criteria

1. `lipikar.shuddhi.metrics.grapheme_cer` computes CER over extended grapheme clusters using
   `regex.findall(r"\X", ...)`, and a test proves it differs from codepoint CER on a Bengali
   conjunct string.
2. All text entering the system is NFC-normalized at a single, tested boundary; an NFD input and
   its NFC twin compare equal through the real code path.
3. The R20.9 adversarial set is covered by tests: conjunct, pre-base vowel sign, mixed Bengali and
   ASCII digits, NFC/NFD equality, ZWJ stripping, danda.
4. The charset loads from a versioned file in `configs/`; an out-of-charset character maps to
   `<unk>` **and** its codepoint is logged.
5. A frozen eval manifest can be written, loaded, and integrity-checked; modifying it is detectable.
6. Metric reporting emits mean, median, p90, worst-N and sample size — never a bare mean.
7. `pytest -q` passes on CPU with no corpus and no GPU present; CI runs it plus the privacy guard,
   and the privacy guard fails hard on a test commit adding a file under `data/`.

## How this epic is measured
Not by a model number — by the metric layer itself being demonstrably correct. The proof artifact is
AC1's test: the same string scoring differently under cluster CER than codepoint CER, with the
cluster number being the defensible one. Plus a green CI run and a demonstrated privacy-guard
rejection.

## Stories

| ID | Title | Intent (one line) | Stage | Depends on | Status |
|---|---|---|---|---|---|
| 1.1 | Dev environment and toolchain | Pinned 3.11/3.12 env, ruff/mypy/pytest, pyproject wired | infra | — | Draft |
| 1.2 | Text normalization boundary | NFC + ZWJ/ZWNJ policy in one tested place | shuddhi | 1.1 | Draft |
| 1.3 | Grapheme-cluster CER and WER | The correct metric, with the adversarial test set | shuddhi | 1.2 | Draft |
| 1.4 | Versioned charset and unknown handling | Alphabet from config; `<unk>` with codepoint logging | shirorekha | 1.2 | Draft |
| 1.5 | Frozen eval manifest | Write, load, integrity-check the eval set definition | infra | 1.3 | Draft |
| 1.6 | Metric reporting | Distribution reporting, never a bare mean | shuddhi | 1.3, 1.5 | Draft |
| 1.7 | CI and the privacy guard | Hard-failing guard against committing deed data | infra | 1.1 | Draft |

Only story 1.1 should be drafted in full initially. The SM drafts each subsequent story after the
previous one lands, per `.bmad/agents/sm.md`.

## Risks
| Risk | Mitigation |
|---|---|
| The team treats the metric layer as boilerplate and rushes it | QA auto-FAILs any codepoint measurement (R20.2) |
| ZWJ/ZWNJ policy chosen inconsistently across stories | Policy fixed in story 1.2 and recorded in `docs/DATA.md` |
| Charset discovered incomplete after training starts | Charset is a versioned config with logged unknowns from day one |

## Retrospective
*(Filled in at epic close by SM.)*

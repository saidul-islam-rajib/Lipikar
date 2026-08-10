# Epic 001 — Foundation and measurement

**Status:** in review · **Owner:** PM (Anwar) · **Depends on:** none

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
- The Rule 70 layer: typed config loading from `configs/*.yaml`, and the `en`/`bn` string resources
  with their key-parity test

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
| 1.1 | Dev environment and toolchain | Pinned 3.11/3.12 env, ruff/mypy/pytest, pyproject wired | infra | — | Review |
| 1.2 | Typed config loader | Rule 70 Part A: `configs/*.yaml` → frozen dataclass, unknown keys rejected | infra | 1.1 | Review |
| 1.3 | Text normalization boundary | NFC + ZWJ/ZWNJ policy in one tested place | shuddhi | 1.1 | Review |
| 1.4 | Grapheme-cluster CER and WER | The correct metric, with the adversarial test set | shuddhi | 1.3 | Review |
| 1.5 | Versioned charset and unknown handling | Alphabet from config; `<unk>` with codepoint logging | shirorekha | 1.2, 1.3 | Review |
| 1.6 | Frozen eval manifest | Write, load, integrity-check the eval set definition | infra | 1.2, 1.4 | Review |
| 1.7 | Metric reporting | Distribution reporting, never a bare mean | shuddhi | 1.4, 1.6 | Review |
| 1.8 | CI and the privacy guard | Hard-failing guard against committing deed data | infra | 1.1 | Review |
| 1.9 | String resources and locale parity | Rule 70 Part B: `en.yaml`/`bn.yaml` + identical-key-set test | infra | 1.2 | Review |
| 1.10 | Stage contracts and region kinds | Architecture §3 dataclasses; region kinds as a configured closed set | infra | 1.2 | Review |

The SM drafts each story in full only after the previous one lands, per `.bmad/agents/sm.md`.

**1.10 was added** because the epic's outcome names a tested skeleton for every stage and
`docs/architecture.md` §3 specifies the dataclasses stages exchange, but no story owned them.

**1.2 and 1.9 were added after the original draft.** Rule 70 is binding and its Part A is a hard
dependency of 1.5, 1.6 and 1.7 — every one of them reads a threshold, path, or charset from
`configs/`, and R70.1 forbids reaching those through `dict["key"]`. Without an owning story the
loader would have been improvised inside whichever story hit it first, in three different shapes,
which R10.12 calls a defect. Part B (1.9) is genuinely less urgent — R70.15 exempts log messages, so
1.5's `<unk>` codepoint logging does not block on it — but it is sequenced inside this epic anyway
so that `bn.yaml` is built as a real deliverable rather than retrofitted at Epic 009 (R70.9).

## Risks
| Risk | Mitigation |
|---|---|
| The team treats the metric layer as boilerplate and rushes it | QA auto-FAILs any codepoint measurement (R20.2) |
| ZWJ/ZWNJ policy chosen inconsistently across stories | Policy fixed in story 1.2 and recorded in `docs/DATA.md` |
| Charset discovered incomplete after training starts | Charset is a versioned config with logged unknowns from day one |

## Retrospective
*(Filled in at epic close by SM.)*

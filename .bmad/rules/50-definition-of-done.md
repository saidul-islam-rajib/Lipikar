# Rule 50 — Definition of Done

A story is Done only when **every** applicable line below is true and evidenced in the story's
completion notes. "Applicable" is judged by QA, not by the implementer.

## R50.0 The green-suite precondition

**Nothing is reported as done, finished, complete, or working while the test suite is red or
unrun.** This is absolute and precedes every other item.

- Run the full suite, not a subset, and not only the tests you added.
- If any test fails, the work is not done. Say so, paste the failure, and keep working or escalate.
- "Tests pass" without pasted output is an unsupported claim and is treated as a breach (R00.3).
- A test skipped because the environment lacks something counts as not run — name it explicitly.
- Never disable, `xfail`, delete, or loosen a failing test to reach green. If a test is genuinely
  wrong, that is a finding to raise, not a thing to silently fix.

## Universal

- [ ] Every acceptance criterion in the story is individually addressed, and the notes say where
- [ ] **The full suite is green** — `pytest -q` run in its entirety, output pasted (R50.0)
- [ ] `ruff check .` and `mypy lipikar` clean, or deviations justified with a reason
- [ ] No inline comments; short docstrings only where the contract is not obvious (R10.5)
- [ ] No hardcoded values — thresholds, paths, model names, field names all in `configs/` (R70.2)
- [ ] No user-facing string literals in code; all via string resources, `en` and `bn` in sync (R70.8, R70.13)
- [ ] Conventions match surrounding modules — one way of doing each thing (R10.12)
- [ ] No secrets, no credentials, no real deed content added to the repo
- [ ] Changes confined to the story's scope; discovered work filed as new `Draft` stories
- [ ] Story file updated: status, file list, completion notes, debug log

## If the story touches text handling

- [ ] NFC normalization applied at the boundary (R20.1)
- [ ] Any character-level measurement uses grapheme clusters (R20.2)
- [ ] Adversarial text tests present: conjunct, pre-base vowel sign, mixed digits, NFC/NFD pair,
      ZWJ stripping, danda (R20.9)
- [ ] No transliteration in stored data, no visual-order storage (R20.3, R20.8)

## If the story touches the recognition path

- [ ] Experiment report committed under `docs/experiments/` from the template
- [ ] Metric reported on the frozen eval set, with sample size and distribution, not just a mean
- [ ] Compared against the recorded baseline
- [ ] Seed, config path, data version, commit hash, and hardware recorded
- [ ] Ten worst predictions reviewed and failure modes named (R40.7)

## If the story touches data

- [ ] `docs/DATA.md` updated with provenance for any new batch (R30.3)
- [ ] Splits writer-disjoint and verified, not assumed (R40.2)
- [ ] No real data committed; samples redacted or synthetic (R30.1, R30.2)
- [ ] Any new external service that receives deed content was authorized by the human (R30.4)

## If the story touches user-facing output

- [ ] Output is presented as a suggestion requiring human verification (R00.6)
- [ ] Confidence, if shown, is calibrated and has a reliability diagram (R40.8)
- [ ] Bengali renders correctly, including conjuncts and pre-base vowel signs, in the target surface

## Gate

QA writes `docs/qa/gates/<story-id>.md` with one decision:

| Decision | Meaning |
|---|---|
| **PASS** | All applicable items true. Story moves to Done. |
| **CONCERNS** | Ships, but named follow-up stories are created and linked. |
| **FAIL** | Returns to Dev with specific, reproducible findings. |
| **WAIVED** | Human explicitly accepted a gap. The human's reason is recorded verbatim. |

Only QA sets the gate. Only the human may WAIVE.

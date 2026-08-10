# Checklist — Dev (self-check before handing to QA)

Answer honestly. An unchecked box that you **state** is fine; an unchecked box you hide is a
process breach. QA will find it, and finding it costs everyone a cycle.

## Story fidelity
- [ ] Every acceptance criterion addressed, and the notes say where (file:line)
- [ ] Nothing implemented that the story did not ask for
- [ ] Discovered work filed as new `Draft` stories, listed by ID in the notes
- [ ] No acceptance criterion reinterpreted to be easier

## Evidence
- [ ] `pytest -q` actually run; real output pasted (failures included if any remain)
- [ ] `ruff check .` and `mypy lipikar` actually run; results recorded
- [ ] No claim in the notes that I did not verify

## Code
- [ ] Frozen dataclasses between stages, not dicts (R10.2)
- [ ] Constants from config, none inline (R10.4)
- [ ] Contract docstrings: units, dtype, range, coordinate space, raises (R10.9)
- [ ] No bare `except`; no silently swallowed decode or normalization error (R10.5)
- [ ] No deed text logged at INFO (R10.6)
- [ ] Runs on CPU; tests need no GPU and no corpus

## Text handling (if applicable)
- [ ] NFC normalization at the boundary (R20.1)
- [ ] Any character measurement uses `regex.findall(r"\X", ...)` (R20.2)
- [ ] No character ordering derived from x-coordinates (R20.3)
- [ ] ZWJ/ZWNJ stripped per policy (R20.4)
- [ ] Out-of-charset → `<unk>` **and the codepoint is logged** (R20.5)
- [ ] Adversarial tests present: conjunct, pre-base vowel sign, mixed digits, NFC/NFD pair,
      ZWJ, danda (R20.9)

## Recognition path (if applicable)
- [ ] Experiment report written from the template
- [ ] One variable changed (R40.4)
- [ ] Metric on the frozen eval set; size and distribution reported, not a lone mean (R40.6)
- [ ] Compared against the recorded baseline
- [ ] Seed, config, data version, commit, hardware recorded
- [ ] Ten worst predictions reviewed; failure modes named (R40.7)

## Data (if applicable)
- [ ] `docs/DATA.md` updated with provenance (R30.3)
- [ ] Writer-disjointness verified by checking writer IDs, not assumed (R40.2)
- [ ] `git status` reviewed — nothing under `data/`, no images, no checkpoints staged (R30.1)

## Handoff
- [ ] Story status set to `Review`
- [ ] File list, completion notes, and debug log filled in
- [ ] I have **not** set a gate decision — that is QA's

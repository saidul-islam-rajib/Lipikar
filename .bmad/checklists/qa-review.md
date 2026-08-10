# Checklist — QA (review and gate)

Verify independently. The Dev agent's pasted output is a claim; your own run is evidence.

## Re-run it yourself
- [ ] `pytest -q` — my own output recorded in the gate file
- [ ] `ruff check .` and `mypy lipikar` — my own output
- [ ] The specific command the story named, run as written

## Acceptance criteria
- [ ] Each criterion checked individually against the code, not against the notes
- [ ] Any criterion met "in spirit" but not literally → not met
- [ ] No criterion was rewritten during implementation (diff the story file's history)

## The ten targeted checks
- [ ] 1. No codepoint-based text measurement anywhere in a metric path (R20.2) — **auto-FAIL**
- [ ] 2. NFC/NFD pair compares equal through the real code path, not a stub (R20.1)
- [ ] 3. No character ordering from x-coordinate sorting (R20.3)
- [ ] 4. Out-of-charset character → `<unk>` and the codepoint is logged, not dropped (R20.5)
- [ ] 5. Writer-disjoint splits verified by inspecting writer IDs across splits (R40.2)
- [ ] 6. Frozen eval manifest unmodified — `git diff` it (R40.1)
- [ ] 7. Nothing under `data/`, no images, no checkpoints in the diff **or history** (R30.1)
- [ ] 8. Metric on the frozen set with size and distribution, compared to baseline (R40.6)
- [ ] 9. Any user-facing confidence has a reliability diagram (R40.8)
- [ ] 10. No surface implies authoritative legal output (R00.6)

## Test quality, not test presence
- [ ] Each test would **fail** against a plausibly broken implementation
- [ ] No test asserts only `is not None`, `len() > 0`, or "did not raise"
- [ ] Edge cases from the story are actually covered
- [ ] Any test I could break by introducing a real bug without it failing → finding

## Scope and hygiene
- [ ] Changes confined to the story; no unrelated refactors smuggled in
- [ ] Discovered work was filed rather than absorbed
- [ ] Docstrings state real contracts (R10.9)
- [ ] Secrets, credentials, and personal data absent from the diff

## Gate
- [ ] Decision recorded: PASS / CONCERNS / FAIL
- [ ] Findings are specific: file, line, failure mode, suggested fix
- [ ] If CONCERNS: follow-up stories **created and linked** (a bare CONCERNS is not a decision)
- [ ] I did not fix the code myself
- [ ] I did not waive anything (human only)

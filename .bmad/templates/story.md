# Story <epic>.<story> — <Title>

**Status:** Draft | Approved | InProgress | Review | Done | Blocked
**Epic:** <epic id and title>
**Stage:** kagoj | binnas | shirorekha | shuddhi | fard | nazir | infra
**Depends on:** <story ids, or none>
**Branch:** `story/<id>-<slug>`

## Context
<Three sentences: why this story exists, what the previous story left behind, what this unlocks.>

## Acceptance criteria
<Numbered, independently verifiable, no compound criteria. Each one is something QA can check.>

1.
2.
3.

## Technical notes
<Quote the architecture inline — do not link to it. Exact module paths, exact signatures, exact
config keys, the dataclass definitions involved. The Dev agent must not need another file.>

**Files to create or modify:**
- `lipikar/<stage>/<module>.py` — <what>
- `tests/unit/test_<module>.py` — <what>
- `configs/<name>.yaml` — <what>

**Signatures:**
```python
```

## Rules that apply
<Cite rule IDs so the Dev agent knows which constraints bind here. Examples:>
- R20.1 — NFC-normalize at the boundary
- R20.2 — grapheme-cluster measurement only
- R10.2 — frozen dataclass, not a dict

## Testing requirements
- Named test cases:
- Adversarial text cases (R20.9), if text is involved: conjunct, pre-base vowel sign, mixed
  digits, NFC/NFD equality, ZWJ stripping, danda
- Command: `pytest tests/unit/test_<module>.py -q`

## Out of scope
<Explicit. This is what stops the Dev agent expanding the story.>

## Definition of Done
Rule 50 — universal section, plus: <which conditional sections apply>

---

## Dev section
*(Dev agent fills this in. SM leaves it empty.)*

**Completion notes:**

**Files changed:**

**Test run output:**
```
```

**Rule 50 self-check:**

**Deviations from story:**

**Discovered work filed:**

---

## QA section
*(QA agent fills this in. Links to `docs/qa/gates/<story-id>.md`.)*

**Gate decision:**
**Findings:**

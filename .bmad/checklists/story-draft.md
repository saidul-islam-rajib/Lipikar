# Checklist — SM (story draft quality)

Run before moving a story out of `Draft` for human approval.

## The self-sufficiency test (the one that matters)
- [ ] A Dev agent reading **only this file** could implement it — no conversation, no other doc
- [ ] Architecture facts are **quoted inline**, not linked ("see architecture.md" is a defect)
- [ ] Exact file paths, function signatures, config keys, and dataclasses are present
- [ ] No decision is left to the Dev agent that belongs to PM or Architect

## Acceptance criteria
- [ ] Numbered and independently verifiable
- [ ] No compound criteria ("does X and Y" → split into two)
- [ ] QA could check each one without asking what it means
- [ ] Copied faithfully from the epic — **not softened to fit an implementation idea**

## Scope
- [ ] One focused change; at most two pipeline stages touched
- [ ] Five or fewer acceptance criteria (more → split the story)
- [ ] "Out of scope" section is explicit and non-empty
- [ ] Dependencies on other stories listed by ID

## Testing
- [ ] Specific test cases named, not "add tests"
- [ ] The R20.9 adversarial text set required if any text handling is involved
- [ ] Exact `pytest` command given
- [ ] Tests specified can run on CPU with no corpus present

## Rules and DoD
- [ ] Applicable rule IDs cited (R20.x, R30.x, R40.x as relevant)
- [ ] The correct conditional sections of Rule 50 are named
- [ ] If the recognition path changes, an experiment report is required in the DoD

## Continuity
- [ ] Verified what the previous story **actually left in the code**, by reading it
- [ ] The repo is in a working, tested state after this story lands
- [ ] Status is `Draft`; Dev and QA sections are left empty

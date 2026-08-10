# Workflow — Development cycle (Phase B)

Repeat per story. Fast, narrow context, one story at a time.

## Sequence

```
   SM drafts ──► Human approves ──► Dev implements ──► QA gates ──► DevOps ships
                                        ▲                  │
                                        └── FAIL ──────────┘
```

### Step 1 — SM drafts the story
From the epic, into `docs/stories/<epic>.<story>.<slug>.md`. Status `Draft`.
**Exit:** `.bmad/checklists/story-draft.md` passes, and the self-sufficiency test holds — a Dev
agent reading only this file could implement it.

### Step 2 — Human approves
`Draft → Approved`. Only the human does this. Approving is where you catch a story that solves the
wrong problem, before any code is written.

### Step 3 — Dev implements
Branch `story/<id>-<slug>`. Status `InProgress`.
Implement, test, run the suite, paste real output, self-check Rule 50, write the experiment report
if the recognition path changed. Status → `Review`.
**Exit:** all acceptance criteria addressed and evidenced; discovered work filed as new stories.

### Step 4 — QA gates
Independent verification. QA re-runs everything and works its ten checks.
Writes `docs/qa/gates/<story-id>.md` with PASS / CONCERNS / FAIL.
- **FAIL** → back to Step 3 with specific findings.
- **CONCERNS** → proceed, follow-up stories created and linked.
- **PASS** → status `Done`.

### Step 5 — DevOps ships
Merge, tag if releasing, register any checkpoint with full provenance, verify health, note the
rollback. Never without a gate.

### Step 6 — Retrospective (end of epic)
SM facilitates. Three questions, answered honestly:
- Which stories were defective as written, and what made them defective?
- Where did the metric mislead us?
- What rule needs to change? (Amend `.bmad/rules/` — the rules are living documents.)

## Running it in Claude Code

Use a subagent per role so context stays isolated:

```
> Act as the SM (.bmad/agents/sm.md) and draft story 1.2 from docs/epics/epic-001-....md
> Act as Dev (.bmad/agents/dev.md) and implement approved story 1.2
> Act as QA (.bmad/agents/qa.md) and gate story 1.2
```

Isolation matters most between Dev and QA: a QA pass that inherited Dev's reasoning is not an
independent check, it is agreement.

## Anti-patterns
- Dev setting its own gate.
- QA fixing the code it just failed (findings, not patches).
- Two stories in flight in one branch.
- Changing acceptance criteria mid-story to match the implementation.
- "Tests pass" with no pasted output.

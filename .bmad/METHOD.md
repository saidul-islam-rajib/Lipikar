# How BMAD runs on Lipikar

BMAD (Breakthrough Method for Agile AI-Driven Development) splits AI-assisted work into
**named roles with narrow mandates**, so that planning artifacts stay stable while
implementation churns. This file is the operating manual for that loop on this project.

## Why the ceremony is worth it here

Lipikar is not a CRUD app. Two properties make ad-hoc prompting fail badly:

1. **The output is legally consequential.** A misread dag number propagates into a land
   record. Roles exist so that "who decided this was good enough" is always answerable.
2. **Progress is measured, not demoed.** "It looks better" is not evidence. Every change to
   the recognition path must move a number on a frozen evaluation set, or it does not land.

So this adaptation adds one artifact that stock BMAD lacks: the **experiment report**
(`.bmad/templates/experiment-report.md`). ML stories close against a measurement, not a
screenshot.

## The two phases

### Phase A — Planning (do this once, revisit rarely)

Slow, high-context, human-in-the-loop. Produces two durable documents.

| Step | Agent | Output |
|---|---|---|
| 1 | Analyst | Domain brief: deed formats, script hazards, corpus survey → `docs/prd.md` §Context |
| 2 | PM | PRD: goals, non-goals, epics, acceptance criteria → `docs/prd.md` |
| 3 | Architect | Architecture: pipeline contracts, model choices, data flow → `docs/architecture.md` |
| 4 | PM + Architect | Shard the PRD into epics under `docs/epics/` |

Planning ends when both documents pass their checklists. **Do not start coding before this.**
The whole point is that the Dev agent later works from a frozen spec instead of guessing.

### Phase B — Development cycle (repeat per story)

Fast, narrow-context. One story at a time.

```
SM drafts story ──► Dev implements ──► QA reviews ──► gate PASS/CONCERNS/FAIL
     ▲                                                      │
     └──────────────── FAIL: back to Dev ◄──────────────────┘
                        PASS: DevOps ships / merges
```

The critical discipline: **the Dev agent reads the story file, not the conversation.** A story
must be self-sufficient — if the Dev agent needs to ask what the acceptance criteria mean, the
SM wrote a bad story and it goes back.

## Role boundaries (the part people violate)

| Agent | Owns | Must NOT do |
|---|---|---|
| **Analyst** | Domain research, corpus survey, feasibility | Commit to scope or schedule |
| **PM** | PRD, epics, acceptance criteria, priority | Choose libraries or model architectures |
| **Architect** | Module contracts, tech choices, data flow | Write story-level implementation code |
| **SM** | Story drafting from epics, sequencing, unblocking | Change acceptance criteria to fit an implementation |
| **Dev** | Code, unit tests, experiment reports | Mark its own work QA-approved, or expand scope past the story |
| **QA** | Independent verification, gate decision, risk calls | Fix the code it just failed (it files findings) |
| **DevOps** | Environments, CI, reproducibility, release | Ship anything that lacks a PASS gate |

If an agent wants to cross a boundary, it stops and escalates to the human. That escalation is
a feature: it is where a person catches a bad plan cheaply.

## Story lifecycle states

`Draft` → `Approved` → `InProgress` → `Review` → `Done` (or → `Blocked`)

Only the human moves `Draft` → `Approved`. Only QA moves `Review` → `Done`.

## Invoking the agents in Claude Code

Each role exists twice, deliberately:

- `.bmad/agents/<role>.md` — the full persona and mandate. Portable to any AI tool.
- `.claude/agents/<role>.md` — a thin Claude Code subagent that loads the above.

So you can either say *"act as the SM and draft the next story"* in a normal session, or spawn
the real subagent for isolated context. Prefer the subagent for Dev and QA work, because the
context isolation is what stops a Dev agent from quietly reading QA's findings and gaming them.

## Where the rules live

`.bmad/rules/` is loaded by agents according to `core-config.yaml`. Three of those files encode
hard-won domain constraints rather than style preferences — read them before writing any code:

- `20-bengali-text.md` — Unicode normalization, grapheme clusters, visual vs. logical order.
  Getting this wrong silently corrupts every metric you report.
- `30-data-privacy.md` — real deeds contain real people's names and thumbprints.
- `40-ml-experiments.md` — writer-disjoint splits, frozen eval sets, seed discipline.

## Starting a session

```
1. Read .bmad/core-config.yaml            (where things live)
2. Read the rules named in always_load    (the non-negotiables)
3. Read docs/prd.md and docs/architecture.md   (the frozen spec)
4. Read the one story you are working on
5. Do only that story
```

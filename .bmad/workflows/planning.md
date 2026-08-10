# Workflow — Planning (Phase A)

Run once at project start, then only when scope genuinely changes. Slow and deliberate; the whole
point is that Phase B can then be fast.

## Sequence

```
Analyst ──► PM ──► Architect ──► PM+Architect (shard) ──► Human approval
   │          │         │                │
 facts     scope    contracts         epics
```

### Step 1 — Analyst: reduce uncertainty
**Input:** the raw idea, sample deeds (redacted).
**Output:** `docs/prd.md` §Context, plus a research note in `docs/experiments/`.
**Exit condition:** the five standing research questions in `.bmad/agents/analyst.md` are answered
or explicitly marked unknown. A measured zero-shot CER exists.

Do not skip this. A PRD with invented accuracy targets produces months of work toward a number
nobody can hit.

### Step 2 — PM: define scope
**Input:** analyst findings.
**Output:** `docs/prd.md` complete — problem, users, goals, non-goals, success metrics, epics.
**Exit condition:** `.bmad/checklists/pm.md` passes. Every target metric traceable to a measured
baseline or to annotator agreement.

### Step 3 — Architect: design
**Input:** PRD.
**Output:** `docs/architecture.md` — stage contracts, dataclasses, model candidates with rejected
alternatives, evaluation harness, deployment shape.
**Exit condition:** `.bmad/checklists/architect.md` passes. Every epic has a "how this is measured"
answer.

### Step 4 — Shard into epics
PM and Architect together produce `docs/epics/epic-<nnn>-<slug>.md`, each with ordered stories
and dependencies. Stories are titles and one-line intents at this stage — the SM writes them
properly later, one at a time.

### Step 5 — Human approval
The human reads both documents and approves. This is the cheapest possible moment to catch a bad
plan, and the last one before code exists.

## Anti-patterns
- Writing the PRD after the code — the spec then only documents what was built.
- Setting a target CER before measuring a baseline.
- Drafting all stories up front. They go stale as the codebase changes.
- Letting the Architect decide scope, or the PM pick model architectures.

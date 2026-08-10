# Checklist — PM (PRD readiness)

Run before declaring `docs/prd.md` ready for the Architect.

## Problem and users
- [ ] The problem is stated in terms of what someone does today and why it is inadequate
- [ ] Personas include their **error tolerance**, split between identifiers and boilerplate
- [ ] Volume expectations stated (deeds per day/week) — this changes the architecture

## Goals
- [ ] Every goal has a measurable success criterion
- [ ] Every target number traces to a **measured** baseline or to annotator agreement (R40.10),
      not to a wish
- [ ] The headline metric is operator time saved at a fixed accuracy bar, not raw CER alone

## Non-goals
- [ ] Autonomous legally-authoritative output is explicitly a non-goal
- [ ] Person identification from thumbprints is explicitly a non-goal (R30.5)
- [ ] Ownership aggregation / people-search is explicitly a non-goal (R30.8)
- [ ] Deferred ideas are recorded as non-goals or later epics, not left ambiguous

## Epics
- [ ] Each epic has a one-sentence outcome and a "how it is measured" answer
- [ ] Epics are ordered, with dependencies stated
- [ ] The first epic reduces the largest uncertainty, not the easiest work
- [ ] Evaluation infrastructure precedes model work in the ordering

## Acceptance criteria
- [ ] Numbered, independently verifiable, no compound criteria
- [ ] Written so the Architect can design against them without asking what they mean
- [ ] Nothing that requires a subjective judgement to verify

## Discipline
- [ ] No library, framework, or model architecture named in the PRD (Architect's mandate)
- [ ] Open questions listed with an owner
- [ ] Risks have mitigations, not just names
- [ ] Assistive framing present on every user-facing goal (R00.6)

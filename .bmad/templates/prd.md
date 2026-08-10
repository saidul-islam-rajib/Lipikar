# Lipikar — Product Requirements Document

**Owner:** PM (Anwar) · **Status:** draft | approved · **Last updated:** <date>

## 1. Problem
<Whose problem, how it is solved today, why that is inadequate. Concrete, not aspirational.>

## 2. Users
<Personas with their error tolerance. For Lipikar, distinguish tolerance on identifiers
(names, dag numbers, area, dates) from tolerance on boilerplate legal phrasing — they differ by
an order of magnitude and this drives everything.>

| Persona | Goal | Error tolerance | Volume |
|---|---|---|---|

## 3. Context and prior findings
<From the Analyst. Measured facts separated from inferences. Include the measured zero-shot
baseline CER and the inter-annotator agreement ceiling.>

## 4. Goals
<Numbered, each with a measurable success criterion traceable to a baseline.>

## 5. Non-goals
<Explicit. What this product will not do, so nobody builds it. For Lipikar this must include:
autonomous legally-authoritative output, person identification from thumbprints, land-ownership
aggregation.>

## 6. Success metrics

| Metric | Baseline (measured) | Phase 1 target | Phase 2 target | How measured |
|---|---|---|---|---|

The headline metric is **operator time saved per deed at a fixed verified-accuracy bar**, not raw
CER. CER is a driver, not the goal.

## 7. Constraints
- Output is assistive; human verification is required before any legal use.
- Deed data is sensitive personal information; see `docs/DATA.md` and Rule 30.
- No local GPU; training on rented hardware.
- Low-resource language: in-domain training data must be created, not downloaded.

## 8. Epics

| ID | Title | Outcome | Depends on |
|---|---|---|---|

## 9. Acceptance criteria per epic
<Numbered and independently verifiable. Written so the Architect can design against them.>

## 10. Open questions
<What is still unknown, and who resolves it.>

## 11. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

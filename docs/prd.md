# Lipikar — Product Requirements Document

**Owner:** PM (Anwar) · **Status:** DRAFT — skeleton seeded, not yet PM-approved
**Last updated:** 2026-08-10

> This file was seeded during project setup so the structure exists. It is **not** an approved
> PRD. Sections marked `TBD-ANALYST` must be filled with *measured* facts before the PM sets
> targets, per `.bmad/workflows/planning.md` Step 1. Do not start Phase B development against
> this document in its current state.

## 1. Problem

Bangladeshi land deeds (দলিল) exist overwhelmingly as handwritten paper documents, many decades
old, written in cursive Bengali with archaic revenue vocabulary. Reading one today means finding a
person who can decipher it. That gates every downstream activity — verifying a chain of title,
settling an inheritance, resolving a boundary dispute, digitizing a land-office backlog.

General OCR does not address this. The text is handwritten, not printed; the script has hazards
(conjuncts, pre-base vowel signs, matra) that generic engines handle poorly; and the documents are
degraded, photographed on phones, annotated in red by registrars, and overlaid with thumb
impressions.

## 2. Users

| Persona | Goal | Error tolerance | Volume |
|---|---|---|---|
| Land-office clerk | Digitize a physical backlog | Near-zero on identifiers; moderate on boilerplate | High, batched |
| Lawyer / title examiner | Verify a chain of title | Near-zero on identifiers and dates | Low, high-stakes |
| Archivist | Preserve and index records | Tolerant; wants searchability | High |
| Private individual | Read an inherited deed | Wants gist plus accurate names and plot data | One or two documents |

The asymmetry matters and drives acceptance criteria: **errors in identifiers (names, dag numbers,
area, dates, amounts) are unacceptable; errors in formulaic legal phrasing are tolerable.** Overall
CER is therefore a driver metric, not the goal metric.

## 3. Context and prior findings

### Measured facts
`TBD-ANALYST` — nothing has been measured yet. Required before targets are set:
- Zero-shot CER of current VLMs on redacted deed pages
- Inter-annotator agreement on deed line transcription (this is the ceiling on achievable CER)
- Lexicon overlap between deed revenue vocabulary and modern Bengali corpora

### Inferences (not yet verified)
- Line-level Bengali handwriting corpora exist publicly but none are deed-domain, so in-domain
  training data must be created rather than downloaded.
- A CRNN+CTC baseline is trainable on a few thousand in-domain lines; a VLM fine-tune needs more.

## 4. Goals

`TBD-PM` — to be written once §3 contains measured facts. Placeholder framing:

1. A human can transcribe and verify a deed substantially faster with Lipikar than without it.
2. Identifier fields are extracted with field-level exact-match high enough that verification is
   confirmation rather than re-entry.
3. Every output carries provenance (the image crop it came from) and a calibrated confidence.

## 5. Non-goals

These are permanent and not subject to scope negotiation:

1. **Autonomous, legally-authoritative output.** Lipikar never certifies a transcription. Output is
   always a suggestion pending human verification.
2. **Person identification from thumb impressions.** Detecting a thumbprint region in order to
   exclude it from recognition is in scope; matching or indexing biometrics is not (R30.5).
3. **Land-ownership aggregation or people-search.** The corpus is not a dataset about individuals
   (R30.8).
4. **Printed-document OCR as a product.** Printed text is handled only where it appears on deeds.
5. **Languages other than Bengali** (with incidental English on stamp headers).

## 6. Success metrics

| Metric | Baseline (measured) | Phase 1 target | Phase 2 target | How measured |
|---|---|---|---|---|
| Grapheme CER | `TBD-ANALYST` | 0.20 | 0.10 | Frozen eval set, NFC, cluster-based (R20.2) |
| Field exact-match (identifiers) | `TBD` | `TBD-PM` | `TBD-PM` | Frozen eval set, per-field |
| Operator minutes per verified deed | `TBD` | `TBD-PM` | `TBD-PM` | Timed human study |

Targets in the config file are provisional placeholders and must be re-derived from the measured
baseline and the annotator-agreement ceiling.

## 7. Constraints

- Assistive only; human verification required before any legal use (R00.6).
- Deed data is sensitive personal information including biometrics (Rule 30).
- No local GPU; training on rented hardware.
- Low-resource language: in-domain data must be created.
- System Python 3.14 is ahead of the ML stack; canonical environment is 3.11/3.12.

## 8. Epics

| ID | Title | Outcome | Depends on |
|---|---|---|---|
| 001 | Foundation and measurement | The project can measure Bengali transcription accuracy correctly before any model exists | — |
| 002 | Feasibility baseline | `TBD-PM` | 001 |
| 003 | Data pipeline and annotation loop | `TBD-PM` | 001 |
| 004 | Image restoration (`kagoj`) | `TBD-PM` | 001 |
| 005 | Layout and line segmentation (`binnas`) | `TBD-PM` | 004 |
| 006 | Recognition baseline (`shirorekha`, CRNN+CTC) | `TBD-PM` | 003, 005 |
| 007 | Post-correction (`shuddhi`) | `TBD-PM` | 006 |
| 008 | Field extraction (`fard`) | `TBD-PM` | 007 |
| 009 | Human verification (`nazir`) | `TBD-PM` | 008 |

Only Epic 001 is specified. The rest are placeholders establishing dependency order.

## 9. Acceptance criteria per epic
See `docs/epics/`. Only epic 001 is written.

## 10. Open questions
- What is the real zero-shot VLM baseline? → Analyst
- What is annotator agreement, and therefore the achievable CER ceiling? → Analyst
- Which deed sections deliver the most user time saved first? → Analyst, then PM
- How will deeds be sourced, with what permission? → Human (blocking for Epic 003)

## 11. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Metrics computed on codepoints, inflating accuracy | High if unguarded | Severe — invalidates all results | Epic 001 ships the correct metric first; QA auto-FAILs codepoint CER |
| Writer leakage across splits | High | Severe — fake accuracy | Writer-disjoint splits enforced and QA-verified (R40.2) |
| Insufficient in-domain data | High | High | Annotation loop early (Epic 003); synthetic augmentation |
| Generic LM "corrects" archaic revenue terms into modern words | Medium | Medium | Lexicon-constrained post-correction (R20.6) |
| Real deed data committed to a public repo | Medium without a guard | Severe, irreversible | Gitignore + hard-failing CI privacy guard |
| Target accuracy set above the annotator-agreement ceiling | Medium | Wasted months | No target before §3 is measured |

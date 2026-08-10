# Lipikar — Model card

**Status:** no model trained yet. This file is the required template; a checkpoint may not be
published until it is filled in (R40.9, R30.6).

## Model identity

| Field | Value |
|---|---|
| Checkpoint ID | |
| Architecture | |
| Base model (if fine-tuned) | |
| Base model licence | |
| Training data version | |
| Config path | |
| Commit hash | |
| Trained on (hardware) | |
| Date | |

## Intended use

Assistive transcription and field extraction from Bangladeshi land deeds, **for human review**.
Output is a suggestion, never a certified reading (R00.6).

## Out-of-scope and prohibited uses

- Any use as an authoritative record of property rights or ownership
- Any legal filing or decision without human verification of every field
- Writer identification, or matching/indexing thumb impressions (R30.5)
- Bulk aggregation of ownership or people-search (R30.8)
- Documents outside the trained formats, without measuring generalization first

## Performance

Grapheme CER (NFC, cluster-based per R20.2) on the frozen eval set.

| Metric | Value |
|---|---|
| Eval set version | |
| Lines / pages / writers | |
| CER mean | |
| CER median | |
| CER p90 | |
| WER | |
| Field exact-match (identifiers) | |

Report the distribution, never a bare mean (R40.6).

## Known failure modes
*(From the qualitative review required by R40.7 — list them plainly.)*

## Confidence calibration
Any confidence surfaced to a human verifier must be calibrated, with a reliability diagram in the
corresponding experiment report (R40.8). Reference it here.

| Item | Value |
|---|---|
| Calibration method | |
| Reliability diagram | `docs/experiments/EXP-___.md` |
| Expected calibration error | |

## Memorization probe (required before publication — R30.6)

Trained models can emit training text verbatim. Deed training text contains real people's names.

| Item | Result |
|---|---|
| Probe method | |
| Verbatim training-name emission observed? | |
| Mitigation applied | |
| Date | |

**A checkpoint may not be published until this section is complete.**

## Licence and attribution

Code is MIT. **The code licence does not cover weights or data.** Record here:

- Base model licence and its obligations for derived weights
- Every training dataset, its licence, and its required attribution
- Any restriction that prevents commercial use or redistribution

## Ethical considerations

Errors in this system's output can affect real property rights and inheritance. The mitigation is
architectural, not aspirational: mandatory human verification, calibrated confidence, provenance
crops for every field, and `verified=False` by default throughout the data model.

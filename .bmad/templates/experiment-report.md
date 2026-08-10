# EXP-<nnn> — <Title>

**Date:** <yyyy-mm-dd> · **Story:** <id> · **Author:** Dev (Mizan)
**Status:** running | complete | abandoned
**Verdict:** improvement | no change | regression | inconclusive

## Hypothesis
<One sentence, falsifiable. "Colour-channel separation in kagoj reduces CER on pages with red
registrar annotations." Not "try to improve preprocessing".>

## What changed
<Exactly one variable (R40.4). If more than one changed, say so and explain why the result is
therefore not attributable.>

## Setup

| Field | Value |
|---|---|
| Config | `configs/<file>.yaml` |
| Commit | `<hash>` |
| Data version | `<manifest id>` |
| Train / val / eval sizes | <lines>, <lines>, <lines> |
| Writer-disjoint splits verified | yes / no — how |
| Seed | <n> |
| Hardware | <GPU type, VRAM> or CPU |
| Wall-clock | <duration> |

## Results

Primary metric: **grapheme CER** (NFC, cluster-based per R20.2) on the frozen eval set.

| Metric | Baseline | This run | Δ |
|---|---|---|---|
| Grapheme CER (mean) | | | |
| Grapheme CER (median) | | | |
| Grapheme CER (p90) | | | |
| WER | | | |
| Field exact-match (identifiers) | | | |

Eval set size: <n> lines across <n> pages, <n> writers.

## Distribution
<Do not report a mean alone (R40.6). Where does the error concentrate? Which pages are worst?>

## Qualitative review (mandatory, R40.7)
<Ten worst predictions examined. Name the failure modes.>

| # | Page/line | Ground truth | Prediction | Failure mode |
|---|---|---|---|---|

Failure modes observed, ranked by frequency:
1.

## Conclusion
<Did the hypothesis hold? Be blunt. A negative result recorded honestly is worth more than a
positive one that will not reproduce.>

## What this implies for the next story
<Concrete next action, or "this line of work is closed because ...".>

## Reproduce
```bash
```

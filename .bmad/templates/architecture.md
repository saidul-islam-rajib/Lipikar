# Lipikar — Architecture

**Owner:** Architect (Rehana) · **Status:** draft | approved · **Last updated:** <date>

## 1. Pipeline overview
<Diagram plus one paragraph. Name each stage's single responsibility.>

## 2. Stage contracts
For each stage: input type, output type, failure modes, how it is evaluated **in isolation**.

### kagoj — image restoration
```python
```
Evaluated standalone by: <metric>

### binnas — layout and line segmentation
### shirorekha — line recognition
### shuddhi — normalization and post-correction
### fard — field extraction
### nazir — human verification

## 3. Data model
<Frozen dataclasses. Coordinate spaces stated explicitly. Every crop traceable to a source pixel.>

## 4. Configuration schema
<What lives in `configs/`, how it loads, how it is versioned. No magic numbers in code (R10.4).>

## 5. Charset specification
<The versioned alphabet file, its contents per R20.5, and unknown-character handling.>

## 6. Evaluation harness
<Built before the first model. The frozen eval manifest, the metric implementation, the report
generator. This is tested code, not notebook cells.>

## 7. Technology decisions (ADR style)

### ADR-001 — <title>
**Decision:** <what>
**Context:** <why the decision was needed>
**Alternatives rejected:** <what, and the specific reason>
**Consequences:** <what this makes easy, what it makes hard, what would make us revisit>

## 8. Model strategy
<Baseline (CRNN+CTC) and challenger (VLM fine-tune), how they are compared, when the challenger
is allowed to replace the baseline.>

## 9. Deployment shape
<Inference service, review UI, retention policy, rollback.>

## 10. Risks and hazards
<Bengali logical-vs-visual order, conjunct long tail, red-ink overlap, page curl, mixed scripts,
no local GPU. For each: how the design absorbs it.>

## 11. What this architecture deliberately does not solve
<Honest boundaries.>

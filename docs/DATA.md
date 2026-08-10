# Lipikar — Data statement

Governed by `.bmad/rules/30-data-privacy.md`. **Data with no provenance entry below may not be used
for training or evaluation** (R30.3).

## Why this file is strict

A single deed image contains the full names of buyers, sellers and witnesses, their parents' names,
signatures, thumb impressions (biometric identifiers), property locations, and transaction amounts.
Every batch is sensitive personal data belonging to identifiable people, many of whom are alive and
none of whom volunteered to be in a machine-learning corpus.

## Provenance log

| Batch ID | Source | Date obtained | Permission basis | Documents | Restrictions | Used for |
|---|---|---|---|---|---|---|
| _(none yet)_ | | | | | | |

For each batch record: who provided it, whether written permission exists, whether the individuals
named were informed, and any restriction on publication or model release.

## Text handling policy (fixed in story 1.3)

Enforced in `lipikar/shuddhi/text.py`, configured in `configs/default.yaml` under `text:`, and
covered by the adversarial tests in `tests/unit/test_text.py` (R20.9). Normalization happens once,
at ingestion — never at comparison time.

| Decision | Value | Rationale |
|---|---|---|
| Unicode normalization | NFC at ingestion | R20.1 — identical rendering, differing bytes |
| ZWJ (U+200D) / ZWNJ (U+200C) | Stripped at ingestion | R20.4 — annotator-inconsistent, meaning-neutral here |
| Character measurement unit | Extended grapheme cluster | R20.2 — codepoint CER inflates accuracy |
| Storage order | Logical, never visual | R20.3 |
| Transliteration | Never in stored data | R20.8 |
| Danda । (U+0964) | Preserved, distinct from `.` | R20.5 |

## Splits

| Split | Writers | Pages | Lines | Manifest |
|---|---|---|---|---|
| train | | | | |
| val | | | | |
| eval (frozen) | | | | |

Splits are **writer-disjoint** and at least one deed format is held out entirely (R40.2). The eval
manifest is versioned and frozen; changing it invalidates all prior numbers and requires a version
bump with a written reason (R40.1).

## Annotation quality

| Measured | Value | Date |
|---|---|---|
| Double-annotated fraction (target ≥5%) | | |
| Inter-annotator agreement (grapheme CER between annotators) | | |

**Annotator agreement is the ceiling on achievable model CER** (R40.10). A target set above it is
chasing noise. Record it before the PM finalizes success metrics.

## Third-party disclosure log

Sending a deed image to any external service — hosted model API, annotation SaaS, cloud storage —
discloses personal data to that vendor and requires explicit human authorization first (R30.4).

| Date | Service | Data sent | Redacted? | Authorized by | Purpose |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |

## Redaction standard

Publishable samples are synthetic, or redacted such that names, signatures, thumbprints, and plot
identifiers are **irreversibly** obscured — flattened pixels, not a removable overlay. A human
reviews every redaction before it ships (R30.2).

## Retention and deletion

- Working corpus lives only in `data/`, which is gitignored.
- Derived caches containing readable text are deleted when a story closes (R30.7).
- Uploaded deeds in the deployed service are not retained beyond the review session unless the
  operator explicitly saves them.

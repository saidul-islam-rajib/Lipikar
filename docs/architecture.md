# Lipikar — Architecture

**Owner:** Architect (Rehana) · **Status:** DRAFT — skeleton seeded, not yet approved
**Last updated:** 2026-08-10

> Seeded during setup. Stage contracts below are **provisional** and must be finalized by the
> Architect against an approved PRD before Phase B begins. Sections marked `TBD-ARCHITECT` are
> genuinely undecided — do not treat a placeholder as a decision.
>
> This document is the home for stage rationale and hazards. Code carries no comments (R10.5), so
> anything a developer needs to know about *why* a stage works the way it does belongs here.

## 1. Pipeline overview

```
  photo
    │
    ▼
┌──────────┐   restored page    ┌──────────┐   ordered lines   ┌──────────────┐
│  kagoj   │ ─────────────────► │  binnas  │ ────────────────► │  shirorekha  │
│ restore  │                    │ segment  │                   │  recognize   │
└──────────┘                    └──────────┘                   └──────────────┘
                                                                       │ raw text
                                                                       ▼
┌──────────┐   verified record  ┌──────────┐   fields          ┌──────────────┐
│  nazir   │ ◄───────────────── │   fard   │ ◄──────────────── │   shuddhi    │
│  verify  │                    │ extract  │                   │   correct    │
└──────────┘                    └──────────┘                   └──────────────┘
```

Each stage has one responsibility and is **independently evaluable**. That is the load-bearing
design decision: without it, a CER regression cannot be attributed to segmentation versus
recognition, and debugging becomes guesswork.

| Stage | Meaning | Responsibility | Evaluated standalone by |
|---|---|---|---|
| `kagoj` | paper | Geometric and photometric restoration | Downstream segmentation IoU on a fixed page set; ink/paper separation quality |
| `binnas` | arrangement | Region classification + line extraction in reading order | Line-level IoU and reading-order correctness against gold polygons |
| `shirorekha` | the top stroke | Line image → text | Grapheme CER on **gold** line crops |
| `shuddhi` | correction | Normalize, measure, lexicon-constrained correction | CER delta on fixed noisy input |
| `fard` | itemized record | Text + layout → structured fields | Field-level exact match given gold transcriptions |
| `nazir` | custodian | Confidence, provenance, human verification | Operator minutes per verified deed; calibration error |

## 2. Stage detail

### 2.1 `kagoj` — image restoration

`Page → RestoredPage`

Order of operations: dewarp → deskew → illumination normalize → denoise → channel separation.
Dewarping is first because every later geometric assumption depends on a flat page.

**Design constraint (ADR-003).** Colour is preserved. Registrar annotations are written in red ink
that overlaps the black body text; a naive grayscale binarization merges the two layers and destroys
both irrecoverably. Output therefore carries a colour image plus separate `ink_mask` and
`annotation_mask`.

`RestoredPage.transform` maps restored coordinates back to **original page coordinates**. Mandatory —
a human verifier must always be shown the exact source pixels.

### 2.2 `binnas` — layout analysis and line segmentation

`RestoredPage → tuple[Region, ...], tuple[Line, ...]`

Region kinds are a closed set, configured not hardcoded (R70.2): `body`, `annotation` (red registrar
ink), `stamp` (printed header), `thumbprint`, `margin_measure`, `slogan`.

Two are easy to get wrong:

- **`thumbprint`** regions are detected in order to *exclude* them from recognition. Detecting them
  is in scope; identifying a person from them is permanently out of scope (R30.5).
- **`margin_measure`** regions are *data, not noise*. The ana/gonda/kora/kranti figures and Bengali
  currency numerator marks in the margins carry the land area (R20.7). Do not discard them.

**Bengali-specific hazard.** The shirorekha (top horizontal stroke) and below-baseline vowel signs
make adjacent lines touch. Projection-profile splitting merges lines on dense pages; expect to need
a learned segmenter.

All polygons are in original page space. Line crops are deskewed but retain the polygon locating
them on the source page.

### 2.3 `shirorekha` — line recognition

`Line → Transcription`

Output text is NFC, logical order, ZWJ/ZWNJ stripped, with per-cluster confidences.

**Model strategy (ADR-002).** CRNN + CTC is the reference baseline and doubles as the CPU smoke
path. A fine-tuned vision-language model is a *challenger*: it must beat the baseline on the frozen
eval set to replace it. Both are maintained through Epics 006–007.

**Charset (R20.5).** Loaded from a versioned file in `configs/`, never inferred from whichever
characters appeared in the training split. Covers Bengali consonants, independent vowels, vowel
signs, hasanta, Bengali digits ০–৯ **and** ASCII 0–9, ASCII letters (stamp headers and act
references are in English), currency and fraction marks ৳ ৴ ৵ ৶ ৷ ৸ ৹, and the danda । which is not
an ASCII full stop. Unknown characters map to the configured unknown token **and their codepoint is
logged** — silent drops hide charset gaps until they poison a training run.

**Ordering hazard (R20.3).** Never derive character order from bounding-box x-coordinates. The vowel
sign ই-kar (ি U+09BF) renders to the *left* of its consonant but is *stored* after it. CTC and
seq2seq operate on logical order; keep it that way end to end and convert to visual order only
inside a renderer.

### 2.4 `shuddhi` — normalization, metrics, correction

Holds the project's measurement layer, built **before any model exists** (Epic 001). A wrong metric
is worse than no metric.

Responsibilities: the single normalization boundary (NFC, ZWJ/ZWNJ stripping, danda preservation);
grapheme CER and WER; lexicon-constrained correction.

**Metric contract (R20.2) — the load-bearing rule.** Character error rate is computed over extended
grapheme clusters via `regex.findall(r"\X", text)`, never over codepoints. কি is one perceived
character but two codepoints; ক্ষ is one cluster but three. Codepoint CER silently inflates apparent
accuracy, because a model that drops a matra is scored as one error among many codepoints rather
than one among few clusters. `regex` is a hard dependency, not a convenience — the stdlib `re`
cannot match grapheme clusters. QA treats any codepoint measurement as an automatic gate FAIL.

**Reporting (R40.6).** Never a bare mean. Mean, median, p90, worst-N, sample size. A mean CER of 12%
hiding a cluster of unreadable pages is a different product from a uniform 12%.

**Correction constraint (R20.6).** Deeds use archaic Perso-Arabic revenue vocabulary — মৌজা,
খতিয়ান, দাগ, দাখিলা, তমসুক, কবলা, বায়না, পত্তন. A general Bengali language model will "correct"
these into common modern words and make output *worse*. Correction is lexicon-constrained against
`data/lexicon/`, and any generic LM rescoring must be tested for exactly this regression.

### 2.5 `fard` — field extraction

`tuple[Transcription, ...], tuple[Region, ...] → tuple[Field, ...]`

Field names and their validation patterns come from config (R70.2), not from literals in code.

**Accuracy asymmetry that shapes this stage.** Users tolerate errors in formulaic legal phrasing and
almost none in identifiers — names, dag numbers, area, dates, amounts. Field-level exact match on
identifiers therefore matters more than overall CER, and this stage is evaluated on that basis.

**Land-measure notation.** Area often appears in ana/gonda/kora/kranti fractional notation with
Bengali currency numerator marks rather than decimal figures (R20.7). Parsing it is this stage's job,
not something to normalize away upstream.

### 2.6 `nazir` — human verification

Presents extracted fields to a human for confirmation or correction, and captures those corrections
as training data. A first-class pipeline component, not a UI afterthought — it needs confidence,
provenance, and the image crop for every field from day one, and retrofitting that is expensive.

**Why this stage is mandatory.** Output describes real property rights. A wrong dag number or a
misread name propagates into a land record with consequences for real people. The system is
assistive by design, enforced architecturally rather than by convention: `Field.verified` defaults to
`False` throughout the data model; every field ships with the polygon of the pixels it came from; and
the assistive-output notice is a string resource referenced everywhere (R70.14) so it cannot be
omitted from one surface.

**Confidence must be calibrated (R40.8).** Humans use these scores to decide where to spend
attention, so an uncalibrated score is actively harmful — it sends the reviewer to the wrong fields.

**Retention (R30.7).** Deed images are not retained beyond the review session unless the operator
explicitly saves them, enforced in code.

TypeScript is permitted in this stage's UI and nowhere else in the project.

## 3. Data model

```python
@dataclass(frozen=True)
class Page:
    page_id: str
    image: np.ndarray
    source_hash: str

@dataclass(frozen=True)
class RestoredPage:
    page_id: str
    image: np.ndarray
    ink_mask: np.ndarray
    annotation_mask: np.ndarray
    transform: Transform

@dataclass(frozen=True)
class Region:
    kind: str
    polygon: Polygon

@dataclass(frozen=True)
class Line:
    line_id: str
    page_id: str
    image: np.ndarray
    polygon: Polygon
    region_kind: str
    reading_order: int

@dataclass(frozen=True)
class Transcription:
    line_id: str
    text: str
    cluster_confidences: tuple[float, ...]
    model_id: str

@dataclass(frozen=True)
class Field:
    name: str
    value: str
    confidence: float
    source_line_ids: tuple[str, ...]
    source_polygon: Polygon
    verified: bool = False
```

Dtype and coordinate-space contracts: `Page.image` and `RestoredPage.image` are `HxWx3` uint8 BGR;
masks are `HxW` uint8 with 0 = ink, 255 = paper; `Line.image` is `HxW` uint8. All text is NFC and in
logical order.

Two invariants that are not negotiable:

- **All polygons live in original page space**, with the transform recorded.
- **`verified` defaults to `False`** everywhere. Nothing is authoritative by default (R00.6).

## 4. Configuration and string resources

Governed by Rule 70. Configuration is YAML in `configs/`, loaded into frozen dataclasses, validated
on load, rejecting unknown keys. Layering: `default.yaml` → `<env>.yaml` → environment variables.
Secrets never appear in `configs/`.

User-facing text lives in `lipikar/resources/strings/en.yaml` and `bn.yaml`, addressed by namespaced
key, interpolated with named placeholders. A test asserts the two locales have identical key sets.
Bengali is a first-class locale, not a stub.

## 5. Evaluation harness

Built in Epic 001, **before any model.** Components: the frozen eval manifest (page IDs + hashes),
grapheme-cluster CER/WER, distribution reporting, per-field exact match. Tested library code in
`lipikar/`, never notebook cells (R00.9).

## 6. Technology decisions (ADR)

### ADR-001 — Python 3.11/3.12, not the system 3.14
**Decision:** pin 3.11 or 3.12 for all ML work.
**Context:** the development machine's system Python is 3.14.5, ahead of PyTorch's wheel availability.
**Alternatives rejected:** system 3.14 (source builds, dependency breakage); conda (extra toolchain
for no gain here).
**Consequences:** contributors need a version manager. Revisit when torch ships 3.14 wheels.

### ADR-002 — Baseline before challenger
**Decision:** CRNN+CTC is the reference recognizer; a VLM fine-tune must beat it on the frozen eval
set to replace it.
**Context:** a VLM fine-tune is the likely long-term winner but is expensive, data-hungry, and slow
to iterate; with no baseline its number means nothing.
**Alternatives rejected:** VLM-only (no reference point, no cheap iteration); Tesseract (does not
work on cursive handwriting).
**Consequences:** two recognizers to maintain during Epics 006–007. Accepted — the CRNN doubles as
the CPU smoke path.

### ADR-003 — Colour preserved through `kagoj`
**Decision:** restoration outputs a colour image plus separate ink and annotation masks.
**Context:** registrar annotations are red ink overlapping black body text; grayscale binarization
merges and destroys both.
**Alternatives rejected:** single binarized channel (loses the annotation layer irrecoverably).
**Consequences:** more memory per page; `binnas` must handle a red-ink region class.

### ADR-004 — Privacy guard is stdlib-only, JSON-configured, and fails closed
**Decision:** `scripts/check_no_sensitive_files.py` reads its patterns from
`configs/privacy_guard.json`, imports nothing outside the standard library, and exits non-zero if
that config is missing or malformed.
**Context:** the patterns are configuration, not logic (R70.2), so they must live outside the code.
But this guard is the only automated defence against an irreversible leak (R30.1), and it has to run
in three environments where the project's dependencies may not be installed: a bare shell, a
pre-commit hook invoked outside an activated venv, and CI before `pip install`.
**Alternatives rejected:** hardcoded patterns (violates R70.2 and the list will change); YAML via
PyYAML (tried first — a guard that cannot import its parser silently stops protecting anything, and
a security control must not depend on a third-party package); fail-open-with-warning (a warning in
CI output is not a control).
**Consequences:** this is the one config file in the project that is JSON rather than YAML, which
deviates from R70.1's format convention. The deviation is deliberate and confined to bootstrap
tooling; every other config remains YAML. Verified behaviour: exits 0 on clean paths, 1 on
violations, and 1 when its own config is absent.

### ADR-005 — `TBD-ARCHITECT`: annotation tooling
Candidates: eScriptorium (purpose-built HTR line transcription), Label Studio. Blocked on Epic 003
and on R30.4 authorization if the tool is hosted.

## 7. Deployment shape

`TBD-ARCHITECT`. Constraints already fixed: FastAPI inference service; deed images not retained
beyond the review session unless explicitly saved; every response marked unverified; structured logs
carry document IDs and timings, never deed text; documented and tested rollback.

## 8. Risks and hazards absorbed

| Hazard | How the design absorbs it |
|---|---|
| Logical vs. visual order (R20.3) | Text is logical order end to end; conversion only in a renderer |
| Conjunct long tail | Charset is a versioned config with logged unknowns, not inferred |
| Red ink over black text | ADR-003: colour preserved, separate annotation mask |
| Page curl from phone capture | Dewarping is the first operation in `kagoj` |
| Mixed Bengali/English/two digit systems | One unified charset, no language-detection branch |
| Bengali word order in UI text | Named placeholders in string resources, never concatenation (R70.10) |
| No local GPU | CPU smoke path per component; training targets rented GPUs |
| Stage-attribution ambiguity | Every stage independently evaluable (§1) |

## 9. What this architecture deliberately does not solve

- Multi-page deeds with cross-page field continuation — deferred.
- Deed formats outside the sampled set; generalization is measured, not assumed.
- Any biometric processing of thumb impressions beyond excluding those regions from recognition.
- Handwriting *writer* identification — permanently out of scope (R30.5).

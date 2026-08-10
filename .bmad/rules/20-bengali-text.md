# Rule 20 — Bengali script and text handling

These are correctness rules, not style preferences. Violating them produces metrics that look
fine and are wrong, which is the most expensive failure mode this project has.

## R20.1 Normalize to NFC at every boundary
Every string entering the system — from an annotation tool, a dataset, a model decode, a
lexicon file — is `unicodedata.normalize("NFC", s)` before anything else touches it.
Un-normalized Bengali produces two byte sequences that render identically, so a "wrong"
prediction may be textually correct. Normalize at ingestion, not at comparison time.

## R20.2 Measure over grapheme clusters, never codepoints
CER for Bengali **must** segment by extended grapheme cluster (Python `regex` module, `\X`),
not by `len(str)`.

```python
import regex
clusters = regex.findall(r"\X", text)   # correct
chars    = list(text)                   # WRONG for Bengali metrics
```

Rationale: কি is one perceived character but two codepoints; ক্ষ is one cluster but three
(ক + ্ + ষ). Codepoint CER silently inflates apparent accuracy because a model that drops a
matra is scored as 1 error out of many codepoints rather than 1 out of few clusters. Any metric
in this repo not using `\X` is a bug.

## R20.3 Visual order is not logical order
The vowel sign ই-kar (ি U+09BF) renders **to the left** of its consonant but is **stored after**
it. Same family of problem for ে, ৈ, ো, ৌ. Consequences:

- Never derive character order from bounding-box x-coordinates.
- Never build a per-character alignment by sorting boxes left to right.
- CTC and seq2seq decoders operate on logical order — keep it that way end to end. Convert to
  visual order only inside a renderer, never in stored data.

## R20.4 Fix a ZWJ/ZWNJ policy and enforce it
U+200D (ZWJ) and U+200C (ZWNJ) change conjunct rendering without changing meaning for our
purposes, and annotators will be inconsistent about them.

**Policy:** strip ZWJ and ZWNJ at ingestion. Record the decision in `docs/DATA.md`. Apply the
same stripping to predictions before scoring, so the metric never rewards or punishes an
invisible character.

## R20.5 Declare the charset explicitly
`shirorekha` must load its output alphabet from a versioned file in `configs/`, never infer it
from whatever appeared in the training split. The charset covers, at minimum:

- Bengali consonants, independent vowels, vowel signs, hasanta (্)
- Bengali digits ০–৯ **and** ASCII digits 0–9 (deeds mix both)
- ASCII letters (stamp headers and act references are in English)
- Bengali currency/fraction marks: ৳ ৴ ৵ ৶ ৷ ৸ ৹ — these appear in land-measure notation
- Punctuation including the danda । (U+0964), which is not a full stop `.`

Unknown-character handling is explicit: map to `<unk>` and **log the codepoint**. Silent drops
hide charset gaps until they poison a training run.

## R20.6 Domain vocabulary is Perso-Arabic, not modern Bengali
Land deeds use archaic revenue terminology — মৌজা, খতিয়ান, দাগ, দাখিলা, তমসুক, কবলা, বায়না,
পত্তন — plus honorifics and formulaic legal phrasing. A general Bengali language model will
"correct" these into common words and make output worse. Therefore:

- `shuddhi` post-correction must be lexicon-constrained using `data/lexicon/`.
- Any generic LM rescoring must be evaluated for exactly this regression before it lands.

## R20.7 Land-measure notation is in scope
The marginal figures on a deed use ana / gonda / kora / kranti fractional notation and Bengali
currency numerator marks. These are **data, not noise**. Do not preprocess them away, and do not
treat their region as a non-text artifact.

## R20.8 Never transliterate in stored data
Store Bengali as Bengali. Romanization is permitted only in log messages and identifiers
(module names like `shirorekha` are fine). A pipeline that stores transliterated text has lost
information irreversibly.

## R20.9 Test with adversarial strings
Every text-handling function ships with tests covering: a conjunct cluster, a pre-base vowel
sign, mixed Bengali/ASCII digits, an NFC-vs-NFD pair that must compare equal, a ZWJ that must
be stripped, and a danda. A text utility without these tests is not done.

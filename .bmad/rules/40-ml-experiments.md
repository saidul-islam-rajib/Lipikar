# Rule 40 — ML experiment discipline

## R40.1 The eval set is frozen and untouchable
One held-out evaluation set, defined once, versioned by manifest file (a list of page IDs and
their hashes) in `configs/`. It is never used for tuning, never used for model selection, and
never regenerated to "include new data" without a version bump and a note explaining why every
prior number is no longer comparable. Use the validation split for tuning.

## R40.2 Splits are writer-disjoint
Split by **writer, then page** — never randomly by line. Handwriting is highly writer-specific;
a random line split leaks a writer's hand across train and test and can inflate apparent
accuracy dramatically. Same rule for deed *format*: keep at least one format entirely unseen so
you know whether the model generalizes or memorizes a template.

## R40.3 Baseline before sophistication
No model change is evaluated in the abstract. Establish the simple baseline first (CRNN + CTC),
record its number, and quote every later result as a delta against it. A VLM fine-tune that
cannot beat the CRNN baseline is a negative result worth recording, not a failure to hide.

## R40.4 One variable per experiment
Change the architecture *or* the augmentation *or* the learning rate. A run with three changes
that improves the metric teaches nothing about which change mattered, and cannot be safely
built on.

## R40.5 Every run produces a report
`docs/experiments/EXP-<nnn>-<slug>.md` from the template, containing: hypothesis, config path,
data version, seed, hardware, primary and secondary metrics, comparison to baseline, and an
honest conclusion. **Negative results are recorded, not deleted** — they are the cheapest thing
this project owns and re-running a known failure is pure waste.

## R40.6 Report metrics honestly
- Primary: grapheme CER per Rule 20. Codepoint CER is not reportable.
- Always report on the frozen eval set, never on a cherry-picked subset.
- Report the *distribution*, not just the mean: median, 90th percentile, and worst pages. A mean
  CER of 12% hiding a cluster of unreadable pages is a different product than a uniform 12%.
- State the sample size. A 2% improvement on 40 lines is noise.

## R40.7 Qualitative review is mandatory
Numbers do not catch systematic failure. Every experiment includes eyeballing at least 10 worst
predictions and naming the failure mode (conjunct confusion, matra dropping, red-ink bleed,
line-merge from segmentation). Findings feed the next story.

## R40.8 Confidence must be calibrated, not decorative
`nazir` shows confidence to humans deciding where to look. An uncalibrated score that reads
0.98 on a wrong field is worse than no score, because it misdirects review effort. Any
confidence surfaced to a user must have a reliability diagram in its experiment report.

## R40.9 Track provenance of every checkpoint
A checkpoint is worthless without: training data version, config, commit hash, and eval number.
Untraceable weights get deleted, not shipped.

## R40.10 Annotation quality is measured
Human transcription is not ground truth by assumption. Double-annotate a sample (target ≥5% of
lines), report inter-annotator agreement in `docs/DATA.md`, and treat that agreement as the
ceiling on achievable CER. If annotators disagree 8% of the time, a model at 8% CER is at
human parity and further tuning is chasing noise.

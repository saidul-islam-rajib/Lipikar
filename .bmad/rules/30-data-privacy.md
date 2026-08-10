# Rule 30 — Data handling and privacy (all agents, always loaded)

Lipikar's inputs are photographs of real legal instruments. A single deed image contains the
full names of buyers, sellers and witnesses, their parents' names, signatures, thumb
impressions (biometric data), property locations, and transaction amounts. Treat every file
under `data/` as sensitive personal information.

## R30.1 Nothing real enters version control
`data/` is gitignored, along with image and PDF extensions repo-wide. Never:

- `git add -f` a deed image, transcription, or extracted JSON
- paste deed contents into a commit message, PR body, issue, or story file
- place a real deed under `docs/assets/`

Git history is effectively permanent. A leak here cannot be undone by a later delete.

## R30.2 Only redacted or synthetic samples are publishable
Documentation and tests use either synthetically rendered deeds or images where names,
signatures, thumbprints, and plot identifiers are irreversibly obscured — flattened pixels, not
an overlay layer that can be removed. Redaction is reviewed by a human before it ships.

## R30.3 Provenance is recorded before use
Every batch added to `data/raw/` gets an entry in `docs/DATA.md`: source, date obtained, how
permission was given, how many documents, and any usage restriction. **Data with no provenance
entry may not be used for training or evaluation.** If you cannot say how you were allowed to
have a document, you are not allowed to train on it.

## R30.4 Third-party services are disclosure
Sending a deed image to a hosted model API, an annotation SaaS, or any external service
discloses personal data to that vendor. Before any such call:

- confirm the human has authorized that specific vendor for that specific data
- record it in `docs/DATA.md`
- prefer redacted or synthetic images for prototyping and vendor evaluation

Do not add a new external dependency that transmits deed content without asking first.

## R30.5 Biometric data gets special care
Thumb impressions are biometric identifiers and attract stricter treatment than ordinary PII in
most regimes. Do not build features that match, index, or search thumbprints. Detecting a
thumbprint region in order to *exclude* it from text recognition is in scope; identifying a
person from it is not, and no story may request it.

## R30.6 Public artifacts are checked for leakage
Trained model weights can memorize and regurgitate training text. Before publishing any
checkpoint: probe it for verbatim emission of training names and note the result in
`docs/MODEL_CARD.md`. Before publishing any evaluation report, confirm example outputs are from
redacted or synthetic inputs.

## R30.7 Local storage discipline
Keep the working corpus in one place (`data/`), out of cloud-synced folders where possible, and
delete derived caches containing readable text when a story closes. Do not scatter copies into
`notebooks/`, temp directories, or the scratchpad.

## R30.8 Purpose limitation
The corpus exists to build transcription and extraction. It is not a dataset for
people-searching, land-ownership aggregation, or any analysis of identifiable individuals. If a
story drifts that way, escalate rather than implement.

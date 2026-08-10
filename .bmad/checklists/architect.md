# Checklist — Architect (design readiness)

Run before handing `docs/architecture.md` to the SM.

## Contracts
- [ ] Every stage has an explicit input and output type
- [ ] Types are frozen dataclasses, not dicts (R10.2)
- [ ] Coordinate spaces stated; every crop traceable back to the source pixel
- [ ] Failure modes named per stage, with what the stage does when it fails

## Measurability
- [ ] **Every stage can be evaluated in isolation** — segmentation without a recognizer,
      recognition on gold crops without a segmenter
- [ ] The evaluation harness is specified as a built component with tests, not a notebook
- [ ] The frozen eval manifest format is defined and versioned
- [ ] The metric implementation is cluster-based per R20.2, and that is stated in the design

## Bengali hazards absorbed
- [ ] Logical order preserved end to end; no design step sorts characters by x-coordinate (R20.3)
- [ ] Charset is a versioned config file, not inferred from data (R20.5)
- [ ] Unknown-character path defined: `<unk>` plus codepoint logging
- [ ] Red registrar ink vs. black body text addressed in `kagoj` (not destroyed by binarization)
- [ ] Land-measure notation regions treated as text, not noise (R20.7)
- [ ] Mixed Bengali/English/two digit systems handled by one charset, not a language branch

## Practical constraints
- [ ] A CPU-runnable smoke path exists for every component
- [ ] Training design assumes rented GPU; no assumption of local CUDA
- [ ] Python 3.11/3.12 pinned, not system 3.14
- [ ] No dependency transmits deed content off-machine without human authorization (R30.4)

## Decisions
- [ ] Each significant choice recorded ADR-style with **rejected alternatives and why**
- [ ] Baseline (CRNN+CTC) specified before challenger (VLM), with the comparison rule
- [ ] Conditions under which each decision would be revisited are stated

## Human-in-the-loop
- [ ] `nazir` receives confidence, provenance, and the image crop for every field from day one
- [ ] Retention policy for uploaded deeds specified and enforceable in code
- [ ] Nothing in the design implies authoritative output (R00.6)

## Honesty
- [ ] "What this architecture does not solve" section is filled in and non-empty
- [ ] Risks include what would invalidate the design, not just what might slow it down

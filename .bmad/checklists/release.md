# Checklist — DevOps (release)

## Gates
- [ ] Every story in this release has a PASS or human-WAIVED gate in `docs/qa/gates/`
- [ ] No FAIL gate is being shipped around
- [ ] Waivers include the human's verbatim reason

## Reproducibility
- [ ] Fresh virtualenv (3.11/3.12) from pinned deps → tests green
- [ ] CI green on the release commit
- [ ] Every reported metric re-derivable from a repo command plus a config file (R00.9)
- [ ] Seeds and configs committed

## Checkpoint provenance (if shipping a model)
- [ ] Training data version recorded
- [ ] Config path recorded
- [ ] Commit hash recorded
- [ ] Eval metric on the frozen set recorded, with the set's version
- [ ] Hardware and environment (torch/CUDA versions) recorded
- [ ] Memorization probe run and result in `docs/MODEL_CARD.md` (R30.6)
- [ ] Base-model licence obligations and dataset attributions satisfied in `MODEL_CARD.md`

## Privacy
- [ ] CI privacy guard active and failing hard, not warning
- [ ] No `data/` paths, images, or checkpoints in git history
- [ ] Deed retention policy enforced in code, not just documented
- [ ] DEBUG logging disabled in the deployed environment (R10.6)
- [ ] No third-party service receives deed content without a `docs/DATA.md` authorization entry

## Deployment
- [ ] Health check responds
- [ ] Request timeouts configured
- [ ] Structured logs carry document IDs and timings, never deed text
- [ ] Every API response marks output unverified and awaiting human confirmation (R00.6)
- [ ] Bengali renders correctly in the deployed UI — conjuncts and pre-base vowel signs verified
      visually, in the real browser, not assumed from the font name

## Rollback
- [ ] Previous checkpoint still available
- [ ] Rollback command written down and **tested**, not theoretical
- [ ] Someone other than me could execute it from the release note

## Release note
- [ ] Written from the DevOps template
- [ ] "Known limitations" is filled in and is not "none"
- [ ] Tag pushed

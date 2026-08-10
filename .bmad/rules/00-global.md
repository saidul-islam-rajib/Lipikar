# Rule 00 — Global rules (all agents, always loaded)

## R00.1 The spec is the contract
`docs/prd.md` and `docs/architecture.md` are frozen inputs during a development story. If
implementation reveals the spec is wrong, **stop and escalate** — do not silently deviate and
do not edit the spec from inside a Dev story. A spec that drifts to match the code destroys the
only independent check the project has.

## R00.2 One story at a time
Work the single story named in the current task. Discovered work becomes a new story in
`docs/stories/` with status `Draft`. Absorbing "while I'm in here" changes makes review
impossible and is the most common way this workflow degrades.

## R00.3 Evidence over assertion
Never write "tests pass", "accuracy improved", or "done" without the artifact that proves it:
test output, a metric delta on the frozen eval set, or a file path. If something was skipped,
say it was skipped. If a test fails, paste the failure.

## R00.4 Stay inside your mandate
Each agent's file lists what it must not do. Crossing that line requires human sign-off.
Escalation is cheap; a bad plan implemented confidently is not.

## R00.5 No fabricated capability
Do not claim a dataset, model, tool, or paper exists without verifying it. This project depends
on low-resource-language resources where availability genuinely varies — an invented dataset
name wastes days. Verify, then cite the URL in the story or experiment report.

## R00.6 Legal-consequence framing
Output describes real property rights in Bangladesh. The system is **assistive**. Every
transcription and field is a suggestion pending human verification, and every surface that
shows output — UI, API, docs, README — must make that explicit. Nothing in this project is
allowed to imply legal authority.

## R00.7 Ask when the answer changes the work
If two readings of a requirement lead to materially different implementations, ask. If they
lead to the same place, pick one, state the assumption in the story, and proceed.

## R00.8 Language and encoding hygiene
All files are UTF-8 without BOM. Bengali text in code, tests, and docs is stored NFC-normalized.
Never "fix" mojibake by transliterating — fix the encoding path.

## R00.9 Reproducibility
Any result worth reporting must be reproducible from a command in the repo plus a config file
in `configs/`. A number produced by an unversioned notebook cell does not count as a result.

## R00.10 Escalation format
When escalating, give: what you were doing, the specific ambiguity or conflict, the options you
see, your recommendation, and what you need from the human. One short block, not an essay.

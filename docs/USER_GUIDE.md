# Lipikar — User guide

How work flows through this repository. Read [`SETUP.md`](SETUP.md) first if you have not set up yet.

> **Audience.** Today that is developers and contributors — the pipeline is not built, so there is no
> end-user application to operate. §7 holds the operator manual and fills in as `nazir` is delivered.

---

## 1. What Lipikar is

A pipeline that reads handwritten Bangladeshi land deeds (দলিল) and turns them into structured,
verifiable records.

```
photo → kagoj → binnas → shirorekha → shuddhi → fard → nazir → verified record
       restore  segment   recognize    correct   extract  verify
```

**It is assistive, never authoritative.** Every transcription and extracted field is a suggestion
pending human confirmation. That constraint is architectural, not a disclaimer: `Field.verified`
defaults to `False`, every field carries the image crop it came from, and the "unverified" notice is
a shared string resource so it cannot be dropped from one surface.

Full design in [`architecture.md`](architecture.md).

---

## 2. Repository map

| Path | What lives there |
|---|---|
| `.bmad/` | The development method: role mandates, rules, templates, checklists, workflows |
| `.claude/agents/` | The same roles as invokable Claude Code subagents |
| `docs/` | PRD, architecture, this guide, data statement, model card, epics, stories, gates |
| `lipikar/` | The Python package — one subpackage per pipeline stage |
| `configs/` | All configuration. Nothing tunable is hardcoded in code (Rule 70) |
| `scripts/` | Operational scripts, including the privacy guard |
| `tests/` | `unit/` (fast, pure) and `integration/` (wiring on synthetic fixtures) |
| `data/` | The corpus. **Gitignored. Never committed.** |

---

## 3. The development method (BMAD)

Work runs through named roles with narrow mandates. The full manual is
[`.bmad/METHOD.md`](../.bmad/METHOD.md); the short version:

**Phase A — Planning** (once, revisited rarely)

```
Analyst → PM → Architect → shard into epics → human approval
 facts   scope  contracts
```

**Phase B — Development** (per story)

```
SM drafts → human approves → Dev implements → QA gates → DevOps ships
                                   ▲              │
                                   └── FAIL ──────┘
```

Story states: `Draft → Approved → InProgress → Review → Done`. Only the human moves
`Draft → Approved`. Only QA moves `Review → Done`.

### Invoking a role

```
> Act as the SM and draft story 1.2 from docs/epics/epic-001-foundation-and-measurement.md
> Act as Dev and implement approved story 1.1
> Act as QA and gate story 1.1
```

Or spawn the subagent directly (`lipikar-sm`, `lipikar-dev`, `lipikar-qa`, …). Prefer subagents for
Dev and QA: the context isolation is what keeps a QA pass from being agreement rather than
verification.

| Role | Owns | Must not |
|---|---|---|
| Analyst | Domain research, measured baselines | Commit to scope |
| PM | PRD, epics, acceptance criteria | Pick libraries or architectures |
| Architect | Contracts, tech decisions | Write story-level implementation |
| SM | Story drafting, sequencing | Soften acceptance criteria |
| Dev | Code, tests, experiment reports | Set its own QA gate |
| QA | Verification, gate decisions | Fix the code it just failed |
| DevOps | Environments, CI, release | Ship without a passing gate |

---

## 4. Working a story end to end

```bash
git checkout -b story/1.1-dev-environment-and-toolchain
```

1. Read the story file in `docs/stories/`. It is self-sufficient by design — if you need to ask what
   it means, it is defective and goes back to the SM.
2. Implement only that story. Discovered work becomes a new `Draft` story, never absorbed.
3. Run the checks:

   ```bash
   pytest -q && ruff check . && mypy lipikar
   ```

4. **The suite must be green before you call anything done.** Paste the real output into the story's
   completion notes. A failure pasted honestly is fine; a claimed pass is a process breach (R50.0).
5. Fill in the story's Dev section, set status to `Review`.
6. Hand to QA. QA re-runs everything itself and writes `docs/qa/gates/<story-id>.md`.

### Commits

One or two commits per story (R60.4a). Each one independently green.

```
feat(shuddhi): measure CER over extended grapheme clusters

Codepoint CER scores a dropped matra as one error among many codepoints
rather than one among few clusters, which made a broken recognizer look
accurate.

Story: 1.3
```

Never put deed content in a commit message, branch name, or PR title — messages are public and
`.gitignore` does not cover them. Use opaque IDs like `page_0142`.

---

## 5. Code conventions

Four rules that differ from many Python projects:

**No comments.** No inline comments at all. A short docstring above a function or module is allowed
only where the contract is not obvious — one to three lines. No commented-out code, no `# TODO`
(file a story). Rationale and hazards go in `docs/`, not in code headers. If code needs a comment,
rename something or split the function.

**Nothing hardcoded.** Thresholds, paths, model names, field names, charsets, ports — all from
`configs/` through a typed frozen dataclass. No `dict["key"]`, no bare `os.environ` in stage code.

**No user-facing string literals.** Human-readable text comes from
`lipikar/resources/strings/{en,bn}.yaml` by namespaced key, interpolated with **named** placeholders.
Never concatenate a sentence — Bengali word order differs from English, so assembled strings produce
broken grammar. `bn.yaml` is a real deliverable, and a test asserts its key set matches `en.yaml`.

**Consistency beats preference.** A new module matches those around it. Two ways of doing one thing
is a defect even when both work.

Full detail: [`10-coding-standards.md`](../.bmad/rules/10-coding-standards.md) and
[`70-configuration-and-strings.md`](../.bmad/rules/70-configuration-and-strings.md).

---

## 6. The three rules that catch real bugs

**Bengali text** — [`20-bengali-text.md`](../.bmad/rules/20-bengali-text.md). CER is measured over
**extended grapheme clusters**, never codepoints:

```python
import regex
clusters = regex.findall(r"\X", text)   # correct
chars    = list(text)                   # wrong — inflates accuracy
```

কি is one perceived character but two codepoints; ক্ষ is one cluster but three. Codepoint CER makes a
model that systematically drops matras look accurate. QA treats it as an automatic gate FAIL. Also:
never order characters by bounding-box x-coordinate — ই-kar renders left of the consonant it is
stored after.

**Data privacy** — [`30-data-privacy.md`](../.bmad/rules/30-data-privacy.md). Deed images contain
names, signatures, and biometric thumb impressions. `data/` is gitignored, the guard blocks commits,
and provenance is recorded in [`DATA.md`](DATA.md) before any batch is used.

**Experiments** — [`40-ml-experiments.md`](../.bmad/rules/40-ml-experiments.md). Writer-disjoint
splits (a random line split leaks a writer's hand and fakes accuracy), a frozen eval set, one
variable per experiment, and negative results recorded rather than deleted.

---

## 7. Operating the pipeline

*Not yet available — the pipeline is unimplemented.* This section fills in as stages land. Planned
surfaces:

| Surface | Delivered by |
|---|---|
| CLI: single deed photo → structured JSON | Epic 008 |
| Batch mode over a directory | Epic 008 |
| `nazir` review UI for field verification | Epic 009 |
| Inference API | Epic 009 |

When it exists, the operator rules are already fixed: output is always marked unverified, every
field shows its source crop and a calibrated confidence, and uploaded deeds are not retained beyond
the review session unless explicitly saved.

---

## 8. Common tasks

| Task | Command |
|---|---|
| Run the full suite | `pytest -q` |
| Fast unit loop | `pytest tests/unit -q` |
| Lint and format | `ruff check . && ruff format .` |
| Type check | `mypy lipikar` |
| Check staged files for sensitive content | `python scripts/check_no_sensitive_files.py` |
| Audit the whole repo | `python scripts/check_no_sensitive_files.py --all` |
| Find experiment commits | `git log --grep '^exp'` |
| Confirm commit identity | `git var GIT_AUTHOR_IDENT` |

---

## 9. Where to look when stuck

| Question | File |
|---|---|
| How does the process work? | [`.bmad/METHOD.md`](../.bmad/METHOD.md) |
| What are we building and why? | [`prd.md`](prd.md) |
| How is it built? | [`architecture.md`](architecture.md) |
| What are the coding rules? | [`.bmad/rules/`](../.bmad/rules/) |
| What is a role allowed to do? | [`.bmad/agents/`](../.bmad/agents/) |
| Where did this data come from? | [`DATA.md`](DATA.md) |
| Can we publish this model? | [`MODEL_CARD.md`](MODEL_CARD.md) |
| Why is the environment like this? | [`SETUP.md`](SETUP.md) |

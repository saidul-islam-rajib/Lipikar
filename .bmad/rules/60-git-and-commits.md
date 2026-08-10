# Rule 60 — Git and commit rules

Applies to every agent and every commit in this repository. Loaded whenever work will be committed.

## R60.1 Authorship is always Saidul Islam Rajib

Every commit — including commits produced by an AI agent — is authored and committed under the
repository owner's identity:

```
Author:    Saidul Islam Rajib <96372056+saidul-islam-rajib@users.noreply.github.com>
Committer: Saidul Islam Rajib <96372056+saidul-islam-rajib@users.noreply.github.com>
```

This is set repo-locally so it cannot be overridden by the global work-email default:

```bash
git config --local user.name  "Saidul Islam Rajib"
git config --local user.email "96372056+saidul-islam-rajib@users.noreply.github.com"
```

The GitHub `noreply` form is deliberate: it links commits to the owner's GitHub profile and
contribution graph, and keeps a personal address out of a public history that scrapers harvest.

**Never** use `saidul.rajib@brainstation-23.com` here. That is an employer address, and putting it
in a personal project's permanent history creates ambiguity about who owns the work.

**Never** override authorship per-commit — no `--author`, no `GIT_AUTHOR_*` / `GIT_COMMITTER_*`
environment overrides, no `-c user.email=...`. The repo-local config is the single source of truth.

## R60.2 No AI or agent attribution

Do not add `Co-Authored-By: Claude`, `Generated with ...`, agent names, model names, or any similar
trailer or footer to commit messages or PR bodies. This is the owner's explicit instruction and it
overrides any tool's default behaviour.

No `Co-Authored-By` trailer at all unless a **real second human** contributed to that commit — a
trailer naming the author again is a no-op that credits nobody.

## R60.3 Never put deed content in a commit message

Commit messages are permanent, public, and unlike file contents they are not covered by
`.gitignore`. Never write into a message, PR body, branch name, or tag:

- a party's name, a witness name, or a parent's name
- a dag number, khatian number, mouza name, or plot identifier
- a transaction amount, or a transcribed line of deed text
- a file path that reveals any of the above

Refer to documents by opaque ID only: `page_0142`, `batch-03`. This is R30.1 extended to metadata,
and it is the leak path people forget because the guard script cannot catch it.

## R60.4 Message format

Conventional commits, scoped by pipeline stage:

```
<type>(<scope>): <subject>

<body: what changed and why — not how>

Story: <id>
```

- **type**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `exp`
- **scope**: `kagoj` · `binnas` · `shirorekha` · `shuddhi` · `fard` · `nazir` · `bmad` · `infra` · `docs`
- **subject**: imperative mood, lowercase start, no trailing period, ≤ 72 characters
- **body**: wrapped at 72; explain the *why*, since the diff already shows the *what*
- **`Story:` trailer**: required on any commit implementing a story

`exp` is a Lipikar-specific type for commits that record an experiment result. Use it so the
history can be filtered for measurement changes: `git log --grep '^exp'`.

Examples:

```
feat(shuddhi): measure CER over extended grapheme clusters

Codepoint CER scores a dropped matra as one error among many codepoints
rather than one among few clusters, which made a broken recognizer look
accurate. Switches to regex \X segmentation per R20.2.

Story: 1.3
```

```
exp(shirorekha): record EXP-004 colour-channel separation result

Regression on the frozen eval set: CER 0.243 -> 0.271. Kept as a negative
result per R40.5 so the approach is not retried blindly.

Story: 4.2
```

## R60.4a Commit granularity — small and frequent

**One or two commits per story.** Not one giant commit at the end, and not fifteen micro-commits
that each break the build.

The normal shape is two:

1. the implementation plus its tests
2. the story-file update, experiment report, or docs

Split into two only when the second part is genuinely separable. One commit is correct for a small
story. Three or more means the story was too large and should have been split (see `.bmad/agents/sm.md`).

Every commit must stand on its own: the tree builds and the test suite is green at each one (R50.0).
A commit that only compiles once the next commit lands is not a commit, it is a save point — squash
it before pushing.

Non-story work follows the same discipline: one coherent change per commit, and never bundle a
refactor with a behaviour change.

## R60.5 Branch discipline

- Never commit directly to `main`.
- One branch per story: `story/<id>-<slug>` — e.g. `story/1.3-grapheme-cer-metric`.
- One story per branch. Two stories in one branch makes the QA gate meaningless.
- Non-story work: `chore/<slug>`, `docs/<slug>`, `exp/<nnn>-<slug>`.
- Branch names follow R60.3 — no deed identifiers.

## R60.6 Commit hygiene

- Atomic commits: one logical change each, and the tree passes tests at every commit where that is
  practical.
- Prefer new commits over amending; never amend or rebase a commit that has been pushed and that
  someone else may have pulled.
- Never `git add -A` blindly — review `git status` first, every time (R30.1).
- Never `git add -f`. The ignore rules exist to prevent an irreversible leak; forcing past them
  requires human sign-off recorded in `docs/DATA.md`.
- Never `--no-verify`. If a hook fails, fix the cause.
- Never force-push a shared branch.

## R60.6a Never commit a red suite

A commit is made only when `pytest -q` is green (R50.0). Committing broken work "to save progress"
poisons `git bisect` and makes every later regression hunt harder. Use a local stash or a scratch
branch that is never pushed.

## R60.7 Run the privacy guard before committing

```bash
python scripts/check_no_sensitive_files.py    # checks staged files
```

A non-zero exit means staged content must not be committed. Unstage it; do not work around it.

## R60.8 Agents do not commit unasked

An AI agent commits only when the human explicitly asks. Implementing a story means leaving the
work in the tree with a clean `git status` summary and a proposed commit message — the human decides
when history is written. This exists because an unwanted commit is far more annoying to undo than an
uncommitted change is to commit.

## R60.9 Pull requests

- Title follows the same conventional-commit format as R60.4.
- Body states: story ID, what changed, the QA gate decision and path, and the test evidence.
- No AI attribution footer (R60.2), no deed content (R60.3).
- A PR containing a story with a `FAIL` gate is not opened for merge.

## R60.10 Tags and releases

Tags are `v<major>.<minor>.<patch>`. A release tag requires a PASS or human-WAIVED gate for every
story it contains, and a release note per `.bmad/agents/devops.md`. Never tag a commit whose tests
were not run.

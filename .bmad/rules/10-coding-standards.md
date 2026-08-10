# Rule 10 — Coding standards

## R10.1 Toolchain
Python 3.11 or 3.12 (not the system 3.14 — the ML stack lags). `ruff` for lint and format,
`mypy` for types, `pytest` for tests. Config lives in `pyproject.toml`; no competing configs.

## R10.2 Typed contracts between stages
Stages exchange **frozen dataclasses**, never loose dicts. A dict passed between modules hides
schema drift until it explodes three stages downstream.

```python
@dataclass(frozen=True)
class Line:
    image: np.ndarray
    polygon: Polygon
    reading_order: int
    source_page_id: str
```

Coordinates are always stored in original page space with the transform recorded, so any crop can
be traced back to the pixel a human needs to look at.

## R10.3 Pure functions at the core, I/O at the edges
Image ops, text ops and metrics take values and return values. File reads, model loading, and
network calls live in thin adapter modules. This is what makes the pipeline testable without a
GPU or a corpus.

## R10.4 Nothing hardcoded
No literal thresholds, kernel sizes, model names, learning rates, paths, field names, URLs, or
magic strings in code. Everything configurable comes from `configs/` through a typed config
object; everything user-facing comes from a string resource. See
**`.bmad/rules/70-configuration-and-strings.md`** — that rule is binding, not advisory.

A tuned constant buried in a function body is invisible to the experiment log, unreproducible,
and impossible to vary across environments.

## R10.5 No comments — write code that does not need them

**Do not write inline comments.** Not above a line, not at the end of a line, not to separate
sections, not to restate what the code does. If code needs an inline comment to be understood,
the fix is a better name or a smaller function, not a comment.

The only permitted prose in code:

1. **A short docstring above a function, method, or class** — one to three lines, stating the
   contract: what it returns, units, dtype and range, coordinate space, and what it raises. Only
   where that is not obvious from the signature.
2. **A short module docstring** — one to three lines saying what the module is for. Detail about
   architecture, hazards and rationale belongs in `docs/`, not in a module header.

Forbidden outright: commented-out code, `# TODO` and `# FIXME` (file a story instead), banner
separators, changelog or attribution comments, and comments restating a rule ID.

The one narrow exception: a single short docstring line may record *why* a non-obvious choice was
made when the alternative looks correct and is not — for example that `regex` is used instead of
`re` because `re` cannot match grapheme clusters. Reserve it for genuine traps.

## R10.6 Fail loudly on data assumptions
Validate at boundaries and raise with context. `assert` is for internal invariants only — it
disappears under `-O`. Never `except: pass` around a decode or a normalization step; a silently
swallowed encoding error becomes a corrupt training label.

## R10.7 Logging, not printing
Use the stdlib `logging` module with module-level loggers. **Never log deed text content at
INFO** — log identifiers, shapes, and counts. Readable personal data belongs in DEBUG at most,
and DEBUG is never enabled in a shared environment.

Log messages are developer-facing and stay in code; they are not string resources. Exception
messages are developer-facing too and stay in code.

## R10.8 Determinism where it is affordable
Seed `random`, `numpy`, and `torch` from config. Record the seed in every experiment report.
Where full determinism costs too much throughput, say so explicitly in the report rather than
pretending the run is reproducible.

## R10.9 Tests, and they must pass
- `tests/unit` — pure functions, no disk, no network, no GPU. Must run in under 30 seconds.
- `tests/integration` — pipeline wiring on tiny synthetic fixtures committed to the repo.
- Text utilities require the adversarial cases in R20.9.
- Minimum coverage 70% on `lipikar/`, and coverage is a floor not a goal — an untested
  normalization function is a defect regardless of the percentage.

**The suite must be green before any claim of completion.** See R50.0 — a red or unrun suite means
the work is not done, and saying otherwise is a process breach.

## R10.10 Naming
Modules use the project's Bengali stage names (`kagoj`, `binnas`, `shirorekha`, `shuddhi`,
`fard`, `nazir`). Inside a module, identifiers are ordinary English. Do not romanize Bengali
domain terms in variable names where an English word exists — `mouza` stays `mouza` because it
has no English equivalent, but use `line_image` not `line_chobi`.

Names carry the meaning that comments are forbidden from carrying (R10.5), so spend effort here.

## R10.11 Commits
See **`.bmad/rules/60-git-and-commits.md`** — authorship, message format, commit granularity,
branch discipline, and the rule that commit messages must never contain deed content.

## R10.12 Consistency over local preference
A new module matches the conventions of the modules around it: same config loading, same error
handling, same logging, same test layout, same naming. Two ways of doing the same thing in one
codebase is a defect even when both work, because it doubles what a reader must learn.

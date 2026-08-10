# Rule 70 — Configuration and string resources

Binding rule. Every value that could differ between runs, environments, or languages lives outside
the code. This is what makes the project maintainable and scalable rather than a pile of tuned
literals.

## Part A — Configuration

### R70.1 One place, typed
All configuration lives in `configs/*.yaml` and is loaded into a **frozen dataclass** before use.
Code reads attributes on a typed object, never `dict["key"]` and never `os.environ` directly.

```python
cfg = load_config(StageConfig, "configs/kagoj.yaml")
threshold = cfg.binarization.window_size
```

A config value reached through a dict lookup has no type, no default, and no validation, which
defeats the purpose of having a config at all.

### R70.2 What must be configuration
Non-exhaustive, but all of these are always config:

- thresholds, kernel sizes, window sizes, tolerances
- model identifiers, checkpoint paths, tokenizer names
- learning rates, batch sizes, epochs, seeds, augmentation parameters
- input and output directory paths
- the recognition charset (R20.5) and its unknown-token symbol
- extracted field names and their validation patterns (`fard`)
- lexicon file paths (`shuddhi`)
- eval manifest paths and metric target thresholds
- timeouts, retry counts, batch limits
- service ports, base URLs, CORS origins

### R70.3 What must never be configuration
Secrets. No credentials, API keys, or tokens in `configs/` — they come from environment variables
loaded at the process edge, and `.env` is gitignored. `.env.example` documents the required names
with empty values.

### R70.4 Layering and precedence
`configs/default.yaml` → `configs/<env>.yaml` → environment variables. Later wins. Every key must
exist in `default.yaml` so the full surface is discoverable in one file.

### R70.5 Validate on load, fail fast
Loading validates types, ranges, and required keys, and **rejects unknown keys**. A typo in a YAML
key must be an error at startup, not a silently ignored setting that makes an experiment
irreproducible.

### R70.6 Config is part of the result
Every experiment report and every checkpoint records the config path and its content hash (R40.5,
R40.9). A number produced by an unrecorded config is not a result.

### R70.7 No environment sniffing in business logic
Stage code never checks `if platform == "win32"` or `if env == "prod"`. Behaviour differences are
expressed as config values that the environment sets.

## Part B — String resources

### R70.8 User-facing text is never a literal in code
Every string a human reads — UI labels, API messages, validation errors shown to an operator,
report headings, CLI help — comes from a resource file, addressed by a stable key.

```
lipikar/resources/strings/en.yaml
lipikar/resources/strings/bn.yaml
```

```python
t("nazir.field.unverified_badge")
```

Never build a user-facing sentence by concatenation.

### R70.9 Bengali is a first-class locale, not an afterthought
This project's users read Bengali. `bn.yaml` is a real deliverable, not a stub, and:

- all Bengali resource values are NFC-normalized (R20.1)
- the file is UTF-8 without BOM
- translations are reviewed by someone who reads Bengali; machine-translated UI text is not shipped

### R70.10 Placeholders, not concatenation
Interpolate with **named** placeholders so translators can reorder them:

```yaml
nazir.review.progress: "{done} of {total} fields verified"
```

Bengali word order differs from English. Positional or concatenated assembly produces broken
grammar and is a defect, not a cosmetic issue.

### R70.11 Keys are namespaced and stable
`<stage>.<component>.<intent>` — e.g. `nazir.field.low_confidence_warning`. Keys are renamed only
deliberately; a key is an API. Never reuse a key for different meaning.

### R70.12 No missing-key fallback to the key itself
A lookup miss raises in development and test, and logs an error in production. Silently rendering
`nazir.field.unverified_badge` to a user is worse than an obvious failure, and it hides gaps in
`bn.yaml`.

### R70.13 Every locale file has the same key set
A test asserts that `bn.yaml` and `en.yaml` have identical keys. Drift between locales is caught by
CI, not by a user seeing an English string in a Bengali interface.

### R70.14 The assistive-output notice is a resource
The mandatory "unverified, awaiting human confirmation" text (R00.6) lives in the resource files in
both locales and is referenced everywhere it appears. It is never re-typed inline, so it can never
be accidentally omitted or weakened in one surface.

### R70.15 What is not a string resource
Log messages, exception messages, and developer-facing docstrings stay in code (R10.7). They are
read by developers, never by users, and externalizing them adds indirection for no benefit.

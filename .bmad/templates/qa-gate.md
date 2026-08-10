# QA Gate — Story <id> <title>

**Decision:** PASS | CONCERNS | FAIL | WAIVED
**Reviewed by:** QA (Sharmin) · **Date:** <yyyy-mm-dd> · **Commit:** `<hash>`

## Verification I performed myself
<What you actually ran, with your own output. Not the Dev agent's pasted output.>

```
$ pytest -q
```

```
$ ruff check . && mypy lipikar
```

## Acceptance criteria

| AC | Statement | Met? | Evidence |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

## Targeted checks (QA agent, §"checks that actually catch bugs")

| # | Check | Result |
|---|---|---|
| 1 | Cluster-based CER, no codepoint measurement | |
| 2 | NFC boundary holds through the real path | |
| 3 | No visual-order / x-sorted character ordering | |
| 4 | Out-of-charset chars → `<unk>` **and logged** | |
| 5 | Writer-disjoint splits verified by inspection | |
| 6 | Frozen eval manifest unmodified | |
| 7 | No data/ or image files in the diff or history | |
| 8 | Metric on frozen set, with size + distribution | |
| 9 | Surfaced confidence is calibrated | |
| 10 | Output framed as assistive, not authoritative | |

*(Mark N/A where genuinely not applicable — and say why.)*

## Test quality assessment
<Do the tests verify behaviour, or just that code runs? Name any test that would pass against a
broken implementation.>

## Findings

| Sev | Location | What is wrong | How it fails | Suggested fix |
|---|---|---|---|---|
| high / med / low | `file:line` | | | |

## Follow-up stories created
<ids and titles, or none. Required if decision is CONCERNS.>

## Waiver
*(Only if WAIVED. Record the human's reason verbatim — do not paraphrase.)*
**Authorized by:** <human> · **Reason:** "<verbatim>"

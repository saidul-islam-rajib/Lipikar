"""Grapheme-cluster error rates. Codepoint measurement on Bengali is a bug (R20.2)."""

from __future__ import annotations

from collections.abc import Sequence

import regex

from lipikar.config import MetricsConfig

GRAPHEME_PATTERN = r"\X"


def grapheme_clusters(text: str) -> tuple[str, ...]:
    """Segment into extended grapheme clusters — what a reader perceives as one character."""
    return tuple(regex.findall(GRAPHEME_PATTERN, text))


def words(text: str, config: MetricsConfig) -> tuple[str, ...]:
    return tuple(token for token in text.split(config.word_separator) if token)


def edit_distance(reference: Sequence[str], hypothesis: Sequence[str]) -> int:
    if not reference:
        return len(hypothesis)
    previous = list(range(len(reference) + 1))
    for hypothesis_index, hypothesis_token in enumerate(hypothesis, start=1):
        current = [hypothesis_index]
        for reference_index, reference_token in enumerate(reference, start=1):
            substitution = previous[reference_index - 1] + (
                0 if reference_token == hypothesis_token else 1
            )
            current.append(min(previous[reference_index] + 1, current[-1] + 1, substitution))
        previous = current
    return previous[-1]


def grapheme_cer(reference: str, hypothesis: str) -> float:
    """Character error rate over grapheme clusters. Inputs must already be normalized (R20.1)."""
    return _error_rate(grapheme_clusters(reference), grapheme_clusters(hypothesis))


def word_error_rate(reference: str, hypothesis: str, config: MetricsConfig) -> float:
    """Word error rate. Inputs must already be normalized (R20.1)."""
    return _error_rate(words(reference, config), words(hypothesis, config))


def codepoint_cer(reference: str, hypothesis: str) -> float:
    """Deliberately wrong for Bengali. Exists so tests can prove the difference (R20.2)."""
    return _error_rate(tuple(reference), tuple(hypothesis))


def _error_rate(reference: Sequence[str], hypothesis: Sequence[str]) -> float:
    if not reference:
        return 0.0 if not hypothesis else 1.0
    return edit_distance(reference, hypothesis) / len(reference)

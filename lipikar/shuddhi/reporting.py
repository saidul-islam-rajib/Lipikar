"""Distribution reporting. A bare mean hides the failures that matter (R40.7)."""

from __future__ import annotations

import math
import statistics
from collections.abc import Iterable
from dataclasses import dataclass

from lipikar.config import MetricsConfig


class ReportingError(Exception):
    """Raised when a summary is requested over no samples at all."""


@dataclass(frozen=True)
class Sample:
    item_id: str
    score: float


@dataclass(frozen=True)
class MetricSummary:
    sample_size: int
    mean: float
    median: float
    percentiles: tuple[tuple[int, float], ...]
    worst: tuple[Sample, ...]


def summarize(samples: Iterable[Sample], config: MetricsConfig) -> MetricSummary:
    """Mean, median, configured percentiles, worst-N and sample size — never a bare mean."""
    collected = tuple(samples)
    if not collected:
        raise ReportingError("cannot summarize an empty sample set")
    scores = sorted(sample.score for sample in collected)
    ranked = sorted(collected, key=lambda sample: (-sample.score, sample.item_id))
    return MetricSummary(
        sample_size=len(collected),
        mean=statistics.fmean(scores),
        median=statistics.median(scores),
        percentiles=tuple(
            (percentile, _percentile(scores, percentile)) for percentile in config.percentiles
        ),
        worst=tuple(ranked[: config.worst_n]),
    )


def _percentile(sorted_scores: list[float], percentile: int) -> float:
    """Nearest-rank percentile — no interpolation, so the value is always an observed score."""
    if not 0 < percentile <= 100:
        raise ReportingError(f"percentile must be in (0, 100]: {percentile}")
    rank = math.ceil(percentile / 100 * len(sorted_scores))
    return sorted_scores[max(rank - 1, 0)]

import pytest

from lipikar.config import AppConfig, MetricsConfig
from lipikar.shuddhi.reporting import ReportingError, Sample, summarize

SAMPLES = tuple(Sample(item_id=f"page_{index:04d}", score=index / 10) for index in range(10))


def test_summary_reports_the_whole_distribution(config: AppConfig) -> None:
    summary = summarize(SAMPLES, config.metrics)
    assert summary.sample_size == 10
    assert summary.mean == pytest.approx(0.45)
    assert summary.median == pytest.approx(0.45)
    assert dict(summary.percentiles) == {90: pytest.approx(0.8), 95: pytest.approx(0.9)}


def test_worst_samples_come_first_and_are_capped(config: AppConfig) -> None:
    metrics = MetricsConfig(worst_n=3, percentiles=config.metrics.percentiles, word_separator=" ")
    summary = summarize(SAMPLES, metrics)
    assert [sample.item_id for sample in summary.worst] == ["page_0009", "page_0008", "page_0007"]


def test_ties_break_deterministically(config: AppConfig) -> None:
    tied = (Sample("page_0002", 0.5), Sample("page_0001", 0.5))
    summary = summarize(tied, config.metrics)
    assert [sample.item_id for sample in summary.worst] == ["page_0001", "page_0002"]


def test_summarizing_nothing_is_an_error(config: AppConfig) -> None:
    with pytest.raises(ReportingError, match="empty sample set"):
        summarize((), config.metrics)


def test_percentile_outside_the_valid_range_is_an_error(config: AppConfig) -> None:
    metrics = MetricsConfig(worst_n=1, percentiles=(0,), word_separator=" ")
    with pytest.raises(ReportingError, match="percentile must be"):
        summarize(SAMPLES, metrics)

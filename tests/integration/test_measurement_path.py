"""The measurement path wired end to end on synthetic text, exactly as a story would use it."""

from pathlib import Path

import pytest

from lipikar.config import AppConfig, load_config
from lipikar.evaluation.manifest import ManifestEntry, build_manifest, load_manifest, write_manifest
from lipikar.shirorekha.charset import decode, encode, load_charset
from lipikar.shuddhi.metrics import grapheme_cer, grapheme_clusters
from lipikar.shuddhi.reporting import Sample, summarize
from lipikar.shuddhi.text import normalize

REPO_ROOT = Path(__file__).resolve().parents[2]

LINE_WITH_ONE_UNSUPPORTED_CHARACTER = "মৌজা ৺ঢাকা"
LINE_CLUSTERS = 6
UNSUPPORTED_CLUSTERS = 1

REFERENCES = {
    "page_0001": "দাগ ১২৩",
    "page_0002": "মৌজা ক্ষেত্র",
    "page_0003": "খতিয়ান 45",
}
PREDICTIONS = {
    "page_0001": "দাগ ১২৩",
    "page_0002": "মৌজা কেত্র",
    "page_0003": "খতিয়ান 46",
}


@pytest.fixture(scope="module")
def app_config() -> AppConfig:
    return load_config(AppConfig, REPO_ROOT / "configs", environ={})


def test_text_survives_the_charset_round_trip(app_config: AppConfig) -> None:
    charset = load_charset(app_config.charset, REPO_ROOT / "configs", app_config.text)
    for reference in REFERENCES.values():
        normalized = normalize(reference, app_config.text)
        assert decode(encode(normalized, charset), charset) == normalized


def test_one_unknown_character_costs_one_cluster(app_config: AppConfig) -> None:
    charset = load_charset(app_config.charset, REPO_ROOT / "configs", app_config.text)
    reference = normalize(LINE_WITH_ONE_UNSUPPORTED_CHARACTER, app_config.text)
    decoded = decode(encode(reference, charset), charset)

    assert len(grapheme_clusters(reference)) == LINE_CLUSTERS
    assert len(grapheme_clusters(decoded)) == LINE_CLUSTERS
    assert grapheme_cer(reference, decoded) == pytest.approx(UNSUPPORTED_CLUSTERS / LINE_CLUSTERS)


def test_scoring_a_frozen_eval_set_produces_a_distribution(app_config: AppConfig) -> None:
    samples = tuple(
        Sample(
            item_id=page_id,
            score=grapheme_cer(
                normalize(REFERENCES[page_id], app_config.text),
                normalize(PREDICTIONS[page_id], app_config.text),
            ),
        )
        for page_id in sorted(REFERENCES)
    )
    summary = summarize(samples, app_config.metrics)

    assert summary.sample_size == len(REFERENCES)
    assert summary.worst[0].item_id == "page_0002"
    assert summary.worst[-1].score == 0.0
    assert dict(summary.percentiles)[90] == summary.worst[0].score


def test_manifest_freezes_the_eval_set(app_config: AppConfig, tmp_path: Path) -> None:
    entries = tuple(
        ManifestEntry(page_id=page_id, content_hash=f"{index:064x}")
        for index, page_id in enumerate(sorted(REFERENCES))
    )
    manifest = build_manifest(entries, app_config.manifest)
    path = tmp_path / "eval_manifest.yaml"
    write_manifest(manifest, path)

    assert load_manifest(path, app_config.manifest).entries == manifest.entries

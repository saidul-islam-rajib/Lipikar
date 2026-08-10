import hashlib
from pathlib import Path

import pytest
import yaml

from lipikar.config import AppConfig, ManifestConfig
from lipikar.evaluation.manifest import (
    EvalManifest,
    ManifestEntry,
    ManifestError,
    build_manifest,
    hash_file,
    load_manifest,
    write_manifest,
)

ENTRIES = (
    ManifestEntry(page_id="page_0002", content_hash="b" * 64),
    ManifestEntry(page_id="page_0001", content_hash="a" * 64),
)


@pytest.fixture
def manifest(config: AppConfig) -> EvalManifest:
    return build_manifest(ENTRIES, config.manifest)


def test_entries_are_ordered_by_page_id(manifest: EvalManifest) -> None:
    assert [entry.page_id for entry in manifest.entries] == ["page_0001", "page_0002"]


def test_checksum_ignores_insertion_order(config: AppConfig, manifest: EvalManifest) -> None:
    assert build_manifest(reversed(ENTRIES), config.manifest).checksum == manifest.checksum


def test_write_then_load_round_trip(
    manifest: EvalManifest, config: AppConfig, tmp_path: Path
) -> None:
    path = tmp_path / "eval.yaml"
    write_manifest(manifest, path)
    assert load_manifest(path, config.manifest) == manifest


def test_editing_an_entry_is_detected(
    manifest: EvalManifest, config: AppConfig, tmp_path: Path
) -> None:
    path = tmp_path / "eval.yaml"
    write_manifest(manifest, path)
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["entries"][0]["content_hash"] = "c" * 64
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    with pytest.raises(ManifestError, match="integrity check failed"):
        load_manifest(path, config.manifest)


def test_adding_an_entry_is_detected(
    manifest: EvalManifest, config: AppConfig, tmp_path: Path
) -> None:
    path = tmp_path / "eval.yaml"
    write_manifest(manifest, path)
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["entries"].append({"page_id": "page_9999", "content_hash": "d" * 64})
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")
    with pytest.raises(ManifestError, match="integrity check failed"):
        load_manifest(path, config.manifest)


def test_duplicate_page_ids_are_rejected(config: AppConfig) -> None:
    duplicated = (*ENTRIES, ManifestEntry(page_id="page_0001", content_hash="e" * 64))
    with pytest.raises(ManifestError, match="duplicate page id"):
        build_manifest(duplicated, config.manifest)


def test_schema_version_mismatch_is_rejected(
    manifest: EvalManifest, config: AppConfig, tmp_path: Path
) -> None:
    path = tmp_path / "eval.yaml"
    write_manifest(manifest, path)
    other = ManifestConfig(
        hash_algorithm=config.manifest.hash_algorithm,
        schema_version=config.manifest.schema_version + 1,
    )
    with pytest.raises(ManifestError, match="schema version"):
        load_manifest(path, other)


def test_hash_file_matches_the_configured_algorithm(config: AppConfig, tmp_path: Path) -> None:
    path = tmp_path / "page.bin"
    payload = b"synthetic page bytes"
    path.write_bytes(payload)
    expected = hashlib.new(config.manifest.hash_algorithm, payload).hexdigest()
    assert hash_file(path, config.manifest) == expected


def test_missing_manifest_fails_loudly(config: AppConfig, tmp_path: Path) -> None:
    with pytest.raises(ManifestError, match="manifest not found"):
        load_manifest(tmp_path / "absent.yaml", config.manifest)

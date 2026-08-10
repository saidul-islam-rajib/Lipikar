"""The frozen eval set definition. Holds opaque page IDs and hashes, never deed text (R30.1)."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from lipikar.config import ManifestConfig

CHECKSUM_FIELD = "checksum"
READ_BLOCK_BYTES = 65536


class ManifestError(Exception):
    """Raised when a manifest is malformed, mis-versioned, or fails its integrity check."""


@dataclass(frozen=True)
class ManifestEntry:
    page_id: str
    content_hash: str


@dataclass(frozen=True)
class EvalManifest:
    schema_version: int
    hash_algorithm: str
    entries: tuple[ManifestEntry, ...]
    checksum: str


def hash_file(path: Path, config: ManifestConfig) -> str:
    digest = hashlib.new(config.hash_algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(READ_BLOCK_BYTES), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(entries: Iterable[ManifestEntry], config: ManifestConfig) -> EvalManifest:
    """Order entries by page ID so the checksum depends on content, not on insertion order."""
    ordered = tuple(sorted(entries, key=lambda entry: entry.page_id))
    identifiers = [entry.page_id for entry in ordered]
    duplicates = sorted({name for name in identifiers if identifiers.count(name) > 1})
    if duplicates:
        raise ManifestError(f"duplicate page id(s): {', '.join(duplicates)}")
    return EvalManifest(
        schema_version=config.schema_version,
        hash_algorithm=config.hash_algorithm,
        entries=ordered,
        checksum=_checksum(config.schema_version, config.hash_algorithm, ordered),
    )


def write_manifest(manifest: EvalManifest, path: Path) -> None:
    document = {
        "schema_version": manifest.schema_version,
        "hash_algorithm": manifest.hash_algorithm,
        "entries": [
            {"page_id": entry.page_id, "content_hash": entry.content_hash}
            for entry in manifest.entries
        ],
        CHECKSUM_FIELD: manifest.checksum,
    }
    path.write_text(yaml.safe_dump(document, sort_keys=True), encoding="utf-8")


def load_manifest(path: Path, config: ManifestConfig) -> EvalManifest:
    """Load and verify. Any edit to the entries after writing makes this raise (R40.3)."""
    if not path.is_file():
        raise ManifestError(f"manifest not found: {path}")
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ManifestError(f"manifest must be a mapping: {path}")
    schema_version = document.get("schema_version")
    if schema_version != config.schema_version:
        raise ManifestError(
            f"manifest schema version {schema_version!r} does not match the configured "
            f"{config.schema_version!r}"
        )
    algorithm = document.get("hash_algorithm")
    if algorithm != config.hash_algorithm:
        raise ManifestError(
            f"manifest hash algorithm {algorithm!r} does not match the configured "
            f"{config.hash_algorithm!r}"
        )
    entries = _read_entries(document.get("entries"), path)
    recorded = document.get(CHECKSUM_FIELD)
    expected = _checksum(config.schema_version, config.hash_algorithm, entries)
    if recorded != expected:
        raise ManifestError(
            f"manifest integrity check failed for {path}: the frozen eval set has been modified"
        )
    return EvalManifest(
        schema_version=config.schema_version,
        hash_algorithm=config.hash_algorithm,
        entries=entries,
        checksum=expected,
    )


def _read_entries(raw: Any, path: Path) -> tuple[ManifestEntry, ...]:
    if not isinstance(raw, list):
        raise ManifestError(f"manifest must define an 'entries' list: {path}")
    entries: list[ManifestEntry] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ManifestError(f"manifest entry must be a mapping: {path}")
        page_id = item.get("page_id")
        content_hash = item.get("content_hash")
        if not isinstance(page_id, str) or not isinstance(content_hash, str):
            raise ManifestError(f"manifest entry needs string page_id and content_hash: {path}")
        entries.append(ManifestEntry(page_id=page_id, content_hash=content_hash))
    return tuple(entries)


def _checksum(schema_version: int, hash_algorithm: str, entries: tuple[ManifestEntry, ...]) -> str:
    digest = hashlib.new(hash_algorithm)
    digest.update(f"{schema_version}\n{hash_algorithm}\n".encode())
    for entry in entries:
        digest.update(f"{entry.page_id}\t{entry.content_hash}\n".encode())
    return digest.hexdigest()

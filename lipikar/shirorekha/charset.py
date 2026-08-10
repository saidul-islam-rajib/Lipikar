"""The recognition alphabet, loaded from a versioned file — never inferred from data (R20.5)."""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from lipikar.config import CharsetConfig, TextConfig
from lipikar.shuddhi.text import normalize

UNKNOWN_INDEX = 0

logger = logging.getLogger(__name__)


class CharsetError(Exception):
    """Raised when the charset file is absent, malformed, or the wrong version."""


@dataclass(frozen=True)
class Charset:
    version: str
    unknown_token: str
    symbols: tuple[str, ...]
    index: Mapping[str, int]


def load_charset(config: CharsetConfig, config_dir: Path, text_config: TextConfig) -> Charset:
    """Load the versioned alphabet, NFC-normalized through the one text boundary (R20.1)."""
    path = config_dir / config.path
    if not path.is_file():
        raise CharsetError(f"charset file not found: {path}")
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise CharsetError(f"charset file must be a mapping: {path}")
    version = document.get("version")
    if version != config.version:
        raise CharsetError(
            f"charset version mismatch: file has {version!r}, config wants {config.version!r}"
        )
    symbols = _collect(document.get("groups"), text_config, path)
    ordered = (config.unknown_token, *symbols)
    return Charset(
        version=config.version,
        unknown_token=config.unknown_token,
        symbols=ordered,
        index=MappingProxyType({symbol: position for position, symbol in enumerate(ordered)}),
    )


def encode(text: str, charset: Charset) -> tuple[int, ...]:
    """Map to alphabet indices; unknown characters become the unknown token and are logged."""
    encoded: list[int] = []
    for character in text:
        position = charset.index.get(character)
        if position is None:
            logger.warning(
                "character U+%04X is outside charset v%s", ord(character), charset.version
            )
            encoded.append(UNKNOWN_INDEX)
        else:
            encoded.append(position)
    return tuple(encoded)


def decode(indices: Sequence[int], charset: Charset) -> str:
    for position in indices:
        if position < 0 or position >= len(charset.symbols):
            raise CharsetError(f"index {position} is outside charset v{charset.version}")
    return "".join(charset.symbols[position] for position in indices)


def _collect(groups: Any, text_config: TextConfig, path: Path) -> tuple[str, ...]:
    if not isinstance(groups, dict):
        raise CharsetError(f"charset file must define a 'groups' mapping: {path}")
    seen: dict[str, None] = {}
    for name, members in groups.items():
        if not isinstance(members, str):
            raise CharsetError(f"charset group {name!r} must be a string: {path}")
        for character in normalize(members, text_config):
            seen.setdefault(character, None)
    if not seen:
        raise CharsetError(f"charset file defines no characters: {path}")
    return tuple(seen)

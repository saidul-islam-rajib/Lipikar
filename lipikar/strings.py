"""String resource lookup. User-facing text is never a literal in code (R70.8)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from importlib import resources
from types import MappingProxyType
from typing import Any

import yaml

from lipikar.config import TextConfig
from lipikar.shuddhi.text import normalize

RESOURCE_PACKAGE = "lipikar"
RESOURCE_DIRECTORY = "resources/strings"
KEY_SEPARATOR = "."


class StringResourceError(Exception):
    """Raised for a missing locale, a malformed resource file, or an unknown key (R70.12)."""


@dataclass(frozen=True)
class StringCatalog:
    locale: str
    entries: Mapping[str, str]


def load_catalog(locale: str, config: TextConfig) -> StringCatalog:
    """Read a locale's resources through the same text boundary as every other string (R20.1)."""
    anchor = resources.files(RESOURCE_PACKAGE).joinpath(f"{RESOURCE_DIRECTORY}/{locale}.yaml")
    if not anchor.is_file():
        raise StringResourceError(f"no string resources for locale {locale!r}")
    document = yaml.safe_load(anchor.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise StringResourceError(f"string resources for {locale!r} must be a mapping")
    flattened: dict[str, str] = {}
    _flatten(document, (), flattened, locale, config)
    return StringCatalog(locale=locale, entries=MappingProxyType(flattened))


def translate(catalog: StringCatalog, key: str, **placeholders: object) -> str:
    """Look up and interpolate. A missing key raises rather than rendering the key (R70.12)."""
    template = catalog.entries.get(key)
    if template is None:
        raise StringResourceError(f"key {key!r} is missing from locale {catalog.locale!r}")
    try:
        return template.format(**placeholders)
    except KeyError as error:
        raise StringResourceError(
            f"key {key!r} in locale {catalog.locale!r} needs placeholder {error.args[0]!r}"
        ) from error


def _flatten(
    document: Mapping[str, Any],
    path: tuple[str, ...],
    target: dict[str, str],
    locale: str,
    config: TextConfig,
) -> None:
    for name, value in document.items():
        location = path + (str(name),)
        if isinstance(value, dict):
            _flatten(value, location, target, locale, config)
        elif isinstance(value, str):
            target[KEY_SEPARATOR.join(location)] = normalize(value, config)
        else:
            raise StringResourceError(
                f"{KEY_SEPARATOR.join(location)} in locale {locale!r} must be a string"
            )

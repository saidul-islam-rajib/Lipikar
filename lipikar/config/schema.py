"""Typed configuration surface. Every key here must exist in `configs/default.yaml` (R70.4)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextConfig:
    normalization_form: str
    zero_width_codepoints: tuple[str, ...]
    danda_codepoint: str


@dataclass(frozen=True)
class BinnasConfig:
    region_kinds: tuple[str, ...]


@dataclass(frozen=True)
class MetricsConfig:
    worst_n: int
    percentiles: tuple[int, ...]
    word_separator: str


@dataclass(frozen=True)
class CharsetConfig:
    path: str
    version: str
    unknown_codepoint: str
    unknown_label: str


@dataclass(frozen=True)
class ManifestConfig:
    hash_algorithm: str
    schema_version: int


@dataclass(frozen=True)
class StringsConfig:
    default_locale: str
    locales: tuple[str, ...]


@dataclass(frozen=True)
class AppConfig:
    text: TextConfig
    binnas: BinnasConfig
    metrics: MetricsConfig
    charset: CharsetConfig
    manifest: ManifestConfig
    strings: StringsConfig

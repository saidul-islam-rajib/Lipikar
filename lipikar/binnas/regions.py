"""Region kinds are a closed set and they come from configuration, not from code (R70.2)."""

from __future__ import annotations

from lipikar.config import BinnasConfig


class RegionKindError(Exception):
    """Raised when a region kind is not in the configured closed set."""


def validate_kind(kind: str, config: BinnasConfig) -> str:
    if kind not in config.region_kinds:
        known = ", ".join(config.region_kinds)
        raise RegionKindError(f"unknown region kind {kind!r}; configured kinds are: {known}")
    return kind

"""The single boundary every string crosses on entry to the system (R20.1, R20.4)."""

from __future__ import annotations

import unicodedata
from typing import Literal, cast

from lipikar.config import TextConfig

NormalizationForm = Literal["NFC", "NFD", "NFKC", "NFKD"]
NORMALIZATION_FORMS = frozenset({"NFC", "NFD", "NFKC", "NFKD"})


class TextPolicyError(Exception):
    """Raised when the configured text policy is not one this codebase can honour."""


def normalize(text: str, config: TextConfig) -> str:
    """Strip zero-width joiners, then normalize. Apply once, at ingestion, never at comparison."""
    stripped = text.translate(dict.fromkeys(_zero_width_ordinals(config)))
    return unicodedata.normalize(_form(config), stripped)


def danda(config: TextConfig) -> str:
    """The Bengali sentence terminator । — never an ASCII full stop (R20.5)."""
    return character_from_codepoint(config.danda_codepoint)


def character_from_codepoint(codepoint: str) -> str:
    """The character a hex codepoint string names — the form configs use for exotic characters."""
    return chr(int(codepoint, 16))


def _form(config: TextConfig) -> NormalizationForm:
    if config.normalization_form not in NORMALIZATION_FORMS:
        raise TextPolicyError(f"unsupported normalization form: {config.normalization_form!r}")
    return cast(NormalizationForm, config.normalization_form)


def _zero_width_ordinals(config: TextConfig) -> tuple[int, ...]:
    return tuple(int(codepoint, 16) for codepoint in config.zero_width_codepoints)

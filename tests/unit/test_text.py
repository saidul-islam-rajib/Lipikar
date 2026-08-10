import unicodedata

import pytest

from lipikar.config import AppConfig, TextConfig
from lipikar.shuddhi.text import TextPolicyError, danda, normalize

CONJUNCT = "ক্ষ"
PRE_BASE_VOWEL = "কি"
COMPOSED_VOWEL = "কো"
ZWJ = "‍"
ZWNJ = "‌"


def test_conjunct_survives_normalization(config: AppConfig) -> None:
    assert normalize(CONJUNCT, config.text) == CONJUNCT


def test_pre_base_vowel_sign_survives_normalization(config: AppConfig) -> None:
    assert normalize(PRE_BASE_VOWEL, config.text) == PRE_BASE_VOWEL


def test_nfd_input_normalizes_equal_to_its_nfc_twin(config: AppConfig) -> None:
    decomposed = unicodedata.normalize("NFD", COMPOSED_VOWEL)
    assert decomposed != COMPOSED_VOWEL
    assert normalize(decomposed, config.text) == normalize(COMPOSED_VOWEL, config.text)


def test_zero_width_joiner_is_stripped(config: AppConfig) -> None:
    assert normalize(f"ক{ZWJ}্ষ", config.text) == CONJUNCT


def test_zero_width_non_joiner_is_stripped(config: AppConfig) -> None:
    assert normalize(f"ক{ZWNJ}্ষ", config.text) == CONJUNCT


def test_danda_is_preserved_and_is_not_a_full_stop(config: AppConfig) -> None:
    terminator = danda(config.text)
    assert terminator == "।"
    assert terminator != "."
    assert normalize(f"বাক্য{terminator}", config.text).endswith(terminator)


def test_mixed_bengali_and_ascii_digits_are_preserved(config: AppConfig) -> None:
    assert normalize("১২৩ 456", config.text) == "১২৩ 456"


def test_unsupported_normalization_form_fails_loudly(config: AppConfig) -> None:
    broken = TextConfig(
        normalization_form="NFZ",
        zero_width_codepoints=config.text.zero_width_codepoints,
        danda_codepoint=config.text.danda_codepoint,
    )
    with pytest.raises(TextPolicyError, match="unsupported normalization form"):
        normalize("ক", broken)

import unicodedata

import pytest

from lipikar.config import AppConfig
from lipikar.shuddhi.metrics import (
    codepoint_cer,
    grapheme_cer,
    grapheme_clusters,
    word_error_rate,
    words,
)
from lipikar.shuddhi.text import normalize

CONJUNCT = "ক্ষ"
PRE_BASE_VOWEL = "কি"
COMPOSED_VOWEL = "কো"
ZWJ = "‍"


def test_conjunct_is_one_cluster_but_three_codepoints() -> None:
    assert len(grapheme_clusters(CONJUNCT)) == 1
    assert len(CONJUNCT) == 3


def test_pre_base_vowel_sign_is_one_cluster_but_two_codepoints() -> None:
    assert len(grapheme_clusters(PRE_BASE_VOWEL)) == 1
    assert len(PRE_BASE_VOWEL) == 2


def test_grapheme_cer_differs_from_codepoint_cer_on_a_conjunct() -> None:
    """Dropping a conjunct is a total error, but codepoint CER scores it as a third of one."""
    assert grapheme_cer(CONJUNCT, "ক") == 1.0
    assert codepoint_cer(CONJUNCT, "ক") == pytest.approx(2 / 3)
    assert grapheme_cer(CONJUNCT, "ক") > codepoint_cer(CONJUNCT, "ক")


def test_nfd_and_nfc_twins_score_zero_through_the_real_path(config: AppConfig) -> None:
    decomposed = unicodedata.normalize("NFD", COMPOSED_VOWEL)
    assert decomposed != COMPOSED_VOWEL
    reference = normalize(COMPOSED_VOWEL, config.text)
    hypothesis = normalize(decomposed, config.text)
    assert grapheme_cer(reference, hypothesis) == 0.0


def test_zero_width_joiner_difference_scores_zero_after_normalization(config: AppConfig) -> None:
    reference = normalize(CONJUNCT, config.text)
    hypothesis = normalize(f"ক{ZWJ}্ষ", config.text)
    assert grapheme_cer(reference, hypothesis) == 0.0


def test_mixed_bengali_and_ascii_digits_are_measured_as_clusters() -> None:
    assert grapheme_clusters("১২ 34") == ("১", "২", " ", "3", "4")
    assert grapheme_cer("১২৩", "১২8") == pytest.approx(1 / 3)


def test_danda_is_a_measured_cluster() -> None:
    assert grapheme_clusters("বাক্য।") == ("বা", "ক্য", "।")
    assert grapheme_cer("বাক্য।", "বাক্য") == pytest.approx(1 / 3)


def test_identical_strings_score_zero() -> None:
    assert grapheme_cer(CONJUNCT, CONJUNCT) == 0.0


def test_empty_reference_scores_zero_only_against_an_empty_hypothesis() -> None:
    assert grapheme_cer("", "") == 0.0
    assert grapheme_cer("", "ক") == 1.0


def test_word_error_rate_counts_whole_words(config: AppConfig) -> None:
    assert words("দাগ ১২৩", config.metrics) == ("দাগ", "১২৩")
    assert word_error_rate("দাগ ১২৩", "দাগ ১২৪", config.metrics) == pytest.approx(0.5)
    assert word_error_rate("দাগ ১২৩", "দাগ ১২৩", config.metrics) == 0.0

import logging
from pathlib import Path

import pytest

from lipikar.config import AppConfig, CharsetConfig
from lipikar.shirorekha.charset import (
    UNKNOWN_INDEX,
    Charset,
    CharsetError,
    decode,
    encode,
    load_charset,
)
from lipikar.shuddhi.text import danda, normalize

OUT_OF_CHARSET = "漢"


@pytest.fixture(scope="session")
def charset(config: AppConfig, config_dir: Path) -> Charset:
    return load_charset(config.charset, config_dir, config.text)


@pytest.mark.parametrize(
    ("character", "category"),
    [
        ("ক", "consonant"),
        ("অ", "independent vowel"),
        ("ি", "pre-base vowel sign"),
        ("্", "hasanta"),
        ("়", "nukta"),
        ("৫", "bengali digit"),
        ("5", "ascii digit"),
        ("A", "ascii letter"),
        ("৳", "currency mark"),
        ("।", "danda"),
        (" ", "space"),
    ],
)
def test_charset_covers_every_required_category(
    charset: Charset, character: str, category: str
) -> None:
    assert character in charset.index, category


def test_charset_version_comes_from_the_versioned_file(charset: Charset) -> None:
    assert charset.version == "1"


def test_unknown_token_occupies_the_reserved_index(charset: Charset) -> None:
    assert charset.symbols[UNKNOWN_INDEX] == charset.unknown_token


def test_encode_decode_round_trip(charset: Charset, config: AppConfig) -> None:
    text = normalize(f"দাগ ১২৩ / A5৳{danda(config.text)}", config.text)
    assert decode(encode(text, charset), charset) == text


def test_out_of_charset_character_maps_to_unknown_and_logs_its_codepoint(
    charset: Charset, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.WARNING):
        encoded = encode(OUT_OF_CHARSET, charset)
    assert encoded == (UNKNOWN_INDEX,)
    assert f"U+{ord(OUT_OF_CHARSET):04X}" in caplog.text


def test_decode_rejects_an_index_outside_the_alphabet(charset: Charset) -> None:
    with pytest.raises(CharsetError, match="outside charset"):
        decode([len(charset.symbols)], charset)


def test_version_mismatch_fails_loudly(config: AppConfig, config_dir: Path) -> None:
    mismatched = CharsetConfig(
        path=config.charset.path, version="99", unknown_token=config.charset.unknown_token
    )
    with pytest.raises(CharsetError, match="version mismatch"):
        load_charset(mismatched, config_dir, config.text)


def test_missing_charset_file_fails_loudly(config: AppConfig, tmp_path: Path) -> None:
    with pytest.raises(CharsetError, match="charset file not found"):
        load_charset(config.charset, tmp_path, config.text)

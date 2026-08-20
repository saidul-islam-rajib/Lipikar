import logging
from dataclasses import replace
from pathlib import Path

import pytest

from lipikar.config import AppConfig
from lipikar.shirorekha.charset import (
    UNKNOWN_INDEX,
    Charset,
    CharsetError,
    decode,
    encode,
    load_charset,
)
from lipikar.shuddhi.metrics import grapheme_cer, grapheme_clusters, word_error_rate
from lipikar.shuddhi.text import character_from_codepoint, danda, normalize

OUT_OF_CHARSET = "漢"
COMPOSED_NUKTA = "\u09dc"
DECOMPOSED_NUKTA = "\u09a1\u09bc"
ALPHABET_SIZE = 156
PINNED_INDICES = ((1, "ক"), (59, "্"), (135, "৳"), (142, "।"), (155, " "))
NORMALIZATION_PRECONDITION = "must already be normalized (R20.1)"


@pytest.fixture(scope="session")
def charset(config: AppConfig, config_dir: Path) -> Charset:
    return load_charset(config.charset, config_dir, config.text)


def write_charset(directory: Path, name: str, version: str, members: str) -> Path:
    directory.mkdir()
    (directory / name).write_text(
        f'version: "{version}"\ngroups:\n  members: "{members}"\n', encoding="utf-8"
    )
    return directory


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


def test_unknown_token_is_a_single_grapheme_cluster(charset: Charset) -> None:
    assert len(grapheme_clusters(decode((UNKNOWN_INDEX,), charset))) == 1


def test_unknown_token_is_not_also_a_charset_member(charset: Charset) -> None:
    assert charset.symbols.count(charset.unknown_token) == 1


def test_alphabet_size_and_indices_are_pinned(charset: Charset) -> None:
    assert len(charset.symbols) == ALPHABET_SIZE
    for position, symbol in PINNED_INDICES:
        assert charset.index[symbol] == position, symbol
        assert charset.symbols[position] == symbol, symbol


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


def test_unknown_label_reaches_diagnostics_but_never_decoded_text(
    charset: Charset, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.WARNING):
        decoded = decode(encode(OUT_OF_CHARSET, charset), charset)
    assert charset.unknown_label in caplog.text
    assert charset.unknown_label not in decoded
    assert decoded == charset.unknown_token


def test_composed_and_decomposed_charset_files_agree(config: AppConfig, tmp_path: Path) -> None:
    composed = write_charset(
        tmp_path / "composed", config.charset.path, config.charset.version, COMPOSED_NUKTA
    )
    decomposed = write_charset(
        tmp_path / "decomposed", config.charset.path, config.charset.version, DECOMPOSED_NUKTA
    )
    from_composed = load_charset(config.charset, composed, config.text)
    from_decomposed = load_charset(config.charset, decomposed, config.text)
    assert from_composed.symbols == from_decomposed.symbols
    assert COMPOSED_NUKTA not in from_composed.index


def test_encode_documents_the_normalization_precondition() -> None:
    assert NORMALIZATION_PRECONDITION in (encode.__doc__ or "")
    assert NORMALIZATION_PRECONDITION in (grapheme_cer.__doc__ or "")
    assert NORMALIZATION_PRECONDITION in (word_error_rate.__doc__ or "")


def test_decode_rejects_an_index_outside_the_alphabet(charset: Charset) -> None:
    with pytest.raises(CharsetError, match="outside charset"):
        decode([len(charset.symbols)], charset)


def test_unknown_codepoint_must_be_a_hex_codepoint(config: AppConfig, config_dir: Path) -> None:
    literal = replace(config.charset, unknown_codepoint=config.charset.unknown_label)
    with pytest.raises(CharsetError, match="not a hex codepoint"):
        load_charset(literal, config_dir, config.text)


def test_unknown_token_colliding_with_a_charset_member_fails_loudly(
    config: AppConfig, tmp_path: Path
) -> None:
    sentinel = character_from_codepoint(config.charset.unknown_codepoint)
    directory = write_charset(
        tmp_path / "collision", config.charset.path, config.charset.version, sentinel
    )
    with pytest.raises(CharsetError, match="is also a charset member"):
        load_charset(config.charset, directory, config.text)


def test_version_mismatch_fails_loudly(config: AppConfig, config_dir: Path) -> None:
    mismatched = replace(config.charset, version="99")
    with pytest.raises(CharsetError, match="version mismatch"):
        load_charset(mismatched, config_dir, config.text)


def test_missing_charset_file_fails_loudly(config: AppConfig, tmp_path: Path) -> None:
    with pytest.raises(CharsetError, match="charset file not found"):
        load_charset(config.charset, tmp_path, config.text)

import unicodedata

import pytest

from lipikar.config import AppConfig
from lipikar.strings import StringCatalog, StringResourceError, load_catalog, translate

ASSISTIVE_NOTICE_KEY = "common.output.assistive_notice"
PROGRESS_KEY = "nazir.review.progress"


@pytest.fixture(scope="session")
def english(config: AppConfig) -> StringCatalog:
    return load_catalog("en", config.text)


@pytest.fixture(scope="session")
def bengali(config: AppConfig) -> StringCatalog:
    return load_catalog("bn", config.text)


def test_every_configured_locale_has_a_catalog(config: AppConfig) -> None:
    for locale in config.strings.locales:
        assert load_catalog(locale, config.text).entries


def test_locales_have_identical_key_sets(english: StringCatalog, bengali: StringCatalog) -> None:
    assert set(english.entries) == set(bengali.entries)


def test_the_assistive_notice_exists_in_both_locales(
    english: StringCatalog, bengali: StringCatalog
) -> None:
    assert english.entries[ASSISTIVE_NOTICE_KEY].strip()
    assert bengali.entries[ASSISTIVE_NOTICE_KEY].strip()


def test_bengali_is_a_real_translation_not_a_copy(
    english: StringCatalog, bengali: StringCatalog
) -> None:
    assert all(bengali.entries[key] != english.entries[key] for key in english.entries)


def test_bengali_values_are_nfc_normalized(bengali: StringCatalog) -> None:
    for key, value in bengali.entries.items():
        assert value == unicodedata.normalize("NFC", value), key


def test_named_placeholders_survive_reordering(
    english: StringCatalog, bengali: StringCatalog
) -> None:
    """Bengali puts {total} before {done}; positional assembly would produce broken grammar."""
    assert translate(english, PROGRESS_KEY, done=3, total=7) == "3 of 7 fields verified"
    rendered = translate(bengali, PROGRESS_KEY, done=3, total=7)
    assert rendered.index("7") < rendered.index("3")


def test_missing_key_raises_instead_of_rendering_the_key(english: StringCatalog) -> None:
    with pytest.raises(StringResourceError, match="is missing from locale"):
        translate(english, "nazir.field.does_not_exist")


def test_missing_placeholder_raises(english: StringCatalog) -> None:
    with pytest.raises(StringResourceError, match="needs placeholder"):
        translate(english, PROGRESS_KEY, done=3)


def test_unknown_locale_raises(config: AppConfig) -> None:
    with pytest.raises(StringResourceError, match="no string resources"):
        load_catalog("xx", config.text)

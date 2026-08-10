import importlib

import pytest
import regex

STAGE_MODULES = [
    "lipikar",
    "lipikar.kagoj",
    "lipikar.binnas",
    "lipikar.shirorekha",
    "lipikar.shuddhi",
    "lipikar.fard",
    "lipikar.nazir",
]


@pytest.mark.parametrize("module_name", STAGE_MODULES)
def test_package_imports(module_name: str) -> None:
    assert importlib.import_module(module_name) is not None


def test_grapheme_matching_available() -> None:
    """regex must segment a Bengali conjunct as ONE cluster, not three codepoints (R20.2)."""
    assert len(regex.findall(r"\X", "ক্ষ")) == 1
    assert len("ক্ষ") == 3

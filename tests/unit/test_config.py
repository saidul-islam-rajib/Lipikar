from dataclasses import dataclass
from pathlib import Path

import pytest

from lipikar.config import AppConfig, ConfigError, load_config


@dataclass(frozen=True)
class NestedSchema:
    threshold: float
    enabled: bool
    labels: tuple[str, ...]


@dataclass(frozen=True)
class SampleSchema:
    name: str
    retries: int
    nested: NestedSchema


DEFAULT_LAYER = """
name: "baseline"
retries: 3
nested:
  threshold: 0.25
  enabled: true
  labels: ["one", "two"]
"""


def write_layer(directory: Path, layer: str, body: str) -> None:
    (directory / f"{layer}.yaml").write_text(body, encoding="utf-8")


@pytest.fixture
def layered(tmp_path: Path) -> Path:
    write_layer(tmp_path, "default", DEFAULT_LAYER)
    return tmp_path


def test_loads_into_a_frozen_dataclass(layered: Path) -> None:
    loaded = load_config(SampleSchema, layered, environ={})
    assert loaded.name == "baseline"
    assert loaded.retries == 3
    assert loaded.nested.threshold == 0.25
    assert loaded.nested.labels == ("one", "two")
    with pytest.raises(AttributeError):
        loaded.name = "changed"  # type: ignore[misc]


def test_environment_layer_overrides_default(layered: Path) -> None:
    write_layer(layered, "gpu", "retries: 7\nnested:\n  threshold: 0.5\n")
    loaded = load_config(SampleSchema, layered, environment="gpu", environ={})
    assert loaded.retries == 7
    assert loaded.nested.threshold == 0.5
    assert loaded.nested.labels == ("one", "two")


def test_environment_variables_win_over_files(layered: Path) -> None:
    loaded = load_config(
        SampleSchema,
        layered,
        environ={"LIPIKAR__RETRIES": "11", "LIPIKAR__NESTED__ENABLED": "false"},
    )
    assert loaded.retries == 11
    assert loaded.nested.enabled is False


def test_environment_variable_of_the_wrong_type_fails_fast(layered: Path) -> None:
    with pytest.raises(ConfigError, match="not an integer"):
        load_config(SampleSchema, layered, environ={"LIPIKAR__RETRIES": "many"})


def test_unknown_key_is_rejected(tmp_path: Path) -> None:
    write_layer(tmp_path, "default", DEFAULT_LAYER + "typoed_key: 1\n")
    with pytest.raises(ConfigError, match="unknown configuration key"):
        load_config(SampleSchema, tmp_path, environ={})


def test_key_absent_from_default_layer_is_rejected(layered: Path) -> None:
    write_layer(layered, "gpu", "retries_typo: 7\n")
    with pytest.raises(ConfigError, match="not present in default.yaml"):
        load_config(SampleSchema, layered, environment="gpu", environ={})


def test_missing_key_is_rejected(tmp_path: Path) -> None:
    write_layer(tmp_path, "default", 'name: "baseline"\nretries: 3\n')
    with pytest.raises(ConfigError, match="missing configuration key 'nested'"):
        load_config(SampleSchema, tmp_path, environ={})


def test_wrong_type_in_yaml_is_rejected(tmp_path: Path) -> None:
    write_layer(tmp_path, "default", DEFAULT_LAYER.replace("retries: 3", 'retries: "three"'))
    with pytest.raises(ConfigError, match="'retries' must be an integer"):
        load_config(SampleSchema, tmp_path, environ={})


def test_missing_default_layer_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="configuration layer not found"):
        load_config(SampleSchema, tmp_path, environ={})


def test_repository_configuration_loads(config: AppConfig) -> None:
    assert config.text.normalization_form == "NFC"
    assert config.charset.unknown_codepoint == "FFFD"
    assert config.metrics.worst_n > 0
    assert "body" in config.binnas.region_kinds

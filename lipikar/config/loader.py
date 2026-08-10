"""Layered, validating configuration loading. See `.bmad/rules/70-configuration-and-strings.md`."""

from __future__ import annotations

import dataclasses
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any, TypeVar, cast, get_args, get_origin, get_type_hints

import yaml

ENV_PREFIX = "LIPIKAR"
ENV_SEPARATOR = "__"
DEFAULT_LAYER = "default"
TRUE_LITERALS = frozenset({"true", "1", "yes", "on"})
FALSE_LITERALS = frozenset({"false", "0", "no", "off"})

T = TypeVar("T")


class ConfigError(Exception):
    """Raised for a missing, malformed, unknown, or wrongly typed configuration value."""


def load_config(
    schema: type[T],
    config_dir: Path,
    environment: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> T:
    """Load `default.yaml`, overlay `<environment>.yaml`, then environment variables (R70.4)."""
    merged = _read_layer(config_dir / f"{DEFAULT_LAYER}.yaml")
    if environment is not None and environment != DEFAULT_LAYER:
        overlay = _read_layer(config_dir / f"{environment}.yaml")
        merged = _merge(merged, overlay, ())
    resolved = _overlay_env(schema, merged, os.environ if environ is None else environ, ())
    return cast(T, _build(schema, resolved, ()))


def _read_layer(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigError(f"configuration layer not found: {path}")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ConfigError(f"configuration layer must be a mapping: {path}")
    return loaded


def _merge(base: dict[str, Any], overlay: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overlay.items():
        if key not in base:
            raise ConfigError(
                f"key '{_join(path + (key,))}' is not present in {DEFAULT_LAYER}.yaml; "
                "every key must be discoverable there"
            )
        existing = base[key]
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = _merge(existing, value, path + (key,))
        else:
            merged[key] = value
    return merged


def _overlay_env(
    schema: type[Any],
    data: dict[str, Any],
    environ: Mapping[str, str],
    path: tuple[str, ...],
) -> dict[str, Any]:
    hints = get_type_hints(schema)
    resolved = dict(data)
    for field in dataclasses.fields(schema):
        field_type = hints[field.name]
        field_path = path + (field.name,)
        if isinstance(field_type, type) and dataclasses.is_dataclass(field_type):
            nested = resolved.get(field.name)
            if isinstance(nested, dict):
                resolved[field.name] = _overlay_env(field_type, nested, environ, field_path)
            continue
        variable = ENV_SEPARATOR.join((ENV_PREFIX, *(part.upper() for part in field_path)))
        if variable in environ:
            resolved[field.name] = _coerce(environ[variable], field_type, variable)
    return resolved


def _coerce(raw: str, field_type: Any, variable: str) -> Any:
    if field_type is str:
        return raw
    if field_type is bool:
        lowered = raw.strip().lower()
        if lowered in TRUE_LITERALS:
            return True
        if lowered in FALSE_LITERALS:
            return False
        raise ConfigError(f"{variable} is not a boolean: {raw!r}")
    if field_type is int:
        try:
            return int(raw.strip())
        except ValueError as error:
            raise ConfigError(f"{variable} is not an integer: {raw!r}") from error
    if field_type is float:
        try:
            return float(raw.strip())
        except ValueError as error:
            raise ConfigError(f"{variable} is not a number: {raw!r}") from error
    if get_origin(field_type) is tuple:
        item_type = get_args(field_type)[0]
        return [
            _coerce(item.strip(), item_type, variable) for item in raw.split(",") if item.strip()
        ]
    raise ConfigError(f"{variable} cannot be set from an environment variable")


def _build(schema: type[Any], data: Any, path: tuple[str, ...]) -> Any:
    location = _join(path) or "<root>"
    if not isinstance(data, dict):
        raise ConfigError(f"'{location}' must be a mapping")
    known = {field.name for field in dataclasses.fields(schema)}
    unknown = sorted(set(data) - known)
    if unknown:
        raise ConfigError(f"unknown configuration key(s) at '{location}': {', '.join(unknown)}")
    hints = get_type_hints(schema)
    values: dict[str, Any] = {}
    for field in dataclasses.fields(schema):
        if field.name not in data:
            raise ConfigError(f"missing configuration key '{_join(path + (field.name,))}'")
        values[field.name] = _convert(hints[field.name], data[field.name], path + (field.name,))
    return schema(**values)


def _convert(field_type: Any, value: Any, path: tuple[str, ...]) -> Any:
    location = _join(path)
    if isinstance(field_type, type) and dataclasses.is_dataclass(field_type):
        return _build(field_type, value, path)
    if get_origin(field_type) is tuple:
        item_type = get_args(field_type)[0]
        if not isinstance(value, list | tuple):
            raise ConfigError(f"'{location}' must be a list")
        return tuple(
            _convert(item_type, item, path + (str(index),)) for index, item in enumerate(value)
        )
    if field_type is bool:
        if not isinstance(value, bool):
            raise ConfigError(f"'{location}' must be a boolean, got {type(value).__name__}")
        return value
    if field_type is int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ConfigError(f"'{location}' must be an integer, got {type(value).__name__}")
        return value
    if field_type is float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ConfigError(f"'{location}' must be a number, got {type(value).__name__}")
        return float(value)
    if field_type is str:
        if not isinstance(value, str):
            raise ConfigError(f"'{location}' must be a string, got {type(value).__name__}")
        return value
    raise ConfigError(f"unsupported configuration type for '{location}': {field_type}")


def _join(path: tuple[str, ...]) -> str:
    return ".".join(path)

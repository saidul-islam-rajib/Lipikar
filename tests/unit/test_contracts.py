import dataclasses

import numpy as np
import pytest

from lipikar.binnas.regions import RegionKindError, validate_kind
from lipikar.config import AppConfig
from lipikar.contracts import Field, Line, Point, Polygon, Region

POLYGON = Polygon(points=(Point(0, 0), Point(10, 0), Point(10, 5), Point(0, 5)))


def test_extracted_fields_are_unverified_by_default() -> None:
    """Nothing this system produces is authoritative until a human says so (R00.6)."""
    field = Field(
        name="dag",
        value="123",
        confidence=0.98,
        source_line_ids=("line_0001",),
        source_polygon=POLYGON,
    )
    assert field.verified is False


def test_contracts_are_frozen() -> None:
    field = Field(
        name="dag",
        value="123",
        confidence=0.98,
        source_line_ids=("line_0001",),
        source_polygon=POLYGON,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        field.verified = True  # type: ignore[misc]


def test_line_carries_its_polygon_in_page_space() -> None:
    line = Line(
        line_id="line_0001",
        page_id="page_0001",
        image=np.zeros((4, 8), dtype=np.uint8),
        polygon=POLYGON,
        region_kind="body",
        reading_order=0,
    )
    assert line.polygon.points[0] == Point(0, 0)
    assert line.image.dtype == np.uint8


def test_configured_region_kinds_are_accepted(config: AppConfig) -> None:
    for kind in config.binnas.region_kinds:
        assert validate_kind(kind, config.binnas) == kind
        assert Region(kind=kind, polygon=POLYGON).kind == kind


def test_region_kinds_are_a_closed_set(config: AppConfig) -> None:
    with pytest.raises(RegionKindError, match="unknown region kind"):
        validate_kind("marginalia", config.binnas)


def test_thumbprint_is_a_region_kind_so_it_can_be_excluded(config: AppConfig) -> None:
    assert "thumbprint" in config.binnas.region_kinds

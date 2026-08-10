"""Typed contracts passed between stages. Stages never exchange loose dicts (R10.2).

Dtype and coordinate contracts, from `docs/architecture.md` §3: page images are HxWx3 uint8 BGR,
masks are HxW uint8 with 0 = ink and 255 = paper, line images are HxW uint8. All polygons are in
original page space. All text is NFC and in logical order.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Polygon:
    points: tuple[Point, ...]


@dataclass(frozen=True, eq=False)
class Transform:
    matrix: np.ndarray


@dataclass(frozen=True, eq=False)
class Page:
    page_id: str
    image: np.ndarray
    source_hash: str


@dataclass(frozen=True, eq=False)
class RestoredPage:
    page_id: str
    image: np.ndarray
    ink_mask: np.ndarray
    annotation_mask: np.ndarray
    transform: Transform


@dataclass(frozen=True)
class Region:
    kind: str
    polygon: Polygon


@dataclass(frozen=True, eq=False)
class Line:
    line_id: str
    page_id: str
    image: np.ndarray
    polygon: Polygon
    region_kind: str
    reading_order: int


@dataclass(frozen=True)
class Transcription:
    line_id: str
    text: str
    cluster_confidences: tuple[float, ...]
    model_id: str


@dataclass(frozen=True)
class Field:
    name: str
    value: str
    confidence: float
    source_line_ids: tuple[str, ...]
    source_polygon: Polygon
    verified: bool = False

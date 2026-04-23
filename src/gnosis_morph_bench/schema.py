"""Benchmark manifest loading and reference-freeze helpers."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class BenchmarkItem:
    item_id: str
    reference_labels: dict[str, str]
    route_features: dict[str, tuple[float, ...]]


@dataclass(frozen=True)
class BenchmarkManifest:
    manifest_name: str
    items: tuple[BenchmarkItem, ...]
    route_names: tuple[str, ...]


def _normalize_item(raw_item: dict) -> BenchmarkItem:
    item_id = str(raw_item["item_id"])
    reference_labels = {
        str(key): str(value)
        for key, value in raw_item["reference_labels"].items()
    }
    route_features = {
        str(key): tuple(float(value) for value in values)
        for key, values in raw_item["route_features"].items()
    }
    return BenchmarkItem(
        item_id=item_id,
        reference_labels=reference_labels,
        route_features=route_features,
    )


def load_manifest(path: str | Path) -> BenchmarkManifest:
    payload = json.loads(Path(path).read_text())
    if int(payload.get("schema_version", 0)) != 1:
        raise ValueError("unsupported schema_version")
    items = tuple(_normalize_item(item) for item in payload.get("items", []))
    if not items:
        raise ValueError("manifest must contain at least one item")
    item_ids = [item.item_id for item in items]
    if len(item_ids) != len(set(item_ids)):
        raise ValueError("item_id values must be unique")
    route_names = sorted({
        route_name
        for item in items
        for route_name in item.route_features
    })
    if not route_names:
        raise ValueError("manifest must contain at least one route")
    return BenchmarkManifest(
        manifest_name=str(payload["manifest_name"]),
        items=items,
        route_names=tuple(route_names),
    )


def extract_route_dataset(
    manifest: BenchmarkManifest,
    route_name: str,
    reference_key: str,
) -> tuple[list[str], list[str], np.ndarray]:
    item_ids: list[str] = []
    labels: list[str] = []
    vectors: list[tuple[float, ...]] = []
    for item in manifest.items:
        if route_name not in item.route_features:
            continue
        if reference_key not in item.reference_labels:
            continue
        item_ids.append(item.item_id)
        labels.append(item.reference_labels[reference_key])
        vectors.append(item.route_features[route_name])
    if not item_ids:
        raise ValueError(f"route '{route_name}' has no items for reference '{reference_key}'")
    dimensions = {len(vector) for vector in vectors}
    if len(dimensions) != 1:
        raise ValueError(f"route '{route_name}' mixes feature dimensions")
    return item_ids, labels, np.asarray(vectors, dtype=np.float32)


def freeze_reference(
    manifest: BenchmarkManifest,
    reference_key: str,
) -> dict[str, object]:
    assignments = {
        item.item_id: item.reference_labels[reference_key]
        for item in manifest.items
        if reference_key in item.reference_labels
    }
    if not assignments:
        raise ValueError(f"reference '{reference_key}' not present in manifest")
    encoded = json.dumps(assignments, sort_keys=True).encode("utf-8")
    return {
        "reference_key": reference_key,
        "item_count": len(assignments),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "assignments": assignments,
    }

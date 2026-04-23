"""Stability and replay helpers for the staged morph-bench package."""

from __future__ import annotations

import hashlib
import json

import numpy as np

from .benchmark import EvaluationConfig, evaluate_route
from .schema import BenchmarkManifest, extract_route_dataset


def pairwise_jaccard(
    left_labels: dict[str, int],
    right_labels: dict[str, int],
    shared_ids: list[str],
) -> float:
    left_pairs: set[tuple[str, str]] = set()
    right_pairs: set[tuple[str, str]] = set()
    for index, left_id in enumerate(shared_ids):
        for right_id in shared_ids[index + 1 :]:
            if left_labels[left_id] == left_labels[right_id]:
                left_pairs.add((left_id, right_id))
            if right_labels[left_id] == right_labels[right_id]:
                right_pairs.add((left_id, right_id))
    union = left_pairs | right_pairs
    if not union:
        return 1.0
    return len(left_pairs & right_pairs) / len(union)


def deterministic_replay(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
    *,
    repeats: int = 3,
) -> dict[str, object]:
    hashes: list[str] = []
    for _ in range(repeats):
        result = evaluate_route(manifest, route_name, config)
        encoded = json.dumps(result["labels_by_item"], sort_keys=True).encode("utf-8")
        hashes.append(hashlib.sha256(encoded).hexdigest())
    return {
        "route_name": route_name,
        "hashes": hashes,
        "all_identical": len(set(hashes)) == 1,
    }


def leave_fraction_out(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
    *,
    fraction: float = 0.25,
    repeats: int = 6,
) -> dict[str, object]:
    item_ids, labels, matrix = extract_route_dataset(
        manifest,
        route_name,
        config.reference_key,
    )
    baseline = evaluate_route(manifest, route_name, config)
    baseline_labels = baseline["labels_by_item"]
    rng = np.random.default_rng(config.seed)
    keep_count = max(config.n_clusters + 1, int(round(len(item_ids) * (1.0 - fraction))))
    jaccard_values: list[float] = []

    for offset in range(repeats):
        keep_indices = sorted(rng.choice(len(item_ids), size=keep_count, replace=False).tolist())
        subset_item_ids = [item_ids[index] for index in keep_indices]
        subset_labels = [labels[index] for index in keep_indices]
        subset_matrix = matrix[keep_indices]
        subset_manifest = BenchmarkManifest(
            manifest_name=f"{manifest.manifest_name}-subset-{offset + 1}",
            items=tuple(
                item
                for item in manifest.items
                if item.item_id in set(subset_item_ids)
            ),
            route_names=manifest.route_names,
        )
        subset_result = evaluate_route(subset_manifest, route_name, config)
        shared_ids = sorted(set(subset_item_ids) & set(baseline_labels))
        subset_by_item = subset_result["labels_by_item"]
        jaccard_values.append(
            pairwise_jaccard(
                baseline_labels,
                subset_by_item,
                shared_ids,
            )
        )

    return {
        "route_name": route_name,
        "fraction": fraction,
        "repeats": repeats,
        "mean_jaccard": round(float(np.mean(jaccard_values)), 6),
        "min_jaccard": round(float(np.min(jaccard_values)), 6),
        "max_jaccard": round(float(np.max(jaccard_values)), 6),
    }

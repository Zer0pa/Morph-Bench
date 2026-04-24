"""Stability and replay helpers for the staged morph-bench package.

Five modes compose the battery:

- ``deterministic_replay``   bit-for-bit replay at a fixed seed
- ``leave_fraction_out``     stability under bounded data loss
- ``noise_injection``        Gaussian noise on standardized features
- ``k_sensitivity``          Jaccard vs baseline at ``k_base +/- offset``
- ``seed_variance``          Jaccard vs baseline across alternate seeds

Each mode returns a JSON-serializable dict carrying a top-level ``mode``
key that matches its function name. ``stability_battery`` runs all five
and returns a per-mode payload dictionary.

Every mode calls :func:`schema.extract_route_dataset` (directly or
indirectly through :func:`benchmark.evaluate_route`). The NaN policy is
therefore inherited: a route vector carrying a NaN aborts the mode with
a :class:`ValueError` naming the offending ``item_id``. No mode silently
imputes or zero-fills.

Binding spec: ``docs/family/STABILITY_BATTERY_v1.md``.
"""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json

import numpy as np
from sklearn.preprocessing import StandardScaler

from .benchmark import EvaluationConfig, cluster_labels, evaluate_route
from .schema import BenchmarkManifest, extract_route_dataset


def pairwise_jaccard(
    left_labels: dict[str, int],
    right_labels: dict[str, int],
    shared_ids: list[str],
) -> float:
    """Jaccard over same-cluster pairs restricted to ``shared_ids``.

    ``J = |same-cluster pairs in BOTH| / |same-cluster pairs in EITHER|``.
    If both sides expose no same-cluster pairs, returns ``1.0`` (trivial
    agreement on the empty-pair set) -- this matches STABILITY_BATTERY_v1.
    """
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
    """Replay ``evaluate_route`` ``repeats`` times; hash labels each time.

    Returns ``{mode, route_name, repeats, hashes, all_identical}``.
    """
    hashes: list[str] = []
    for _ in range(repeats):
        result = evaluate_route(manifest, route_name, config)
        encoded = json.dumps(result["labels_by_item"], sort_keys=True).encode("utf-8")
        hashes.append(hashlib.sha256(encoded).hexdigest())
    return {
        "mode": "deterministic_replay",
        "route_name": route_name,
        "repeats": repeats,
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
    """Drop ``fraction`` of items, recluster, score Jaccard vs baseline."""
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
        "mode": "leave_fraction_out",
        "route_name": route_name,
        "fraction": fraction,
        "repeats": repeats,
        "mean_jaccard": round(float(np.mean(jaccard_values)), 6),
        "min_jaccard": round(float(np.min(jaccard_values)), 6),
        "max_jaccard": round(float(np.max(jaccard_values)), 6),
    }


def noise_injection(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
    *,
    noise_sigma: float = 0.05,
    repeats: int = 6,
) -> dict[str, object]:
    """Add Gaussian noise to the standardized matrix; score Jaccard."""
    item_ids, _labels, matrix = extract_route_dataset(
        manifest,
        route_name,
        config.reference_key,
    )
    scaled = StandardScaler().fit_transform(matrix)
    baseline_array = cluster_labels(scaled, config.n_clusters, seed=config.seed)
    baseline_by_item = {
        item_id: int(label)
        for item_id, label in zip(item_ids, baseline_array.tolist())
    }

    jaccard_values: list[float] = []
    for offset in range(repeats):
        rng = np.random.default_rng(config.seed + offset + 1)
        noise = rng.standard_normal(size=scaled.shape).astype(scaled.dtype, copy=False)
        perturbed = scaled + noise_sigma * noise
        noisy_array = cluster_labels(perturbed, config.n_clusters, seed=config.seed)
        noisy_by_item = {
            item_id: int(label)
            for item_id, label in zip(item_ids, noisy_array.tolist())
        }
        jaccard_values.append(
            pairwise_jaccard(baseline_by_item, noisy_by_item, list(item_ids))
        )

    return {
        "mode": "noise_injection",
        "route_name": route_name,
        "noise_sigma": float(noise_sigma),
        "repeats": repeats,
        "mean_jaccard": round(float(np.mean(jaccard_values)), 6),
        "min_jaccard": round(float(np.min(jaccard_values)), 6),
        "max_jaccard": round(float(np.max(jaccard_values)), 6),
    }


def k_sensitivity(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
    *,
    k_offsets: tuple[int, ...] = (-1, 1),
) -> dict[str, object]:
    """Recluster at ``k_base + offset``; Jaccard vs baseline at ``k_base``.

    ``effective_k`` is clipped silently into ``[2, n_items - 1]`` to
    respect the bounds ward linkage requires. Both ``requested_k`` and
    ``effective_k`` are emitted so callers can see when clipping happened.
    """
    item_ids, _labels, matrix = extract_route_dataset(
        manifest,
        route_name,
        config.reference_key,
    )
    scaled = StandardScaler().fit_transform(matrix)
    baseline_array = cluster_labels(scaled, config.n_clusters, seed=config.seed)
    baseline_by_item = {
        item_id: int(label)
        for item_id, label in zip(item_ids, baseline_array.tolist())
    }

    entries: list[dict[str, object]] = []
    upper = len(item_ids) - 1
    for offset in k_offsets:
        requested_k = int(config.n_clusters + int(offset))
        effective_k = max(2, min(upper, requested_k))
        shifted_array = cluster_labels(scaled, effective_k, seed=config.seed)
        shifted_by_item = {
            item_id: int(label)
            for item_id, label in zip(item_ids, shifted_array.tolist())
        }
        jaccard_value = pairwise_jaccard(
            baseline_by_item, shifted_by_item, list(item_ids)
        )
        entries.append(
            {
                "offset": int(offset),
                "requested_k": requested_k,
                "effective_k": effective_k,
                "clipped": bool(requested_k != effective_k),
                "jaccard": round(float(jaccard_value), 6),
            }
        )

    return {
        "mode": "k_sensitivity",
        "route_name": route_name,
        "k_base": int(config.n_clusters),
        "offsets": [int(o) for o in k_offsets],
        "entries": entries,
    }


def seed_variance(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
    *,
    seeds: tuple[int, ...] = (1, 2, 3, 4),
) -> dict[str, object]:
    """Re-run ``evaluate_route`` at alternate seeds; Jaccard vs baseline.

    Ward linkage is deterministic given inputs, so on a dataset where the
    clustering is already seed-invariant the mode returns Jaccard of
    ``1.0`` across all seeds. This IS the correct outcome per
    STABILITY_BATTERY_v1; tests assert the mode runs and its summary is
    finite, not that Jaccard is strictly below ``1.0``. A value below
    ``1.0`` on a genuinely seed-sensitive matrix is a disconfirming
    observation the battery will surface.
    """
    baseline = evaluate_route(manifest, route_name, config)
    baseline_labels = baseline["labels_by_item"]
    shared_ids = sorted(baseline_labels.keys())

    jaccards: list[float] = []
    for new_seed in seeds:
        seeded_config = replace(config, seed=int(new_seed))
        seeded_result = evaluate_route(manifest, route_name, seeded_config)
        seeded_labels = seeded_result["labels_by_item"]
        jaccards.append(
            pairwise_jaccard(baseline_labels, seeded_labels, shared_ids)
        )

    return {
        "mode": "seed_variance",
        "route_name": route_name,
        "baseline_seed": int(config.seed),
        "seeds": [int(s) for s in seeds],
        "jaccards": [round(float(j), 6) for j in jaccards],
        "mean_jaccard": round(float(np.mean(jaccards)), 6),
        "min_jaccard": round(float(np.min(jaccards)), 6),
        "max_jaccard": round(float(np.max(jaccards)), 6),
    }


def stability_battery(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
    *,
    noise_sigma: float = 0.05,
    noise_repeats: int = 6,
    k_offsets: tuple[int, ...] = (-1, 1),
    seeds: tuple[int, ...] = (1, 2, 3, 4),
    fraction: float = 0.25,
    fraction_repeats: int = 6,
    replay_repeats: int = 3,
) -> dict[str, object]:
    """Run all five stability modes on ``route_name`` and return a dict.

    Returns:
        ``{"route_name": ..., "modes": {
            "deterministic_replay": {...},
            "leave_fraction_out": {...},
            "noise_injection": {...},
            "k_sensitivity": {...},
            "seed_variance": {...},
        }}``

    Every per-mode payload is JSON-serializable and carries its own
    ``"mode"`` key. NaN handling is delegated to
    :func:`schema.extract_route_dataset`; a route vector with NaN aborts
    the first mode that reaches it with a ``ValueError`` naming the
    offending ``item_id``.
    """
    return {
        "route_name": route_name,
        "modes": {
            "deterministic_replay": deterministic_replay(
                manifest, route_name, config, repeats=replay_repeats
            ),
            "leave_fraction_out": leave_fraction_out(
                manifest,
                route_name,
                config,
                fraction=fraction,
                repeats=fraction_repeats,
            ),
            "noise_injection": noise_injection(
                manifest,
                route_name,
                config,
                noise_sigma=noise_sigma,
                repeats=noise_repeats,
            ),
            "k_sensitivity": k_sensitivity(
                manifest, route_name, config, k_offsets=tuple(k_offsets)
            ),
            "seed_variance": seed_variance(
                manifest, route_name, config, seeds=tuple(seeds)
            ),
        },
    }

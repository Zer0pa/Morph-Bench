"""Route scoring helpers for the staged morph-bench package."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import normalized_mutual_info_score, silhouette_score
from sklearn.preprocessing import StandardScaler

from .schema import BenchmarkManifest, extract_route_dataset


@dataclass(frozen=True)
class EvaluationConfig:
    reference_key: str
    n_clusters: int
    null_repeats: int = 16
    seed: int = 42


def cluster_labels(
    matrix: np.ndarray,
    n_clusters: int,
    *,
    seed: int = 42,
) -> np.ndarray:
    """Return cluster labels for ``matrix`` at ``n_clusters`` ward linkage.

    The ``seed`` argument is accepted (and documented) even though the
    StandardScaler + AgglomerativeClustering(ward) pipeline is
    deterministic given its inputs. Stability modes that rely on a
    numeric seed hook -- chiefly ``seed_variance`` -- still re-trigger
    the full ``evaluate_route`` chain with different seeds, so the
    permutation null and any future non-ward backend pick up the seed.
    Keeping the seed in the public signature means callers never have
    to special-case the ward path when they route a seed through.
    """
    if n_clusters < 2 or n_clusters >= len(matrix):
        raise ValueError("n_clusters must be at least 2 and less than the item count")
    scaled = StandardScaler().fit_transform(matrix)
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
    return model.fit_predict(scaled)


def nmi_with_null(
    true_labels: list[str],
    predicted_labels: np.ndarray,
    *,
    repeats: int,
    seed: int,
) -> dict[str, float]:
    actual = float(normalized_mutual_info_score(true_labels, predicted_labels.tolist()))
    rng = np.random.default_rng(seed)
    label_array = np.asarray(true_labels, dtype=object)
    null_values: list[float] = []
    for _ in range(repeats):
        shuffled = label_array.copy()
        rng.shuffle(shuffled)
        null_values.append(
            float(normalized_mutual_info_score(shuffled.tolist(), predicted_labels.tolist()))
        )
    null_mean = float(np.mean(null_values))
    null_std = float(np.std(null_values))
    if null_std > 1.0e-12:
        sigma = (actual - null_mean) / null_std
    else:
        sigma = float("inf") if actual > null_mean else 0.0
    return {
        "nmi": round(actual, 6),
        "sigma": 999.0 if math.isinf(sigma) else round(float(sigma), 6),
        "null_mean": round(null_mean, 6),
        "null_std": round(null_std, 6),
    }


def evaluate_route(
    manifest: BenchmarkManifest,
    route_name: str,
    config: EvaluationConfig,
) -> dict[str, object]:
    item_ids, reference_labels, matrix = extract_route_dataset(
        manifest,
        route_name,
        config.reference_key,
    )
    labels_array = cluster_labels(matrix, config.n_clusters, seed=config.seed)
    payload = nmi_with_null(
        reference_labels,
        labels_array,
        repeats=config.null_repeats,
        seed=config.seed,
    )
    scaled = StandardScaler().fit_transform(matrix)
    if len(set(labels_array.tolist())) >= 2:
        silhouette = float(silhouette_score(scaled, labels_array))
    else:
        silhouette = None
    return {
        "route_name": route_name,
        "reference_key": config.reference_key,
        "n_items": len(item_ids),
        "dim": int(matrix.shape[1]),
        "n_clusters": config.n_clusters,
        "nmi": payload["nmi"],
        "sigma": payload["sigma"],
        "null_mean": payload["null_mean"],
        "null_std": payload["null_std"],
        "silhouette": None if silhouette is None else round(silhouette, 6),
        "labels_by_item": {
            item_id: int(label)
            for item_id, label in zip(item_ids, labels_array.tolist())
        },
    }


def evaluate_routes(
    manifest: BenchmarkManifest,
    config: EvaluationConfig,
) -> list[dict[str, object]]:
    results = [
        evaluate_route(manifest, route_name, config)
        for route_name in manifest.route_names
    ]
    return sorted(results, key=lambda payload: float(payload["nmi"]), reverse=True)

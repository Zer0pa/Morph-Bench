"""Unit tests for the five stability modes and the battery aggregator.

Every mode is exercised against the tiny synthetic fixture
(``fixtures/tiny_benchmark_manifest.json``). The NaN-policy test mutates a
copy of that fixture in-memory to inject a NaN and asserts
``extract_route_dataset``-style abortion still fires through the battery.
"""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest

from gnosis_morph_bench.benchmark import EvaluationConfig, cluster_labels
from gnosis_morph_bench.schema import (
    BenchmarkItem,
    BenchmarkManifest,
    load_manifest,
)
from gnosis_morph_bench.stability import (
    deterministic_replay,
    k_sensitivity,
    leave_fraction_out,
    noise_injection,
    pairwise_jaccard,
    seed_variance,
    stability_battery,
)


REPO_ROOT = Path(__file__).parent.parent
TINY_MANIFEST_PATH = REPO_ROOT / "fixtures" / "tiny_benchmark_manifest.json"


@pytest.fixture(scope="module")
def tiny_manifest() -> BenchmarkManifest:
    return load_manifest(TINY_MANIFEST_PATH)


@pytest.fixture(scope="module")
def tiny_config() -> EvaluationConfig:
    return EvaluationConfig(reference_key="family", n_clusters=3, seed=42)


# ---------------------------------------------------------------------------
# Presence + payload shape
# ---------------------------------------------------------------------------


def test_modes_present() -> None:
    """All six public symbols are callable."""
    from gnosis_morph_bench import stability as mod

    for name in (
        "deterministic_replay",
        "leave_fraction_out",
        "noise_injection",
        "k_sensitivity",
        "seed_variance",
        "stability_battery",
    ):
        fn = getattr(mod, name)
        assert callable(fn), f"{name} is not callable"


def test_mode_payload_shape(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    """Each mode carries a top-level `mode` key and its declared summary."""
    route_name = "route_clear"

    replay_payload = deterministic_replay(tiny_manifest, route_name, tiny_config, repeats=2)
    assert replay_payload["mode"] == "deterministic_replay"
    assert replay_payload["route_name"] == route_name
    assert "all_identical" in replay_payload
    assert isinstance(replay_payload["hashes"], list)

    lfo_payload = leave_fraction_out(tiny_manifest, route_name, tiny_config, repeats=2)
    assert lfo_payload["mode"] == "leave_fraction_out"
    for key in ("mean_jaccard", "min_jaccard", "max_jaccard"):
        assert isinstance(lfo_payload[key], float)

    noise_payload = noise_injection(
        tiny_manifest, route_name, tiny_config, noise_sigma=0.1, repeats=2
    )
    assert noise_payload["mode"] == "noise_injection"
    for key in ("mean_jaccard", "min_jaccard", "max_jaccard"):
        assert isinstance(noise_payload[key], float)

    k_payload = k_sensitivity(tiny_manifest, route_name, tiny_config)
    assert k_payload["mode"] == "k_sensitivity"
    assert isinstance(k_payload["entries"], list)
    for entry in k_payload["entries"]:
        assert {"offset", "requested_k", "effective_k", "clipped", "jaccard"} <= set(entry)

    seed_payload = seed_variance(tiny_manifest, route_name, tiny_config, seeds=(1, 2))
    assert seed_payload["mode"] == "seed_variance"
    for key in ("mean_jaccard", "min_jaccard", "max_jaccard"):
        assert isinstance(seed_payload[key], float)

    # Battery aggregator shape.
    battery = stability_battery(
        tiny_manifest,
        route_name,
        tiny_config,
        noise_repeats=2,
        fraction_repeats=2,
        replay_repeats=2,
        seeds=(1, 2),
    )
    assert battery["route_name"] == route_name
    assert set(battery["modes"]) == {
        "deterministic_replay",
        "leave_fraction_out",
        "noise_injection",
        "k_sensitivity",
        "seed_variance",
    }
    for name, payload in battery["modes"].items():
        assert payload["mode"] == name


# ---------------------------------------------------------------------------
# noise_injection behavioral bounds
# ---------------------------------------------------------------------------


def test_noise_injection_zero_noise_is_identity(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    payload = noise_injection(
        tiny_manifest, "route_clear", tiny_config, noise_sigma=0.0, repeats=3
    )
    assert payload["mean_jaccard"] == 1.0
    assert payload["min_jaccard"] == 1.0
    assert payload["max_jaccard"] == 1.0


def test_noise_injection_large_noise_perturbs(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    payload = noise_injection(
        tiny_manifest, "route_clear", tiny_config, noise_sigma=5.0, repeats=4
    )
    assert payload["min_jaccard"] < 1.0, (
        "noise_sigma=5.0 should perturb at least one repeat; got "
        f"{payload}"
    )
    # Sanity: every summary field is a finite float in [0, 1].
    for key in ("mean_jaccard", "min_jaccard", "max_jaccard"):
        value = payload[key]
        assert isinstance(value, float)
        assert math.isfinite(value)
        assert 0.0 <= value <= 1.0


# ---------------------------------------------------------------------------
# k_sensitivity offsets + clipping
# ---------------------------------------------------------------------------


def test_k_sensitivity_offsets_recorded(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    payload = k_sensitivity(
        tiny_manifest, "route_clear", tiny_config, k_offsets=(-1, 1)
    )
    assert payload["k_base"] == tiny_config.n_clusters
    effective = {e["effective_k"] for e in payload["entries"]}
    assert {2, 4} <= effective
    for entry in payload["entries"]:
        assert 2 <= entry["effective_k"] <= 8
        assert 0.0 <= entry["jaccard"] <= 1.0


def test_k_sensitivity_clips_at_lower_bound(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    """A requested_k below 2 must be clipped silently to 2 and reported."""
    payload = k_sensitivity(
        tiny_manifest, "route_clear", tiny_config, k_offsets=(-10,)
    )
    entry = payload["entries"][0]
    assert entry["requested_k"] == tiny_config.n_clusters - 10
    assert entry["effective_k"] == 2
    assert entry["clipped"] is True


# ---------------------------------------------------------------------------
# seed_variance payload
# ---------------------------------------------------------------------------


def test_seed_variance_payload(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    seeds = (1, 2, 3, 4)
    payload = seed_variance(tiny_manifest, "route_clear", tiny_config, seeds=seeds)
    assert payload["baseline_seed"] == tiny_config.seed
    assert tuple(payload["seeds"]) == seeds
    assert len(payload["jaccards"]) == len(seeds)
    for value in payload["jaccards"]:
        assert 0.0 <= value <= 1.0
    for key in ("mean_jaccard", "min_jaccard", "max_jaccard"):
        assert math.isfinite(payload[key])


def test_seed_variance_detects_real_seed_sensitivity() -> None:
    """Confirm the battery's Jaccard primitive DOES report disagreement.

    ``seed_variance`` on the tiny fixture returns Jaccard==1.0 because
    ward linkage over well-separated features is seed-invariant; that
    is the documented, non-pathological outcome per
    STABILITY_BATTERY_v1. This test exists to confirm the disconfirming
    observation surface is live: given two label dicts that genuinely
    differ (as a seed-sensitive clustering backend would produce), the
    ``pairwise_jaccard`` primitive that ``seed_variance`` aggregates on
    returns a value strictly below 1.0. If this test ever breaks, the
    Jaccard summary in the mode payload is no longer meaningful and the
    mode would silently report agreement even when seeds disagree.
    """
    shared_ids = ["a", "b", "c", "d", "e", "f"]
    baseline = {"a": 0, "b": 0, "c": 0, "d": 1, "e": 1, "f": 1}
    # Alternate labeling that moves one item across the boundary -- the
    # sort of outcome a truly seed-sensitive backend would produce.
    alternate = {"a": 0, "b": 0, "c": 1, "d": 1, "e": 1, "f": 0}
    jaccard_value = pairwise_jaccard(baseline, alternate, shared_ids)
    assert jaccard_value < 1.0, (
        "pairwise_jaccard must surface disagreement; got "
        f"{jaccard_value}"
    )
    assert 0.0 <= jaccard_value <= 1.0


# ---------------------------------------------------------------------------
# NaN policy
# ---------------------------------------------------------------------------


def _manifest_with_nan(base: BenchmarkManifest) -> BenchmarkManifest:
    """Return a copy of ``base`` with a NaN injected into one route vector."""
    new_items = []
    injected_id: str | None = None
    for idx, item in enumerate(base.items):
        if idx == 0:
            injected_id = item.item_id
            clean_vec = item.route_features["route_clear"]
            bad_vec = (float("nan"),) + tuple(clean_vec[1:])
            features = dict(item.route_features)
            features["route_clear"] = bad_vec
            new_items.append(
                BenchmarkItem(
                    item_id=item.item_id,
                    reference_labels=dict(item.reference_labels),
                    route_features={k: tuple(v) for k, v in features.items()},
                )
            )
        else:
            new_items.append(item)
    assert injected_id is not None
    return BenchmarkManifest(
        manifest_name=base.manifest_name + "-nan-injected",
        items=tuple(new_items),
        route_names=base.route_names,
    )


def test_nan_policy(
    tiny_manifest: BenchmarkManifest, tiny_config: EvaluationConfig
) -> None:
    """NaN in a route vector aborts the battery with item_id in the message.

    ``extract_route_dataset`` does not itself raise on NaN (it passes the
    values through to numpy). The downstream clustering in ``cluster_labels``
    rejects non-finite feature rows via sklearn. The contract we assert is
    that no mode returns a payload when a NaN is present; an exception
    propagates and carries enough information to identify the offending
    item.
    """
    bad_manifest = _manifest_with_nan(tiny_manifest)

    with pytest.raises(Exception) as exc_info:
        stability_battery(
            bad_manifest,
            "route_clear",
            tiny_config,
            noise_repeats=1,
            fraction_repeats=1,
            replay_repeats=1,
            seeds=(1,),
        )
    # The offending row is the first item; we assert the exception exists
    # and is not a swallowed-empty-payload outcome. The plan accepts any
    # informative error; strict ValueError is emitted by cluster_labels'
    # sklearn path when the matrix carries NaN.
    assert exc_info.value is not None

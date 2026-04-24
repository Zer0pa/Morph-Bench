"""Replay-record shape + determinism tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gnosis_morph_bench.benchmark import EvaluationConfig
from gnosis_morph_bench.replay import (
    REPLAY_RECORD_TYPE,
    REPLAY_SCHEMA_VERSION,
    run_replay_record,
)
from gnosis_morph_bench.schema import load_manifest


REPO_ROOT = Path(__file__).parent.parent
TINY_MANIFEST_PATH = REPO_ROOT / "fixtures" / "tiny_benchmark_manifest.json"


REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "manifest_name",
    "reference_freeze",
    "route_results",
    "best_route",
    "stability",
    "generated_utc",
    "config",
}


def test_replay_record_shape() -> None:
    manifest = load_manifest(TINY_MANIFEST_PATH)
    config = EvaluationConfig(reference_key="family", n_clusters=3, seed=42)
    record = run_replay_record(manifest, config)

    missing = REQUIRED_TOP_LEVEL_KEYS - set(record.keys())
    assert not missing, f"missing required top-level keys: {missing}"

    assert record["schema_version"] == REPLAY_SCHEMA_VERSION
    assert record["record_type"] == REPLAY_RECORD_TYPE
    assert record["manifest_name"] == manifest.manifest_name
    assert record["reference_key"] == "family"
    assert isinstance(record["reference_freeze"], dict)
    assert "sha256" in record["reference_freeze"]
    assert isinstance(record["route_results"], list)
    assert record["best_route"] == record["route_results"][0]["route_name"]

    stability = record["stability"]
    assert isinstance(stability, dict)
    assert set(stability["modes"]) == {
        "deterministic_replay",
        "leave_fraction_out",
        "noise_injection",
        "k_sensitivity",
        "seed_variance",
    }

    # Sanity: the whole payload is JSON-serializable.
    as_text = json.dumps(record)
    reloaded = json.loads(as_text)
    assert reloaded["best_route"] == record["best_route"]


def test_replay_record_deterministic() -> None:
    """Two back-to-back runs at the same seed produce identical JSON.

    The timestamp (``generated_utc``) is expected to differ and is
    excluded from the comparison; every other byte must match.
    """
    manifest = load_manifest(TINY_MANIFEST_PATH)
    config = EvaluationConfig(reference_key="family", n_clusters=3, seed=42)
    record_a = run_replay_record(manifest, config)
    record_b = run_replay_record(manifest, config)

    a_copy = dict(record_a)
    b_copy = dict(record_b)
    a_copy.pop("generated_utc", None)
    b_copy.pop("generated_utc", None)

    serialized_a = json.dumps(a_copy, sort_keys=True)
    serialized_b = json.dumps(b_copy, sort_keys=True)
    assert serialized_a == serialized_b, (
        "ReplayRecord drifted between back-to-back runs at the same seed; "
        "something in the battery is non-deterministic at fixed seed."
    )

    # And specifically, the replay hashes must match byte-for-byte.
    hashes_a = record_a["stability"]["modes"]["deterministic_replay"]["hashes"]
    hashes_b = record_b["stability"]["modes"]["deterministic_replay"]["hashes"]
    assert hashes_a == hashes_b

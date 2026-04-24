"""End-to-end Phase-4-like flow: adapter CLI -> replay subcommand.

Runs the adapter from plan 02-01 against the synthetic Phase-4-shaped
fixtures to emit a neutral BenchmarkManifest, then runs the replay
subcommand against that manifest and verifies:

- both commands exit 0
- the replay record exposes all five stability modes
- reference-freeze SHA matches byte-for-byte between the adapter run
  record and the replay record
- the best_route selected by replay is one of the surviving adapter
  routes

No live Phase 3c data is touched; fixtures come from
``tests/fixtures/phase4_like_*``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gnosis_morph_bench.adapters.indus_phase4 import main as adapter_main
from gnosis_morph_bench.cli import main as cli_main


def test_phase4_like_adapter_to_replay(
    tmp_path: Path,
    phase4_like_paths: dict[str, Path],
    phase4_like_fixture_sha: str,
) -> None:
    neutral_manifest_path = tmp_path / "neutral_manifest.json"
    adapter_run_record_path = tmp_path / "neutral_manifest_run.json"

    adapter_rc = adapter_main(
        [
            "--feature-manifest",
            str(phase4_like_paths["feature_manifest"]),
            "--reference-frozen",
            str(phase4_like_paths["reference_frozen_good"]),
            "--output",
            str(neutral_manifest_path),
            "--run-record",
            str(adapter_run_record_path),
        ]
    )
    assert adapter_rc == 0, "adapter CLI must exit 0 on clean fixtures"
    assert neutral_manifest_path.is_file()
    assert adapter_run_record_path.is_file()

    adapter_run_record = json.loads(adapter_run_record_path.read_text())
    adapter_freeze_sha = adapter_run_record["reference_freeze"]["sha256"]
    assert adapter_freeze_sha == phase4_like_fixture_sha, (
        "adapter freeze SHA drifted from the fixture's canonical SHA"
    )
    surviving_routes = set(adapter_run_record["routes_out"])
    assert surviving_routes, "adapter emitted no surviving routes"

    replay_record_path = tmp_path / "replay_record.json"
    replay_rc = cli_main(
        [
            "replay",
            str(neutral_manifest_path),
            "--output",
            str(replay_record_path),
            "--reference-key",
            "icit_set",
            "--clusters",
            "3",
            "--seed",
            "42",
            "--noise-repeats",
            "2",
            "--fraction-repeats",
            "2",
            "--replay-repeats",
            "2",
            "--seeds",
            "1,2",
        ]
    )
    assert replay_rc == 0, "replay CLI must exit 0 on adapter-emitted manifest"
    assert replay_record_path.is_file()

    replay_record = json.loads(replay_record_path.read_text())
    assert set(replay_record["stability"]["modes"]) == {
        "deterministic_replay",
        "leave_fraction_out",
        "noise_injection",
        "k_sensitivity",
        "seed_variance",
    }
    replay_freeze_sha = replay_record["reference_freeze"]["sha256"]
    assert replay_freeze_sha == adapter_freeze_sha, (
        "reference-freeze SHA mismatch between adapter run record and "
        "replay record; the neutral anchor should be identical"
    )

    assert replay_record["best_route"] in surviving_routes, (
        f"best_route={replay_record['best_route']!r} must come from the "
        f"adapter's surviving-route set {surviving_routes!r}"
    )

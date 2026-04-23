"""Behavioral tests for the Indus Phase 4 v1 adapter.

Every test uses only synthetic fixtures under ``tests/fixtures/`` and
writes all outputs into ``tmp_path``. No test reaches outside the
repo.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from gnosis_morph_bench.adapters.indus_phase4 import (
    DEFAULT_GOVERNING_ROUTE,
    DEFAULT_OUTPUT,
    build_parser,
    main,
)
from gnosis_morph_bench.benchmark import EvaluationConfig, evaluate_route
from gnosis_morph_bench.schema import load_manifest


REQUIRED_FLAGS = {"--feature-manifest", "--reference-frozen"}
OPTIONAL_FLAGS = {
    "--output",
    "--manifest-name",
    "--reference-key",
    "--include-route",
    "--drop-item-with-nan",
    "--run-record",
}


def _parser_option_strings() -> set[str]:
    parser = build_parser()
    flags: set[str] = set()
    for action in parser._actions:
        for opt in action.option_strings:
            flags.add(opt)
    return flags


def _invoke_adapter(
    tmp_path: Path,
    feature_manifest: Path,
    reference_frozen: Path,
    *,
    extra: list[str] | None = None,
    output_name: str = "benchmark.json",
    run_record_name: str = "benchmark_run.json",
) -> tuple[int, Path, Path]:
    output = tmp_path / output_name
    run_record = tmp_path / run_record_name
    argv = [
        "--feature-manifest",
        str(feature_manifest),
        "--reference-frozen",
        str(reference_frozen),
        "--output",
        str(output),
        "--run-record",
        str(run_record),
    ]
    if extra:
        argv.extend(extra)
    code = main(argv)
    return code, output, run_record


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------


def test_adapter_cli_surface() -> None:
    """ADAPTER_CONTRACT_v1 required + optional flags all present."""
    flags = _parser_option_strings()
    for flag in REQUIRED_FLAGS | OPTIONAL_FLAGS:
        assert flag in flags, f"missing CLI flag: {flag}"


def test_required_flags_marked_required() -> None:
    parser = build_parser()
    for action in parser._actions:
        for opt in action.option_strings:
            if opt in REQUIRED_FLAGS:
                assert action.required, f"{opt} should be marked required"


# ---------------------------------------------------------------------------
# Round-trip through load_manifest + evaluate_route
# ---------------------------------------------------------------------------


def test_adapter_roundtrip(tmp_path: Path, phase4_like_paths: dict) -> None:
    code, output, _ = _invoke_adapter(
        tmp_path,
        phase4_like_paths["feature_manifest"],
        phase4_like_paths["reference_frozen_good"],
    )
    assert code == 0
    manifest = load_manifest(output)
    assert manifest.manifest_name == "indus-phase4"
    assert len(manifest.items) >= 9
    assert DEFAULT_GOVERNING_ROUTE in manifest.route_names

    cfg = EvaluationConfig(
        reference_key="icit_set", n_clusters=3, null_repeats=8, seed=42
    )
    result = evaluate_route(manifest, DEFAULT_GOVERNING_ROUTE, cfg)
    nmi = result["nmi"]
    assert isinstance(nmi, float)
    assert math.isfinite(nmi)
    assert 0.0 <= nmi <= 1.0


# ---------------------------------------------------------------------------
# Freeze parity + mismatch exit code 2
# ---------------------------------------------------------------------------


def test_freeze_parity(
    tmp_path: Path, phase4_like_paths: dict, phase4_like_fixture_sha: str
) -> None:
    code, _, run_record = _invoke_adapter(
        tmp_path,
        phase4_like_paths["feature_manifest"],
        phase4_like_paths["reference_frozen_good"],
    )
    assert code == 0
    record = json.loads(run_record.read_text(encoding="utf-8"))
    assert record["reference_freeze"]["sha256"] == phase4_like_fixture_sha


def test_freeze_mismatch_exit_code(
    tmp_path: Path, phase4_like_paths: dict, capsys: pytest.CaptureFixture[str]
) -> None:
    code, _, run_record = _invoke_adapter(
        tmp_path,
        phase4_like_paths["feature_manifest"],
        phase4_like_paths["reference_frozen_bad"],
    )
    assert code == 2
    captured = capsys.readouterr()
    assert "icit_set" in captured.err
    assert run_record.exists(), "run record must be written on contract-violation path"
    record = json.loads(run_record.read_text(encoding="utf-8"))
    assert "contract_violation_reason" in record
    assert "icit_set" in record["contract_violation_reason"]


# ---------------------------------------------------------------------------
# Label surface carried / dropped
# ---------------------------------------------------------------------------


def test_label_surface_carried(tmp_path: Path, phase4_like_paths: dict) -> None:
    code, output, _ = _invoke_adapter(
        tmp_path,
        phase4_like_paths["feature_manifest"],
        phase4_like_paths["reference_frozen_good"],
    )
    assert code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    for item in payload["items"]:
        labels = item["reference_labels"]
        assert list(labels.keys()) == ["icit_set"], (
            f"item {item['item_id']} carries extra label columns: {list(labels.keys())}"
        )
        assert isinstance(labels["icit_set"], str)
        assert labels["icit_set"].strip() != ""


def test_label_surface_dropped(tmp_path: Path, phase4_like_paths: dict) -> None:
    code, output, _ = _invoke_adapter(
        tmp_path,
        phase4_like_paths["feature_manifest"],
        phase4_like_paths["reference_frozen_good"],
    )
    assert code == 0
    text = output.read_text(encoding="utf-8")
    for banned in (
        "provenance_url",
        "authorial_note",
        "stroke_encoding",
        "broken_route_nonnumeric",
        "broken_route_mixed_lengths",
    ):
        assert banned not in text, f"emitted manifest contains dropped key: {banned}"


# ---------------------------------------------------------------------------
# NaN handling
# ---------------------------------------------------------------------------


def _copy_fixture_with_nan(
    source: Path, dest: Path, item_index: int = 2
) -> tuple[str, Path]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    item = payload["items"][item_index]
    item_id = item["item_id"]
    vec = list(item["route_features"]["pixel_full_concat_31d_single"])
    vec[0] = float("nan")
    item["route_features"]["pixel_full_concat_31d_single"] = vec
    dest.write_text(json.dumps(payload), encoding="utf-8")
    return item_id, dest


def _regenerate_frozen_for(
    feature_manifest_path: Path, dest: Path, reference_key: str = "icit_set"
) -> Path:
    """Recompute the canonical SHA for a modified fixture copy.

    A NaN injection does not change the label assignments, so the SHA
    is the same as the original. We still regenerate rather than reuse
    to keep the test free of assumptions about the fixture layout.
    """
    import hashlib

    payload = json.loads(feature_manifest_path.read_text(encoding="utf-8"))
    assignments = {
        item["item_id"]: item["reference_labels"][reference_key]
        for item in payload["items"]
    }
    encoded = json.dumps(assignments, sort_keys=True).encode("utf-8")
    sha = hashlib.sha256(encoded).hexdigest()
    dest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "reference_key": reference_key,
                "sha256": sha,
                "item_count": len(assignments),
            }
        ),
        encoding="utf-8",
    )
    return dest


def test_nan_strict_default(
    tmp_path: Path,
    phase4_like_paths: dict,
    capsys: pytest.CaptureFixture[str],
) -> None:
    nan_manifest = tmp_path / "manifest_with_nan.json"
    nan_item_id, _ = _copy_fixture_with_nan(
        phase4_like_paths["feature_manifest"], nan_manifest
    )
    frozen = _regenerate_frozen_for(nan_manifest, tmp_path / "frozen.json")

    code, _, _ = _invoke_adapter(tmp_path, nan_manifest, frozen)
    assert code == 2
    captured = capsys.readouterr()
    assert nan_item_id in captured.err


def test_drop_item_with_nan_flag(
    tmp_path: Path, phase4_like_paths: dict
) -> None:
    """With --drop-item-with-nan the adapter drops and continues.

    Dropping an item changes the label-assignment set, so the neutral
    freeze computed post-drop does NOT equal the freeze over the full
    upstream assignments. To exercise exit-0 we regenerate a frozen
    reference over the post-drop assignment set and feed that instead.
    """
    # Step 1: inject NaN.
    nan_manifest = tmp_path / "manifest_with_nan.json"
    nan_item_id, _ = _copy_fixture_with_nan(
        phase4_like_paths["feature_manifest"], nan_manifest
    )

    # Step 2: build a post-drop manifest view and freeze over that.
    post_manifest = json.loads(nan_manifest.read_text(encoding="utf-8"))
    post_manifest["items"] = [
        i for i in post_manifest["items"] if i["item_id"] != nan_item_id
    ]
    post_path = tmp_path / "post_drop_manifest.json"
    post_path.write_text(json.dumps(post_manifest), encoding="utf-8")
    frozen = _regenerate_frozen_for(post_path, tmp_path / "frozen_post_drop.json")

    # Step 3: run with --drop-item-with-nan; expect success and a
    # recorded drop entry.
    code, output, run_record = _invoke_adapter(
        tmp_path, nan_manifest, frozen, extra=["--drop-item-with-nan"]
    )
    assert code == 0
    record = json.loads(run_record.read_text(encoding="utf-8"))
    dropped_ids = [entry["item_id"] for entry in record["items_dropped"]]
    assert nan_item_id in dropped_ids
    dropped_reasons = {
        entry["item_id"]: entry["reason"] for entry in record["items_dropped"]
    }
    assert "NaN" in dropped_reasons[nan_item_id]


# ---------------------------------------------------------------------------
# Include-route whitelist
# ---------------------------------------------------------------------------


def test_include_route_whitelist(tmp_path: Path, phase4_like_paths: dict) -> None:
    code, output, _ = _invoke_adapter(
        tmp_path,
        phase4_like_paths["feature_manifest"],
        phase4_like_paths["reference_frozen_good"],
        extra=["--include-route", DEFAULT_GOVERNING_ROUTE],
    )
    assert code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    for item in payload["items"]:
        assert list(item["route_features"].keys()) == [DEFAULT_GOVERNING_ROUTE], (
            f"item {item['item_id']} exposes routes {list(item['route_features'].keys())}"
        )


# ---------------------------------------------------------------------------
# Default output path lives under artifacts/adapters/
# ---------------------------------------------------------------------------


def test_output_defaults_under_artifacts_adapters(
    tmp_path: Path, phase4_like_paths: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    argv = [
        "--feature-manifest",
        str(phase4_like_paths["feature_manifest"]),
        "--reference-frozen",
        str(phase4_like_paths["reference_frozen_good"]),
    ]
    code = main(argv)
    assert code == 0
    expected = Path(DEFAULT_OUTPUT)
    assert expected.exists(), f"default output path missing: {expected}"
    assert expected.parts[:2] == ("artifacts", "adapters")
    # Run record default lives next to it.
    default_run = expected.parent / "indus_phase4_benchmark_manifest_run.json"
    assert default_run.exists(), f"default run record missing: {default_run}"

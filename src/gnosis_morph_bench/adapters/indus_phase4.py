"""Indus Phase 4 v1 adapter.

Translates an admitted upstream Phase 4 feature manifest (shape only --
no domain content is baked into this module) into a neutral
``BenchmarkManifest`` JSON consumable by
``gnosis_morph_bench.schema.load_manifest``.

Binding spec: ``docs/family/ADAPTER_CONTRACT_v1.md``.

This module is pure CLI + library. It does not reach outside its
declared inputs, does not import any upstream runtime helper, does not
perform image preprocessing, and does not write outside its declared
output paths.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any

from gnosis_morph_bench import _utils
from gnosis_morph_bench.schema import freeze_reference, load_manifest


ADAPTER_NAME = "indus_phase4_v1"
ADAPTER_VERSION = "0.1.0"
DEFAULT_OUTPUT = "artifacts/adapters/indus_phase4_benchmark_manifest.json"
DEFAULT_MANIFEST_NAME = "indus-phase4"
DEFAULT_GOVERNING_ROUTE = "pixel_full_concat_31d_single"


class ContractViolation(Exception):
    """Raised when the adapter detects a contract breach.

    Examples: NaN in strict mode, missing reference label on an item,
    upstream SHA disagreement with the neutral freeze.
    """


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Return the adapter's CLI parser.

    Flags match the "Required CLI arguments" and "Optional CLI
    arguments" tables in ADAPTER_CONTRACT_v1.md.
    """
    parser = argparse.ArgumentParser(
        prog="gnosis-morph-bench-adapter-indus-phase4",
        description=(
            "Translate an admitted Indus Phase 4 source family into a "
            "neutral BenchmarkManifest."
        ),
    )
    parser.add_argument(
        "--feature-manifest",
        required=True,
        help="Path to the upstream Phase 3c feature manifest JSON.",
    )
    parser.add_argument(
        "--reference-frozen",
        required=True,
        help="Path to the upstream SHA-frozen reference JSON (e.g., ICIT reference).",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=(
            "Destination for the neutral BenchmarkManifest JSON "
            f"(default: {DEFAULT_OUTPUT})."
        ),
    )
    parser.add_argument(
        "--manifest-name",
        default=DEFAULT_MANIFEST_NAME,
        help="Human-readable manifest_name to embed in the emitted JSON.",
    )
    parser.add_argument(
        "--reference-key",
        default=None,
        help=(
            "Which reference key to carry as the label column. If "
            "omitted, the key declared in the frozen-reference JSON is used."
        ),
    )
    parser.add_argument(
        "--include-route",
        action="append",
        default=None,
        help=(
            "Whitelist a specific route name. Repeat to include "
            "multiple. Default: include all valid routes."
        ),
    )
    parser.add_argument(
        "--drop-item-with-nan",
        action="store_true",
        help=(
            "Drop items whose chosen route vectors contain NaN instead "
            "of aborting. Default: off (strict)."
        ),
    )
    parser.add_argument(
        "--run-record",
        default=None,
        help=(
            "Optional explicit path for the adapter-run record. "
            "Default: <output>_run.json alongside the manifest."
        ),
    )
    return parser


# ---------------------------------------------------------------------------
# Translation core
# ---------------------------------------------------------------------------


def _is_real_number(value: Any) -> bool:
    """True iff ``value`` is a finite or non-finite real scalar (no bools)."""
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def _vector_has_nan(vector: list[float]) -> bool:
    for scalar in vector:
        if isinstance(scalar, float) and math.isnan(scalar):
            return True
    return False


def _resolve_reference_key(
    reference_frozen: dict[str, Any],
    explicit_key: str | None,
) -> str:
    if explicit_key:
        return str(explicit_key)
    upstream_key = reference_frozen.get("reference_key")
    if not upstream_key:
        raise ContractViolation(
            "frozen reference does not declare `reference_key` and none was "
            "passed via --reference-key"
        )
    return str(upstream_key)


def _collect_route_names(raw_items: list[dict[str, Any]]) -> list[str]:
    seen: list[str] = []
    seen_set: set[str] = set()
    for item in raw_items:
        for route_name in (item.get("route_features") or {}).keys():
            if route_name not in seen_set:
                seen.append(str(route_name))
                seen_set.add(str(route_name))
    return seen


def _classify_route(
    route_name: str,
    raw_items: list[dict[str, Any]],
) -> tuple[bool, str | None]:
    """Check whether ``route_name`` can cross the adapter boundary.

    Returns (carried, drop_reason). ``carried`` is True if every
    exposure of the route is a numeric vector of the same length across
    the items that expose it. Otherwise the route is dropped and
    ``drop_reason`` names why.
    """
    seen_lengths: set[int] = set()
    exposure_count = 0
    for item in raw_items:
        route_features = item.get("route_features") or {}
        if route_name not in route_features:
            continue
        exposure_count += 1
        vector = route_features[route_name]
        if not isinstance(vector, list):
            return False, "route values are not lists"
        for scalar in vector:
            if not _is_real_number(scalar):
                return False, "route vector contains non-numeric value"
        seen_lengths.add(len(vector))
    if exposure_count == 0:
        return False, "route is not exposed by any item"
    if len(seen_lengths) != 1:
        return False, "route vector length varies across items"
    length = next(iter(seen_lengths))
    if length == 0:
        return False, "route vector length is zero"
    if exposure_count < 2:
        return False, "route exposed by fewer than two items"
    return True, None


def translate(
    feature_manifest: dict[str, Any],
    reference_frozen: dict[str, Any],
    *,
    reference_key: str,
    include_routes: list[str] | None,
    drop_item_with_nan: bool,
    manifest_name: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Translate an upstream feature manifest into neutral shape.

    Returns ``(benchmark_manifest_payload, translation_record)`` where
    ``translation_record`` is a partial run-record fragment containing
    ``items_in``, ``items_out``, ``items_dropped``, ``routes_in``,
    ``routes_out``, and ``routes_dropped``. The caller combines this
    fragment with input-path/hash/freeze data to produce the final run
    record described in the contract.
    """
    raw_items = list(feature_manifest.get("items") or [])
    if not raw_items:
        raise ContractViolation("upstream feature manifest has no items")

    # Every item MUST carry the chosen reference key.
    for raw_item in raw_items:
        item_id = raw_item.get("item_id")
        labels = raw_item.get("reference_labels") or {}
        if reference_key not in labels:
            raise ContractViolation(
                f"item '{item_id}' is missing required reference key "
                f"'{reference_key}' in reference_labels"
            )
        value = labels[reference_key]
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ContractViolation(
                f"item '{item_id}' has empty label for reference key "
                f"'{reference_key}'"
            )

    route_names_all = _collect_route_names(raw_items)
    if not route_names_all:
        raise ContractViolation("upstream feature manifest exposes no routes")

    # Pass 1: classify each route.
    routes_dropped: list[dict[str, str]] = []
    carried_routes: list[str] = []
    for route_name in route_names_all:
        carried, reason = _classify_route(route_name, raw_items)
        if not carried:
            routes_dropped.append(
                {"route_name": route_name, "reason": reason or "unknown"}
            )
            continue
        if include_routes is not None and route_name not in include_routes:
            routes_dropped.append(
                {"route_name": route_name, "reason": "excluded by --include-route whitelist"}
            )
            continue
        carried_routes.append(route_name)

    if include_routes is not None:
        for wanted in include_routes:
            if wanted not in route_names_all:
                routes_dropped.append(
                    {"route_name": wanted, "reason": "whitelisted route not present upstream"}
                )

    if not carried_routes:
        raise ContractViolation("no routes survive the adapter gate")

    # Pass 2: walk items, build neutral payload, handle NaN.
    items_out: list[dict[str, Any]] = []
    items_dropped: list[dict[str, str]] = []
    for raw_item in raw_items:
        item_id = str(raw_item.get("item_id"))
        label_value = str(raw_item["reference_labels"][reference_key])
        raw_routes = raw_item.get("route_features") or {}
        nan_trigger: str | None = None
        clean_routes: dict[str, list[float]] = {}
        for route_name in carried_routes:
            if route_name not in raw_routes:
                continue
            vector = [float(x) for x in raw_routes[route_name]]
            if _vector_has_nan(vector):
                nan_trigger = route_name
                break
            clean_routes[route_name] = vector

        if nan_trigger is not None:
            if not drop_item_with_nan:
                raise ContractViolation(
                    f"item '{item_id}' has NaN in route '{nan_trigger}'"
                )
            items_dropped.append(
                {
                    "item_id": item_id,
                    "reason": f"NaN in route '{nan_trigger}'",
                }
            )
            continue

        if not clean_routes:
            items_dropped.append(
                {
                    "item_id": item_id,
                    "reason": "item exposes no carried routes after gating",
                }
            )
            continue

        items_out.append(
            {
                "item_id": item_id,
                "reference_labels": {reference_key: label_value},
                "route_features": clean_routes,
            }
        )

    if not items_out:
        raise ContractViolation("no items survive the adapter gate")

    # Post-filter routes: a route that no surviving item exposes is
    # silently dropped too, but we record it for provenance.
    surviving_routes = sorted({
        route_name
        for item in items_out
        for route_name in item["route_features"].keys()
    })
    for route_name in carried_routes:
        if route_name not in surviving_routes:
            routes_dropped.append(
                {"route_name": route_name, "reason": "no surviving item exposes this route after NaN handling"}
            )

    benchmark_manifest_payload: dict[str, Any] = {
        "schema_version": 1,
        "manifest_name": str(manifest_name),
        "items": items_out,
    }

    translation_record = {
        "items_in": len(raw_items),
        "items_out": len(items_out),
        "items_dropped": items_dropped,
        "routes_in": route_names_all,
        "routes_out": surviving_routes,
        "routes_dropped": routes_dropped,
    }
    return benchmark_manifest_payload, translation_record


# ---------------------------------------------------------------------------
# Freeze parity helpers
# ---------------------------------------------------------------------------


def compute_freeze(
    benchmark_manifest_payload: dict[str, Any],
    reference_key: str,
) -> dict[str, Any]:
    """Round-trip the payload through ``load_manifest`` and freeze it.

    Keeping ``schema.freeze_reference`` as the sole freeze implementation
    guarantees parity between what the adapter writes and what a neutral
    consumer would compute.
    """
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as handle:
        json.dump(benchmark_manifest_payload, handle)
        temp_path = handle.name
    try:
        manifest = load_manifest(temp_path)
        freeze = freeze_reference(manifest, reference_key)
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
    # Strip the full assignments dict from the freeze block we embed in
    # the run record — the sha is the stable anchor.
    return {
        "reference_key": freeze["reference_key"],
        "item_count": freeze["item_count"],
        "sha256": freeze["sha256"],
    }


def verify_upstream_freeze(
    neutral_freeze: dict[str, Any],
    upstream: dict[str, Any],
    reference_key: str,
) -> None:
    """Raise ``ContractViolation`` if the upstream SHA disagrees."""
    upstream_key = upstream.get("reference_key")
    if upstream_key and str(upstream_key) != reference_key:
        raise ContractViolation(
            f"frozen-reference key mismatch: upstream declares "
            f"'{upstream_key}' but adapter is using '{reference_key}'"
        )
    upstream_sha = upstream.get("sha256")
    if not upstream_sha:
        raise ContractViolation(
            f"frozen reference for key '{reference_key}' has no sha256"
        )
    if str(upstream_sha) != str(neutral_freeze["sha256"]):
        raise ContractViolation(
            f"frozen-SHA mismatch on reference key '{reference_key}': "
            f"upstream={upstream_sha} neutral={neutral_freeze['sha256']}"
        )


# ---------------------------------------------------------------------------
# Run record + main entrypoint
# ---------------------------------------------------------------------------


def _resolve_run_record_path(output: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    stem = output.with_suffix("")
    return stem.parent / f"{stem.name}_run.json"


def _assemble_failure_record(
    args: argparse.Namespace,
    reason: str,
    translation_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": 1,
        "adapter": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
        "manifest_name": args.manifest_name,
        "input_paths": {
            "feature_manifest": str(Path(args.feature_manifest).resolve())
            if args.feature_manifest
            else None,
            "reference_frozen": str(Path(args.reference_frozen).resolve())
            if args.reference_frozen
            else None,
        },
        "input_hashes": {},
        "items_in": None,
        "items_out": None,
        "items_dropped": [],
        "routes_in": [],
        "routes_out": [],
        "routes_dropped": [],
        "reference_freeze": None,
        "contract_violation_reason": reason,
    }
    try:
        record["input_hashes"]["feature_manifest_sha256"] = _utils.sha256_file(
            args.feature_manifest
        )
    except OSError:
        record["input_hashes"]["feature_manifest_sha256"] = None
    try:
        record["input_hashes"]["reference_frozen_sha256"] = _utils.sha256_file(
            args.reference_frozen
        )
    except OSError:
        record["input_hashes"]["reference_frozen_sha256"] = None
    if translation_record is not None:
        record.update(
            {
                "items_in": translation_record.get("items_in"),
                "items_out": translation_record.get("items_out"),
                "items_dropped": translation_record.get("items_dropped", []),
                "routes_in": translation_record.get("routes_in", []),
                "routes_out": translation_record.get("routes_out", []),
                "routes_dropped": translation_record.get("routes_dropped", []),
            }
        )
    return record


def run(args: argparse.Namespace) -> int:
    """Execute the adapter. Returns exit code (0 success, 2 contract)."""
    output_path = Path(args.output)
    run_record_path = _resolve_run_record_path(output_path, args.run_record)

    # Load inputs.
    try:
        feature_manifest = _utils.read_json(args.feature_manifest)
    except FileNotFoundError as exc:
        record = _assemble_failure_record(
            args, reason=f"feature manifest not readable: {exc}"
        )
        _utils.write_json(run_record_path, record)
        print(
            f"contract violation: feature manifest not readable: {exc}",
            file=sys.stderr,
        )
        return 2
    try:
        reference_frozen = _utils.read_json(args.reference_frozen)
    except FileNotFoundError as exc:
        record = _assemble_failure_record(
            args, reason=f"reference frozen not readable: {exc}"
        )
        _utils.write_json(run_record_path, record)
        print(
            f"contract violation: reference frozen not readable: {exc}",
            file=sys.stderr,
        )
        return 2

    # Resolve the reference key.
    try:
        reference_key = _resolve_reference_key(reference_frozen, args.reference_key)
    except ContractViolation as exc:
        record = _assemble_failure_record(args, reason=str(exc))
        _utils.write_json(run_record_path, record)
        print(f"contract violation: {exc}", file=sys.stderr)
        return 2

    # Translate.
    try:
        benchmark_manifest_payload, translation_record = translate(
            feature_manifest,
            reference_frozen,
            reference_key=reference_key,
            include_routes=args.include_route,
            drop_item_with_nan=args.drop_item_with_nan,
            manifest_name=args.manifest_name,
        )
    except ContractViolation as exc:
        record = _assemble_failure_record(args, reason=str(exc))
        _utils.write_json(run_record_path, record)
        print(f"contract violation: {exc}", file=sys.stderr)
        return 2

    # Freeze and verify parity with upstream.
    try:
        neutral_freeze = compute_freeze(benchmark_manifest_payload, reference_key)
        verify_upstream_freeze(neutral_freeze, reference_frozen, reference_key)
    except ContractViolation as exc:
        record = _assemble_failure_record(
            args, reason=str(exc), translation_record=translation_record
        )
        _utils.write_json(run_record_path, record)
        print(f"contract violation: {exc}", file=sys.stderr)
        return 2

    # Assemble success record.
    input_hashes = {
        "feature_manifest_sha256": _utils.sha256_file(args.feature_manifest),
        "reference_frozen_sha256": _utils.sha256_file(args.reference_frozen),
    }
    success_record: dict[str, Any] = {
        "schema_version": 1,
        "adapter": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
        "manifest_name": args.manifest_name,
        "input_paths": {
            "feature_manifest": str(Path(args.feature_manifest).resolve()),
            "reference_frozen": str(Path(args.reference_frozen).resolve()),
        },
        "input_hashes": input_hashes,
        "items_in": translation_record["items_in"],
        "items_out": translation_record["items_out"],
        "items_dropped": translation_record["items_dropped"],
        "routes_in": translation_record["routes_in"],
        "routes_out": translation_record["routes_out"],
        "routes_dropped": translation_record["routes_dropped"],
        "reference_freeze": neutral_freeze,
        "generated_at": _utils.utc_now_iso(),
    }

    _utils.write_json(output_path, benchmark_manifest_payload)
    _utils.write_json(run_record_path, success_record)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse argv and invoke :func:`run`.

    Converts uncaught ``ContractViolation`` into exit code 2 and any
    other unexpected exception into exit code 1 with a full traceback
    printed to stderr -- never a silent swallow.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except ContractViolation as exc:  # pragma: no cover -- run() handles these
        print(f"contract violation: {exc}", file=sys.stderr)
        return 2
    except Exception:  # pragma: no cover -- defensive
        traceback.print_exc()
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

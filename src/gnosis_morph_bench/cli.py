"""CLI entrypoints for the staged morph-bench package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .benchmark import EvaluationConfig, evaluate_routes
from .schema import freeze_reference, load_manifest
from .stability import deterministic_replay, leave_fraction_out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the staged morph-bench smoke path.")
    parser.add_argument("manifest", help="Path to a benchmark manifest JSON file.")
    parser.add_argument(
        "--output",
        default="artifacts/smoke/smoke_report.json",
        help="Where to write the JSON smoke report.",
    )
    parser.add_argument("--reference-key", default="family")
    parser.add_argument("--clusters", type=int, default=3)
    parser.add_argument("--null-repeats", type=int, default=16)
    parser.add_argument("--seed", type=int, default=42)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = load_manifest(args.manifest)
    config = EvaluationConfig(
        reference_key=args.reference_key,
        n_clusters=args.clusters,
        null_repeats=args.null_repeats,
        seed=args.seed,
    )
    route_results = evaluate_routes(manifest, config)
    best_route = route_results[0]["route_name"]
    payload = {
        "schema_version": 1,
        "manifest_name": manifest.manifest_name,
        "reference_freeze": freeze_reference(manifest, args.reference_key),
        "route_results": route_results,
        "best_route": best_route,
        "replay": deterministic_replay(manifest, best_route, config),
        "leave_fraction_out": leave_fraction_out(manifest, best_route, config),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2))
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

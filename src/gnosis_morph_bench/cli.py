"""CLI entrypoints for the staged morph-bench package.

Two subcommands:

- ``smoke``  runs the minimal synthetic-fixture smoke path
  (``evaluate_routes`` + ``deterministic_replay`` + ``leave_fraction_out``)
  and writes the same ``smoke_report.json`` shape as before this plan.
- ``replay`` runs :func:`replay.run_replay_record` against any
  :class:`BenchmarkManifest` (synthetic fixture or adapter-emitted
  neutral manifest) and writes a ReplayRecord JSON.

A legacy invocation (no subcommand, first positional is the manifest
path) remains backward-compatible. It emits a one-line deprecation note
on stderr and dispatches to ``smoke``. This keeps the
``gnosis-morph-bench-smoke`` console entrypoint declared in
``pyproject.toml`` working without a pyproject edit.

Defaults land under repo-local ``artifacts/...``. No ``workspace/``
paths. No upstream monorepo imports.
"""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path
from typing import Any

from ._utils import write_json
from .benchmark import EvaluationConfig, evaluate_routes
from .replay import run_replay_record
from .schema import freeze_reference, load_manifest
from .stability import deterministic_replay, leave_fraction_out


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _add_shared_arguments(sub: argparse.ArgumentParser) -> None:
    """Flags shared by both `smoke` and `replay`."""
    sub.add_argument("manifest", help="Path to a BenchmarkManifest JSON file.")
    sub.add_argument("--reference-key", default="family")
    sub.add_argument("--clusters", type=int, default=3)
    sub.add_argument("--null-repeats", type=int, default=16)
    sub.add_argument("--seed", type=int, default=42)


def build_parser() -> argparse.ArgumentParser:
    """Return the two-subcommand parser used by :func:`main`."""
    parser = argparse.ArgumentParser(
        prog="gnosis-morph-bench",
        description=(
            "Neutral morph-bench CLI. `smoke` runs the minimal synthetic "
            "smoke path; `replay` runs the full five-mode stability battery "
            "and emits a ReplayRecord."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    smoke = subparsers.add_parser(
        "smoke",
        help="Run the minimal synthetic smoke pipeline.",
    )
    _add_shared_arguments(smoke)
    smoke.add_argument(
        "--output",
        default="artifacts/smoke/smoke_report.json",
        help="Where to write the JSON smoke report.",
    )

    replay = subparsers.add_parser(
        "replay",
        help="Run the full battery and emit a ReplayRecord.",
    )
    _add_shared_arguments(replay)
    replay.add_argument(
        "--output",
        default="artifacts/replay/replay_record.json",
        help="Where to write the ReplayRecord JSON.",
    )
    replay.add_argument("--noise-sigma", type=float, default=0.05)
    replay.add_argument("--noise-repeats", type=int, default=6)
    replay.add_argument(
        "--k-offsets",
        default="-1,1",
        help="Comma-separated integer offsets relative to --clusters.",
    )
    replay.add_argument(
        "--seeds",
        default="1,2,3,4",
        help="Comma-separated integer seeds for the seed_variance mode.",
    )
    replay.add_argument("--fraction", type=float, default=0.25)
    replay.add_argument("--fraction-repeats", type=int, default=6)
    replay.add_argument("--replay-repeats", type=int, default=3)

    return parser


# ---------------------------------------------------------------------------
# Subcommand dispatch
# ---------------------------------------------------------------------------


def _build_config(args: argparse.Namespace) -> EvaluationConfig:
    return EvaluationConfig(
        reference_key=args.reference_key,
        n_clusters=args.clusters,
        null_repeats=args.null_repeats,
        seed=args.seed,
    )


def _parse_int_list(raw: str, *, flag: str) -> tuple[int, ...]:
    pieces = [piece.strip() for piece in raw.split(",") if piece.strip()]
    if not pieces:
        raise ValueError(f"{flag} must contain at least one integer")
    try:
        return tuple(int(piece) for piece in pieces)
    except ValueError as exc:  # pragma: no cover -- argparse surfaces the message
        raise ValueError(f"{flag} must be comma-separated integers") from exc


def _run_smoke(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    config = _build_config(args)
    route_results = evaluate_routes(manifest, config)
    best_route = str(route_results[0]["route_name"])
    payload: dict[str, Any] = {
        "schema_version": 1,
        "manifest_name": manifest.manifest_name,
        "reference_freeze": freeze_reference(manifest, args.reference_key),
        "route_results": route_results,
        "best_route": best_route,
        "replay": deterministic_replay(manifest, best_route, config),
        "leave_fraction_out": leave_fraction_out(manifest, best_route, config),
    }
    output_path = Path(args.output)
    write_json(output_path, payload)
    print(str(output_path))
    return 0


def _run_replay(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    config = _build_config(args)
    stability_kwargs: dict[str, Any] = {
        "noise_sigma": float(args.noise_sigma),
        "noise_repeats": int(args.noise_repeats),
        "k_offsets": _parse_int_list(args.k_offsets, flag="--k-offsets"),
        "seeds": _parse_int_list(args.seeds, flag="--seeds"),
        "fraction": float(args.fraction),
        "fraction_repeats": int(args.fraction_repeats),
        "replay_repeats": int(args.replay_repeats),
    }
    record = run_replay_record(
        manifest,
        config,
        stability_kwargs=stability_kwargs,
        reference_key=args.reference_key,
    )
    output_path = Path(args.output)
    write_json(output_path, record)
    print(str(output_path))
    return 0


# ---------------------------------------------------------------------------
# Legacy shim + main entrypoint
# ---------------------------------------------------------------------------


_SUBCOMMANDS = ("smoke", "replay")


def _looks_like_legacy_invocation(argv: list[str]) -> bool:
    """True iff argv appears to be the pre-02-02 single-positional form.

    The old CLI took ``manifest_path [--flags...]`` with no subcommand.
    This helper treats argv as legacy iff argv is non-empty and its first
    token is neither a known subcommand nor an option flag (``-...``).
    """
    if not argv:
        return False
    first = argv[0]
    if first in _SUBCOMMANDS:
        return False
    if first.startswith("-"):
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    """Entry point for ``python -m gnosis_morph_bench`` and console script.

    Returns ``0`` on success, ``1`` on unexpected error. On error the
    traceback is written to stderr; there is no silent swallow.
    """
    raw_argv = list(argv if argv is not None else sys.argv[1:])
    if _looks_like_legacy_invocation(raw_argv):
        print(
            "gnosis-morph-bench: deprecation: no subcommand given; "
            "defaulting to `smoke`. Use `smoke <manifest>` explicitly.",
            file=sys.stderr,
        )
        raw_argv = ["smoke", *raw_argv]

    parser = build_parser()
    args = parser.parse_args(raw_argv)

    if args.command is None:
        parser.print_help(sys.stderr)
        return 2

    try:
        if args.command == "smoke":
            return _run_smoke(args)
        if args.command == "replay":
            return _run_replay(args)
    except Exception:
        traceback.print_exc()
        return 1

    # Should be unreachable because argparse enforces the choice.
    print(f"unknown command: {args.command}", file=sys.stderr)  # pragma: no cover
    return 2  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

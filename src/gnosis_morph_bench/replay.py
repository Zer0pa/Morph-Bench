"""Neutral ReplayRecord assembly for the staged morph-bench package.

A :class:`ReplayRecord` is a single JSON-serializable dict that bundles:

- the schema version + record type tag
- the manifest name and chosen reference key
- a ``reference_freeze`` block (anchor SHA from
  :func:`schema.freeze_reference`)
- the :func:`benchmark.evaluate_routes` payload (sorted by NMI desc)
- the governing route name (highest-NMI entry)
- the full five-mode stability battery payload from
  :func:`stability.stability_battery`
- a UTC-ISO timestamp of when the record was generated

The record is emitted under ``artifacts/replay/`` by the CLI; callers
using :func:`run_replay_record` directly receive the dict in memory and
choose where to write.

No upstream runtime helper is imported; no sibling monorepo path is
walked; no ``workspace/...`` default is baked in. The forbidden-pattern
lint in ``tests/test_forbidden_patterns.py`` enforces this.
"""

from __future__ import annotations

from typing import Any

from ._utils import utc_now_iso
from .benchmark import EvaluationConfig, evaluate_routes
from .schema import BenchmarkManifest, freeze_reference
from .stability import stability_battery


REPLAY_RECORD_TYPE = "replay_record_v1"
REPLAY_SCHEMA_VERSION = 1


def run_replay_record(
    manifest: BenchmarkManifest,
    config: EvaluationConfig,
    *,
    stability_kwargs: dict[str, Any] | None = None,
    reference_key: str | None = None,
) -> dict[str, Any]:
    """Assemble a neutral ReplayRecord from a manifest + config.

    The governing route is the top-ranked entry in ``evaluate_routes``
    (sorted by NMI descending). The stability battery runs against that
    route. ``stability_kwargs`` is passed through to
    :func:`stability.stability_battery` as-is; callers must use only the
    declared kwargs that function accepts.

    ``reference_key`` defaults to ``config.reference_key`` when the caller
    does not pass one explicitly.

    Returns the ReplayRecord dict. The caller is responsible for writing
    it (the CLI's ``replay`` subcommand handles that through
    ``_utils.write_json``).
    """
    effective_reference_key = reference_key or config.reference_key
    route_results = evaluate_routes(manifest, config)
    if not route_results:
        raise ValueError("evaluate_routes returned no route payloads")
    best_route = str(route_results[0]["route_name"])

    stability = stability_battery(
        manifest,
        best_route,
        config,
        **(stability_kwargs or {}),
    )

    reference_freeze_payload = freeze_reference(manifest, effective_reference_key)

    record: dict[str, Any] = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "record_type": REPLAY_RECORD_TYPE,
        "manifest_name": manifest.manifest_name,
        "reference_key": effective_reference_key,
        "reference_freeze": reference_freeze_payload,
        "config": {
            "reference_key": config.reference_key,
            "n_clusters": config.n_clusters,
            "null_repeats": config.null_repeats,
            "seed": config.seed,
        },
        "route_results": route_results,
        "best_route": best_route,
        "stability": stability,
        "generated_utc": utc_now_iso(),
    }
    return record

# Adapter Contract v1 — Indus Phase 4

## Purpose

Specify the contract that a Phase 02 adapter must satisfy to convert the
admitted Indus Phase 4 source family into the neutral `BenchmarkManifest`
schema owned by `gnosis_morph_bench.schema`. This contract is design only. It
does not port live code, vendor heavy data, or promote any Phase 4 numeric
value to repo-custody status.

Target source family (see `../../../02_source_inventory/SOURCE_INVENTORY.md`):

- `scripts/indus/phase4_route_selection.py`
- `scripts/indus/phase4_stability.py`
- `scripts/indus/stability_tester.py`

Target authority bundle (see `../../../04_evidence_manifest/EVIDENCE_MANIFEST.md`):

- `workspace/artifacts/indus/phase4/governing_route_selection.json`
- `workspace/artifacts/indus/phase4/icit_reference_frozen.json`
- `workspace/artifacts/indus/phase4/stability_report.json`
- `workspace/artifacts/indus/phase4/dt05_replay.json`
- Plus the upstream feature manifest that Phase 4 consumed
  (`prebinarized_feature_manifest.json` family under
  `workspace/artifacts/indus/phase3c/`).

## Scope

The v1 adapter is the minimum translation layer needed so that a subsequent
Phase 02 replay can call `load_manifest`, `evaluate_routes`,
`freeze_reference`, `deterministic_replay`, and `leave_fraction_out` from
`src/gnosis_morph_bench/` against admitted Indus Phase 4 inputs without any
monorepo path coupling. The v1 adapter does not attempt to reproduce the full
stability battery or any cuneiform input.

## Forbidden Behaviors (Replaces Path-Rewrite Ledger Patterns)

The adapter MUST NOT exhibit any of the following patterns. Each one is the
live-source behavior that the adapter exists to replace; references point to
`../../../02_source_inventory/PATH_REWRITE_LEDGER.md`:

1. `REPO = Path(__file__).resolve().parents[2]` (or any depth-based ancestor
   discovery). The adapter takes all source locations as explicit CLI / env
   inputs.
2. Hardcoded `workspace/artifacts/...` path constants. The adapter takes
   upstream artifact locations as CLI / env inputs only.
3. `from stroke_native_encoding import ...`, `from stroke_zpe_pipeline import
   ...`, or any other glyph-kernel / image-preprocessing import. The adapter
   consumes already-computed feature vectors from the upstream manifest; it
   never re-binarizes images.
4. `from phase3_common import ...` or any other hidden monorepo runtime
   import. Any JSON / hashing / timestamp helper the adapter needs is
   implemented inside `gnosis_morph_bench` itself.
5. `sys.path.insert(...)` surgery. The adapter is installed as part of the
   `gnosis_morph_bench` package and imported cleanly.
6. Direct writes into `workspace/artifacts/...` or any path outside the staged
   repo. Output paths default to repo-local `artifacts/` only.

If any of these patterns appear in the adapter code during Phase 02, the
adapter fails this contract and must be rewritten.

## Inputs

The adapter is a CLI command under `gnosis_morph_bench` that takes all inputs
explicitly. No path is inferred from the current working directory, from the
script's `__file__`, or from any environment outside the declared inputs.

### Required CLI arguments

| Argument | Type | Meaning |
|---|---|---|
| `--feature-manifest` | path | Upstream Phase 3c feature manifest (the prebinarized feature manifest family Phase 4 consumed). Must be readable JSON. |
| `--reference-frozen` | path | `icit_reference_frozen.json` (SHA-frozen ICIT reference). Used as the label source. |
| `--output` | path | Destination for the neutral `BenchmarkManifest` JSON. Defaults to `artifacts/adapters/indus_phase4_benchmark_manifest.json` under the staged repo. |
| `--manifest-name` | string | Human-readable name to embed in the emitted manifest. Defaults to `indus-phase4`. |

### Optional CLI arguments

| Argument | Type | Meaning |
|---|---|---|
| `--reference-key` | string | Which ICIT reference partition to carry as a label column (see "Reference-freeze behavior"). Defaults to the Phase 4 governing key. |
| `--include-route` | string, repeatable | Whitelist specific route names. Default: include all routes present in the feature manifest. |
| `--drop-item-with-nan` | flag | If set, drop items whose chosen route vector contains any NaN. Default: off, and any NaN aborts the run with a clear error. |
| `--run-record` | path | Optional path for the adapter-run record (see "Outputs"). Default: alongside the manifest with suffix `_run.json`. |

### Environment

The adapter may read at most these environment variables, all optional:

- `GNOSIS_MORPH_BENCH_ADAPTER_ROOT` — a base path joined to relative CLI paths
  if the caller prefers. Must never be defaulted to a monorepo root.
- `GNOSIS_MORPH_BENCH_ADAPTER_SEED` — seed forwarded into any downstream
  stability helper invoked by a wrapper. The adapter itself is deterministic
  from inputs alone.

No other env vars, no implicit `REPO`, no `workspace/` defaults.

## Output Shape

The adapter emits a JSON file that `gnosis_morph_bench.schema.load_manifest`
accepts without modification. The shape is exactly:

```json
{
  "schema_version": 1,
  "manifest_name": "indus-phase4",
  "items": [
    {
      "item_id": "<stable id from upstream manifest>",
      "reference_labels": {
        "<reference_key>": "<label>"
      },
      "route_features": {
        "<route_name>": [<float>, <float>, ...]
      }
    }
  ]
}
```

Fields MUST conform to `BenchmarkManifest` / `BenchmarkItem` in
`src/gnosis_morph_bench/schema.py`:

- `schema_version` is the integer `1`.
- `manifest_name` is a non-empty string.
- `items` is a non-empty array with unique `item_id` values after string
  coercion.
- `reference_labels` is a string-to-string mapping.
- `route_features` is a string-to-list-of-number mapping, and for any given
  route name every item that exposes that route MUST use the same vector
  length (this is validated by `extract_route_dataset`).

The emitted manifest MUST round-trip cleanly through `load_manifest` and MUST
expose at least the governing route required to exercise `evaluate_route`,
`deterministic_replay`, and `leave_fraction_out`.

## Carried And Dropped Label Columns

The adapter carries a narrow, explicit label surface into `reference_labels`:

**Carried by default:**

- The Phase 4 governing reference key (the ICIT Set assignment used as the
  governing comparator). One label per item, non-empty string.

**Dropped by default:**

- Provenance URLs and upstream dataset prose.
- Per-item processing logs, timestamps, and human-authored commentary.
- Catalogue-authorial labels beyond the admitted ICIT reference keys.
- Any image-derived side channel (stroke encodings, ZPE tensors, raw pixel
  payloads).

The adapter MAY carry a second reference key in `reference_labels` (for
example ICIT Graph) if the caller asks for it explicitly via a future
`--extra-reference-key` flag. v1 does not expose that flag.

## Carried And Dropped Route-Feature Columns

The adapter maps upstream route vectors into `route_features`:

**Carried by default:**

- All route-name keys present in the upstream feature manifest whose values
  are per-item numeric vectors of consistent length. In particular, the
  governing route `pixel_full_concat_31d_single` MUST be carried whenever it
  is present in the upstream manifest.
- Vectors are cast to `float`. `int` values are coerced to `float`.

**Dropped by default:**

- Any route whose vectors are not all numeric (strings, nested objects,
  heterogeneous shapes).
- Any route whose vector length is inconsistent across items. Such a route is
  dropped with a warning rather than partially carried.
- Any route that maps to fewer than two items after missing-value handling
  (the neutral evaluator cannot cluster a one-item route).
- Derived columns that are not route vectors (summary statistics, per-run
  hashes, debug fields).

## Missing / NaN Handling

The adapter follows a single, explicit rule:

1. A NaN or `null` in a route vector is a hard error by default. The adapter
   aborts with an error message naming the `item_id` and route.
2. If the caller passes `--drop-item-with-nan`, the adapter drops any item
   whose chosen-route vector contains a NaN, records the drop in the
   adapter-run record, and continues. It does NOT impute values and does NOT
   silently coerce NaN to zero.
3. Missing route entries (an item that does not expose a given route) are
   not an error — that item is simply absent from that route's view. This
   matches `extract_route_dataset` semantics in `schema.py`.
4. Missing reference-label entries are an error: every item MUST carry the
   chosen reference key.

The adapter MUST NOT fill NaNs with zeros, means, or medians. Imputation
belongs upstream of the neutral benchmark contract.

## Hash-Freeze Behavior

The adapter integrates with `freeze_reference` in
`src/gnosis_morph_bench/schema.py`. Concretely:

1. After emitting the manifest, the adapter calls
   `freeze_reference(manifest, reference_key)` to compute the canonical
   SHA-256 over the chosen label assignments.
2. The adapter writes that freeze payload into the run record (see below)
   under the key `reference_freeze`.
3. If the caller supplies an upstream frozen reference (for example
   `icit_reference_frozen.json`), the adapter MUST compare the neutral
   `sha256` against the upstream-declared SHA for the same reference key and
   fail loudly on mismatch. A silent pass when the freeze disagrees is a
   contract violation.
4. The adapter never edits or re-signs any upstream authority artifact.

## Adapter Run Record

Alongside the manifest, the adapter writes a JSON run record. This is the
single source of adapter-run provenance and is explicitly neutral (no domain
verdict text). Required keys:

```json
{
  "schema_version": 1,
  "adapter": "indus_phase4_v1",
  "manifest_name": "indus-phase4",
  "input_paths": {
    "feature_manifest": "<absolute path>",
    "reference_frozen": "<absolute path>"
  },
  "input_hashes": {
    "feature_manifest_sha256": "...",
    "reference_frozen_sha256": "..."
  },
  "items_in": <int>,
  "items_out": <int>,
  "items_dropped": [{"item_id": "...", "reason": "..."}],
  "routes_in": [...],
  "routes_out": [...],
  "routes_dropped": [{"route_name": "...", "reason": "..."}],
  "reference_freeze": {...},
  "adapter_version": "0.1.0"
}
```

The run record MUST be written whether the adapter succeeds or fails; on
failure it records the reason and omits the freeze payload.

## CLI Shape

The adapter is exposed as a Python entrypoint and a subcommand pattern:

```
python -m gnosis_morph_bench.adapters.indus_phase4 \
  --feature-manifest <path> \
  --reference-frozen <path> \
  [--reference-key <key>] \
  [--include-route <name> --include-route <name>] \
  [--drop-item-with-nan] \
  [--output <path>] \
  [--run-record <path>] \
  [--manifest-name <string>]
```

The adapter's exit code is `0` on a clean emission, `2` on a contract
violation (missing required input, NaN in strict mode, frozen-SHA mismatch),
and `1` on an unexpected internal error. The adapter does not swallow
exceptions silently.

## Integration With Existing Package Surface

The v1 adapter does not edit `src/gnosis_morph_bench/schema.py`,
`src/gnosis_morph_bench/benchmark.py`,
`src/gnosis_morph_bench/stability.py`, or
`src/gnosis_morph_bench/cli.py`. It is added as a new module under
`src/gnosis_morph_bench/adapters/indus_phase4.py` (plus any tiny repo-local
utility module) in Phase 02. The synthetic smoke path remains untouched.

After a Phase 02 replay emits a neutral manifest via this adapter, the
existing smoke CLI can be pointed at it:

```
python -m gnosis_morph_bench <path-to-neutral-manifest> \
  --reference-key <governing-key> \
  --clusters <k> \
  --seed <seed>
```

That command is the same one that today runs the synthetic fixture. The
adapter's job is to make it runnable against admitted Indus inputs without
widening the repo boundary.

## Non-Claims

- This contract does not assert that any Phase 4 numeric value has been
  reproduced from repo custody. It specifies a translation layer only.
- This contract does not widen `BenchmarkManifest`. If a future adapter needs
  a new field, that extension goes through a new contract revision.
- This contract does not authorize vendoring heavy data into the staged
  repo.
- This contract does not cover the cuneiform benchmark family. A separate
  adapter contract is required before any cuneiform work begins.

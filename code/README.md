# Code README

## Scope

This file describes the code-facing surface of `gnosis-morph-bench`: package
interfaces, fixture contracts, adapter boundaries, and current technical
limits.

## Layout

| Path | Purpose |
|---|---|
| `src/gnosis_morph_bench/` | package root for schema, scoring, stability, and CLI helpers |
| `fixtures/tiny_benchmark_manifest.json` | synthetic manifest for install and smoke verification |
| `artifacts/smoke/` | default output directory for smoke reports |
| `docs/family/BENCHMARK_SCHEMA_CONTRACT.md` | human-readable schema contract |

## Build Or Run

```bash
python3 -m pip install -e .
gnosis-morph-bench-smoke fixtures/tiny_benchmark_manifest.json --output artifacts/smoke/smoke_report.json
```

## Interface Surface

| Interface | Path | Input | Output | Stability |
|---|---|---|---|---|
| Manifest loader | `src/gnosis_morph_bench/schema.py` | benchmark manifest JSON | typed manifest and reference freeze payload | `EXPERIMENTAL` |
| Route evaluator | `src/gnosis_morph_bench/benchmark.py` | manifest, route name, reference key, cluster config | NMI/null/silhouette metrics | `EXPERIMENTAL` |
| Stability helpers | `src/gnosis_morph_bench/stability.py` | manifest, route name, reference key, cluster config | Jaccard and replay payloads | `EXPERIMENTAL` |
| Smoke / replay CLI | `src/gnosis_morph_bench/cli.py` | fixture path and optional output path | JSON smoke or replay report | `EXPERIMENTAL` |
| Indus adapter CLI | `src/gnosis_morph_bench/adapters/indus_phase4.py` | admitted Phase 3c manifest and reference freeze | neutral `BenchmarkManifest` plus run record | `EXPERIMENTAL` |

## Artifact Outputs

| Artifact | Produced By | Path | Used By |
|---|---|---|---|
| Smoke report | `gnosis-morph-bench-smoke` | `artifacts/smoke/smoke_report.json` | install verification and audit path |
| Reference freeze payload | schema helpers | in-memory or file output | replay and adapter work |
| Replay record | `python -m gnosis_morph_bench replay` | `artifacts/replay/replay_record.json` | stability-battery audit |

## Known Boundaries

- The package is corpus-neutral by design; it does not vendor the full live
  Phase 4 or cuneiform source stack.
- The local fixture proves installability and interface coherence, not the full
  source-repo benchmark result.

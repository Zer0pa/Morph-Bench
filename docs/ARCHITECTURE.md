# Architecture

## Purpose

This file maps where technical truth lives in `gnosis-morph-bench` and where
cited source authority is still required.

## System Snapshot

| Layer | What Lives Here | Source Of Truth |
|---|---|---|
| Public docs | front door, governance, audit limits, migration boundary | `README.md`, `GOVERNANCE.md`, `PUBLIC_AUDIT_LIMITS.md`, `SOURCE_BOUNDARY.md`, `DATA_POLICY.md` |
| Code or runtime | schema loader, route evaluator, stability helpers, smoke CLI | `src/gnosis_morph_bench/` |
| Evidence artifacts | on-demand synthetic smoke report | `artifacts/smoke/` after local execution |
| Source authority outside repo custody | live Phase 4 methods findings and cuneiform benchmark manifest family | summarized in `docs/PROMOTION_READINESS.md` and `PUBLIC_AUDIT_LIMITS.md` until admitted artifacts land |

## Component Map

| Component | Responsibility | Inputs | Outputs | Notes |
|---|---|---|---|---|
| `schema.py` | load and validate the neutral benchmark manifest | JSON manifest | typed manifest objects and reference freeze payloads | current scope is synthetic and corpus-neutral |
| `benchmark.py` | route evaluation with NMI, null separation, and silhouette | manifest, route name, reference key, cluster config | per-route score payloads | repo-local methods surface |
| `stability.py` | five-mode stability battery | manifest, route name, reference key, cluster config | stability and replay payloads | deterministic replay plus perturbation modes |
| `cli.py` | runnable smoke command | fixture path and output path | JSON smoke report | minimum staged acceptance surface |

## Authority Artifacts

| Artifact | Path | Why It Matters | Public? |
|---|---|---|---|
| Sovereign repo PRD | `../PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` | Defines scope, gates, and anti-overclaim posture | `YES` |
| Promotion readiness | `../docs/PROMOTION_READINESS.md` | Names pass-now evidence and open gates | `YES` |
| Public audit limits | `../PUBLIC_AUDIT_LIMITS.md` | States what a clone cannot prove | `YES` |
| Smoke fixture | `../fixtures/tiny_benchmark_manifest.json` | Small runnable manifest for install verification | `YES` |

## Truth Surface Boundaries

- `README.md` owns the front door and claim boundary.
- `AUDITOR_PLAYBOOK.md` owns the quickest honest inspection path.
- `PUBLIC_AUDIT_LIMITS.md` says what a clone cannot prove.
- `code/README.md` owns the code-facing interface description.
- `docs/family/BENCHMARK_SCHEMA_CONTRACT.md` owns the manifest contract.

## Known Gaps

- The live Phase 4 rerun is blocked on admitted Phase 3c manifest custody.
- The cuneiform adapter contract is deferred by scope.

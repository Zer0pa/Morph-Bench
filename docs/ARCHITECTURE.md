# Architecture

## Purpose

This file maps where technical truth lives in the staged `gnosis-morph-bench`
repo and where cited source-repo authority is still required.

## System Snapshot

| Layer | What Lives Here | Source Of Truth |
|---|---|---|
| Public docs | front door, governance, audit limits, migration boundary | `README.md`, `GOVERNANCE.md`, `PUBLIC_AUDIT_LIMITS.md`, `SOURCE_BOUNDARY.md`, `DATA_POLICY.md` |
| Code or runtime | schema loader, route evaluator, stability helpers, smoke CLI | `src/gnosis_morph_bench/` |
| Evidence artifacts | on-demand synthetic smoke report | `artifacts/smoke/` after local execution |
| Source authority outside repo custody | live Phase 4 methods findings and cuneiform benchmark manifest family | cited paths in `../01_prd_and_authority/AUTHORITY_CHAIN.md` and `../04_evidence_manifest/` |

## Component Map

| Component | Responsibility | Inputs | Outputs | Notes |
|---|---|---|---|---|
| `schema.py` | load and validate the neutral benchmark manifest | JSON manifest | typed manifest objects and reference freeze payloads | current scope is synthetic and corpus-neutral |
| `benchmark.py` | route evaluation with NMI, null separation, and silhouette | manifest, route name, reference key, cluster config | per-route score payloads | derived from live route-selection logic, but simplified for the starter |
| `stability.py` | leave-out Jaccard and deterministic replay checks | manifest, route name, reference key, cluster config | stability and replay payloads | starter version is fixture-focused |
| `cli.py` | runnable smoke command | fixture path and output path | JSON smoke report | minimum staged acceptance surface |

## Authority Artifacts

| Artifact | Path | Why It Matters | Public? |
|---|---|---|---|
| Sovereign repo PRD | `../PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` | Defines scope, gates, and anti-overclaim posture | `YES` |
| Source authority chain | `../../01_prd_and_authority/AUTHORITY_CHAIN.md` | Names the control canon and live source-repo artifacts | `YES` inside the package |
| Evidence manifest | `../../04_evidence_manifest/evidence_manifest.json` | Freezes the cited authority bundle and hashes | `YES` inside the package |
| Smoke fixture | `../fixtures/tiny_benchmark_manifest.json` | Small runnable manifest for install verification | `YES` |

## Truth Surface Boundaries

- `README.md` owns the front door and claim boundary.
- `AUDITOR_PLAYBOOK.md` owns the quickest honest inspection path.
- `PUBLIC_AUDIT_LIMITS.md` says what a clone cannot prove.
- `code/README.md` owns the code-facing interface description.
- `docs/family/BENCHMARK_SCHEMA_CONTRACT.md` owns the manifest contract.

## Known Gaps

- The live Phase 4 and cuneiform helper logic is not fully ported into this
  repo yet.
- Source-repo scientific artifacts are cited, not rerun from local custody.

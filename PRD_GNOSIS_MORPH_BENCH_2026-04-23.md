# Gnosis Morph Bench - Sovereign PRD
Sector: Gnosis extraction program
Sector Folder: `workstreams/gnosis-morph-bench/05_repo_scaffold/`
Document Class: `SECTOR_SPECIFIC_PRD`
Version: `0.1.0`
Created: `2026-04-23`
Last Modified: `2026-04-23`
Status: `ACTIVE`
PRD Class: `IMMUTABLE_CHARTER + MUTABLE_EXPERIMENT_PROGRAM`
Source Corpus:
- `_control/research/WORKSTREAM_VALUE_RANKING.md`
- `_control/research/BUILD_VS_BORROW_CANON.md`
- `_control/verification/CORRECTED_WORKSTREAM_SET.md`
- `_control/verification/PROMOTION_PRIORITY_VERDICT.md`
- `scripts/indus/phase4_route_selection.py`
- `scripts/indus/phase4_stability.py`
- `scripts/indus/stability_tester.py`
- `scripts/cuneiform/annotated_sign_benchmark_common.py`
- `scripts/cuneiform/revert_phase2_common.py`
- `workspace/artifacts/indus/phase4/*`
- `workspace/artifacts/cuneiform/annotated_sign_benchmark_manifest.json`
Authority Metric:
- Stage gate now: staged repo installs standalone and the corpus-neutral smoke
  benchmark runs from repo custody.
- Promotion gate later: live route-selection, stability, replay, and
  reference-freeze logic rerun from repo custody without hidden monorepo
  dependencies.
Comparator State: `FROZEN_TO_2026-04-23_SOURCE_PACK`
PRD Hash: `UNFROZEN_STAGE_DRAFT`

## 1. Mission and Structural Thesis

### 1.1 One-Sentence Mission

Extract the neutral evaluation and replay logic behind the Gnosis
reference-bottleneck finding into a benchmark-first repo that does not inherit
domain claims.

### 1.2 Structural Thesis

Route comparison, permutation-null separation, stability/Jaccard checks,
deterministic replay, and reference-freeze helpers form one coherent methods
surface that can be parameterized across corpora. The owning repo should expose
metric contracts and replay discipline, while domain repos retain corpus
preprocessing and scientific verdicts.

### 1.3 Falsification Condition

If the live logic cannot be extracted without dragging in domain-specific image
preprocessing kernels, path-coupled monorepo state, or domain-specific verdict
language, this repo boundary is false and must shrink or be merged back into a
consumer repo.

### 1.4 Agent-Readable Brief

`gnosis-morph-bench` is the benchmark-first methods repo for Gnosis. It should
own route scoring, null metrics, stability, replay, and reference-freeze
helpers only. It must not pretend to own Indus or cuneiform scientific verdicts
or heavy corpora. The immediate gate is standalone install plus a synthetic
smoke benchmark. Public promotion stays blocked until the live source logic is
ported and rerun from repo custody.

### 1.5 Superordinate Goal

Turn the existing Phase 4 benchmark surface into a standalone, corpus-neutral
evaluation repo that downstream workstreams can trust and replay.

## 2. Scope and Boundaries

### 2.1 In-Scope Artifacts

| Artifact | Type | Lane | Target Path |
|---|---|---|---|
| Sovereign repo PRD | doc | methods | `05_repo_scaffold/PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` |
| Staged repo starter | repo | methods | `05_repo_scaffold/` |
| Package root | code | methods | `05_repo_scaffold/src/gnosis_morph_bench/` |
| Benchmark schema contract | doc | methods | `05_repo_scaffold/docs/family/BENCHMARK_SCHEMA_CONTRACT.md` |
| Handover docs | doc | methods | `06_handover/*.md` |

### 2.2 Out-of-Scope

- Indus or cuneiform papers as repo-owned truth
- heavy image corpora or raw benchmark bundles
- search demo packaging
- preprocessing kernels except what a tiny synthetic fixture requires

### 2.3 Source Corpus and Coverage Matrix

| Source ID | Path | Type | Required For | Status | Notes |
|---|---|---|---|---|---|
| SRC-01 | `_control/research/WORKSTREAM_VALUE_RANKING.md` | control | scope, priority | VERIFIED | Benchmark-first rank source |
| SRC-02 | `_control/research/BUILD_VS_BORROW_CANON.md` | control | boundary | VERIFIED | Confirms benchmark harness sovereignty |
| SRC-03 | `_control/verification/CORRECTED_WORKSTREAM_SET.md` | control | status | VERIFIED | Marks lane as lead public workstream |
| SRC-04 | `_control/verification/PROMOTION_PRIORITY_VERDICT.md` | control | promotion gate | VERIFIED | Public readiness still blocked |
| SRC-05 | `scripts/indus/phase4_route_selection.py` | code | extraction | VERIFIED | Primary route comparison source |
| SRC-06 | `scripts/indus/phase4_stability.py` | code | extraction | VERIFIED | Primary stability source |
| SRC-07 | `scripts/indus/stability_tester.py` | code | extraction | VERIFIED | Replay and perturbation helper source |
| SRC-08 | `scripts/cuneiform/annotated_sign_benchmark_common.py` | code | extraction | VERIFIED | Shared benchmark manifest helpers |
| SRC-09 | `scripts/cuneiform/revert_phase2_common.py` | code | extraction | VERIFIED | Cross-validation and null helpers |
| SRC-10 | `workspace/artifacts/indus/phase4/` | artifacts | authority | VERIFIED | Live Phase 4 authority bundle |
| SRC-11 | `workspace/artifacts/cuneiform/annotated_sign_benchmark_manifest.json` | artifact | schema mapping | VERIFIED | Heavy source; do not vendor casually |

### 2.4 Lane Boundaries

| Lane ID | Name | Folder Boundary | Integration Phase |
|---|---|---|---|
| L1 | Morph Bench methods surface | `workstreams/gnosis-morph-bench/` | immediate |
| L2 | Glyph kernels | `workstreams/gnosis-glyph-engine/` | only through declared dependency |
| L3 | Domain consumers | `workstreams/gnosis-indus/`, `workstreams/gnosis-cuneiform/` | after neutral interfaces are stable |

## 3. Architecture and Component Decisions

### 3.1 System Architecture

```text
fixture or admitted manifest
        |
        v
  schema loader / validator
        |
        +--> reference freeze helper
        |
        +--> route evaluator (NMI + null separation + silhouette)
        |
        +--> stability battery (leave-out, noise, replay)
        |
        v
  JSON report + doc surfaces
```

### 3.2 Component Selection

| Component | Choice | Rationale |
|---|---|---|
| Array math | `numpy` | Commodity substrate; do not rebuild |
| Clustering and metrics | `scikit-learn` | Commodity substrate for NMI, silhouette, agglomerative clustering |
| Manifest format | JSON fixture and contract docs | Smallest portable staged surface |
| Image preprocessing | excluded from current starter | Belongs to upstream kernels unless later proven necessary |

### 3.3 Dependency and License Constraints

- Do not vendor heavy or image-bearing corpora into the staged repo.
- Keep the staged repo private until canonical license text is supplied.
- Review-pack artifacts remain cited source authority, not staged repo payload.

## 4. Phase Plan and Execution Gates

| Phase | Name | Objective | Exit Gate | Status |
|---|---|---|---|---|
| P0 | Bootstrap | Build the staged scaffold and handover docs | Seven-subfolder pack and installable starter exist | PASS |
| P1 | Source Admission | Freeze live sources, ownership, and path rewrites | Source boundary and migration plan are explicit | IN_PROGRESS |
| P2 | Neutral Module Extraction | Port live benchmark helpers into package modules | No hidden monorepo imports remain | NOT_STARTED |
| P3 | Replay And Blind Clone | Rerun smoke and admitted live paths from repo custody | Install, smoke, and blind-clone pass | NOT_STARTED |
| P4 | Promotion Readiness | Close legal and data-release blockers | Private remote ready; public still optional | NOT_STARTED |

## 5. Current Acceptance Criteria

### Pass Now

- `05_repo_scaffold/` is self-contained enough to install and run the synthetic
  smoke path.
- the source boundary, data policy, and evidence chain are explicit
- domain overclaiming is removed from the repo front door

### Block Public Promotion

- full live source parity not yet rerun from repo custody
- canonical license text not yet supplied
- heavy data boundary not yet closed for public release

## 6. Deliverables

- staged repo starter with docs, package root, and smoke fixture
- handover docs promoted into repo root
- source inventory and evidence manifest for future extraction work

## 7. Anti-Narrative Rules

- Do not treat the synthetic smoke path as proof of the live Phase 4 result.
- Do not promote domain-specific verdicts as intrinsic repo truth.
- Do not widen the story because the staged repo now looks coherent.

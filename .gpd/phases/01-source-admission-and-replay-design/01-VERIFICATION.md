# Phase 01 Verification

- Status: `pass`
- Governing test: one real source-manifest replay target and adapter contract
  are explicit

## Pass Condition

- the chosen replay target is documented
- adapter inputs and exclusions are explicit
- no boundary violation is introduced

## Sources Read During This Plan

| Source | Path | Role |
|---|---|---|
| Sovereign PRD | `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` | repo boundary and phase gates |
| Source inventory | `../../../../02_source_inventory/SOURCE_INVENTORY.md` | admitted live source families and extraction risks |
| Path-rewrite ledger | `../../../../02_source_inventory/PATH_REWRITE_LEDGER.md` | forbidden patterns the adapter must replace |
| Evidence manifest | `../../../../04_evidence_manifest/EVIDENCE_MANIFEST.md` | authority artifacts available per candidate |
| Authority chain | `../../../../01_prd_and_authority/AUTHORITY_CHAIN.md` | measured Phase 4 values and custody boundary |
| Migration plan | `../../../../06_handover/MIGRATION_PLAN.md` | phase sequencing |
| Repo source boundary | `../../../../06_handover/SOURCE_BOUNDARY.md` | what this repo may own |
| Schema contract | `../../../docs/family/BENCHMARK_SCHEMA_CONTRACT.md` | neutral manifest surface |
| Schema code | `../../../src/gnosis_morph_bench/schema.py` | `BenchmarkManifest`, `load_manifest`, `extract_route_dataset`, `freeze_reference` |
| Benchmark code | `../../../src/gnosis_morph_bench/benchmark.py` | `EvaluationConfig`, `evaluate_route`, `evaluate_routes`, NMI with null |
| Stability code | `../../../src/gnosis_morph_bench/stability.py` | `deterministic_replay`, `leave_fraction_out` |
| CLI | `../../../src/gnosis_morph_bench/cli.py` | current smoke entrypoint and parameter surface |
| Data policy | `../../../DATA_POLICY.md` | heavy-data exclusions |
| Evidence JSON | `../../../../04_evidence_manifest/evidence_manifest.json` | SHA and size verification for candidate authority bundles |

The live scripts themselves (`scripts/indus/...`, `scripts/cuneiform/...`) are
not present on this machine; the comparison reasons from the source inventory
and path-rewrite ledger descriptions only.

## Deliverables Check

| Deliverable | Path | Status |
|---|---|---|
| First replay target decision | `../../../docs/family/FIRST_REPLAY_TARGET_DECISION.md` | written |
| Adapter contract v1 | `../../../docs/family/ADAPTER_CONTRACT_v1.md` | written |
| STATE advance | `.gpd/STATE.md` | updated |
| REQUIREMENTS progress marks | `.gpd/REQUIREMENTS.md` | updated |

## Adapter Contract Coverage

Required `BenchmarkManifest` fields (per `src/gnosis_morph_bench/schema.py`):

| Field | Covered in contract |
|---|---|
| `schema_version` pinned to `1` | yes — "Output Shape" fixes it to integer `1` |
| `manifest_name` non-empty string | yes — `--manifest-name` CLI flag, default `indus-phase4` |
| `items[]` non-empty with unique `item_id` | yes — adapter-run record tracks `items_in` / `items_out`, and unique-ID is enforced downstream by `load_manifest` |
| `items[].reference_labels` string-to-string | yes — "Carried And Dropped Label Columns" forbids non-string and pins to ICIT governing key |
| `items[].route_features` string-to-numeric-vector | yes — "Carried And Dropped Route-Feature Columns" casts to float and enforces consistent length |
| Consistent route-vector dimensions | yes — routes with inconsistent length are dropped with a warning, matching `extract_route_dataset` validation |
| At least one usable route | yes — governing route `pixel_full_concat_31d_single` must be carried when present |

Path-rewrite ledger patterns (per `../../../../02_source_inventory/PATH_REWRITE_LEDGER.md`):

| Forbidden live pattern | Adapter contract clause |
|---|---|
| `REPO = Path(__file__).resolve().parents[2]` | Forbidden Behaviors #1 |
| Hardcoded `workspace/artifacts/...` constants | Forbidden Behaviors #2 |
| `from stroke_native_encoding import ...` | Forbidden Behaviors #3 |
| `from phase3_common import ...` | Forbidden Behaviors #4 |
| `sys.path.insert(...)` | Forbidden Behaviors #5 |
| Direct writes into source artifact folders | Forbidden Behaviors #6 |

All six ledger patterns are explicitly named and forbidden by the contract.

## Numeric Targets Recoverable From The Chosen Authority Bundle

The Indus Phase 4 authority bundle (per `AUTHORITY_CHAIN.md` and the SHA-anchored
`evidence_manifest.json`) carries these values as source authority. They are
NOT yet repo-custody proof; they are the targets a Phase 02 replay will be
measured against after the v1 adapter lands.

| Measure | Live value | Source artifact |
|---|---|---|
| Governing route | `pixel_full_concat_31d_single` at `k=70` | `governing_route_selection.json` |
| Best agglomerative NMI vs ICIT Set | `0.5793` | `governing_route_selection.json` |
| Best agglomerative NMI vs ICIT Graph | `0.4312` | `governing_route_selection.json` |
| Sigma vs ICIT Set | `5.65` | `phase4_governing_verdict.md` |
| Leave-10%-out Jaccard | `0.4351` | `phase4_governing_verdict.md` |
| Noise injection Jaccard | `0.5005` | `phase4_governing_verdict.md` |
| Replay verdict | `3/3 identical` | `dt05_replay.json` |

The cuneiform bundle does not carry an equivalent numeric-target set — only a
heavy manifest and a lightweight summary — which is the primary reason the
first replay target is Phase 4 and not cuneiform.

## Boundary Check

- No live script content was copied into the staged repo.
- No heavy data was vendored.
- No Phase 4 numeric value was promoted as repo-custody proof.
- Existing synthetic smoke path and existing `src/gnosis_morph_bench/` code
  were not modified.
- The adapter is scoped to a new module under
  `src/gnosis_morph_bench/adapters/indus_phase4.py` for Phase 02; no such file
  was written in this plan.

## Open Follow-Ups For Phase 02

- Obtain read access to an admitted copy of the Phase 3c feature manifest
  family so the v1 adapter can actually run.
- Implement the v1 adapter and the tiny repo-local utility module it needs.
- Add adapter-level regression tests using a synthetic miniature of the Phase
  4 input shape.
- Draft a separate cuneiform adapter contract before any cuneiform code port
  begins.

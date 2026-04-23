# First Replay Target Decision

## Purpose

Freeze which admitted live source family becomes the first repo-custody replay
target for `gnosis-morph-bench`. This is a design decision only. No heavy data
is vendored, no live scripts are copied, and no Phase 4 numeric value is
promoted to repo-custody status by this document.

## Candidates

Two admitted live source families are in scope (see
`../../../02_source_inventory/SOURCE_INVENTORY.md` and
`../../../04_evidence_manifest/EVIDENCE_MANIFEST.md`):

- **A. Indus Phase 4** — `scripts/indus/phase4_route_selection.py` (362 lines),
  `scripts/indus/phase4_stability.py` (389 lines),
  `scripts/indus/stability_tester.py` (225 lines), with authority bundle under
  `workspace/artifacts/indus/phase4/`.
- **B. Cuneiform benchmark** —
  `scripts/cuneiform/annotated_sign_benchmark_common.py` (446 lines),
  `scripts/cuneiform/revert_phase2_common.py` (299 lines), with authority
  manifest at `workspace/artifacts/cuneiform/annotated_sign_benchmark_manifest.json`.

The live scripts themselves are not present in this staged repo. The comparison
below reasons from the source inventory, the path-rewrite ledger, and the
evidence manifest — not from script contents.

## Comparison Axes

| Axis | A — Indus Phase 4 | B — Cuneiform benchmark | Advantage |
|---|---|---|---|
| Path-coupling risk | `REPO = Path(__file__).resolve().parents[2]` + `workspace/artifacts/...` constants in two files | `sys.path.insert(...)` in `revert_phase2_common.py` plus `workspace/artifacts/...` constants | A |
| Domain leakage risk | `from stroke_native_encoding import ...` pulls glyph-kernel ownership; `from phase3_common import ...` is a monorepo runtime helper | Live helpers mix generic 1-NN / cross-validation math with cuneiform-specific manifest semantics and image-bearing item IDs | A |
| Heavy-data dependence | Needs `prebinarized_feature_manifest.json` (multi-megabyte; listed as a risk in `SOURCE_INVENTORY.md`) | Needs `annotated_sign_benchmark_manifest.json` at 9,280,260 bytes (SHA `e4d85abf...`); `DATA_POLICY.md` explicitly says do not vendor this | A |
| Schema alignment with `BenchmarkManifest` (`src/gnosis_morph_bench/schema.py`) | Routes × ICIT references × numeric feature vectors maps almost 1-to-1 onto `route_features` + `reference_labels`; `governing_route_selection.json` already tabulates route-by-reference NMI/Sigma | Centroid/1-NN classifier over sign families is a different evaluation contract; mapping into route/reference pairs requires reshaping "feature family" columns into pseudo-routes and collapsing classification scoring into clustering-vs-reference scoring | A |
| Helpers to neutralize before first replay | `REPO` depth surgery, `workspace/...` constants, `stroke_native_encoding` import, `phase3_common` import, artifact-folder writes | `sys.path.insert`, `workspace/...` constants, cuneiform manifest assumptions, artifact-folder writes | comparable — neither is a trivial port |
| Strength of existing authority bundle | Six artifacts in the evidence manifest: `governing_route_selection.json` (183 KB, route-by-route NMI/Sigma), `stability_report.json`, `dt05_replay.json` (3/3 identical), `icit_reference_frozen.json` (SHA-frozen reference), plus the two governing-verdict markdown files | Two artifacts: the 9.28 MB manifest and a lightweight summary markdown. No governing-verdict file. No replay evidence file. No frozen reference file. | A |

Interpretation: A wins on five of six axes. On the sixth ("helpers to
neutralize") the two candidates are comparable — the cuneiform family has fewer
lines of pure script code (745 vs 976) but more tangled domain-specific
manifest semantics.

## Choice

**First repo-custody replay target: A — the Indus Phase 4 source family.**

Rationale: the Phase 4 authority bundle is the only admitted source that
already gives a recoverable numeric target set for a first replay — a governing
route (`pixel_full_concat_31d_single` at `k=70`), route-by-route NMI and Sigma
values, a Jaccard stability value, a deterministic replay verdict (3/3
identical), and a SHA-frozen reference. That numeric target set is what the
adapter contract can be measured against during Phase 02 without leaning on
heavy data and without overclaiming. The cuneiform manifest family is heavier,
has no matching replay evidence bundle, and its native evaluation shape
(centroid / 1-NN classifier) is further from the neutral `BenchmarkManifest`
contract. Those values remain source authority only; this document does not
promote them to repo-custody proof.

## Explicit Exclusions For The First Adapter

The first adapter will NOT handle any of the following. These are carried
forward as Phase 02 or later work items.

- **Cuneiform benchmark manifest family.** Out of scope for the first adapter.
  A later pass can reuse only neutral matrix/classification helpers, per the
  existing source-boundary discipline in
  `../../../02_source_inventory/SOURCE_INVENTORY.md`.
- **Glyph-kernel preprocessing.** No adapter will import
  `stroke_native_encoding`, `stroke_zpe_pipeline`, or any other glyph/image
  kernel — those belong to `gnosis-glyph-engine` or a domain repo.
- **`phase3_common` runtime helpers.** Any JSON, hashing, or timestamp helpers
  the adapter needs will be implemented as a small, repo-local utility module
  under `gnosis_morph_bench`.
- **Heavy-data vendoring.** The adapter will not copy
  `prebinarized_feature_manifest.json`, raw binarized images, or any
  `workspace/artifacts/...` payload into the staged repo. Adapter inputs are
  declared paths / environment variables only.
- **Domain verdicts.** The adapter will not emit ICIT-specific verdict prose,
  decipherment claims, or anything that looks like a scientific verdict. It
  emits the neutral `BenchmarkManifest` JSON plus an adapter-run record.
- **Runtime writes into source-repo artifact folders.** Output paths default to
  repo-local `artifacts/` only; the adapter forbids writes outside the staged
  repo.
- **Full cross-phase stability battery.** The first adapter only produces the
  neutral manifest and the minimum fields needed to run `evaluate_routes`,
  `deterministic_replay`, and `leave_fraction_out` from
  `src/gnosis_morph_bench/`. The fuller stability surface (noise injection,
  k-sensitivity sweep, seed battery) is a follow-on adapter plan.
- **Public promotion of any recovered numeric target.** A Phase 02 replay may
  reproduce Phase 4 numbers from repo custody; promoting those numbers into
  public-facing docs is blocked until the legal and data-release gates close.

## Non-Claims

- This document does not assert that the live Phase 4 values have been
  reproduced from repo custody. They remain source authority only.
- This document does not commit the staged repo to vendor any Phase 4 data.
- This document does not rule out a future cuneiform adapter; it only defers
  that work behind the Phase 4 adapter.

## Downstream References

- The concrete adapter contract is in `ADAPTER_CONTRACT_v1.md`.
- The Phase 01 verification record is in
  `../../.gpd/phases/01-source-admission-and-replay-design/01-01-VERIFICATION.md`.

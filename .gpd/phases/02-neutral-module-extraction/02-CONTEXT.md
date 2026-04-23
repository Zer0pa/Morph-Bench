# Phase 02 Context: Neutral Module Extraction

## Phase goal

Port live route-selection, stability, and replay helpers into
`src/gnosis_morph_bench/` such that:

1. Repo-local modules replace hidden monorepo imports.
2. Live-source rerun artifacts can exist under repo custody (the adapter
   surface is in place, even though the actual live rerun lives in Phase 03
   and requires admitted Phase 3c feature-manifest access that is out of
   scope here).
3. Domain claims remain outside the repo boundary.

## Starting reality (must read before planning)

- The package already exposes working, neutral implementations of the
  core math:
  - `src/gnosis_morph_bench/benchmark.py` — `evaluate_route`,
    `evaluate_routes`, `nmi_with_null` (permutation null + sigma).
  - `src/gnosis_morph_bench/stability.py` — `deterministic_replay`,
    `leave_fraction_out`, `pairwise_jaccard`.
  - `src/gnosis_morph_bench/schema.py` — `load_manifest`,
    `extract_route_dataset`, `freeze_reference`.
  - `src/gnosis_morph_bench/cli.py` — runs the full pipeline on the
    synthetic fixture and emits `smoke_report.json`.
- Phase 02 is therefore not "write the math from scratch". It is:
  (a) build the `indus_phase4` adapter that lands admitted inputs onto the
  neutral manifest shape, (b) fill the Phase-4-style stability battery
  modes that are still missing, (c) retarget the CLI so both the synthetic
  smoke path and the neutral manifest emitted by the adapter run through a
  single entrypoint, (d) harden the package against the six forbidden
  monorepo-coupling patterns.

## Frozen contract

- `docs/family/ADAPTER_CONTRACT_v1.md` is the binding specification for
  plan 02-01. Every "MUST" clause in that contract must map to at least
  one test assertion or lint check inside this phase.
- `02_source_inventory/PATH_REWRITE_LEDGER.md` enumerates six forbidden
  patterns. A forbidden-pattern lint test must cover all six and fail on
  any hit inside `src/gnosis_morph_bench/` (the adapter module included).

## Stability-battery gap (must not be ignored in 02-02)

The current `stability.py` implements only `deterministic_replay`,
`leave_fraction_out`, and `pairwise_jaccard`. The Phase 4 stability
battery additionally requires:

- **Noise injection** on feature vectors: Jaccard between baseline
  clustering and clustering on feature-vectors perturbed by Gaussian
  noise with configurable sigma.
- **k-sensitivity**: Jaccard between baseline clustering at the
  governing `n_clusters` and clusterings at neighboring values
  (e.g., `k-1`, `k+1`).
- **Seed-variance**: Jaccard across multiple clustering seeds, which is
  orthogonal to `deterministic_replay` (deterministic replay measures
  bit-for-bit reproducibility at a fixed seed; seed variance measures
  stability across seeds).

Plan 02-02 owns these three additions.

## Constraints and non-claims

- **No live code is available on this machine or on the RunPod pod.** The
  live scripts (`phase4_route_selection.py`, `phase4_stability.py`,
  `stability_tester.py`) are documented through the adapter contract and
  `02_source_inventory/SOURCE_INVENTORY.md` but cannot be opened directly.
  All work in Phase 02 must be derivable from the adapter contract and
  from the neutral schema dataclasses.
- **No admitted Phase 3c feature manifest is available yet.** All tests
  in this phase must use synthetic fixtures that simulate the
  Phase-4-style manifest shape. The real rerun against the admitted
  Phase 3c feature manifest (recovery of NMI 0.5793, Sigma 5.65, Jaccard
  0.4351, Replay 3/3) is a Phase 03 concern gated on admitted access.
- **Phase 02 does not promote any Phase 4 numeric value to repo-custody
  proof.** The phase builds the substrate; it does not run the real
  replay.
- **Phase 02 does not touch the cuneiform family.** A separate adapter
  contract is required before any cuneiform work begins.

## Domain-boundary reminders

- The adapter carries the ICIT Set governing reference key as a label
  column. It does not carry any authorial verdict text, URLs, or
  image-derived side channels.
- The adapter never re-binarizes images or imports glyph-kernel modules.
  It consumes already-computed feature vectors from the upstream
  manifest.
- All adapter outputs land under the staged repo (`artifacts/adapters/`
  by default), never under `workspace/artifacts/...`.

## Chaining

Plan 02-01 (adapter) must land before plan 02-02 (stability modes + CLI
refactor), because 02-02's Phase-4-style CLI flow may call
`evaluate_routes` against an adapter-emitted neutral manifest and
therefore depends on the adapter surface being in place.

## Decisions carried into this phase

- [Phase 00]: keep heavy corpora outside the staged repo.
- [Phase 00]: treat live Phase 4 metrics as source authority until rerun
  under repo custody.
- [Phase 01]: first repo-custody replay target is Indus Phase 4.
- [Phase 01]: v1 adapter is design only in Phase 01; Phase 02 implements
  it.

## Pending todos consumed by this phase

- Implement the Phase 02 v1 adapter under
  `src/gnosis_morph_bench/adapters/indus_phase4.py`.
- Port live route-selection math onto the neutral manifest path produced
  by the v1 adapter (no live scripts available; port by contract).
- Port live stability and replay helpers (fill noise, k-sensitivity,
  seed-variance gaps).

## Pending todos explicitly deferred

- Obtain admitted access to the Phase 3c feature manifest for a real
  Phase 4 rerun under repo custody → Phase 03.
- Draft a cuneiform adapter contract → later phase.
- Run blind-clone verification → Phase 03.

## Open questions that do NOT block Phase 02

- Whether a second reference key (ICIT Graph) is required before the
  first real replay. v1 adapter is single-governing-key by default; a
  future `--extra-reference-key` flag was deferred explicitly in the
  contract and is not re-opened in Phase 02.
- Which cuneiform helper subset eventually belongs in this repo. Not a
  Phase 02 concern.

## Open questions that DO need owner attention before Phase 03

- Access path for the admitted Phase 3c feature manifest (authority,
  custody, hashes). This unblocks the real replay but is not blocking
  for Phase 02 delivery.

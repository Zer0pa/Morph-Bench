# Research State

## Project Reference

See: `.gpd/PROJECT.md`

**Core research or build question:** Can the benchmark and replay logic behind
the live Phase 4 finding be extracted into a standalone methods repo that
installs and runs from repo custody while keeping domain verdicts outside the
boundary?
**Current focus:** Phase 01 complete at design tier; begin the Phase 02 adapter
implementation once an admitted copy of the Phase 3c feature manifest is
accessible from repo custody.

## Current Position

**Current Phase:** 02
**Current Phase Name:** Neutral Module Extraction
**Total Phases:** `4`
**Current Plan:** 02-02
**Total Plans In Phase:** 2
**Status:** Plan 02-01 complete; 02-02 ready to execute
**Status Detail:** Plan 02-01 landed the Indus Phase 4 v1 adapter at
`src/gnosis_morph_bench/adapters/indus_phase4.py`, the `_utils.py`
helper module, three synthetic Phase-4-shaped fixtures under
`tests/fixtures/`, and a 16-case pytest suite covering CLI surface,
round-trip into `load_manifest`/`evaluate_route`, freeze parity and
mismatch (exit code 2), NaN handling (strict + drop), label-surface
carry/drop, forbidden-pattern lint (with positive control), and
ADAPTER_CONTRACT_v1 MUST-clause coverage. Zero unsatisfied contract
clauses; zero forbidden-pattern hits under `src/`. The console
entrypoint `gnosis-morph-bench-adapter-indus-phase4` is wired. Plan
02-02 extends the stability battery with noise injection,
k-sensitivity, and seed variance, adds `replay.py` emitting a neutral
`ReplayRecord`, refactors the CLI into `smoke` / `replay` subcommands,
and publishes `STABILITY_BATTERY_v1.md`. No live Phase 3c data is
required; 02-02 continues to use synthetic fixtures.
**Last Activity:** 2026-04-24
**Last Activity Description:** Plan 02-01 executed end-to-end; six
atomic commits (ccbee89, e61cb0c, 7a7457d, 6abe835, 9664e5d, 9a5ad6b);
pytest 16/16 pass; SUMMARY.md written.

**Execution Doctrine:** no interim reporting unless there is a real blocker
that cannot be removed locally or on admitted surfaces.

**Progress:** [######----] `55%`

## Active Calculations

- Synthetic smoke benchmark on `fixtures/tiny_benchmark_manifest.json`
- Indus Phase 4 v1 adapter implemented at
  `src/gnosis_morph_bench/adapters/indus_phase4.py`; exercised on the
  three synthetic Phase-4-shaped fixtures under `tests/fixtures/`.
- Plan 02-02 in queue: stability-battery modes (noise, k-sensitivity,
  seed variance) + `replay.py` + CLI refactor + STABILITY_BATTERY_v1.md.

## Intermediate Results

- The staged repo is installable and exposes a corpus-neutral starter contract.
- Source-repo authority is cited cleanly without being misrepresented as
  repo-custody proof.
- First repo-custody replay target is frozen to the Indus Phase 4 source
  family. Rationale recorded in
  `docs/family/FIRST_REPLAY_TARGET_DECISION.md` across six extraction-risk
  axes (path coupling, domain leakage, heavy-data dependence, schema
  alignment, helpers to neutralize, authority-bundle strength).
- v1 adapter contract names every path-rewrite-ledger forbidden pattern and
  pins output conformance to `BenchmarkManifest` in
  `src/gnosis_morph_bench/schema.py`.

## Open Questions

- Can an admitted copy of the Phase 3c feature manifest be made accessible to
  this staged repo without vendoring heavy data, so the v1 adapter can run?
- Does the v1 adapter need a second reference key (ICIT Graph) before Phase
  02 begins, or is the governing ICIT Set key sufficient for the first
  replay pass?
- Which cuneiform helper subset will belong in this repo versus the consuming
  domain repo once a separate cuneiform adapter contract is drafted?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| Bootstrap initialization | current session | 1 | staged repo + workstream docs |

## Accumulated Context

### Decisions

- [Phase 00]: keep heavy corpora outside the staged repo.
- [Phase 00]: treat live Phase 4 metrics as source authority until rerun here.
- [Phase 00]: use a synthetic smoke fixture as the minimum standalone install
  gate.
- [Phase 01]: first repo-custody replay target is the Indus Phase 4 source
  family; rationale tied to six extraction-risk axes.
- [Phase 01]: v1 adapter is design only — no live code ported, no heavy data
  vendored in this plan.

### Pending Todos

- Obtain admitted access to the Phase 3c feature manifest for repo-custody
  adapter runs (Phase 03).
- Port live route-selection math from `scripts/indus/phase4_route_selection.py`
  onto the neutral manifest path produced by the v1 adapter (Phase 03;
  requires admitted data).
- Port live stability and replay helpers from
  `scripts/indus/phase4_stability.py` and `scripts/indus/stability_tester.py`
  — Plan 02-02 covers the repo-local pieces (noise, k-sensitivity,
  seed variance, `replay.py`).
- Draft a separate cuneiform adapter contract before any cuneiform work
  begins.
- Run blind-clone verification (Phase 03).

### Blockers/Concerns

- Final license text is still owner-deferred.
- Real-source replay is still pending; Phase 02 is blocked on admitted
  Phase 3c feature manifest access.

## Session Continuity

**Last session:** `2026-04-24T00:00:00Z`
**Stopped at:** Plan 02-01 complete (adapter + utils + fixtures + 16
pytest cases green); ready to execute Plan 02-02.
**Resume file:** `.gpd/phases/02-neutral-module-extraction/02-02-PLAN.md`.

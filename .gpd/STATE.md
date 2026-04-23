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
**Current Plan:** 02-01
**Total Plans In Phase:** 2
**Status:** Planned, ready to execute
**Status Detail:** Phase 02 planning complete. Two plans drafted:
02-01 implements the Indus Phase 4 v1 adapter, utils module, synthetic
Phase-4-like fixtures, forbidden-pattern lint, and ADAPTER_CONTRACT_v1
MUST-clause coverage test. 02-02 extends the stability battery with
noise injection, k-sensitivity, and seed variance, adds `replay.py`
emitting a neutral `ReplayRecord`, refactors the CLI into `smoke` /
`replay` subcommands, and publishes `STABILITY_BATTERY_v1.md`. No live
Phase 3c data is required; all tests use synthetic fixtures.
**Last Activity:** 2026-04-24
**Last Activity Description:** Phase 02 plans 02-01 and 02-02 drafted;
`.gpd/phases/02-neutral-module-extraction/02-CONTEXT.md` published.

**Execution Doctrine:** no interim reporting unless there is a real blocker
that cannot be removed locally or on admitted surfaces.

**Progress:** [####------] `40%`

## Active Calculations

- Synthetic smoke benchmark on `fixtures/tiny_benchmark_manifest.json`
- Indus Phase 4 adapter contract drafted at
  `docs/family/ADAPTER_CONTRACT_v1.md`; implementation deferred to Phase 02

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
  adapter runs.
- Implement the Phase 02 v1 adapter under
  `src/gnosis_morph_bench/adapters/indus_phase4.py`.
- Port live route-selection math from `scripts/indus/phase4_route_selection.py`
  onto the neutral manifest path produced by the v1 adapter.
- Port live stability and replay helpers from
  `scripts/indus/phase4_stability.py` and `scripts/indus/stability_tester.py`.
- Draft a separate cuneiform adapter contract before any cuneiform work
  begins.
- Run blind-clone verification.

### Blockers/Concerns

- Final license text is still owner-deferred.
- Real-source replay is still pending; Phase 02 is blocked on admitted
  Phase 3c feature manifest access.

## Session Continuity

**Last session:** `2026-04-24T00:00:00Z`
**Stopped at:** Phase 01 plan 01-01 complete; replay target and v1 adapter
contract frozen.
**Resume file:** `.gpd/phases/02-neutral-module-extraction/` (to be created
when Phase 02 starts).

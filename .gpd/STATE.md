# Research State

## Project Reference

See: `.gpd/PROJECT.md`

**Core research or build question:** Can the benchmark and replay logic behind
the live Phase 4 finding be extracted into a standalone methods repo that
installs and runs from repo custody while keeping domain verdicts outside the
boundary?
**Current focus:** Freeze the first real source-manifest replay target after the
bootstrap pass.

## Current Position

**Current Phase:** `01`
**Current Phase Name:** Source Admission And Replay Design
**Total Phases:** `4`
**Current Plan:** `1`
**Total Plans In Phase:** `1`
**Status:** `IN_PROGRESS`
**Status Detail:** bootstrap is complete; the repo now needs its first real
source-manifest replay target and adapter design.
**Last Activity:** `2026-04-23`
**Last Activity Description:** instantiated the migration-ready workstream pack,
specialized the repo docs, and added the standalone smoke path

**Execution Doctrine:** no interim reporting unless there is a real blocker
that cannot be removed locally or on admitted surfaces.

**Progress:** [###-------] `30%`

## Active Calculations

- Synthetic smoke benchmark on `fixtures/tiny_benchmark_manifest.json`
- Source-boundary freeze for the live Phase 4 and cuneiform helper families

## Intermediate Results

- The staged repo is installable and exposes a corpus-neutral starter contract.
- Source-repo authority is cited cleanly without being misrepresented as
  repo-custody proof.

## Open Questions

- Which real source-manifest family should become the first repo-custody replay
  gate?
- Which cuneiform helper subset belongs in this repo versus the consuming
  domain repo?

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

### Pending Todos

- Select the first real replay target.
- Port live route-selection helpers.
- Port live stability and replay helpers.
- Run blind-clone verification.

### Blockers/Concerns

- Final license text is still owner-deferred.
- Real-source replay is still pending.

## Session Continuity

**Last session:** `2026-04-23T00:00:00Z`
**Stopped at:** staged repo created, awaiting first real replay-target design
**Resume file:** `.gpd/phases/01-source-admission-and-replay-design/01-01-PLAN.md`

# Research State

## Project Reference

See: `.gpd/PROJECT.md`

**Core research or build question:** Can the benchmark and replay logic behind
the live Phase 4 finding be extracted into a standalone methods repo that
installs and runs from repo custody while keeping domain verdicts outside the
boundary?

**Current focus:** repo-orchestrator greenlight readiness for Morph-Bench as the
benchmark/replay framework and first public-planning candidate. The current wave
aligns the repo front door, promotion-readiness surfaces, data/license boundary,
and CI hygiene checks with the canonical repo-docs playbook. Live Indus replay,
heavy-data admission, cuneiform coverage, and Ops-Gates consumption remain named
gates rather than hidden claims.

## Current Position

**Current Phase:** 03
**Current Phase Name:** Greenlight readiness and promotion boundary
**Total Phases:** `4`
**Current Plan:** greenlight hygiene wave
**Total Plans In Phase:** `1`
**Status:** STAGED
**Status Detail:** Package, smoke, replay, adapter-contract, forbidden-pattern,
license, and historical blind-clone evidence are present. Current public-facing
surfaces now separate Apache-2.0 code / CC-BY-4.0 docs from data, artifacts,
image-bearing payloads, endpoint logs, and private HF custody. The repo is ready
for repo-orchestrator review after branch verification passes, but not for
claims that require admitted live Phase 3c manifest custody.
**Last Activity:** 2026-04-28
**Last Activity Description:** Front-door and operational-state refresh for
repo-orchestrator greenlight; Ops-Gates adoption marked deferred until
`Gnosis-Ops-Gates` is green on its own CI and exposes a Morph-compatible
profile.

**Execution Doctrine:** no interim reporting unless there is a real blocker
that cannot be removed locally or on admitted surfaces.

**Progress:** [########--] `80%`

## Active Calculations

- Verify this branch with repo hygiene scan, stale-language scan, `pytest -q`,
  and synthetic smoke output written outside the repo.
- Keep package/test/fixture logic unchanged in this wave unless verification
  falsifies the greenlight claim.
- Treat Ops-Gates as deferred integration, not a silent dependency, until its
  canonical self-CI is green and a pinned Morph-compatible invocation exists.

## Intermediate Results

- The repo is installable and exposes a corpus-neutral benchmark/replay
  contract.
- Source-repo authority is cited cleanly without being represented as
  Morph-Bench repo-custody proof.
- The Indus Phase 4 source family remains the first repo-custody replay target.
- The v1 adapter contract names forbidden path-coupling patterns and pins
  output conformance to `BenchmarkManifest`.
- Code/docs license posture is now Apache-2.0 and CC-BY-4.0; data/artifact
  release remains separately gated.

## Open Questions

- Can an admitted copy of the Phase 3c feature manifest be made accessible to
  this repo without vendoring heavy or image-bearing data?
- What explicit policy will govern public admission of private HF artifacts,
  endpoint logs, corpora, and image-bearing payloads?
- Which cuneiform helper subset belongs in this repo versus the consuming
  domain repo once a second-family adapter is authorized?
- What exact Ops-Gates profile should Morph consume once Ops-Gates is green?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| Greenlight readiness wave | 2026-04-28 | 1 | front door, operational docs, CI hygiene, `.gpd` state |

## Accumulated Context

### Decisions

- [Phase 00]: keep heavy corpora outside the staged repo.
- [Phase 00]: treat live Phase 4 metrics as source authority until rerun here.
- [Phase 00]: use a synthetic smoke fixture as the minimum standalone install
  gate.
- [Phase 01]: first repo-custody replay target is the Indus Phase 4 source
  family; rationale tied to six extraction-risk axes.
- [Phase 01]: v1 adapter began as design-first and now has package-facing
  coverage without vendoring heavy data.
- [Greenlight 2026-04-28]: license posture is settled for code/docs; do not use
  license closure to promote data, artifact, or live replay claims.
- [Greenlight 2026-04-28]: defer Ops-Gates consumption until the gate repo is
  self-green and provides a stable Morph invocation.

### Pending Todos

- Run and record branch verification: no package/test/fixture drift, hygiene
  scan, stale-current-surface scan, `pytest -q`, and smoke to `/tmp`.
- Obtain admitted access to the Phase 3c feature manifest for repo-custody live
  replay.
- Write the heavy-data/image-bearing release policy before any such payload
  enters a public repo or website surface.
- Draft a cuneiform adapter contract only after explicit authorization or after
  the Indus live replay gate closes.
- Adopt Ops-Gates in CI only after `Gnosis-Ops-Gates` self-CI is green and a
  pinned Morph-compatible profile is available.

### Blockers/Concerns

- Real-source replay is still pending on admitted Phase 3c feature manifest
  custody.
- Public rights for corpora, image-bearing payloads, endpoint logs, and private
  HF artifacts remain blocked on separate owner policy.
- Ops-Gates cannot be load-bearing here while its own canonical CI is red.

## Session Continuity

**Last session:** `2026-04-28T00:00:00+02:00`
**Stopped at:** greenlight readiness branch under verification.
**Resume file:** `docs/PROMOTION_READINESS.md`.

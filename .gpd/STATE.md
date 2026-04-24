# Research State

## Project Reference

See: `.gpd/PROJECT.md`

**Core research or build question:** Can the benchmark and replay logic behind
the live Phase 4 finding be extracted into a standalone methods repo that
installs and runs from repo custody while keeping domain verdicts outside the
boundary?
**Current focus:** Phase 03 is planned. Plan 03-01 (blind-clone verification)
is the next executable unit; Plan 03-02 (promotion-readiness documentation)
lands behind it. The admitted Phase 3c live replay is NOT in scope for Phase
03 — it is carried forward as a named unblock item in
`docs/PROMOTION_READINESS.md` under the blockers-are-tasks doctrine.

## Current Position

**Current Phase:** 03
**Current Phase Name:** —
**Total Phases:** `4`
**Current Plan:** —
**Total Plans In Phase:** —
**Status:** Milestone complete
**Status Detail:** Phase 03 planned at
`.gpd/phases/03-blind-clone-and-promotion-review/` with three artifacts:
`03-CONTEXT.md` (phase framing, environment choice rationale, hard
constraints), `03-01-PLAN.md` (blind-clone verification — primary macOS
clone into `/tmp/blind-clone-<epoch>/` on Python >= 3.10; secondary
RunPod clone on pod `<RUNPOD_POD_ID>` that honestly reports the Python
3.8.10 floor gap; 2 tasks; 6 contract claims; 9 acceptance tests; only
carry-back is `artifacts/blind_clone/03-01_*`), and `03-02-PLAN.md`
(promotion-readiness documentation — authors `docs/PROMOTION_READINESS.md`
with 11 sections including the three mandatory external blockers
(Phase 3c manifest, canonical license, heavy-data release policy) each
carrying Owner / Unblock artifact / Unblock condition markers; updates
`TODO.md` with cross-references; 2 tasks; 6 contract claims; 7
acceptance tests; no fabricated LICENSE; no promoted live Phase 4
numeric values). Hard constraints honored: no live Phase 3c data
required, no license fabricated, live Phase 4 numbers stay as
source-authority citations.
**Last Activity:** 2026-04-24
**Last Activity Description:** Phase 03 complete
03-01-PLAN.md, 03-02-PLAN.md created. ROADMAP and state.json updated
to reflect the two-plan shape. Ready to execute Plan 03-01.

**Execution Doctrine:** no interim reporting unless there is a real blocker
that cannot be removed locally or on admitted surfaces.

**Progress:** [######----] `65%`

## Active Calculations

- Plan 03-01 queued: blind-clone verification. Primary run: macOS
  `/tmp/blind-clone-<epoch>/` with `python3.11 -m venv`, `pip install -e .`,
  `python -m gnosis_morph_bench smoke` byte-parity vs committed
  `artifacts/smoke/smoke_report.json`, `python -m gnosis_morph_bench replay`
  shape check, `pytest -q tests/` == 32 passed, external forbidden-pattern
  grep under `src/gnosis_morph_bench/`. Secondary run: RunPod pod
  `<RUNPOD_POD_ID>` with reported Python 3.8.10 floor gap and an explicit
  install-Python-3.11 attempt documented in the transcript.
- Plan 03-02 queued: author `docs/PROMOTION_READINESS.md` anchored to the
  03-01 transcript disposition; update `TODO.md` cross-references; no
  fabricated LICENSE; three mandatory named blockers (Phase 3c manifest,
  canonical license, heavy-data release policy) each with Owner + Unblock
  artifact + Unblock condition markers.

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

- Run Plan 03-01: blind-clone verification (macOS primary, RunPod secondary).
- Run Plan 03-02: author `docs/PROMOTION_READINESS.md` and update `TODO.md`
  cross-references.
- Obtain admitted access to the Phase 3c feature manifest for a future
  repo-custody live replay (carried as named unblock item in
  `docs/PROMOTION_READINESS.md` under the blockers-are-tasks doctrine;
  NOT executable inside Phase 03).
- Owner decision on canonical license text (OWNER_DEFERRED; carried as
  named unblock item; Plan 03-02 does NOT fabricate a LICENSE).
- Owner decision on heavy-data release policy for image-bearing assets
  (carried as named unblock item).
- Draft a separate cuneiform adapter contract before any cuneiform work
  begins (deferred by scope; not a blocker).

### Blockers/Concerns

- Final license text is still owner-deferred.
- Real-source replay is still pending; Phase 02 is blocked on admitted
  Phase 3c feature manifest access.

## Session Continuity

**Last session:** `2026-04-24T00:00:00Z`
**Stopped at:** Phase 03 planned with two plans (03-01 blind-clone
verification, 03-02 promotion-readiness documentation). ROADMAP, STATE,
and state.json updated.
**Resume file:** `.gpd/phases/03-blind-clone-and-promotion-review/03-01-PLAN.md`.

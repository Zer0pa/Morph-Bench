# Roadmap: gnosis-morph-bench

## Overview

Phase 00 bootstrapped the staged repo and smoke package. Phase 01 now freezes
the first real source-manifest replay target and adapter design. Phase 02 ports
the live source logic into repo-local modules. Phase 03 runs blind-clone and
promotion review gates.

## Phases

- [x] **Phase 00: Bootstrap** - Build the staged repo, docs, and synthetic smoke path.
- [ ] **Phase 01: Source Admission And Replay Design** - Freeze the first real
      replay target and adapter contract.
- [ ] **Phase 02: Neutral Module Extraction** - Port live route, stability, and
      replay helpers into repo-local modules.
- [ ] **Phase 03: Blind Clone And Promotion Review** - Verify clean-clone
      install and review public-blocker status.

## Phase Details

### Phase 00: Bootstrap

**Goal:** create a truthful staged repo with docs, package root, and a runnable
synthetic smoke path.
**Success criteria:**

1. repo-local truth surfaces exist and agree
2. the package installs
3. the smoke path runs

### Phase 01: Source Admission And Replay Design

**Goal:** choose the first admitted real-source replay target and design the
adapter without widening scope.
**Success criteria:**

1. one real source-manifest family is selected
2. adapter inputs, outputs, and exclusions are explicit
3. no hidden dependency on glyph kernels or domain papers is added

Plans:

- [ ] **01-01**: Freeze the first real replay target

### Phase 02: Neutral Module Extraction

**Goal:** port live route-selection, stability, and replay helpers into
`src/gnosis_morph_bench/`.
**Success criteria:**

1. repo-local modules replace hidden monorepo imports
2. live-source rerun artifacts exist under repo custody
3. domain claims remain outside the repo boundary

**Plans:** 2 plans

Plans:

- [ ] **02-01**: Indus Phase 4 v1 adapter (`src/gnosis_morph_bench/adapters/indus_phase4.py`) with forbidden-pattern lint and MUST-clause coverage against `docs/family/ADAPTER_CONTRACT_v1.md`.
- [ ] **02-02**: Complete Phase-4-style stability battery (noise injection, k-sensitivity, seed variance) + `replay.py` + two-subcommand CLI (`smoke` / `replay`) + `STABILITY_BATTERY_v1.md`.

Plan chain: 02-01 lands first (adapter surface), then 02-02 (stability + replay CLI that consumes adapter-emitted manifests).

Phase 02 does NOT run the admitted Phase 3c replay — that is a Phase 03 concern.

### Phase 03: Blind Clone And Promotion Review

**Goal:** prove the repo runs from a clean clone and review public blockers.
**Success criteria:**

1. clean temp-clone install and smoke pass
2. release blockers are explicit
3. legal and data boundaries remain visible

**Plans:** 2 plans

Plans:

- [ ] **03-01**: Blind-clone verification — primary macOS clone into
      `/tmp/blind-clone-<epoch>/` with fresh venv on Python >= 3.10; secondary
      RunPod clone on pod `7k3riasglemecu` that reports the Python 3.8.10
      floor gap honestly. Emits `artifacts/blind_clone/03-01_transcript.md`
      and five carry-back evidence files. Covers the executable subset of
      PRD-P3 "Replay And Blind Clone"; the admitted live Phase 3c replay is
      out of scope and is carried forward as a named unblock item.
- [ ] **03-02**: Promotion-readiness documentation — authors
      `docs/PROMOTION_READINESS.md` with Pass Now / Blocked On External
      Dependencies / Deferred By Scope / License Posture / Data Release
      Posture / Trust Boundary sections. Updates `TODO.md` with
      cross-references; no fabricated LICENSE. Covers the documentation
      subset of PRD-P4 "Promotion Readiness".

Plan chain: 03-01 lands first (its transcript is the anchor 03-02 cites),
then 03-02. 03-02 may still land if 03-01 is PARTIAL, in which case
PROMOTION_READINESS reflects PARTIAL honestly.

Phase 03 does NOT run the admitted Phase 3c live replay — that is an
external-data blocker carried as a documented unblock item in
`docs/PROMOTION_READINESS.md`.

## Progress

| Phase | Plans Complete | Status | Completed |
| ----- | -------------- | ------ | --------- |
| 00. Bootstrap | 1/1 | Done | 2026-04-23 |
| 01. Source Admission And Replay Design | 0/1 | In progress | - |
| 02. Neutral Module Extraction | 2/2 | Done | 2026-04-24 |
| 03. Blind Clone And Promotion Review | 0/2 | Planned, ready to execute | - |

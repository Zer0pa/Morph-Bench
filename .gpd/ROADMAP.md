# Roadmap: gnosis-morph-bench

## Overview

Morph-Bench is the Gnosis benchmark/replay framework. Its operational authority
comes from repo-local package execution, explicit replay/data boundaries, and
truthful public-facing claims. The current repo is staged for repo-orchestrator
review, not for unrestricted scientific or data-release promotion.

## Phases

- [x] **Phase 00: Bootstrap** - Build the staged repo, docs, and synthetic smoke path.
- [x] **Phase 01: Source Admission And Replay Design** - Freeze the first real
      replay target and adapter contract.
- [x] **Phase 02: Neutral Module Extraction** - Port neutral adapter, stability,
      and replay helpers into repo-local modules.
- [~] **Phase 03: Blind Clone And Promotion Review** - Clean-clone evidence and
      promotion surfaces exist; current branch is under greenlight verification.

## Phase Details

### Phase 00: Bootstrap

**Goal:** create a truthful staged repo with docs, package root, and a runnable
synthetic smoke path.

**Status:** Done.

### Phase 01: Source Admission And Replay Design

**Goal:** choose the first admitted real-source replay target and design the
adapter without widening scope.

**Status:** Done for target and contract selection. The Indus Phase 4 source
family remains the first real replay target; live replay execution remains
blocked on admitted Phase 3c manifest custody.

### Phase 02: Neutral Module Extraction

**Goal:** port neutral route-selection, stability, and replay helpers into
`src/gnosis_morph_bench/`.

**Status:** Done for package-local methods framework, synthetic fixtures,
replay CLI, stability battery, Indus v1 adapter shape, forbidden-pattern guard,
and adapter-contract coverage.

### Phase 03: Blind Clone And Promotion Review

**Goal:** prove the repo runs from a clean clone and keep public/release
boundaries truthful.

**Status:** Partially closed. Historical blind-clone evidence exists for the
Phase 03 closeout baseline. The current greenlight branch requires fresh local
verification and repo-orchestrator review before website sync.

## Current Forward Work

| Priority | Work | Status | Close Condition |
|---|---|---|---|
| P0 | Greenlight branch verification | In progress | hygiene scan, stale-current-surface scan, `pytest -q`, and smoke pass |
| P1 | Phase 3c manifest admission | Blocked | feature manifest JSON plus SHA-256 admitted to repo custody |
| P1 | Heavy-data/image-bearing policy | Blocked | owner policy names classes, terms, size bounds, storage, and review owner |
| P2 | Ops-Gates CI consumption | Deferred | `Gnosis-Ops-Gates` self-CI green plus pinned Morph-compatible invocation |
| P2 | Cuneiform adapter contract | Deferred | explicit Phase 04 plan or second-family authorization |

## Progress

| Phase | Status | Completed |
| ----- | ------ | --------- |
| 00. Bootstrap | Done | 2026-04-23 |
| 01. Source Admission And Replay Design | Done | 2026-04-24 |
| 02. Neutral Module Extraction | Done | 2026-04-24 |
| 03. Blind Clone And Promotion Review | Partial / current greenlight verification | 2026-04-28 |

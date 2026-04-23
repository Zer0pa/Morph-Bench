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

Plans:

- [ ] **02-01**: Extract route scoring and null metrics
- [ ] **02-02**: Extract stability and replay helpers

### Phase 03: Blind Clone And Promotion Review

**Goal:** prove the repo runs from a clean clone and review public blockers.
**Success criteria:**

1. clean temp-clone install and smoke pass
2. release blockers are explicit
3. legal and data boundaries remain visible

Plans:

- [ ] **03-01**: Run blind-clone verification

## Progress

| Phase | Plans Complete | Status | Completed |
| ----- | -------------- | ------ | --------- |
| 00. Bootstrap | 1/1 | Done | 2026-04-23 |
| 01. Source Admission And Replay Design | 0/1 | In progress | - |
| 02. Neutral Module Extraction | 0/2 | Pending | - |
| 03. Blind Clone And Promotion Review | 0/1 | Pending | - |

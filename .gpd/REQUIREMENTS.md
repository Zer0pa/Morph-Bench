# Requirements: gnosis-morph-bench

**Defined:** 2026-04-23
**Core Research Or Build Question:** Can the benchmark and replay logic behind
the live Phase 4 finding be extracted into a standalone methods repo that
installs and runs from repo custody while keeping domain verdicts outside the
boundary?

## Primary Requirements

### Data And Anchors

- [x] **DATA-01**: Admit the workstream substrate inside this repo and the wider
      package.
- [x] **DATA-02**: Freeze the live source boundary, authority bundle, and
      benchmark-first posture.
- [~] **DATA-03**: Admit the first real source-manifest adapter to replace the
      synthetic-only path. _Progressing: Indus Phase 4 v1 adapter and contract
      exist; real manifest admission is still pending Phase 3c custody._

### Derivations And Contracts

- [x] **DERV-01**: Define the neutral benchmark schema contract.
- [x] **DERV-02**: Define the migration boundary and data policy.
- [x] **DERV-03**: Define the first repo-custody replay contract against a real
      source manifest. _First target chosen (Indus Phase 4), v1 adapter
      contract frozen, and package-facing adapter shape covered by tests._

### Calculations And Analysis

- [x] **CALC-01**: Run the standalone smoke benchmark.
- [~] **CALC-02**: Port and rerun the live route-scoring logic from repo
      custody. _Neutral route-scoring surface exists; live manifest rerun is
      blocked on admitted Phase 3c custody._
- [~] **CALC-03**: Port and rerun the live stability and replay helpers from
      repo custody. _Replay/stability helpers exist for synthetic fixtures;
      live rerun is blocked on admitted Phase 3c custody._

### Simulation And Implementation

- [x] **SIMU-01**: Create an installable starter package.
- [x] **SIMU-02**: Replace hidden monorepo imports and path coupling in the
      extracted package logic.

### Validations

- [x] **VALD-01**: Verify source boundary and provenance truth.
- [x] **VALD-02**: Verify the staged repo installs and runs locally.
- [ ] **VALD-03**: Verify repo-custody replay against admitted live sources.
- [x] **VALD-04**: Verify blind-clone install plus smoke. _Historical Phase 03
      closeout evidence exists; current branch still requires normal local/CI
      verification before sync._

### Writing And Packaging

- [x] **WRIT-01**: Produce the staged repo docs, PRD, and handover surfaces.
- [~] **WRIT-02**: Produce promotion-ready release surfaces. _Code/docs legal
      posture is closed; live replay and data/artifact gates remain open and
      named._

## Out Of Scope

| Topic | Reason |
| ----- | ------ |
| Heavy corpus vendoring | blocked by rights and data-policy posture |
| Domain verdict packaging | belongs to consuming repos |
| Search demo extraction | belongs to another lane |

## Accuracy And Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| `DATA-01 / VALD-01` | source boundary explicit | repo-local audit |
| `CALC-01 / VALD-02` | standalone install plus smoke pass | smoke run |
| `CALC-02 / CALC-03 / VALD-03` | repo-custody replay works | live-source rerun artifacts |
| `VALD-04` | clean temp clone passes | blind-clone rerun |
| `WRIT-02` | no public overclaim or legal contradiction | release review |

## Traceability

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| `DATA-01`, `DERV-01`, `DERV-02`, `SIMU-01`, `VALD-01`, `VALD-02`, `WRIT-01` | Phase 00: Bootstrap | Done |
| `DATA-03` | Phase 01: Source Admission And Replay Design | Partial: adapter exists; real manifest admission pending |
| `DERV-03` | Phase 01: Source Admission And Replay Design | Done |
| `CALC-02`, `CALC-03` | Phase 02: Neutral Module Extraction | Partial: synthetic/replay helpers done; live rerun pending |
| `SIMU-02` | Phase 02: Neutral Module Extraction | Done |
| `VALD-03` | Phase 02/03: Live Source Replay | Pending admitted Phase 3c manifest |
| `VALD-04` | Phase 03: Blind Clone And Promotion Review | Done for historical closeout baseline |
| `WRIT-02` | Phase 03: Promotion Readiness | Partial: public surfaces coherent, replay/data gates open |

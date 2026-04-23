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
- [ ] **DATA-03**: Admit the first real source-manifest adapter to replace the
      synthetic-only path.

### Derivations And Contracts

- [x] **DERV-01**: Define the neutral benchmark schema contract.
- [x] **DERV-02**: Define the migration boundary and data policy.
- [ ] **DERV-03**: Define the first repo-custody replay contract against a real
      source manifest.

### Calculations And Analysis

- [x] **CALC-01**: Run the standalone smoke benchmark.
- [ ] **CALC-02**: Port and rerun the live route-scoring logic from repo
      custody.
- [ ] **CALC-03**: Port and rerun the live stability and replay helpers from
      repo custody.

### Simulation And Implementation

- [x] **SIMU-01**: Create an installable starter package.
- [ ] **SIMU-02**: Replace hidden monorepo imports and path coupling in the
      extracted live logic.

### Validations

- [x] **VALD-01**: Verify source boundary and provenance truth.
- [x] **VALD-02**: Verify the staged repo installs and runs locally.
- [ ] **VALD-03**: Verify repo-custody replay against admitted live sources.
- [ ] **VALD-04**: Verify blind-clone install plus smoke.

### Writing And Packaging

- [x] **WRIT-01**: Produce the staged repo docs, PRD, and handover surfaces.
- [ ] **WRIT-02**: Produce promotion-ready release surfaces only after replay
      and legal gates close.

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
| `DATA-03`, `DERV-03` | Phase 01: Source Admission And Replay Design | Pending |
| `CALC-02`, `CALC-03`, `SIMU-02`, `VALD-03` | Phase 02: Neutral Module Extraction | Pending |
| `VALD-04`, `WRIT-02` | Phase 03: Blind Clone And Promotion Review | Pending |

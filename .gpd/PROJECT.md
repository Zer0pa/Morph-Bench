# Project: gnosis-morph-bench

## What This Is

`gnosis-morph-bench` is the governed workstream for extracting neutral route
evaluation, null metrics, stability checks, replay helpers, and reference-freeze
surfaces into a standalone repo.

It exists to answer whether the live benchmark logic can be moved into this repo
without dragging in domain claims, heavy corpora, or hidden monorepo
dependencies.

## Core Research Or Build Question

Can the benchmark and replay logic behind the live Phase 4 finding be extracted
into a standalone methods repo that installs and runs from repo custody while
keeping domain verdicts outside the boundary?

## Scoping Contract Summary

### Contract Coverage

- `claim-substrate`: this repo carries its own starter package, smoke path, and
  source boundary
- `claim-governing-gate`: future extraction must rerun the real live-source
  logic from repo custody
- `claim-packaging`: only surviving repo-custody claims get promoted
- `False progress to reject`: synthetic smoke treated as final proof, heavy data
  vendoring, hidden monorepo imports, or domain overclaiming

### User Or Sponsor Guidance To Preserve

- `User-stated observables`: benchmark-first posture, no overclaiming,
  migration-ready scaffold
- `User-stated deliverables`: standard workstream pack plus repo-ready starter
- `Must-have references or prior outputs`: control canon, PRD canon, live Phase
  4 bundle, live source scripts
- `Stop or rethink conditions`: repo boundary collapses into domain code or
  hidden monorepo state

### Scope Boundaries

**In scope**

- route scoring and null metrics
- stability, replay, and reference-freeze helpers
- schema contracts and smoke fixtures

**Out of scope**

- heavy corpora
- domain-specific scientific verdict packaging
- search demo ownership

### Active Anchor Registry

| Anchor ID | Locator | Why It Matters | Carry Forward | Required Action |
| --------- | ------- | -------------- | ------------- | --------------- |
| `ref-prd` | `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` | sovereign repo boundary | planning, execution, verification | read, obey |
| `ref-agents` | `AGENTS.md` | execution boundary | planning, execution | read, obey |
| `ref-source-code` | `../../02_source_inventory/SOURCE_INVENTORY.md` | admitted source families | execution, verification | read, compare |
| `ref-source-authority` | `../../01_prd_and_authority/AUTHORITY_CHAIN.md` | live authority chain | execution, writing | cite, bound |

### Carry-Forward Inputs

- `../../01_prd_and_authority/SOVEREIGN_PRD.md`
- `../../04_evidence_manifest/evidence_manifest.json`
- `fixtures/tiny_benchmark_manifest.json`

### Skeptical Review

- `Weakest anchor`: local repo-custody replay beyond the synthetic smoke path
- `Unvalidated assumptions`: live scripts can be neutralized cleanly; source
  manifest families can map into one contract without leaking domain logic
- `Competing explanation`: the live code may belong in a consumer repo rather
  than a standalone methods repo
- `Disconfirming observation`: extraction requires copying glyph kernels or
  domain PRDs to stay runnable

### Open Contract Questions

- Which subset of the live cuneiform helpers belongs here versus a domain repo?
- Which real-source manifest should become the first repo-custody replay target?

## Research Questions

### Active

- [ ] Can the live route-selection logic be parameterized around manifest inputs?
- [ ] Can stability and replay helpers become repo-local without image-domain
      imports?
- [ ] Which real-source adapter should become the first replay gate?

## Research Context

### Physical Or Operational System

`A benchmark-first methods repo inside a migration package.`

### Theoretical Or Engineering Framework

`Reference-bottleneck evaluation, permutation-null scoring, stability testing,
and deterministic replay.`

### Key Parameters And Scales

| Parameter | Symbol | Regime | Notes |
| --------- | ------ | ------ | ----- |
| standalone install + smoke pass | `G_stage` | required now | current authority metric for the scaffold |
| repo-custody live replay pass | `G_replay` | required before promotion | future promotion gate |

### Known Results

- live source repo already has a Phase 4 methods finding
- live source repo already has route-selection, stability, and replay artifacts
- this staged repo already has a standalone synthetic smoke path

### What Is New

`This repo isolates the methods boundary and makes it runnable without the live
monorepo layout.`

### Target Environment Or Venue

`Private staged repo first, public promotion only after replay and legal gates.`

### Computational Or Operational Environment

`Python 3.10+, NumPy, scikit-learn, synthetic fixtures first, real-source
adapters later.`

## Notation And Conventions

See `.gpd/CONVENTIONS.md`.

## Requirements

See `.gpd/REQUIREMENTS.md`.

## Constraints

- `Workspace locality`: repo-local state is sovereign inside this scaffold
- `Authority doctrine`: live-source citations remain citations until rerun here
- `Logging discipline`: materially important runs write JSON artifacts
- `Evidence discipline`: no claim promotion without an artifact chain

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | ------- |
| Keep a tiny synthetic smoke path in-repo | Needed for a real standalone install gate | `ADOPTED` |
| Keep heavy corpora outside the staged repo | Prevents false completeness and rights drift | `ADOPTED` |

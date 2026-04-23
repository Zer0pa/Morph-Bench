# Contributing

## First Rule

Contribute only what this methods repo can honestly support. Do not import
domain verdicts, heavy corpora, or release language from another lane.

## Before You Start

1. Read `README.md` for the current truth.
2. Read `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` for the governing repo boundary.
3. Read `SOURCE_BOUNDARY.md` and `DATA_POLICY.md`.
4. Read `docs/ARCHITECTURE.md` and `code/README.md`.

## Contribution Rules

- Keep scope tight. One change should have one coherent reason.
- If you port live-source logic, update the source inventory in the same change.
- If you add or change a public claim, update the evidence path with it.
- If you cannot verify a statement, mark it `PARTIAL`, `UNKNOWN`,
  `UNVERIFIED`, or `OWNER_DEFERRED`.
- Do not widen legal, roadmap, or data-release language opportunistically.

## Pull Requests

Every PR should state:

- what changed
- why it changed
- what evidence or test supports it
- what source boundary changed, if any
- what remains unknown or deferred

## Boundaries

- Security-sensitive issues belong in `SECURITY.md`.
- Evidence disputes belong in the evidence dispute template.
- Domain-specific scientific claims belong in the consuming domain repo, not
  here.

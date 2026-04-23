# Auditor Playbook

## Goal

Use this file to verify what this staged repo proves today without confusing
source-repo authority for repo-custody proof.

## Fast Path

1. Read the authority block in `README.md`.
2. Read `docs/ARCHITECTURE.md` to see which truth surfaces are local and which
   are still cited from the source repo.
3. Read `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` for the governing repo boundary.
4. Run the synthetic smoke path in `SMOKE_TESTS.md`.
5. Read `PUBLIC_AUDIT_LIMITS.md` before promoting any portfolio-level or
   scientific claim.

## Claim Replay Map

| Claim | Evidence Path | Publicly Verifiable? | Caveat |
|---|---|---|---|
| The live source repo contains a real Phase 4 morph-benchmark finding | `../01_prd_and_authority/AUTHORITY_CHAIN.md` plus the cited source-repo artifact paths named there | `PARTIAL` | The artifacts are cited source authority, not local repo-custody reruns |
| This staged repo installs and runs a tiny synthetic smoke benchmark | `pyproject.toml`, `src/gnosis_morph_bench/`, `fixtures/tiny_benchmark_manifest.json`, `SMOKE_TESTS.md` | `YES` | Synthetic only; it does not prove the full live benchmark |
| The source boundary for this repo is explicit | `SOURCE_BOUNDARY.md`, `docs/family/BENCHMARK_SCHEMA_CONTRACT.md`, `code/README.md` | `YES` | Future extraction work can still change implementation details |

## Minimum Replay Steps

1. Verify the staged repo root contains the expected docs and package files.
2. Run the smoke command from `SMOKE_TESTS.md`.
3. Compare the README claims against `PUBLIC_AUDIT_LIMITS.md`.
4. If you inspect the live Phase 4 values, treat them as cited source authority
   until the rerun happens from this repo.

## If You Find A Problem

- Use the evidence dispute issue template for claim/evidence disagreements.
- Use the bug report template for reproducible implementation defects.
- Downgrade overreach to `PARTIAL`, `UNKNOWN`, or `UNVERIFIED` instead of
  narrating around the contradiction.

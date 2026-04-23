# Governance

## Scope

This document defines how `gnosis-morph-bench` states truth, separates staged
repo proof from cited source authority, and decides promotion readiness.

## Truth Hierarchy

1. `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` governs the repo boundary and active
   acceptance gates.
2. Repo-local artifacts and runnable smoke paths outrank prose.
3. Cited source-repo artifacts may justify the repo boundary, but they are not
   repo-custody proof until rerun here.
4. Public docs summarize current truth; they do not override artifacts.

## Status Vocabulary

| Token | Meaning |
|---|---|
| `VERIFIED` | Backed by current evidence in this repo |
| `PARTIAL` | Some evidence exists, but the claim is bounded |
| `UNKNOWN` | No evidence surface exists yet |
| `UNVERIFIED` | Claimed or proposed, but not closed |
| `INFERRED` | Reasonable interpretation, not direct proof |
| `OWNER_DEFERRED` | Requires owner-supplied input before closure |

If the repo uses a Commercial Readiness `Verdict` field, use only:
`STAGED`, `PASS`, `PARTIAL`, `BLOCKED`, `FAIL`, or `INCONCLUSIVE`.

## Decision Rights

| Topic | Authority | Notes |
|---|---|---|
| PRD amendments | Owner or delegated repo maintainer | Threshold changes must be explicit |
| Promoted public claims | Owner or delegated repo maintainer | No proxy-only closure |
| Release approval | Owner or delegated repo maintainer | Must satisfy `RELEASING.md` |
| Legal statements | Owner only until license text exists | Must match final license text |

## Claim Discipline

- One canonical authority block lives in `README.md`.
- Domain-specific scientific verdicts stay with domain repos.
- This repo may promote methods truth, replay discipline, and schema contracts.
- If a claim depends on source-repo artifacts, say so directly.

## Dispute Handling

1. Point to the exact statement under dispute.
2. Point to the missing or conflicting evidence path.
3. Classify the issue as overclaim, contradiction, missing artifact, or stale
   source citation.
4. Repair the evidence or downgrade the claim. Do not widen prose to hide the
   mismatch.

# Autonomous Execution Policy

This policy is the runtime operating contract for agents working inside a
bootstrapped workstream.

## Governing Laws

1. The top acceptance gate for the active PRD is sovereign.
2. Runtime truth and artifact truth outrank prose.
3. Contradictions stay visible until resolved.
4. Runbook or phase plan before production code.
5. Falsify before promote.
6. Baseline loss is failure even if side metrics improve.
7. Unknowns stay `UNKNOWN`, `UNTESTED`, `INCONCLUSIVE`, or `BLOCKED`.
8. No toy demos, no proxy passes, no narrativized wins.

## Execution Mode

- Work end to end inside the assigned workstream without interim reporting.
- Repo-local manifests, plans, summaries, logs, and reports are mandatory
  evidence artifacts.
- User-facing or orchestrator-facing reporting is end-only unless there is a
  blocker that cannot be removed locally or on admitted surfaces.
- If a narrower write set is assigned, stay inside it.
- Do not revert or overwrite unrelated work from other agents.

## Required Session Start Sequence

1. Read the active PRD or sovereign brief.
2. Read the local GPD pack in full enough to know the current truth.
3. Read the active phase files and machine state.
4. Confirm lane boundary, environment, current phase, and open blockers.
5. Check the anti-pattern guard before beginning work.

## Required Work Loop

1. Freeze the governing gate, baseline, comparator, and scope boundary.
2. Write or update the active phase plan before coding.
3. Execute only the declared scope.
4. Record artifacts, commands, and outcomes on disk.
5. If a gate fails, diagnose, amend the plan, apply the minimal justified fix,
   and rerun the failed gate plus downstream checks.
6. Promote claims only when the artifact chain supports them.

## What Counts As A Blocker

A blocker is real only if at least one of these is true:

- a required source, credential, dataset, or hardware surface is unavailable
- another agent owns the file or compute surface needed for the next step
- the PRD, source corpus, or lane boundary is contradictory enough that work
  would likely corrupt truth
- legal or licensing constraints prevent the next required action

Confusion, partial failure, or ugly results are not blockers. They stay in the
fix loop.

## Output Contract

- Every materially different hypothesis or route gets an explicit candidate or
  route ID.
- Phase plans and phase summaries are append-only truth surfaces once written.
- Machine-readable state must stay current.
- If scope changes, amend the GPD surfaces before narrating a new objective.
- If the governing gate fails, record the real failure instead of widening the
  story.

## Anti-Pattern Guard

Raise a blocker if any of these happen:

- coding before the plan or runbook exists
- promoting a claim without an artifact path
- treating proxy evidence as closure for a core gate
- quietly changing thresholds, seeds, fixtures, or comparators after freeze
- hiding baseline loss behind secondary wins
- cleaning up contradictions by rewriting prose instead of resolving evidence
- declaring success because the narrative sounds coherent
- using docs, plans, or handover files as a substitute for the real gate

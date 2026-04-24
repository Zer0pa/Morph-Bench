# Phase 03 Context: Blind Clone And Promotion Review

## Phase goal (from ROADMAP.md)

Prove the repo runs from a clean clone and review public blockers.

Success criteria:

1. clean temp-clone install and smoke pass
2. release blockers are explicit
3. legal and data boundaries remain visible

## PRD mapping

Phase 03 (GPD-internal) covers:

- the **executable subset** of PRD-P3 "Replay And Blind Clone"
  (`PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` §4): rerun the smoke path from a
  clean clone. The "admitted live replay" subset of PRD-P3 (rerun the Phase 3c
  live feature manifest under repo custody) is NOT covered here — the live
  Phase 3c feature manifest is not present on this Mac and not on the RunPod
  pod. That is a real external-dependency blocker and is recorded as a
  documented unblock item in `docs/PROMOTION_READINESS.md`, not as an
  executable task.
- the **documentation subset** of PRD-P4 "Promotion Readiness": enumerate
  what is ready, what is blocked, and what is deferred, without fabricating a
  license and without softening the boundary.

## Starting reality (must read before planning)

- Phase 02 landed (SUMMARY at
  `.gpd/phases/02-neutral-module-extraction/02-02-SUMMARY.md`): 32/32 pytest
  cases green, zero forbidden-pattern hits under `src/gnosis_morph_bench/`,
  `smoke` and `replay` CLI subcommands wired, `python -m gnosis_morph_bench`
  runnable, `gnosis-morph-bench-adapter-indus-phase4` console_script wired.
- The synthetic smoke artifact
  `artifacts/smoke/smoke_report.json` is committed and is the byte-reference
  for blind-clone reproduction.
- `pyproject.toml` declares `requires-python = ">=3.10"`.
- Two console_scripts are declared:
  `gnosis-morph-bench-smoke = gnosis_morph_bench.cli:main`
  and
  `gnosis-morph-bench-adapter-indus-phase4 = gnosis_morph_bench.adapters.indus_phase4:main`.
- The legal surface today is a placeholder:
  `LICENSE_PLACEHOLDER.md` (not a license), plus
  `OWNER_DEFERRED_*` markers in `RELEASING.md`.
- `DATA_POLICY.md`, `SOURCE_BOUNDARY.md`, `PUBLIC_AUDIT_LIMITS.md` are already
  aligned to the "do-not-vendor-heavy-data" and "no-public-promotion-yet"
  posture; Phase 03 must preserve this alignment.

## Environment decision: primary vs secondary blind clone

**Primary blind-clone surface: local macOS in `/tmp/`.**

Rationale:

- macOS has Python 3.11+ available (this repo's own venv is 3.11), which
  matches the declared `requires-python = ">=3.10"` floor.
- A clean `/tmp/` work dir is guaranteed outside the committed repo tree and
  outside the `.venv` already bound to `05_repo_scaffold`.
- Round-trip is fast (no SSH), so failures surface immediately.

**Secondary blind-clone surface: RunPod pod `7k3riasglemecu`
(`ssh -i ~/.ssh/id_ed25519 -p 34587 root@38.80.152.147`).**

Rationale and caveat:

- RunPod pod `python3 --version` reports Python **3.8.10**, below the declared
  3.10 floor. This is not a repo defect — it is exactly the kind of
  environment drift a blind-clone check is supposed to surface.
- The RunPod run is a **secondary check** whose job is to report the
  environment readiness gap (install Python 3.11 via `uv` or deadsnakes,
  document the command, record the gap in the transcript). It is NOT the
  authoritative pass gate.
- If the RunPod environment cannot be brought above the Python floor without
  escalating privileges beyond what a researcher doing a blind clone would
  normally have, that is recorded as a transcript note and an unblock item in
  `docs/PROMOTION_READINESS.md` rather than a plan failure.

## Hard constraints (carried from the directive)

- No plan task may require the live Indus Phase 3c feature manifest.
- No plan may generate a fabricated license.
- No plan may promote live Phase 4 numbers as repo-custody proof.
- Blind-clone work writes under `/tmp/` (macOS) or `/workspace/blind-clone-*`
  (RunPod), never inside `05_repo_scaffold/`.
- The ONLY artifact that lands back into the repo is a transcript file under
  `artifacts/blind_clone/` documenting the run.
- No claims, no deliverables, and no verification tasks depend on output that
  has not already been produced by Phase 02 under repo custody.

## Blockers-are-tasks doctrine

When something cannot be done inside this phase, it becomes a documented
task in `docs/PROMOTION_READINESS.md` with:

- the exact unblock condition,
- the owning authority pointer (`OWNER_DEFERRED` where appropriate), and
- a named artifact path the unblock would produce.

Blockers are never hidden behind prose softening.

## Constraints and non-claims

- Phase 03 does not run the live Phase 4 rerun. The admitted-data replay
  is out of scope here and is recorded as a named unblock item.
- Phase 03 does not invent or inline a LICENSE. Option (b) from the
  directive is adopted: `docs/PROMOTION_READINESS.md` documents that the
  repo remains private until canonical license text lands, and
  `LICENSE_PLACEHOLDER.md` stays unchanged.
- Phase 03 does not touch the cuneiform family, does not add new
  stability-battery modes, and does not edit any module under
  `src/gnosis_morph_bench/` unless the blind clone uncovers a genuine
  install-blocking defect (a Deviation Rule 4 fix would then be
  documented per AGENTS.md).
- Phase 03 does not vendor Phase 3c data to make the live rerun appear
  doable.

## Open questions consumed by this phase

- **None of the live-data open questions.** The Phase 3c access question
  surfaces as a documented unblock item, not as an executable question in
  Phase 03.

## Plans in this phase

- **03-01: Blind-clone verification (primary macOS, secondary RunPod).**
  Clean-clone install, smoke parity check, replay record check, adapter
  entrypoint check, forbidden-pattern scan, pytest run. Emits a
  transcript file under `artifacts/blind_clone/`. Reports the
  environment gap on RunPod.

- **03-02: Promotion-readiness documentation.** Writes
  `docs/PROMOTION_READINESS.md` enumerating what passes the staged gate,
  what is externally blocked, and what is deferred. Updates
  `TODO.md` cross-references where appropriate. No fabricated license.

## Chaining

Plan 03-01 should land first because the transcript it produces is
concrete input that Plan 03-02 can cite as "what we proved under repo
custody today." 03-02 does not block on 03-01 if the blind clone fails
hard — 03-02 can still land and name the failure as an open blocker —
but the clean case is 03-01 → 03-02.

## Decisions carried into this phase

- [Phase 00]: keep heavy corpora outside the staged repo.
- [Phase 00]: treat live Phase 4 metrics as source authority until rerun here.
- [Phase 00]: use a synthetic smoke fixture as the minimum standalone install
  gate.
- [Phase 01]: first repo-custody replay target is Indus Phase 4; Phase 3c
  feature manifest is the admitted live surface and remains external.
- [Phase 02]: adapter surface and stability battery are complete under
  synthetic fixtures; no live Phase 4 numeric value is promoted to
  repo-custody proof.

## Pending todos explicitly deferred beyond Phase 03

- Obtain admitted access to the Phase 3c feature manifest → documented as a
  named unblock item in `docs/PROMOTION_READINESS.md`; not executable here.
- Draft a cuneiform adapter contract → later phase.
- Publish the repo publicly → remains blocked until license text and
  heavy-data release policy are supplied. Documented, not executed.

## Required reading for the executor

- `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` §4 (Phase table P3 and P4)
- `SOURCE_BOUNDARY.md`, `DATA_POLICY.md`, `PUBLIC_AUDIT_LIMITS.md`,
  `RELEASING.md`
- `LICENSE_PLACEHOLDER.md` (as the thing NOT to fabricate away)
- `.gpd/phases/02-neutral-module-extraction/02-02-SUMMARY.md`
- `artifacts/smoke/smoke_report.json` (the committed byte-reference)

# Releasing

## Release Principle

Release only when the public truth surface matches the current accepted state.
For this repo, that means the staged starter, the source boundary, and the
license boundary all agree.

## Release Types

| Release Type | Use When | Minimum Gate |
|---|---|---|
| Snapshot | sharing a dated staged state for review | docs and smoke path are coherent |
| Tagged release | shipping a named repo version | evidence, docs, and license surface agree |
| Breaking release | changing schema or public semantics | migration note and downstream review exist |

## Required Checks

- `README.md` and `AUDITOR_PLAYBOOK.md` still match.
- `PUBLIC_AUDIT_LIMITS.md` still reflects the actual custody boundary.
- `docs/ARCHITECTURE.md` and `code/README.md` reflect the package layout.
- License references are correct for the release being published.
- No domain-specific scientific result is implied as repo-custody proof unless
  rerun artifacts exist here.

## Live Sync Sequence

1. Freeze the intended acquisition surface.
2. Run the smoke path.
3. Run one coherence pass across README, audit, architecture, governance, legal
   boundaries, and data policy.
4. Publish only after the rendered repo matches the approved local state.

## Owner Inputs

- versioning scheme: `0.y.z until source-custody replay passes`
- release notes location: `OWNER_DEFERRED_ADD_CHANGELOG_BEFORE_FIRST_RELEASE`
- license identity: `OWNER_DEFERRED`
- downstream compatibility promise: `NO_STABILITY_PROMISE_BEFORE_REAL_EXTRACTION`

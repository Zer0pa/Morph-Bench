# Security

## Reporting

Report security issues privately to `OWNER_DEFERRED_PRIVATE_ROUTE`.

If you are unsure whether something is security-sensitive, default to private
reporting first.

## What To Include

- affected version, branch, or commit
- reproduction steps
- impact description
- whether the issue depends on omitted heavy assets or owner-held inputs

## Response Targets

| Step | Target |
|---|---|
| Initial acknowledgement | `OWNER_DEFERRED` |
| Triage decision | `OWNER_DEFERRED` |
| Fix or mitigation update | `OWNER_DEFERRED` |

## Public Issues

Do not open public issues for vulnerabilities that could expose private asset
paths, omitted datasets, or unpatched attack paths.

## Repo Boundary

- This staged repo should not expose sensitive local absolute paths in code or
  docs.
- Security posture for later heavy benchmark assets remains unresolved until the
  data-release boundary is closed.

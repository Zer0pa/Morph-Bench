# Repo-Docs Starter Pack Usage

This pack is a reusable documentation skeleton for a live synced Zer0pa repo.
It copies structure and discipline from the repo-docs playbook. It must not copy
claims, metrics, proof paths, acquisition links, or legal terms from another
repo.

## How To Use This Pack

1. Copy the files into the target repo at the same paths.
2. Replace every bracketed token such as `[REPO_NAME]`.
3. Remove sections that are not true for the target repo.
4. If a fact is not evidenced yet, write `UNKNOWN`, `UNVERIFIED`,
   `INFERRED`, or `OWNER_DEFERRED`.
5. Keep one canonical authority block in the root `README.md`.
6. Run one falsification pass before publishing.

## What Must Stay Repo-Specific

- Repo name, URL, contact, acquisition surface, and default branch.
- Product thesis, domain, scope, and customer/problem framing.
- Current authority artifact, proof paths, metrics, and caveats.
- What is public truth, operator truth, historical only, or unknown.
- Downstream contracts, compatibility posture, and runtime boundaries.
- Security reporting path and response expectations.
- Governance decisions, roadmap items, and release gates.
- License identity and any legal or commercial statements.

## What May Be Reused

- File layout and section ordering.
- Zer0pa truth discipline and status vocabulary.
- The split between front-door, audit, architecture, governance, and support
  surfaces.
- The live-synced-repo posture: useful now, improving continuously.

## Visual System Note

- If the target repo is using the ZPE-IMC bootstrap visual system, apply the
  shared masthead consistently.
- The root `README.md` is the only doc that should carry the two extra GIF
  slots.
- Do not ship broken asset paths. Rendering failures are doc failures.

## Recommended Companion Files

This pack stays focused on the requested starter set. Most live repos should add
the following alongside it:

- `CHANGELOG.md`
- `CODE_OF_CONDUCT.md`
- `CITATION.cff`
- `LICENSE` once the owner supplies the final legal text

## Final Acceptance Check

- No borrowed claims from another repo remain.
- Public docs do not outrun the evidence surface.
- `README.md`, `AUDITOR_PLAYBOOK.md`, `PUBLIC_AUDIT_LIMITS.md`, and
  `docs/ARCHITECTURE.md` agree on the current truth.
- Issue and PR intake templates match the repo's actual governance.
- Anything still missing is named plainly instead of implied away.

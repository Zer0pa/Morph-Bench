# Roadmap

## How To Read This File

This roadmap states extraction sequence and blockers. It is not itself proof of
the live benchmark result.

## Active Priorities

| Priority | Item | Why It Matters | Entry Gate | Evidence Needed | Status | Owner |
|---|---|---|---|---|---|---|
| P0 | Port live route-selection and stability helpers into `src/gnosis_morph_bench/` | The repo is not sovereign until the real methods logic lives here | staged scaffold exists | repo-local rerun artifacts and no hidden imports | `IN_PROGRESS` | `OWNER_DEFERRED` |
| P1 | Add converters for admitted Indus and cuneiform manifest families | The schema contract is only useful if the live source families can map into it | P0 design settled | documented adapters and fixture-backed tests | `NOT_STARTED` | `OWNER_DEFERRED` |
| P2 | Run blind-clone install plus smoke and one admitted replay path | Promotion cannot rest on local ambient state | P0 and P1 complete enough to rerun | clean temp-clone transcript | `NOT_STARTED` | `OWNER_DEFERRED` |

## Deferred Or Blocked Work

| Item | Reason | Unblock Condition | Status |
|---|---|---|---|
| Public remote | canonical license text absent | owner supplies final license text and release boundary | `BLOCKED` |
| Heavy benchmark vendoring | data rights and public-purpose boundary unresolved | explicit publish/fetch decision per asset family | `BLOCKED` |
| Domain claim promotion | methods repo must not swallow consumer truth | domain repos rerun against this repo and keep custody boundaries explicit | `DEFERRED` |

## Status Rules

- Use `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `DEFERRED`, or `DONE`.
- If a priority depends on owner input, say so plainly.
- A synthetic smoke win is not equivalent to the live-source replay gate.

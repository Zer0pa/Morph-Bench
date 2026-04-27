# Legal Boundaries

## Authority

The legal authority for repository code is `LICENSE` (Apache License 2.0).
Documentation, reports, and written materials are released under Creative
Commons Attribution 4.0 International unless a narrower file-level notice says
otherwise.

`NOTICE` records attribution, trademark, third-party, and data-boundary notes.
`DATA_POLICY.md` controls whether data, fixtures, corpora, model weights, or
image-bearing artifacts may be redistributed.

## Public Summary Rules

- Do not claim rights broader than Apache-2.0 for code and CC-BY-4.0 for docs.
- Do not imply that code openness licenses raw corpora, cultural-heritage
  imagery, private HF artifacts, endpoint logs, or model weights.
- Do not describe a blocked scientific claim as closed merely because the repo
  has a public license.
- Keep claim, no-go, and retraction language aligned with the README and proof
  anchors.

## Current Public Boundary

| Topic | Current Public Statement | Source Of Authority |
|---|---|---|
| Code license | Apache-2.0 | `LICENSE` |
| Documentation and reports | CC-BY-4.0 | `README.md`, `NOTICE` |
| Data and fixtures | repo-specific; not automatically licensed | `DATA_POLICY.md` |
| Model weights and checkpoints | separate release required | `DATA_POLICY.md`, HF custody registers |
| Trademarks | not granted by Apache-2.0 or CC-BY-4.0 | `TRADEMARKS.md` |

## Inputs Still Needed Before Visibility Flip

- final public/non-public visibility decision for this repo
- data/artifact scrub for any rights-gated assets
- third-party dependency re-audit before a tagged public release

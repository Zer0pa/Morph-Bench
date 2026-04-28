# Data Policy

## Current Public-Repo Boundary

Morph-Bench may carry:

- documentation and governance metadata
- neutral package code
- tiny synthetic fixtures
- synthetic smoke and replay outputs
- adapter-run records whose inputs are admitted and hashed

Morph-Bench may cite, but must not treat as repo-custody proof:

- live Phase 4 authority artifacts from the Indus source chain
- cuneiform benchmark manifest families
- private HF custody records that have not been admitted into this repo

Morph-Bench must not carry in the public GitHub repo today:

- raw corpora
- image-bearing benchmark payloads
- restricted cultural-heritage image assets
- review-pack artifacts
- model weights or checkpoints
- endpoint logs, SSH transcripts, tokens, or operational secrets

## License Separation

Repository code is Apache-2.0. Documentation, reports, and written materials
are CC-BY-4.0 unless a narrower file-level notice says otherwise.

Those licenses do not license data, corpora, image-bearing payloads, private
HF artifacts, model weights, endpoint logs, or operational transcripts. Data
and artifact admission is separate from code/docs licensing.

## Image-Bearing Release Boundary

No image-bearing payload is admitted to this public repo at the current gate.
Before any such payload is added, the admission record must name:

1. the asset family and rights class
2. the source authority and checksum
3. whether the payload is public, private HF-only, or excluded
4. size bounds and storage location
5. redaction or transformation applied before release
6. the reviewer/owner who accepted the release boundary

Until that record exists, image-bearing assets remain excluded. A successful
code/docs license rollout does not change this data boundary.

## HF Custody

Private `Architect-Prime/*` HF datasets may hold recovery snapshots and future
admitted authority bundles. They are operational custody surfaces, not public
license grants. Public GitHub visibility does not make private HF content
public.

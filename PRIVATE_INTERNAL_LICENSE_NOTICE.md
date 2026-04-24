# Private / Internal License Notice

**Status:** INTERNAL / PRIVATE — no public license granted.
**Date:** 2026-04-24
**Applies to:** the entirety of the `Zer0pa/Morph-Bench` GitHub repository, including code, documentation, tests, fixtures, configuration, and any derived artifacts produced by running the code in this repo.

---

## Plain statement

No public license is granted unless and until a license file is added to this repository by Zer0pa.

This repository is distributed to internal collaborators and authorized reviewers only. It is not open source, not public domain, not covered by MIT / Apache-2.0 / BSD / GPL / LGPL / MPL / CC-BY / CC0 / any other public license, and not available for redistribution, sublicensing, modification for redistribution, commercial use, or public disclosure.

## What this means for you

- **If you are an internal Zer0pa collaborator:** your use of this repo is governed by your existing employment, contractor, or contributor agreement with Zer0pa. Consult that agreement for scope.
- **If you are an external reviewer (grant, legal, partner):** you have been granted temporary read access for the specific review you were engaged for. Do not fork, mirror, redistribute, or quote verbatim outside that engagement.
- **If you obtained this code by mistake:** do not use, copy, or distribute it. Contact `architects@zer0pa.ai`.

## Relationship to other files in this repo

- `LICENSE_PLACEHOLDER.md` — owner-deferred canonical license status. When Zer0pa legal chooses the canonical license matrix (see `docs/LEGAL_REVIEW_PREP.md`), that file will be replaced by a real `LICENSE` file and this notice may be revised or retired.
- `docs/PROMOTION_READINESS.md` — `Blocked-2` names canonical LICENSE text as a gate to public promotion. This notice documents what is true in the meantime.
- `docs/LEGAL_REVIEW_PREP.md` — the questions Zer0pa legal is being asked before any public license choice is made.

## Third-party provenance inside this repo

This repo depends on the following third-party libraries at runtime:

- `numpy` — BSD-3-Clause (permissive, compatible with any end-state license decision)
- `scikit-learn` — BSD-3-Clause

No third-party source code is vendored into this repo. All third-party code is declared as a package dependency in `pyproject.toml` and installed from PyPI at `pip install -e .` time.

## Changing this notice

Only Zer0pa (or its authorized legal agent) may revise or retire this notice. Individual contributors must not edit it.

## Contact

Legal questions: `architects@zer0pa.ai`.

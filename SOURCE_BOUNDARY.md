# Source Boundary

## This Repo Should Own

- route evaluation and route ranking
- permutation-null metrics
- stability and Jaccard helpers
- deterministic replay helpers
- reference-freeze helpers
- benchmark schema contracts and manifest adapters

## This Repo Should Not Own

- image preprocessing kernels
- domain-specific catalogue construction
- search demo packaging
- papers, grant prose, or domain verdict files
- raw corpora and heavy image assets

## Live Source Families Admitted For Extraction

- `scripts/indus/phase4_route_selection.py`
- `scripts/indus/phase4_stability.py`
- `scripts/indus/stability_tester.py`
- `scripts/cuneiform/annotated_sign_benchmark_common.py`
- `scripts/cuneiform/revert_phase2_common.py`

## Explicit Dependency Boundary

- borrow from `gnosis-glyph-engine` only through declared optional adapters or
  future package dependencies
- do not edit the sibling staged repos from this lane
- keep domain results in `gnosis-indus` and `gnosis-cuneiform`

## Hard Exclusions

- `workspace/data/`
- `workspace/papers/`
- `workspace/share/*review*`
- any owner-held private legal surface beyond cited references

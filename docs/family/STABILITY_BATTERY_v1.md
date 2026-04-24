# Stability Battery v1

## Purpose

Specify the five stability modes that `gnosis_morph_bench.stability` exposes
when Phase 02 is complete. The battery runs on any
`BenchmarkManifest` -- synthetic fixture or adapter-emitted neutral manifest --
and emits JSON-serializable, deterministic-at-fixed-seed payloads that a
`ReplayRecord` aggregator can write to disk under repo custody.

This doc is binding for Phase 02 and Phase 03: every test assertion in the
plan frontmatter must map to at least one section here, and the CLI's
`replay` subcommand is an obligation to keep these five modes available.

## Modes

The battery has five modes. Each mode returns a dict whose top-level `mode`
field names the mode. Every mode except `deterministic_replay` also emits a
`mean_jaccard`, `min_jaccard`, and `max_jaccard` scalar summary (Jaccard over
same-cluster pairs, bounded in `[0.0, 1.0]`).

1. **`deterministic_replay`** — re-evaluates the governing route multiple
   times at the same seed and hashes `labels_by_item`. Payload includes
   `hashes` (list) and `all_identical` (bool). This measures bit-for-bit
   reproducibility at a fixed seed, not cross-seed stability.

2. **`leave_fraction_out`** — drops a random fraction of items, reclusters
   the remainder, and scores pairwise Jaccard between the baseline and the
   subset clustering on the shared item ids. Measures stability under
   bounded data loss.

3. **`noise_injection`** — adds Gaussian noise of configurable sigma to the
   **standardized** feature matrix (i.e., after `StandardScaler`), reclusters,
   and scores Jaccard against baseline. Sigma is in standardized-feature
   units, not raw-feature units; a sigma of `0.0` must return Jaccard 1.0,
   and a sigma of `5.0` must strictly perturb at least one repeat.

4. **`k_sensitivity`** — reclusters at `k_base + offset` for each declared
   offset (default `(-1, +1)`) and scores Jaccard against the baseline
   clustering at `k_base`. The effective `k` is clipped silently to
   `[2, n_items - 1]`; both the `requested_k` and the `effective_k` are
   recorded per entry so callers see when clipping happened.

5. **`seed_variance`** — re-runs the full `evaluate_route` chain at a list
   of alternate seeds (default `(1, 2, 3, 4)`) and scores Jaccard against
   the baseline. For the ward linkage backend currently shipped in
   `benchmark.cluster_labels`, the clustering itself is deterministic given
   inputs, so Jaccard `== 1.0` across all seeds is the expected,
   non-pathological outcome on a dataset where ward is globally seed-
   invariant. The mode is meaningful because it also re-triggers the
   permutation null (which consumes the seed) and any future non-ward
   backend. A disconfirming observation is a seed-variance mean_jaccard of
   `1.0` on a genuinely seed-sensitive feature matrix; tests must therefore
   assert the mode _runs_ and its summary is finite, not that Jaccard is
   strictly less than 1.0.

## Aggregator

`stability_battery(manifest, route_name, config, **kwargs)` calls all five
modes and returns:

```json
{
  "route_name": "<governing route>",
  "modes": {
    "deterministic_replay": { ... },
    "leave_fraction_out": { ... },
    "noise_injection": { ... },
    "k_sensitivity": { ... },
    "seed_variance": { ... }
  }
}
```

Every value is JSON-serializable and every per-mode payload carries a
`"mode"` string that matches the function name.

## NaN Policy

- No silent imputation. No zero-fill. No median/mean substitution.
- NaN in any route vector MUST abort the mode with a `ValueError` whose
  message names the offending `item_id`. The policy is inherited from
  `schema.extract_route_dataset`, which is called directly by every mode.
- The adapter (`adapters.indus_phase4`) enforces the same rule upstream
  in strict mode; downstream the battery is allowed to assume the
  manifest it is given is already NaN-clean, but it never compensates
  if it is not.

## Jaccard Definition

The `pairwise_jaccard(left_labels, right_labels, shared_ids)` helper
computes:

```
J = |same-cluster pairs in BOTH| / |same-cluster pairs in EITHER|
```

where a pair `(a, b)` with `a, b ∈ shared_ids` and `a < b` is a
same-cluster pair under a labeling `L` iff `L[a] == L[b]`. When both
sides have no same-cluster pairs, Jaccard is defined as `1.0` (trivial
agreement on the empty-pair set).

## Default Output Paths

All stability-battery outputs default to repo-local
`artifacts/replay/` and never to `workspace/...`. The `replay` CLI
subcommand writes `artifacts/replay/replay_record.json` by default; the
directory is created on demand and is tracked under repo custody by a
`.gitkeep` file so a blind clone can find it.

## Validity Bounds

- `noise_sigma` is in **standardized-feature units** (post-StandardScaler),
  not raw-feature units. A value on the order of `0.05` corresponds to a
  small perturbation of the standardized feature geometry; a value of
  `5.0` is explicitly a stress test. Interpreting a result at
  `noise_sigma >> 1` as "a small perturbation" is a misread of the mode.
- `k_offsets` entries are clipped silently into `[2, n_items - 1]`. If the
  clip is active the mode records both `requested_k` and `effective_k` so
  downstream consumers can see the clip happened. A mode run where every
  requested offset was clipped still returns a complete payload; callers
  that need a non-trivial sweep should extend the offsets.
- `seed_variance` seeds are arbitrary ints; the default list
  `(1, 2, 3, 4)` is four distinct seeds that differ from the default
  `EvaluationConfig.seed=42`, so at most five distinct seeds are sampled
  across the full battery.

## Non-Claims

- The battery does NOT prove any Phase 4 numeric value. Recovery of the
  live Phase 4 NMI / Sigma / Jaccard / Replay quadruple is a Phase 03
  obligation gated on admitted Phase 3c feature-manifest access.
- The battery does NOT claim the clustering backend is non-deterministic.
  Ward linkage is deterministic given inputs; the aggregator simply
  plumbs a seed through so the permutation null and any future backend
  pick it up.
- The battery does NOT sweep `k` across a wide range. The default
  `k_offsets = (-1, +1)` exposes the hook; a full sweep is deferred to a
  later battery revision.
- The battery does NOT add new clustering algorithms, silhouette variants,
  or alternative distance metrics. Those are a Phase 03+ concern.

## Forbidden Behaviors

No mode in this battery may:

- Import from `phase3_common`, `stroke_*`, or any monorepo runtime module.
- Call `sys.path.insert(...)` or `Path(__file__).resolve().parents[N]`.
- Write to `workspace/...` at any path.
- Silently replace NaN with a finite number.
- Reconstruct cluster labels from cached state without calling
  `cluster_labels` or `evaluate_route`.

The forbidden-pattern lint in `tests/test_forbidden_patterns.py` is the
mechanical enforcement; this list is the doc that explains why.

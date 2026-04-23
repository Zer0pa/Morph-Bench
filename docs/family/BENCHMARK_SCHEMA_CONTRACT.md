# Benchmark Schema Contract

## Purpose

Define the minimal corpus-neutral manifest contract for route scoring,
reference-freeze helpers, stability checks, and smoke execution.

## Current Manifest Shape

```json
{
  "schema_version": 1,
  "manifest_name": "tiny-smoke",
  "items": [
    {
      "item_id": "1",
      "reference_labels": {
        "family": "alpha"
      },
      "route_features": {
        "route_name": [0.0, 0.1]
      }
    }
  ]
}
```

## Required Fields

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | integer | manifest contract version |
| `manifest_name` | string | human-readable manifest label |
| `items` | array | ordered benchmark items |
| `items[].item_id` | string | stable item identifier |
| `items[].reference_labels` | object | one or more named reference partitions |
| `items[].route_features` | object | route-name to numeric feature vector mapping |

## Rules

- all items must expose the same route set for any route being evaluated
- feature vectors within one route must have consistent dimensionality
- `reference_labels` must contain the requested key for any evaluation run
- the repo may add optional metadata fields later, but the current smoke path
  relies only on the fields above

## Source Mapping Targets

| Live source family | Expected adapter behavior |
|---|---|
| `workspace/artifacts/indus/phase3c/prebinarized_feature_manifest.json` | map route variants into `route_features` and ICIT labels into `reference_labels` |
| `workspace/artifacts/cuneiform/annotated_sign_benchmark_manifest.json` | map feature families and train labels into the neutral contract |

## Non-Claims

- this contract does not yet freeze the full production schema for every future
  benchmark lane
- this contract does not imply that all source families are already converted

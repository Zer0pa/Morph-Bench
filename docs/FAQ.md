# FAQ

## What is this repo?

It is the benchmark and replay framework for the neutral Gnosis methods layer.
It packages route scoring, null metrics, stability checks, deterministic
replay, and the first Indus Phase 4 adapter boundary.

## How does this relate to the wider Zer0pa portfolio?

It is one methods repo inside a portfolio, not a platform core. It should own
only benchmark and replay logic, not domain-specific scientific claims.

## What is actually verified here?

The package installs, the synthetic benchmark schema runs end-to-end, adapter
contract coverage is tested, and the synthetic smoke path has blind-clone
evidence across macOS and Linux. The live Phase 4 methods finding is cited
source authority but not yet rerun from this repo's custody.

## What is still unknown or deferred?

Live Phase 4 rerun from Morph custody, heavy-data/image-bearing release terms,
and the cuneiform adapter contract remain open or deferred. Code/docs license
posture is settled; data and private artifacts remain separate.

## Why does public documentation mention audit limits?

Because the source-repo authority artifacts and the staged repo's local proof
are not the same thing. The docs keep that custody boundary explicit.

## Where should I start if I want to inspect the technical structure?

Read `docs/ARCHITECTURE.md`, then `code/README.md`, then
`docs/family/BENCHMARK_SCHEMA_CONTRACT.md`.

## Where do I report defects, disputes, or questions?

Use the issue templates for bugs, evidence disputes, feature requests, and
questions. Use `SECURITY.md` for private vulnerability reporting.

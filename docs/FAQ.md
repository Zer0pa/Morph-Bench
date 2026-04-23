# FAQ

## What is this repo?

It is the staged extraction target for the neutral benchmark and replay layer
behind the Gnosis reference-bottleneck finding.

## How does this relate to the wider Zer0pa portfolio?

It is one methods repo inside a portfolio, not a platform core. It should own
only benchmark and replay logic, not domain-specific scientific claims.

## What is actually verified here?

The staged repo installs, exposes a synthetic benchmark schema, and runs a tiny
smoke benchmark. The live Phase 4 methods finding is cited source authority but
not yet rerun from this repo's custody.

## What is still unknown or deferred?

Full extraction parity with the live Phase 4 and cuneiform helper scripts,
blind-clone success on a clean checkout, final license text, and public data
release posture.

## Why does public documentation mention audit limits?

Because the source-repo authority artifacts and the staged repo's local proof
are not the same thing. The docs keep that custody boundary explicit.

## Where should I start if I want to inspect the technical structure?

Read `docs/ARCHITECTURE.md`, then `code/README.md`, then
`docs/family/BENCHMARK_SCHEMA_CONTRACT.md`.

## Where do I report defects, disputes, or questions?

Use the issue templates for bugs, evidence disputes, feature requests, and
questions. Use `SECURITY.md` for private vulnerability reporting.

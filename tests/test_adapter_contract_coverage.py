"""ADAPTER_CONTRACT_v1.md MUST-clause coverage test.

Every line in the contract containing the token ``MUST`` is slugified
(first six words, lowercased, non-alphanumerics collapsed to
underscores) and checked against a hand-maintained coverage map that
names one or more acceptance-test ids from the Plan 02-01 frontmatter.

If a contract revision introduces a new MUST clause, the slug will not
be in ``MUST_COVERAGE`` and this test will fail with the uncovered
text, forcing a coverage-map update.
"""

from __future__ import annotations

import re
from pathlib import Path


CONTRACT_PATH = Path(__file__).parent.parent / "docs" / "family" / "ADAPTER_CONTRACT_v1.md"


# ---------------------------------------------------------------------------
# Hand-maintained coverage map.
# Keys = slug of the MUST-bearing line in ADAPTER_CONTRACT_v1.md.
# Values = list of acceptance-test ids from Plan 02-01 frontmatter
# (contract.acceptance_tests[*].id). At least one mapping per MUST
# clause; multiple are allowed and encouraged.
# ---------------------------------------------------------------------------


MUST_COVERAGE: dict[str, list[str]] = {
    # "The adapter MUST NOT exhibit any of the following patterns..."
    "the_adapter_must_not_exhibit_any": [
        "test-forbidden-patterns",
    ],
    # "Fields MUST conform to BenchmarkManifest / BenchmarkItem..."
    "fields_must_conform_to_benchmarkmanifest_benchmarkitem": [
        "test-adapter-roundtrip",
    ],
    # "... every item that exposes that route MUST use the same vector length..."
    "route_name_every_item_that_exposes": [
        "test-adapter-roundtrip",
    ],
    # "The emitted manifest MUST round-trip cleanly through load_manifest..."
    "the_emitted_manifest_must_round_trip": [
        "test-adapter-roundtrip",
    ],
    # "... governing route pixel_full_concat_31d_single MUST be carried..."
    "governing_route_pixel_full_concat_31d_single_must_be_carried": [
        "test-adapter-roundtrip",
        "test-label-surface-carried",
    ],
    # "Missing reference-label entries are an error: every item MUST carry the chosen reference key."
    "4_missing_reference_label_entries_are": [
        "test-label-surface-carried",
    ],
    # "The adapter MUST NOT fill NaNs with zeros, means, or medians."
    "the_adapter_must_not_fill_nans": [
        "test-freeze-mismatch-exit-code",  # the adapter exits 2 on NaN-strict, covered together with the drop-item flag
    ],
    # "... the adapter MUST compare the neutral sha256 against the upstream-declared SHA..."
    "icit_reference_frozen_json_the_adapter_must_compare": [
        "test-freeze-parity",
        "test-freeze-mismatch-exit-code",
    ],
    # "The run record MUST be written whether the adapter succeeds or fails..."
    "the_run_record_must_be_written": [
        "test-freeze-parity",
        "test-freeze-mismatch-exit-code",
    ],
}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def _slugify(line: str) -> str:
    words = re.findall(r"\w+", line.lower())
    first_six = words[:6]
    slug = "_".join(first_six)
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug)
    return slug.strip("_")


def _extract_must_lines(contract_text: str) -> list[tuple[int, str]]:
    """Return [(line_no, line_text), ...] for every non-code-block line with ``MUST``."""
    out: list[tuple[int, str]] = []
    in_code = False
    for line_no, line in enumerate(contract_text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if "MUST" in line:
            out.append((line_no, line))
    return out


def _extract_slugs(contract_text: str) -> dict[str, list[tuple[int, str]]]:
    slug_map: dict[str, list[tuple[int, str]]] = {}
    for line_no, line in _extract_must_lines(contract_text):
        slug = _slugify(line)
        slug_map.setdefault(slug, []).append((line_no, line.strip()))
    return slug_map


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_every_must_clause_is_covered() -> None:
    assert CONTRACT_PATH.exists(), f"contract file missing: {CONTRACT_PATH}"
    slugs = _extract_slugs(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert slugs, "no MUST clauses found -- parser or contract is broken"
    uncovered: list[str] = []
    for slug, occurrences in slugs.items():
        if slug not in MUST_COVERAGE:
            rendered = "; ".join(f"L{lno}: {text}" for lno, text in occurrences)
            uncovered.append(f"[{slug}] {rendered}")
    assert not uncovered, (
        "Contract has uncovered MUST clauses. Either add an acceptance "
        "test id in MUST_COVERAGE or record an accepted gap with an "
        "xfail test.\n" + "\n".join(uncovered)
    )


def test_coverage_map_has_no_stale_slugs() -> None:
    """Every slug in MUST_COVERAGE must correspond to a current contract line."""
    slugs = set(_extract_slugs(CONTRACT_PATH.read_text(encoding="utf-8")).keys())
    stale = sorted(k for k in MUST_COVERAGE if k not in slugs)
    assert not stale, (
        "MUST_COVERAGE contains entries that no longer match any MUST line in "
        "the contract: " + ", ".join(stale)
    )


def test_coverage_map_includes_core_acceptance_tests() -> None:
    """Sanity floor: the coverage map is not silently truncated."""
    all_ids = {tid for ids in MUST_COVERAGE.values() for tid in ids}
    assert "test-forbidden-patterns" in all_ids, (
        "test-forbidden-patterns must appear in MUST_COVERAGE"
    )
    assert "test-adapter-roundtrip" in all_ids, (
        "test-adapter-roundtrip must appear in MUST_COVERAGE"
    )

"""Shared pytest fixtures for Phase 02-01 adapter tests.

Exposes the three synthetic Phase-4-like fixtures plus a helper that
recomputes the canonical SHA-256 the frozen-reference fixture pins, so a
drifted fixture is caught at import time rather than deep inside a
test.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest


FIXTURES_DIR = Path(__file__).parent / "fixtures"

FEATURE_MANIFEST_PATH = FIXTURES_DIR / "phase4_like_feature_manifest.json"
REFERENCE_FROZEN_GOOD_PATH = FIXTURES_DIR / "phase4_like_reference_frozen.json"
REFERENCE_FROZEN_BAD_PATH = FIXTURES_DIR / "phase4_like_reference_frozen_mismatch.json"


def _compute_icit_sha(feature_manifest: dict) -> str:
    """Recompute the canonical SHA-256 over the governing label assignments."""
    assignments = {
        item["item_id"]: item["reference_labels"]["icit_set"]
        for item in feature_manifest["items"]
    }
    encoded = json.dumps(assignments, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@pytest.fixture(scope="session")
def phase4_like_paths() -> dict[str, Path]:
    """Return a dict of the three on-disk fixture paths."""
    return {
        "feature_manifest": FEATURE_MANIFEST_PATH,
        "reference_frozen_good": REFERENCE_FROZEN_GOOD_PATH,
        "reference_frozen_bad": REFERENCE_FROZEN_BAD_PATH,
    }


@pytest.fixture(scope="session")
def phase4_like_fixture_sha() -> str:
    """Return the SHA the fixture ships with, re-verified against the manifest."""
    feature_manifest = json.loads(FEATURE_MANIFEST_PATH.read_text(encoding="utf-8"))
    frozen = json.loads(REFERENCE_FROZEN_GOOD_PATH.read_text(encoding="utf-8"))
    expected = _compute_icit_sha(feature_manifest)
    assert frozen["sha256"] == expected, (
        "frozen-reference fixture SHA drifted from its feature manifest; "
        "regenerate tests/fixtures/phase4_like_reference_frozen.json"
    )
    return expected

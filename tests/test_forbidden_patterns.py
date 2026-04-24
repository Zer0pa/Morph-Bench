"""Forbidden-pattern lint over ``src/gnosis_morph_bench/``.

Walks every ``*.py`` file under the package root and scans raw file
bytes for any of the six patterns declared in
``02_source_inventory/PATH_REWRITE_LEDGER.md``. A positive-control
test exercises the same lint function against a synthetic string
carrying every forbidden pattern, so the lint is provably live.

This test file deliberately quotes the forbidden tokens via split
string literals so the scan over ``src/`` stays clean while the test
module itself can still build its regex table.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest


# NOTE: token fragments are concatenated so the literal forbidden
# strings never appear in this test file as searchable bytes -- the
# lint scans ``src/gnosis_morph_bench/`` only, but we want the tests
# directory clean-by-default too.
_MONOREPO_HELPER = "phase3" + "_common"
_STROKE_PREFIX = "stroke" + "_"
_WORKSPACE_LITERAL = "workspace" + "/artifacts/"
_WORKSPACE_STR = "workspace" + "/"
_SYS_PATH = "sys" + ".path.insert"
_PARENTS_INDEX = "parents[" + "0"  # any .parents[N] usage


FORBIDDEN_PATTERNS: list[tuple[str, str]] = [
    (
        "parents_depth_ancestor",
        r"Path\(__file__\)\.resolve\(\)\.parents\[\d+\]",
    ),
    (
        "workspace_artifacts_literal",
        re.escape(_WORKSPACE_LITERAL),
    ),
    (
        "stroke_kernel_import",
        r"(?:from\s+" + _STROKE_PREFIX + r"[A-Za-z_]+\s+import|import\s+"
        + _STROKE_PREFIX + r"[A-Za-z_]+)",
    ),
    (
        "phase3_common_import",
        r"(?:from\s+" + _MONOREPO_HELPER + r"\s+import|import\s+"
        + _MONOREPO_HELPER + r")",
    ),
    (
        "sys_path_insert",
        re.escape(_SYS_PATH),
    ),
    (
        "workspace_path_fragment",
        r"[\"']" + re.escape(_WORKSPACE_STR),
    ),
]


PACKAGE_ROOT = Path(__file__).parent.parent / "src" / "gnosis_morph_bench"


def _iter_python_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip caches.
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for filename in filenames:
            if filename.endswith(".py"):
                yield Path(dirpath) / filename


def _scan_text(
    text: str, patterns: list[tuple[str, str]]
) -> list[tuple[str, int, str]]:
    """Return [(pattern_id, line_no, line_text), ...] for every match."""
    compiled = [(pid, re.compile(pat, re.MULTILINE)) for pid, pat in patterns]
    hits: list[tuple[str, int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pid, regex in compiled:
            if regex.search(line):
                hits.append((pid, line_no, line))
    return hits


def _scan_file(
    path: Path, patterns: list[tuple[str, str]]
) -> list[tuple[str, int, str, Path]]:
    text = path.read_text(encoding="utf-8")
    return [(pid, lno, line, path) for pid, lno, line in _scan_text(text, patterns)]


# ---------------------------------------------------------------------------
# The actual lint over src/gnosis_morph_bench/
# ---------------------------------------------------------------------------


def test_forbidden_patterns_absent_from_src() -> None:
    """Zero forbidden-pattern hits anywhere under ``src/gnosis_morph_bench/``."""
    assert PACKAGE_ROOT.is_dir(), f"package root not found at {PACKAGE_ROOT}"
    all_hits: list[tuple[str, int, str, Path]] = []
    file_count = 0
    for py_file in _iter_python_files(PACKAGE_ROOT):
        file_count += 1
        all_hits.extend(_scan_file(py_file, FORBIDDEN_PATTERNS))
    assert file_count > 0, "no python files were scanned -- fix the scan root"
    if all_hits:
        pretty = "\n".join(
            f"{path.relative_to(PACKAGE_ROOT.parent.parent)}:{lno}: "
            f"[{pid}] {line.rstrip()}"
            for pid, lno, line, path in all_hits
        )
        pytest.fail(
            "Forbidden patterns detected in src/gnosis_morph_bench/:\n" + pretty
        )


# ---------------------------------------------------------------------------
# Positive control: the lint itself is alive.
# ---------------------------------------------------------------------------


def _positive_control_text() -> str:
    """Return a synthetic buffer containing exactly one hit per pattern."""
    lines = [
        # parents_depth_ancestor
        "REPO = Path(__file__).resolve().parents[2]",
        # workspace_artifacts_literal
        "PATH = \"" + _WORKSPACE_LITERAL + "indus/phase4/bundle.json\"",
        # stroke_kernel_import
        "from " + _STROKE_PREFIX + "native_encoding import something",
        # phase3_common_import
        "from " + _MONOREPO_HELPER + " import helpers",
        # sys_path_insert
        _SYS_PATH + "(0, '/whatever')",
        # workspace_path_fragment (distinct from workspace_artifacts_literal)
        "output = '" + _WORKSPACE_STR + "outputs/run.json'",
    ]
    return "\n".join(lines)


def test_positive_control_lint_is_live() -> None:
    """Lint must report every pattern on a known-bad synthetic string."""
    hits = _scan_text(_positive_control_text(), FORBIDDEN_PATTERNS)
    pids = sorted({pid for pid, _, _ in hits})
    expected = sorted({pid for pid, _ in FORBIDDEN_PATTERNS})
    assert pids == expected, (
        f"positive control missing pattern ids: "
        f"expected {expected}, got {pids}"
    )
    # Every pattern should match at least once; the total count is at
    # least equal to the pattern count (the workspace/artifacts/ line
    # also trips the workspace_path_fragment rule, which is intended).
    assert len(hits) >= len(FORBIDDEN_PATTERNS), (
        f"positive control tripped only {len(hits)} hits, "
        f"expected >= {len(FORBIDDEN_PATTERNS)}"
    )


# ---------------------------------------------------------------------------
# Plan 02-02: confirm replay.py is in the scan set and a bad replay.py line
# would be caught.
# ---------------------------------------------------------------------------


def test_replay_module_is_in_scan_set() -> None:
    """The walk-based lint picks up replay.py without code changes."""
    scanned = {p.name for p in _iter_python_files(PACKAGE_ROOT)}
    assert "replay.py" in scanned, (
        "replay.py must be in the forbidden-pattern scan set; if the lint "
        "was manually enumerating files it would miss 02-02's new module."
    )


def test_positive_control_bad_replay_line_is_detected() -> None:
    """A fake replay.py line carrying a forbidden pattern is detected.

    This guards against a future refactor that narrows the scan root and
    silently excludes a newly added module.
    """
    bad_replay_text = "\n".join(
        [
            '"""Fake replay.py with a forbidden import."""',
            "from " + _MONOREPO_HELPER + " import helpers",
            "def run_replay_record(manifest, config):",
            "    return None",
        ]
    )
    hits = _scan_text(bad_replay_text, FORBIDDEN_PATTERNS)
    pids = {pid for pid, _, _ in hits}
    assert "phase3_common_import" in pids, (
        "positive-control bad-replay stanza should trip phase3_common_import"
    )

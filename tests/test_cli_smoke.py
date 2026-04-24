"""CLI smoke-subcommand tests: explicit `smoke` path + legacy shim."""

from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stderr
from pathlib import Path

import pytest

from gnosis_morph_bench.cli import main


REPO_ROOT = Path(__file__).parent.parent
TINY_MANIFEST_PATH = str(REPO_ROOT / "fixtures" / "tiny_benchmark_manifest.json")


def test_cli_smoke_subcommand(tmp_path: Path) -> None:
    """Explicit `smoke <manifest>` writes schema_version=1 output."""
    output_path = tmp_path / "smoke_report.json"
    rc = main(
        [
            "smoke",
            TINY_MANIFEST_PATH,
            "--output",
            str(output_path),
        ]
    )
    assert rc == 0
    assert output_path.is_file()

    payload = json.loads(output_path.read_text())
    assert payload["schema_version"] == 1
    assert payload["manifest_name"] == "tiny-smoke"
    assert "replay" in payload
    assert payload["replay"]["mode"] == "deterministic_replay"
    assert "leave_fraction_out" in payload
    assert payload["leave_fraction_out"]["mode"] == "leave_fraction_out"


def test_cli_smoke_legacy_path(tmp_path: Path) -> None:
    """No subcommand + first positional = manifest path triggers the shim.

    The shim prepends `smoke` and emits a one-line deprecation note on
    stderr. The output file still lands at the requested --output path.
    """
    output_path = tmp_path / "smoke_report.json"
    stderr_buf = io.StringIO()
    with redirect_stderr(stderr_buf):
        rc = main(
            [
                TINY_MANIFEST_PATH,
                "--output",
                str(output_path),
            ]
        )
    assert rc == 0
    assert output_path.is_file()
    stderr = stderr_buf.getvalue()
    assert "deprecation" in stderr.lower()
    assert "smoke" in stderr

    payload = json.loads(output_path.read_text())
    assert payload["schema_version"] == 1

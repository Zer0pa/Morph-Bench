"""Repo-local helpers for JSON I/O, file hashing, and UTC timestamps.

Replaces any prior monorepo helper import the live source family relied
on. Only stdlib is imported; nothing here reaches outside its arguments.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def read_json(path):
    """Read and parse a JSON document at ``path`` using UTF-8 decoding."""
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)


def write_json(path, payload, *, indent: int = 2) -> None:
    """Write ``payload`` as JSON to ``path``, creating parents as needed.

    Uses ``sort_keys=True`` and ``ensure_ascii=False`` for deterministic,
    non-mangled output. Always terminates the file with a trailing newline.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=indent, sort_keys=True, ensure_ascii=False)
    target.write_text(text + "\n", encoding="utf-8")


def sha256_file(path) -> str:
    """Return the SHA-256 hex digest of the file at ``path``.

    Streams the file in 1 MiB chunks so large inputs do not explode memory.
    """
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string with seconds."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

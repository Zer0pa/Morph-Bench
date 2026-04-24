"""Unit tests for :mod:`gnosis_morph_bench.hf_cache`.

No real HF network calls are made. A stub opener-factory replays
canned byte streams so the loader's SHA-256 verification path, cache
placement, and mismatch cleanup are exercised deterministically.
"""

from __future__ import annotations

import hashlib
import io
from pathlib import Path

import pytest

from gnosis_morph_bench import hf_cache


class _StubResponse:
    """Minimal file-like stand-in for urllib's HTTPResponse."""

    def __init__(self, payload: bytes) -> None:
        self._buffer = io.BytesIO(payload)

    def read(self, size: int = -1) -> bytes:
        return self._buffer.read(size)

    def close(self) -> None:
        self._buffer.close()


class _StubOpener:
    """Captures the outbound Request and returns a canned response."""

    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self.last_request = None

    def open(self, request):
        self.last_request = request
        return _StubResponse(self._payload)


def _factory_for(opener: _StubOpener):
    def _build():
        return opener
    return _build


def test_fetch_artifact_writes_cache_and_verifies_sha(tmp_path: Path) -> None:
    payload = b'{"hello": "world"}\n'
    expected_sha = hashlib.sha256(payload).hexdigest()
    opener = _StubOpener(payload)

    result = hf_cache.fetch_artifact(
        repo="Zer0pa/gnosis-morph-bench-artifacts",
        artifact_path="replay/example.json",
        expected_sha256=expected_sha,
        cache_dir=tmp_path,
        token="fake-token",
        opener_factory=_factory_for(opener),
    )

    assert result.path == tmp_path / "Zer0pa/gnosis-morph-bench-artifacts/replay/example.json"
    assert result.path.is_file()
    assert result.path.read_bytes() == payload
    assert result.sha256 == expected_sha
    assert result.bytes_written == len(payload)

    # Bearer header was attached (token is never logged; just verified present).
    assert opener.last_request is not None
    assert opener.last_request.headers.get("Authorization") == "Bearer fake-token"
    assert opener.last_request.full_url == (
        "https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-artifacts"
        "/resolve/main/replay/example.json"
    )


def test_fetch_artifact_raises_on_sha_mismatch_and_removes_partial(
    tmp_path: Path,
) -> None:
    payload = b"real bytes here"
    bogus_sha = "0" * 64
    opener = _StubOpener(payload)

    expected_cache_path = (
        tmp_path / "Zer0pa/gnosis-morph-bench-artifacts/replay/bad.json"
    )

    with pytest.raises(hf_cache.Sha256MismatchError) as excinfo:
        hf_cache.fetch_artifact(
            repo="Zer0pa/gnosis-morph-bench-artifacts",
            artifact_path="replay/bad.json",
            expected_sha256=bogus_sha,
            cache_dir=tmp_path,
            token=None,
            opener_factory=_factory_for(opener),
        )

    assert "SHA-256 mismatch" in str(excinfo.value)
    # Partial file must be cleaned up on mismatch so stale bytes never
    # linger in the cache.
    assert not expected_cache_path.exists()


def test_fetch_artifact_rejects_non_hex_sha(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        hf_cache.fetch_artifact(
            repo="Zer0pa/gnosis-morph-bench-artifacts",
            artifact_path="replay/x.json",
            expected_sha256="not-a-hex-string",
            cache_dir=tmp_path,
        )


def test_fetch_artifact_rejects_wrong_length_sha(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        hf_cache.fetch_artifact(
            repo="Zer0pa/gnosis-morph-bench-artifacts",
            artifact_path="replay/x.json",
            expected_sha256="abc123",
            cache_dir=tmp_path,
        )


def test_fetch_artifact_omits_auth_when_no_token(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    payload = b"no-auth payload"
    opener = _StubOpener(payload)
    monkeypatch.delenv("HF_TOKEN", raising=False)

    result = hf_cache.fetch_artifact(
        repo="Zer0pa/gnosis-morph-bench-artifacts",
        artifact_path="replay/public.json",
        expected_sha256=hashlib.sha256(payload).hexdigest(),
        cache_dir=tmp_path,
        token=None,
        opener_factory=_factory_for(opener),
    )

    assert result.sha256 == hashlib.sha256(payload).hexdigest()
    assert opener.last_request is not None
    # No Authorization header emitted when neither arg nor env supplies one.
    assert opener.last_request.headers.get("Authorization") is None

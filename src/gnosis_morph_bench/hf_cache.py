"""SHA-256 pinned fetch-back for Hugging Face dataset artifacts.

Companion to ``docs/HF_STORAGE.md``. Consumers call
:func:`fetch_artifact` with a repo name, artifact path, and expected
SHA-256; the loader downloads the file from the HF HTTPS endpoint to
``artifacts/hf_cache/<repo_name>/<artifact_path>`` and verifies the
SHA-256 before declaring success. SHA mismatch is a hard failure that
deletes the partial download and raises
:class:`Sha256MismatchError`.

Only stdlib is used so blind clones reach this loader without any
optional dependency. Authentication is via the ``HF_TOKEN`` environment
variable; the token is never logged or written to disk by this module.
"""

from __future__ import annotations

import hashlib
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


HF_HOST = "https://huggingface.co"
DEFAULT_CACHE_DIR = Path("artifacts/hf_cache")
CHUNK_SIZE = 1 << 20  # 1 MiB


class Sha256MismatchError(RuntimeError):
    """Raised when a downloaded artifact's SHA-256 does not match the pin."""


class HfCacheError(RuntimeError):
    """Raised for any non-SHA fetch failure (network, auth, missing file)."""


@dataclass(frozen=True)
class FetchResult:
    """Outcome of a successful pinned fetch.

    ``path`` is the local cache path the file now lives at. ``sha256``
    is the verified hex SHA-256, equal to the pin the caller passed in.
    ``bytes_written`` is the number of bytes written to disk.
    """

    path: Path
    sha256: str
    bytes_written: int


def _hf_dataset_resolve_url(repo: str, artifact_path: str, revision: str) -> str:
    """Build the raw-file URL on the HF HTTPS endpoint for a dataset repo."""
    clean_path = artifact_path.lstrip("/")
    return f"{HF_HOST}/datasets/{repo}/resolve/{revision}/{clean_path}"


def _sha256_of_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _open_url(
    url: str, token: str | None, opener_factory=urllib.request.build_opener
):
    """Open an HF HTTPS URL with optional bearer auth.

    ``opener_factory`` is injectable so unit tests can stub out the
    network call without monkey-patching the stdlib.
    """
    request = urllib.request.Request(url)
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    opener = opener_factory()
    try:
        return opener.open(request)
    except urllib.error.HTTPError as exc:
        raise HfCacheError(
            f"HF fetch failed for {url}: HTTP {exc.code} {exc.reason}"
        ) from exc
    except urllib.error.URLError as exc:
        raise HfCacheError(f"HF fetch failed for {url}: {exc.reason}") from exc


def fetch_artifact(
    repo: str,
    artifact_path: str,
    expected_sha256: str,
    *,
    revision: str = "main",
    cache_dir: Path | str = DEFAULT_CACHE_DIR,
    token: str | None = None,
    opener_factory=urllib.request.build_opener,
) -> FetchResult:
    """Fetch ``artifact_path`` from the HF dataset repo ``repo`` and verify SHA.

    Parameters
    ----------
    repo:
        ``<org-or-user>/<name>`` form, e.g. ``"Architect-Prime/gnosis-morph-bench-artifacts"``.
    artifact_path:
        Path inside the HF repo, e.g.
        ``"replay/indus_phase4_live_2026-05-01.json"``.
    expected_sha256:
        Lowercase hex SHA-256 the file must match. 64 hex chars.
    revision:
        Git revision on the HF side. Defaults to ``"main"``.
    cache_dir:
        Root of the local cache. The file is written to
        ``<cache_dir>/<repo>/<artifact_path>``. Parents are created
        on demand.
    token:
        Optional HF bearer token. Falls back to the ``HF_TOKEN``
        environment variable if not supplied. Never logged.
    opener_factory:
        Injectable urllib opener factory for unit testing.

    Returns
    -------
    FetchResult
        With the cache path, verified SHA, and byte count.

    Raises
    ------
    ValueError
        If ``expected_sha256`` is not a 64-char hex string.
    Sha256MismatchError
        If the downloaded bytes do not hash to ``expected_sha256``.
        The partial cache file is deleted before raising.
    HfCacheError
        For network errors or HTTP errors (including 401/403/404).
    """
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise ValueError(
            "expected_sha256 must be a 64-char hex string, "
            f"got {len(expected_sha256) if isinstance(expected_sha256, str) else type(expected_sha256).__name__}"
        )
    try:
        int(expected_sha256, 16)
    except ValueError as exc:
        raise ValueError(
            f"expected_sha256 is not hex: {expected_sha256!r}"
        ) from exc

    resolved_token = token if token is not None else os.environ.get("HF_TOKEN")
    url = _hf_dataset_resolve_url(repo, artifact_path, revision)
    cache_root = Path(cache_dir)
    target = cache_root / repo / artifact_path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)

    bytes_written = 0
    response = _open_url(url, resolved_token, opener_factory=opener_factory)
    try:
        with target.open("wb") as handle:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                handle.write(chunk)
                bytes_written += len(chunk)
    finally:
        response.close()

    actual_sha = _sha256_of_file(target)
    if actual_sha != expected_sha256.lower():
        try:
            target.unlink()
        except OSError:
            # best-effort cleanup; the exception below is the real signal
            pass
        raise Sha256MismatchError(
            f"SHA-256 mismatch for {repo}:{artifact_path} "
            f"(expected {expected_sha256.lower()}, got {actual_sha}); "
            "partial file removed"
        )

    return FetchResult(path=target, sha256=actual_sha, bytes_written=bytes_written)


__all__ = [
    "DEFAULT_CACHE_DIR",
    "FetchResult",
    "HfCacheError",
    "Sha256MismatchError",
    "fetch_artifact",
]

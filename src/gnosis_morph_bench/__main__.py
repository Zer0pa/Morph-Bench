"""Module entrypoint so ``python -m gnosis_morph_bench <cmd> ...`` works.

Dispatches to :func:`gnosis_morph_bench.cli.main`.
"""

from __future__ import annotations

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())

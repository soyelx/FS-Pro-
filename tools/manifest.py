"""Generate ``fonts/manifest.json``: a machine-readable index of every font.

Usage::

    python -m tools.manifest           # (re)write the manifest
    python -m tools.manifest --check   # exit 1 if the committed manifest is stale
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from tools.catalog import REPO_ROOT, FontFile, discover, fonts_dir

SCHEMA_VERSION = 1


def manifest_path() -> Path:
    """Return the manifest location, honouring the optional ``MANIFEST_PATH`` env var."""
    configured = Path(os.environ.get("MANIFEST_PATH", "fonts/manifest.json"))
    return configured if configured.is_absolute() else REPO_ROOT / configured


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _entry(font: FontFile) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "path": font.relative_path(),
        "family": font.family,
        "style": font.style,
        "italic": font.italic,
        "variable": font.variable,
        "format": font.format,
        "bytes": font.path.stat().st_size,
        "sha256": _sha256(font.path),
    }
    if font.weight is not None:
        entry["cssWeight"] = font.weight
    return entry


def build(fonts: list[FontFile] | None = None) -> dict[str, Any]:
    entries = fonts if fonts is not None else discover()
    return {
        "schemaVersion": SCHEMA_VERSION,
        "license": "Apple San Francisco Font License (see NOTICE.md)",
        "fonts": [_entry(font) for font in entries],
    }


def render(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if the manifest is out of date")
    args = parser.parse_args(argv)

    target = manifest_path()
    expected = render(build())

    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != expected:
            print(f"{target} is out of date; run `python -m tools.manifest`.", file=sys.stderr)
            return 1
        print(f"OK: {target.relative_to(REPO_ROOT)} is up to date")
        return 0

    target.write_text(expected, encoding="utf-8")
    count = len(discover(fonts_dir()))
    print(f"Wrote {target.relative_to(REPO_ROOT)} ({count} fonts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

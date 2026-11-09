"""Validate that every font file is intact and matches its name and folder.

Usage::

    python -m tools.validate          # exit code 1 on any problem
"""

from __future__ import annotations

import sys
from pathlib import Path

from fontTools.ttLib import TTFont, TTLibError

from tools.catalog import FontFile, discover, expected_files, fonts_dir

# OS/2.fsSelection bit 0 marks an italic face.
_FS_SELECTION_ITALIC = 1 << 0
_REQUIRED_TABLES = ("name", "OS/2", "cmap", "head", "hhea", "hmtx", "maxp", "post")


def _family_name(font: TTFont) -> str | None:
    name = font["name"]
    # Prefer the typographic family (ID 16); fall back to the legacy family (ID 1).
    return name.getDebugName(16) or name.getDebugName(1)


def check_font(entry: FontFile) -> list[str]:
    """Return a list of human-readable problems for one font (empty = OK)."""
    label = entry.path.name
    try:
        font = TTFont(entry.path, lazy=True)
    except (TTLibError, OSError) as exc:
        return [f"{label}: cannot be parsed ({exc})"]

    problems: list[str] = []
    try:
        missing = [tag for tag in _REQUIRED_TABLES if tag not in font]
        if missing:
            problems.append(f"{label}: missing tables {', '.join(missing)}")
            return problems

        expected_outline = "glyf" if entry.variable else "CFF "
        if expected_outline not in font:
            problems.append(f"{label}: expected {expected_outline.strip()} outlines")

        if ("fvar" in font) != entry.variable:
            kind = "variable" if entry.variable else "static"
            problems.append(f"{label}: file name implies a {kind} font")

        family = _family_name(font)
        if family != entry.family:
            problems.append(f"{label}: family is {family!r}, expected {entry.family!r}")

        is_italic = bool(font["OS/2"].fsSelection & _FS_SELECTION_ITALIC)
        if is_italic != entry.italic:
            problems.append(f"{label}: italic flag is {is_italic}, file name says {entry.italic}")

        copyright_notice = font["name"].getDebugName(0) or ""
        if "Apple" not in copyright_notice:
            problems.append(f"{label}: Apple copyright notice is missing from the name table")
    finally:
        font.close()
    return problems


def validate(root: Path | None = None) -> list[str]:
    """Validate the whole collection and return every problem found."""
    base = root if root is not None else fonts_dir()
    problems: list[str] = []
    try:
        entries = discover(base)
    except ValueError as exc:
        return [str(exc)]

    present = {f"{e.folder}/{e.path.name}" for e in entries}
    for name in sorted(expected_files() - present):
        problems.append(f"missing font: {name}")
    for name in sorted(present - expected_files()):
        problems.append(f"unexpected font: {name}")

    for entry in entries:
        problems.extend(check_font(entry))
    return problems


def main() -> int:
    problems = validate()
    if problems:
        print(f"Found {len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"OK: {len(discover())} font files validated in {fonts_dir()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Discover and describe the font files shipped in this repository.

The catalog is derived purely from the directory layout and file names, so it
can be computed without opening any binary font data. ``tools.validate`` then
cross-checks this metadata against the actual font tables.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

#: Static style names mapped to their standard CSS ``font-weight`` value.
WEIGHTS: dict[str, int] = {
    "Ultralight": 100,
    "Thin": 200,
    "Light": 300,
    "Regular": 400,
    "Medium": 500,
    "Semibold": 600,
    "Bold": 700,
    "Heavy": 800,
    "Black": 900,
}

#: Sub-directory of ``fonts/`` -> font family name stored in the font itself.
FAMILIES: dict[str, str] = {
    "display": "SF Pro Display",
    "text": "SF Pro Text",
    "rounded": "SF Pro Rounded",
    "variable": "SF Pro",
}

#: Families that ship an italic for every static weight.
FAMILIES_WITH_ITALICS: frozenset[str] = frozenset({"display", "text"})

_STATIC_RE = re.compile(
    r"^SF-Pro-(?P<family>Display|Text|Rounded)-"
    r"(?P<style>" + "|".join(WEIGHTS) + r")(?P<italic>Italic)?\.otf$"
)
_VARIABLE_RE = re.compile(r"^SF-Pro(?P<italic>-Italic)?\.ttf$")

FONT_SUFFIXES: frozenset[str] = frozenset({".otf", ".ttf"})


@dataclass(frozen=True, slots=True)
class FontFile:
    """Metadata for one font file, derived from its location and name."""

    path: Path
    folder: str
    family: str
    style: str
    italic: bool
    variable: bool

    @property
    def weight(self) -> int | None:
        """CSS weight for static fonts; ``None`` for variable fonts."""
        return None if self.variable else WEIGHTS[self.style]

    @property
    def format(self) -> str:
        return "truetype-variable" if self.variable else "opentype-cff"

    def relative_path(self, root: Path = REPO_ROOT) -> str:
        return self.path.resolve().relative_to(root.resolve()).as_posix()


def fonts_dir() -> Path:
    """Return the fonts directory, honouring the optional ``FONTS_DIR`` env var."""
    configured = os.environ.get("FONTS_DIR", "fonts")
    path = Path(configured)
    return path if path.is_absolute() else REPO_ROOT / path


def parse_font_path(path: Path) -> FontFile:
    """Build a :class:`FontFile` from ``fonts/<folder>/<file>``.

    Raises:
        ValueError: if the folder is unknown or the file name does not follow
            the ``SF-Pro-<Family>-<Style>[Italic].otf`` /
            ``SF-Pro[-Italic].ttf`` convention for that folder.
    """
    folder = path.parent.name
    if folder not in FAMILIES:
        raise ValueError(f"{path}: unknown font folder {folder!r}")

    if folder == "variable":
        match = _VARIABLE_RE.match(path.name)
        if not match:
            raise ValueError(f"{path}: expected SF-Pro.ttf or SF-Pro-Italic.ttf")
        italic = bool(match["italic"])
        return FontFile(
            path=path,
            folder=folder,
            family=FAMILIES[folder],
            style="Italic" if italic else "Roman",
            italic=italic,
            variable=True,
        )

    match = _STATIC_RE.match(path.name)
    if not match:
        raise ValueError(f"{path}: name does not match SF-Pro-<Family>-<Style>.otf")
    if match["family"].lower() != folder:
        raise ValueError(f"{path}: {match['family']} font stored in {folder}/")
    return FontFile(
        path=path,
        folder=folder,
        family=FAMILIES[folder],
        style=match["style"],
        italic=bool(match["italic"]),
        variable=False,
    )


def discover(root: Path | None = None) -> list[FontFile]:
    """Return every font under ``root`` (default: :func:`fonts_dir`), sorted."""
    base = root if root is not None else fonts_dir()
    paths = sorted(p for p in base.rglob("*") if p.suffix.lower() in FONT_SUFFIXES)
    return [parse_font_path(p) for p in paths]


def expected_files() -> set[str]:
    """The complete set of ``<folder>/<file>`` names this collection should contain."""
    names: set[str] = {"variable/SF-Pro.ttf", "variable/SF-Pro-Italic.ttf"}
    for folder in ("display", "text", "rounded"):
        family = folder.capitalize()
        for style in WEIGHTS:
            names.add(f"{folder}/SF-Pro-{family}-{style}.otf")
            if folder in FAMILIES_WITH_ITALICS:
                names.add(f"{folder}/SF-Pro-{family}-{style}Italic.otf")
    return names

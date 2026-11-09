from pathlib import Path

import pytest

from tools.catalog import REPO_ROOT, discover, fonts_dir
from tools.manifest import build, manifest_path, render
from tools.validate import check_font, validate

FONTS = discover()


def test_collection_is_complete_and_valid() -> None:
    assert validate() == []


def test_no_fonts_left_in_repository_root() -> None:
    stray = [p.name for p in REPO_ROOT.iterdir() if p.suffix.lower() in {".otf", ".ttf"}]
    assert stray == []


@pytest.mark.parametrize("font", FONTS, ids=lambda f: f.path.name)
def test_font_matches_its_name(font) -> None:
    assert check_font(font) == []


def test_corrupt_font_is_reported(tmp_path: Path) -> None:
    folder = tmp_path / "text"
    folder.mkdir()
    (folder / "SF-Pro-Text-Regular.otf").write_bytes(b"not a font")
    problems = validate(tmp_path)
    assert any("cannot be parsed" in p for p in problems)
    assert any(p.startswith("missing font:") for p in problems)


def test_committed_manifest_is_up_to_date() -> None:
    assert manifest_path().read_text(encoding="utf-8") == render(build())


def test_manifest_lists_every_font_once() -> None:
    paths = [entry["path"] for entry in build()["fonts"]]
    assert len(paths) == len(set(paths)) == len(discover(fonts_dir()))

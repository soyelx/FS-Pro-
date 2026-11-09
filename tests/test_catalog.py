from pathlib import Path

import pytest

from tools.catalog import WEIGHTS, expected_files, parse_font_path


def test_static_font_name_is_parsed() -> None:
    font = parse_font_path(Path("fonts/display/SF-Pro-Display-SemiboldItalic.otf"))
    assert font.family == "SF Pro Display"
    assert font.style == "Semibold"
    assert font.italic is True
    assert font.variable is False
    assert font.weight == 600


def test_bold_maps_to_css_700() -> None:
    font = parse_font_path(Path("fonts/text/SF-Pro-Text-Bold.otf"))
    assert font.weight == 700


def test_variable_font_has_no_fixed_weight() -> None:
    font = parse_font_path(Path("fonts/variable/SF-Pro-Italic.ttf"))
    assert font.variable is True
    assert font.italic is True
    assert font.weight is None


def test_font_in_wrong_folder_is_rejected() -> None:
    with pytest.raises(ValueError, match="stored in text/"):
        parse_font_path(Path("fonts/text/SF-Pro-Display-Regular.otf"))


def test_unknown_folder_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown font folder"):
        parse_font_path(Path("fonts/misc/SF-Pro-Text-Regular.otf"))


def test_badly_named_file_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_font_path(Path("fonts/text/sf-pro-text-regular.otf"))


def test_expected_collection_size() -> None:
    # 9 weights x 2 (roman + italic) for Display and Text, 9 for Rounded, 2 variable.
    assert len(WEIGHTS) == 9
    assert len(expected_files()) == 18 + 18 + 9 + 2

<div align="center">

# SF Pro Fonts

**Apple's San Francisco Pro typeface — every official weight, neatly organised, validated and indexed.**

[![CI](https://github.com/soyelx/FS-Pro-/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/soyelx/FS-Pro-/actions/workflows/ci.yml)
[![Stars](https://img.shields.io/github/stars/soyelx/FS-Pro-?style=flat&logo=github)](https://github.com/soyelx/FS-Pro-/stargazers)
[![Forks](https://img.shields.io/github/forks/soyelx/FS-Pro-?style=flat&logo=github)](https://github.com/soyelx/FS-Pro-/network/members)
[![License: MIT (tooling)](https://img.shields.io/github/license/soyelx/FS-Pro-?label=license%20%28tooling%29)](LICENSE)
[![Fonts: Apple license](https://img.shields.io/badge/fonts-Apple%20license-lightgrey?logo=apple)](NOTICE.md)
![Font files](https://img.shields.io/badge/font%20files-47-blue)

[Overview](#overview--architecture) •
[Features](#core-features) •
[Tech stack](#tech-stack) •
[Getting started](#getting-started) •
[Structure](#project-structure) •
[Usage](#usage-guide) •
[Contributing](#contributing) •
[License](#license)

</div>

> [!IMPORTANT]
> The fonts are **© Apple Inc.** and are **not** MIT-licensed. Apple allows them
> only for creating UI mock-ups for Apple platforms. The MIT license covers this
> repository's docs and tooling only. Read [`NOTICE.md`](NOTICE.md) before use.

---

## Overview & Architecture

This repository is a curated mirror of the **SF Pro** font family as published at
[developer.apple.com/fonts](https://developer.apple.com/fonts/). It has no
application server, API or database: it is a set of font files plus small
Python tooling that proves the collection is complete and intact.

```text
            ┌───────────────────────────┐
            │  fonts/<family>/*.otf|ttf │  47 official Apple font files
            └─────────────┬─────────────┘
                          │ discovered by
                          ▼
            ┌───────────────────────────┐
            │      tools/catalog.py     │  folder + file name → family, weight, italic
            └──────┬─────────────┬──────┘
                   │             │
                   ▼             ▼
   ┌────────────────────┐   ┌────────────────────────┐
   │ tools/validate.py  │   │   tools/manifest.py    │
   │ parses each font,  │   │ writes                 │
   │ checks name/italic │   │ fonts/manifest.json    │
   │ /outline/copyright │   │ (size, sha256, weight) │
   └─────────┬──────────┘   └───────────┬────────────┘
             └────────────┬─────────────┘
                          ▼
            ┌───────────────────────────┐
            │  GitHub Actions (ci.yml)  │  lint → validate → manifest check → pytest
            └───────────────────────────┘
```

## Core Features

- **Complete family** — SF Pro Display and SF Pro Text (9 weights, roman and italic), SF Pro Rounded (9 weights) and the SF Pro variable fonts (roman and italic).
- **Organised by family** — files sorted into `display/`, `text/`, `rounded/` and `variable/` instead of 47 files in one folder.
- **Integrity checks** — every file is parsed with [fontTools](https://github.com/fonttools/fonttools); family name, italic flag, outline format, variable axes and Apple's copyright notice are checked against the file name.
- **Machine-readable manifest** — `fonts/manifest.json` lists each font's path, family, style, CSS weight, size and SHA-256, so scripts and design tools can find the right file and confirm it hasn't changed.
- **Fast CI** — lazy font loading checks all 47 files in under a second; a matrix runs on Python 3.10 and 3.12.
- **Clean history** — binary-safe `.gitattributes`, `.editorconfig`, and Conventional Commits.

### Font inventory

| Family          | Folder            | Format             | Weights | Italics | Files |
| --------------- | ----------------- | ------------------ | :-----: | :-----: | :---: |
| SF Pro Display  | `fonts/display/`  | OpenType (CFF)     | 9       | ✅      | 18    |
| SF Pro Text     | `fonts/text/`     | OpenType (CFF)     | 9       | ✅      | 18    |
| SF Pro Rounded  | `fonts/rounded/`  | OpenType (CFF)     | 9       | —       | 9     |
| SF Pro          | `fonts/variable/` | TrueType variable  | 1–1000  | ✅      | 2     |

Variable font axes: `wght` 1–1000, `opsz` 17–28; the italic adds `YAXS` 400–1000.

> **Display vs Text:** Apple's guidance is to use **Text** below 20 pt and
> **Display** at 20 pt and above. The variable font switches automatically through its `opsz` axis.

## Tech Stack

| Category          | Technology                                   | Purpose                                     |
| ----------------- | -------------------------------------------- | ------------------------------------------- |
| Assets            | OpenType CFF (`.otf`), TrueType variable (`.ttf`) | Apple's original font binaries          |
| Tooling           | Python 3.10+, [fontTools](https://github.com/fonttools/fonttools) | Font parsing, validation, manifest |
| Testing           | pytest                                       | Unit and integrity tests                    |
| Code quality      | Ruff, markdownlint                           | Python lint/format, Markdown lint           |
| DevOps            | GitHub Actions                               | CI on every push and pull request to `main` |
| Backend / Database / Cache | —                                   | Not applicable: no server or data store     |

## Getting Started

### Prerequisites

- **Git**
- **Python 3.10+** — only needed to run the tooling, not to install the fonts.

### 1. Get the fonts

```bash
git clone https://github.com/soyelx/FS-Pro-.git
cd FS-Pro-
```

### 2. Install on your machine

| OS      | Steps |
| ------- | ----- |
| macOS   | Select the files in `fonts/` → double-click → **Install Font** in Font Book. Or copy them to `~/Library/Fonts/`. |
| Windows | Select the files → right-click → **Install** (or **Install for all users**). |
| Linux   | `mkdir -p ~/.local/share/fonts/sf-pro && cp -r fonts/*/ ~/.local/share/fonts/sf-pro/ && fc-cache -f` |

Then choose **SF Pro Display**, **SF Pro Text**, **SF Pro Rounded** or **SF Pro** in Figma, Sketch, Keynote and other design tools.

### 3. Set up the tooling (optional)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env               # optional: only to override default paths
```

### 4. Run the checks

```bash
python -m tools.validate           # development: verify every font
python -m tools.manifest           # regenerate fonts/manifest.json
python -m tools.manifest --check   # CI/production: fail if the manifest is stale
pytest                             # unit tests
ruff check . && ruff format --check .
```

### Environment variables

Both are optional; see [`.env.example`](.env.example).

| Variable        | Default               | Description                                   |
| --------------- | --------------------- | --------------------------------------------- |
| `FONTS_DIR`     | `fonts`               | Folder containing the family sub-folders.     |
| `MANIFEST_PATH` | `fonts/manifest.json` | Output path for `python -m tools.manifest`.   |

## Project Structure

```text
FS-Pro-/
├── .github/
│   └── workflows/
│       └── ci.yml            # Lint, validate fonts, check manifest, run tests
├── fonts/
│   ├── display/              # SF Pro Display — 9 weights × roman/italic (.otf)
│   ├── text/                 # SF Pro Text    — 9 weights × roman/italic (.otf)
│   ├── rounded/              # SF Pro Rounded — 9 weights (.otf)
│   ├── variable/             # SF-Pro.ttf, SF-Pro-Italic.ttf (variable)
│   └── manifest.json         # Generated index: path, style, weight, size, sha256
├── tools/
│   ├── catalog.py            # Discovers fonts and derives metadata from names
│   ├── validate.py           # Checks each font's tables against its name
│   └── manifest.py           # Generates / checks fonts/manifest.json
├── tests/                    # pytest suite for the tooling and the collection
├── .editorconfig             # Consistent whitespace across editors
├── .env.example              # Optional path overrides for the tooling
├── .gitattributes            # Marks fonts as binary
├── .gitignore                # Python, Node, OS, build and secret files
├── .markdownlint.jsonc       # Markdown lint rules
├── CONTRIBUTING.md           # How to contribute
├── LICENSE                   # MIT — tooling and docs only
├── NOTICE.md                 # Licensing split: Apple fonts vs MIT tooling
├── pyproject.toml            # Project metadata, pytest and Ruff config
├── requirements-dev.txt      # Pinned tooling dependencies
└── README.md
```

## Usage Guide

### Pick the right file

| CSS weight | Style      | Display file                     | Text file                     | Rounded file                     |
| :--------: | ---------- | -------------------------------- | ----------------------------- | -------------------------------- |
| 100        | Ultralight | `SF-Pro-Display-Ultralight.otf`  | `SF-Pro-Text-Ultralight.otf`  | `SF-Pro-Rounded-Ultralight.otf`  |
| 200        | Thin       | `SF-Pro-Display-Thin.otf`        | `SF-Pro-Text-Thin.otf`        | `SF-Pro-Rounded-Thin.otf`        |
| 300        | Light      | `SF-Pro-Display-Light.otf`       | `SF-Pro-Text-Light.otf`       | `SF-Pro-Rounded-Light.otf`       |
| 400        | Regular    | `SF-Pro-Display-Regular.otf`     | `SF-Pro-Text-Regular.otf`     | `SF-Pro-Rounded-Regular.otf`     |
| 500        | Medium     | `SF-Pro-Display-Medium.otf`      | `SF-Pro-Text-Medium.otf`      | `SF-Pro-Rounded-Medium.otf`      |
| 600        | Semibold   | `SF-Pro-Display-Semibold.otf`    | `SF-Pro-Text-Semibold.otf`    | `SF-Pro-Rounded-Semibold.otf`    |
| 700        | Bold       | `SF-Pro-Display-Bold.otf`        | `SF-Pro-Text-Bold.otf`        | `SF-Pro-Rounded-Bold.otf`        |
| 800        | Heavy      | `SF-Pro-Display-Heavy.otf`       | `SF-Pro-Text-Heavy.otf`       | `SF-Pro-Rounded-Heavy.otf`       |
| 900        | Black      | `SF-Pro-Display-Black.otf`       | `SF-Pro-Text-Black.otf`       | `SF-Pro-Rounded-Black.otf`       |

Italic Display/Text files add `Italic` before the extension, e.g. `SF-Pro-Text-BoldItalic.otf`.

> Apple's Bold files report weight class 600 internally (same as Semibold). The
> manifest's `cssWeight` uses the standard CSS value 700.

### Read the manifest

`fonts/manifest.json` sample entry:

```json
{
  "path": "fonts/text/SF-Pro-Text-Regular.otf",
  "family": "SF Pro Text",
  "style": "Regular",
  "italic": false,
  "variable": false,
  "format": "opentype-cff",
  "bytes": 2230172,
  "cssWeight": 400,
  "sha256": "…"
}
```

Find every italic Display file with [`jq`](https://jqlang.github.io/jq/):

```bash
jq -r '.fonts[] | select(.family == "SF Pro Display" and .italic) | .path' fonts/manifest.json
```

Or from Python:

```python
import json
from pathlib import Path

manifest = json.loads(Path("fonts/manifest.json").read_text())
bold = [f["path"] for f in manifest["fonts"] if f.get("cssWeight") == 700]
```

### Verify a download

```bash
python -m tools.validate
# OK: 47 font files validated in …/fonts
```

On failure the command exits with code `1` and lists each problem, e.g. `missing font: text/SF-Pro-Text-Bold.otf`.

### On the web

Apple's license doesn't cover embedding these files with `@font-face`. To show SF Pro to visitors on Apple devices, use the system font stack, which loads the copy built into the device:

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
```

## Contributing

Contributions to the docs and tooling are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup, checks and commit conventions. In short:

1. Fork the repo and create a branch: `git checkout -b docs/improve-install-guide`.
2. Make your change and run `python -m tools.validate && pytest`.
3. Commit with a [Conventional Commit](https://www.conventionalcommits.org/) message.
4. Open a pull request against `main`; CI must pass.

## License

- **Tooling, docs and configuration:** [MIT](LICENSE) © 2026 soyelx.
- **Font files:** © Apple Inc., under the *License Agreement for the Apple San Francisco Font*. Not covered by MIT. See [`NOTICE.md`](NOTICE.md).

San Francisco and SF Pro are trademarks of Apple Inc. This project is not affiliated with or endorsed by Apple.

# Contributing

Thanks for helping keep this collection tidy. Because the fonts themselves are
Apple's work, contributions focus on **organisation, tooling and documentation**.

## What we accept

- Fixes and improvements to the README, `NOTICE.md` or this guide.
- Improvements to the Python tooling in `tools/` and its tests in `tests/`.
- Replacing fonts with a **newer official release** downloaded directly from
  <https://developer.apple.com/fonts/> (state the version in the pull request).

## What we do not accept

- Modified, converted (e.g. `.woff2`) or third-party re-exports of the fonts.
- Fonts that are not part of SF Pro (SF Mono, SF Compact, New York, …) — those
  belong in separate repositories.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Before opening a pull request

```bash
ruff check . && ruff format --check .   # lint & formatting
python -m tools.validate                # every font parses and matches its name
python -m tools.manifest                # regenerate fonts/manifest.json if fonts changed
pytest                                  # unit tests
```

CI runs the same checks on every push and pull request to `main`.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Type       | Use for                                  |
| ---------- | ---------------------------------------- |
| `feat`     | new tooling capability                   |
| `fix`      | bug fix in tooling or a broken font file |
| `docs`     | documentation only                       |
| `refactor` | moving or renaming files, no behaviour change |
| `test`     | adding or updating tests                 |
| `ci`       | workflow changes                         |
| `chore`    | repository housekeeping                  |

Example: `fix(validate): report missing name table instead of crashing`.

## Naming rules

Files must live in the folder for their family and follow the existing names;
`python -m tools.validate` enforces this.

| Folder             | Pattern                                    |
| ------------------ | ------------------------------------------ |
| `fonts/display/`   | `SF-Pro-Display-<Weight>[Italic].otf`      |
| `fonts/text/`      | `SF-Pro-Text-<Weight>[Italic].otf`         |
| `fonts/rounded/`   | `SF-Pro-Rounded-<Weight>.otf`              |
| `fonts/variable/`  | `SF-Pro.ttf`, `SF-Pro-Italic.ttf`          |

`<Weight>` is one of: Ultralight, Thin, Light, Regular, Medium, Semibold, Bold,
Heavy, Black.

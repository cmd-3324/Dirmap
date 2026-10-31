# DIRMAP - Directory Analyzer

A small, dependency-free **Python command-line tool** that scans, analyzes, and reports on directory structures and file metadata.

## Features

| Feature | Description |
|---------|-------------|
| **File scanning** | Recursively traverses a directory and collects file metadata (name, size, type, modified date) |
| **File analysis** | Counts files by type, lists the largest files, totals size by extension, and shows the oldest/newest files |
| **Duplicate detection** | Finds duplicate files by both name and size |
| **Empty folder detection** | Identifies empty directories in the scanned hierarchy |
| **Tree visualization** | Displays the folder structure as an ASCII tree |
| **Data export** | Exports scan results to CSV and JSON |
| **Interactive menu** | Box-drawing character interface — no arguments needed |

## Requirements

- Python **3.13+**
- No third-party runtime dependencies

## Installation

Clone the repository and install it with [uv](https://docs.astral.sh/uv/):

```bash
git clone <repo-url>
cd Dirmap
uv sync
```

Or with `pip`:

```bash
git clone <repo-url>
cd Dirmap
pip install .
```

## Usage

Run the interactive menu:

```bash
uv run dirmap      # with uv
dirmap             # after pip install
python -m dirmap   # run as a module from the project root
```

From the menu:

| Option | Action |
|--------|--------|
| `1` | Scan a folder and count files |
| `2` | Analyze a folder (types, largest files, sizes, age range, empty folders) |
| `3` | Find duplicate files by name and size |
| `4` | Export the scan to `output/results.csv` and `output/result.json` |
| `5` | Print the folder tree (configurable max depth) |
| `6` | Exit |

Pressing Enter without a path uses the current directory (`.`). Export paths can be overridden when calling `export_csv()` / `export_json()` directly.

## Project Structure

```
Dirmap/
├── pyproject.toml
├── README.md
├── output/                  # Generated scan reports (gitignored)
└── src/dirmap/
    ├── __init__.py
    ├── __main__.py          # `python -m dirmap`
    ├── core/                # Scanning and analysis
    │   ├── scanner.py       # Recursive file scanning
    │   ├── analyzer.py      # Statistics: types, sizes, age, empty folders
    │   └── duplicates.py    # Duplicate detection by name/size
    ├── reporting/           # Output and visualization
    │   ├── exporter.py      # CSV/JSON export
    │   └── treeview.py      # ASCII tree generator
    └── cli/                 # Command-line interface
        ├── menu.py          # Menu framework (Menu, BoxMenu, MenuItem)
        ├── app.py           # Application shell
        └── main.py          # Menu actions and entry point
```

## Development

Install the project in editable mode with its development environment:

```bash
uv sync
uv run dirmap
```

The package uses the `src/` layout, so imports are always absolute, e.g.:

```python
from dirmap.core.scanner import scan_directory
```

## Who is this for?

System administrators, developers, and anyone who wants to quickly understand disk usage, find duplicate files, or audit directory structures from the terminal — without installing heavy GUI tools.

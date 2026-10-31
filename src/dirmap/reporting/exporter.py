"""CSV and JSON export of scan results."""

import csv
import json
from pathlib import Path

DEFAULT_CSV = "output/results.csv"
DEFAULT_JSON = "output/result.json"


def _ensure_parent(filename):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)


def export_csv(files, filename=DEFAULT_CSV):
    fieldnames = ["name", "suffix", "size_bytes", "path", "modified"]
    _ensure_parent(filename)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(files)
        print(f"Saved Files to {filename} - saved {len(files)} rows to {filename}")


def export_json(files, filename=DEFAULT_JSON):
    clean = [{**f, "modified": str(f["modified"])} for f in files]
    _ensure_parent(filename)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)
    print(f"Saved to {filename}")

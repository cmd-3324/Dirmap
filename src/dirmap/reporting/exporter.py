"""CSV and JSON export of scan results."""

import csv
import json
from pathlib import Path

from dirmap.errors import ExportError

DEFAULT_CSV = "output/results.csv"
DEFAULT_JSON = "output/result.json"


def _ensure_parent(filename) -> None:
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ExportError(f"Cannot create output folder for {filename}: {exc}") from exc


def export_csv(files, filename=DEFAULT_CSV) -> None:
    """Write ``files`` to a CSV report.

    Raises:
        ExportError: If the report cannot be written.
    """
    fieldnames = ["name", "suffix", "size_bytes", "path", "modified"]
    _ensure_parent(filename)
    try:
        with open(filename, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(files)
    except OSError as exc:
        raise ExportError(f"Cannot write {filename}: {exc}") from exc

    print(f"Saved Files to {filename} - saved {len(files)} rows to {filename}")


def export_json(files, filename=DEFAULT_JSON) -> None:
    """Write ``files`` to a JSON report.

    Raises:
        ExportError: If the report cannot be written.
    """
    clean = [{**file, "modified": str(file["modified"])} for file in files]
    _ensure_parent(filename)
    try:
        with open(filename, "w", encoding="utf-8") as handle:
            json.dump(clean, handle, indent=2)
    except OSError as exc:
        raise ExportError(f"Cannot write {filename}: {exc}") from exc

    print(f"Saved to {filename}")

"""Recursive directory scanning."""

from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from dirmap.errors import ScanError

ErrorHandler = Callable[[Path, OSError], None]


def _validate_root(folder_path) -> Path:
    root = Path(folder_path)
    if not root.exists():
        raise ScanError(f"Folder does not exist: {root}")
    if not root.is_dir():
        raise ScanError(f"Not a folder: {root}")
    return root


def _build_record(path: Path) -> dict:
    stat = path.stat()
    return {
        "path": str(path),
        "name": path.name,
        "suffix": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
    }


def scan_directory(
    folder_path,
    *,
    on_error: Optional[ErrorHandler] = None,
) -> list[dict]:
    """Return metadata for every file under ``folder_path``.

    The result is sorted by size, largest first. Files that cannot be read are
    skipped; pass ``on_error`` to observe the failures instead of ignoring them.

    Raises:
        ScanError: If ``folder_path`` does not exist or is not a directory.
    """
    root = _validate_root(folder_path)
    results: list[dict] = []

    for path in root.rglob("*"):
        try:
            if path.is_file():
                results.append(_build_record(path))
        except OSError as exc:
            if on_error is not None:
                on_error(path, exc)

    results.sort(key=lambda file: file["size_bytes"], reverse=True)
    return results

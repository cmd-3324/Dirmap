"""Statistical analysis of scanned files."""

from collections import Counter
from pathlib import Path
from typing import Callable, Optional

from dirmap.errors import ScanError

ErrorHandler = Callable[[Path, OSError], None]


def count_by_type(files) -> None:
    counts = Counter(file["suffix"] for file in files)

    print("\n  FILE COUNT BY TYPE")
    print("─" * 35)
    for ext, count in counts.most_common():
        print(f"  {ext:12} {count:>4} files")


def largest_files(files, n: int = 10) -> None:
    sorted_files = sorted(files, key=lambda file: file["size_bytes"], reverse=True)

    print(f"\n  TOP {n} LARGEST FILES")
    print("─" * 55)
    print(f"  {'#':<4} {'Name':<30} {'Size':>10}")
    print("  " + "─" * 48)

    for i, file in enumerate(sorted_files[:n], 1):
        size_kb = file["size_bytes"] / 1024
        if size_kb > 1024:
            size_str = f"{size_kb / 1024:.1f} MB"
        else:
            size_str = f"{size_kb:.1f} KB"
        print(f"  {i:<4} {file['name']:<30} {size_str:>10}")


def size_by_type(files) -> None:
    totals: dict[str, int] = {}
    for file in files:
        ext = file["suffix"]
        totals[ext] = totals.get(ext, 0) + file["size_bytes"]

    print("\n  TOTAL SIZE BY TYPE")
    print("─" * 45)
    print(f"  {'Extension':<12} {'Size':>10}")
    print("  " + "─" * 28)

    for ext, size in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        size_mb = size / (1024 * 1024)
        if size_mb < 1:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size_mb:.1f} MB"
        print(f"  {ext:<12} {size_str:>10}")


def oldest_newest(files) -> None:
    if not files:
        return

    oldest = min(files, key=lambda file: file["modified"])
    newest = max(files, key=lambda file: file["modified"])

    print("\n  FILE AGE RANGE")
    print("─" * 55)
    print(f"  Oldest : {oldest['name']:<30} {oldest['modified']}")
    print(f"  Newest : {newest['name']:<30} {newest['modified']}")


def empty_folders(
    folder_path,
    *,
    on_error: Optional[ErrorHandler] = None,
) -> list[Path]:
    """Return every empty directory under ``folder_path``.

    Unreadable directories are skipped; pass ``on_error`` to observe them.

    Raises:
        ScanError: If ``folder_path`` does not exist or is not a directory.
    """
    base = Path(folder_path)
    if not base.exists():
        raise ScanError(f"Folder does not exist: {base}")
    if not base.is_dir():
        raise ScanError(f"Not a folder: {base}")

    empties: list[Path] = []
    for directory in base.rglob("*"):
        try:
            if directory.is_dir() and not any(directory.iterdir()):
                empties.append(directory)
        except OSError as exc:
            if on_error is not None:
                on_error(directory, exc)

    if empties:
        print(f"\n  EMPTY FOLDERS ({len(empties)})")
        print("─" * 60)
        for directory in empties:
            print(f"  {directory.name:<30} {directory}")
    else:
        print("\n  No empty folders found.")

    return empties

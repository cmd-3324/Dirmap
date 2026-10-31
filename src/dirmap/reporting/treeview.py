"""ASCII folder tree rendering."""

from pathlib import Path

from dirmap.errors import ScanError


def print_tree(folder_path: str, prefix: str = "", max_depth: int = 3) -> None:
    """Print the folder tree under ``folder_path``.

    Raises:
        ScanError: If ``folder_path`` does not exist or cannot be read.
    """
    base = Path(folder_path)

    if max_depth == 0:
        return

    if not base.exists():
        raise ScanError(f"Folder does not exist: {base}")
    if not base.is_dir():
        raise ScanError(f"Not a folder: {base}")

    try:
        items = sorted(base.iterdir(), key=lambda path: (path.is_file(), path.name))
    except OSError as exc:
        raise ScanError(f"Cannot read folder {base}: {exc}") from exc

    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item.name}")

        if item.is_dir() and max_depth > 1:
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension, max_depth - 1)

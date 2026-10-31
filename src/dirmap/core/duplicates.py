"""Duplicate file detection."""

from collections import defaultdict
from typing import Callable, Hashable


def _group_by(files, key: Callable[[dict], Hashable]) -> dict:
    """Group non-empty files by ``key`` and keep only groups with 2+ paths."""
    groups: dict = defaultdict(list)
    for file in files:
        if file["size_bytes"] > 0:
            groups[key(file)].append(file["path"])
    return {value: paths for value, paths in groups.items() if len(paths) > 1}


def _report(groups: dict, empty_message: str) -> None:
    print(f"\n  Duplicate Files \t ")
    print("-" * 44)
    if not groups:
        print(empty_message)
        return
    for value, paths in groups.items():
        print(f"{value} \t {paths}")


def duplicates_by_name(files) -> dict[str, list[str]]:
    """Return duplicate groups keyed by file name.

    An empty ``files`` list is not an error: a message is printed and an empty
    mapping is returned.
    """
    if not files:
        print("\n  No files to analyze.")
        return {}

    groups = _group_by(files, lambda file: file["name"])
    _report(groups, "No Duplicate Files(by name)")
    return groups


def duplicates_by_size(files) -> dict[int, list[str]]:
    """Return duplicate groups keyed by size in bytes.

    An empty ``files`` list is not an error: a message is printed and an empty
    mapping is returned.
    """
    if not files:
        print("\n  No files to analyze.")
        return {}

    groups = _group_by(files, lambda file: file["size_bytes"])
    _report(groups, "No Duplicate Files(by size)")
    return groups

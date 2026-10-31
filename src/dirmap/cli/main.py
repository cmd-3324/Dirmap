"""Entry point and menu actions for DIRMAP."""

import sys

from dirmap.cli.app import App
from dirmap.cli.menu import BoxMenu
from dirmap.core.analyzer import (
    count_by_type,
    empty_folders,
    largest_files,
    oldest_newest,
    size_by_type,
)
from dirmap.core.duplicates import duplicates_by_name, duplicates_by_size
from dirmap.core.scanner import scan_directory
from dirmap.reporting.exporter import export_csv, export_json
from dirmap.reporting.treeview import print_tree


def action_scan():
    path = input("  Folder path: ").strip()
    if not path:
        path = "."
    files = scan_directory(path)
    print(f"\n  Found {len(files)} files.")

    input("\n  Press Enter to continue...")


def action_analyze():
    path = input("  Folder path: ").strip() or "."
    files = scan_directory(path)
    count_by_type(files)
    largest_files(files, 5)
    size_by_type(files)
    oldest_newest(files)
    empty_folders(path)
    input("\n Press Enter ...")


def action_duplicates():
    path = input("  Folder path: ").strip() or "."
    files = scan_directory(path)
    duplicates_by_name(files)
    duplicates_by_size(files)
    input("\n  Press Enter...")


def action_export():
    path = input("  Folder path: ").strip() or "."
    files = scan_directory(path)
    export_csv(files)
    export_json(files)
    input("\n  Press Enter...")


def action_exit():
    print("\n  Done.\n")
    sys.exit(0)


def action_empty():
    path = input("  Folder path: ").strip()
    if not path:
        path = "."
    empty_folders(path)


def action_tree():
    path = input("  Folder path: ").strip() or "."
    depth = input("  Max depth (default 3): ").strip()
    depth = int(depth) if depth.isdigit() else 3

    print(f"\n  {path}")
    print_tree(path, max_depth=depth)
    input("\n  Press Enter...")


# ---- Main ----
def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    menu = BoxMenu("DIRMAP - Directory Analyzer")
    menu.add_item("1", "Scan Folder", action_scan)
    menu.add_item("2", "Analyze Files", action_analyze)
    menu.add_item("3", "Find Duplicates", action_duplicates)
    menu.add_item("4", "Export Report", action_export)
    menu.add_item("5", "Show Tree", action_tree)
    menu.add_item("6", "Exit", action_exit)

    app = App()
    app.register_menu(menu)
    app.start()


if __name__ == "__main__":
    main()

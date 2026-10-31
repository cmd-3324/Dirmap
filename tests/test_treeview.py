"""Tests for :mod:`dirmap.reporting.treeview`."""

import pytest

from dirmap.errors import ScanError
from dirmap.reporting.treeview import print_tree


def test_print_tree_lists_items(tmp_path, capsys):
    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "file.txt").write_text("x")

    print_tree(str(tmp_path))

    out = capsys.readouterr().out
    assert "folder" in out
    assert "file.txt" in out


def test_print_tree_respects_max_depth(tmp_path, capsys):
    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "file.txt").write_text("x")

    print_tree(str(tmp_path), max_depth=1)

    out = capsys.readouterr().out
    assert "folder" in out
    assert "file.txt" not in out


def test_print_tree_rejects_missing_path(tmp_path):
    with pytest.raises(ScanError):
        print_tree(str(tmp_path / "missing"))

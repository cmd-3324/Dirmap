"""Tests for :mod:`dirmap.core.duplicates`."""

from dirmap.core.duplicates import duplicates_by_name, duplicates_by_size


def _files():
    return [
        {"name": "same.txt", "size_bytes": 10, "path": "a/same.txt"},
        {"name": "same.txt", "size_bytes": 10, "path": "b/same.txt"},
        {"name": "other.txt", "size_bytes": 10, "path": "c/other.txt"},
        {"name": "empty.txt", "size_bytes": 0, "path": "d/empty.txt"},
        {"name": "empty2.txt", "size_bytes": 0, "path": "e/empty2.txt"},
    ]


def test_duplicates_by_name(capsys):
    groups = duplicates_by_name(_files())

    assert groups == {"same.txt": ["a/same.txt", "b/same.txt"]}
    assert "same.txt" in capsys.readouterr().out


def test_duplicates_by_size(capsys):
    groups = duplicates_by_size(_files())

    assert groups == {10: ["a/same.txt", "b/same.txt", "c/other.txt"]}
    assert "10" in capsys.readouterr().out


def test_empty_input_is_not_an_error(capsys):
    assert duplicates_by_name([]) == {}
    assert duplicates_by_size([]) == {}
    assert "No files to analyze" in capsys.readouterr().out

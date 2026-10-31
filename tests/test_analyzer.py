"""Tests for :mod:`dirmap.core.analyzer`."""

import pytest

from dirmap.core.analyzer import (
    count_by_type,
    empty_folders,
    largest_files,
    oldest_newest,
    size_by_type,
)
from dirmap.errors import ScanError


def _files():
    return [
        {
            "name": "a.txt",
            "suffix": ".txt",
            "size_bytes": 2048,
            "path": "a.txt",
            "modified": "2024-01-01",
        },
        {
            "name": "b.txt",
            "suffix": ".txt",
            "size_bytes": 1024,
            "path": "b.txt",
            "modified": "2024-01-02",
        },
        {
            "name": "c.py",
            "suffix": ".py",
            "size_bytes": 512,
            "path": "c.py",
            "modified": "2024-01-03",
        },
    ]


def test_count_by_type(capsys):
    count_by_type(_files())

    out = capsys.readouterr().out
    assert ".txt" in out
    assert "2 files" in out


def test_largest_files(capsys):
    largest_files(_files(), n=2)

    out = capsys.readouterr().out
    assert out.index("a.txt") < out.index("b.txt")
    assert "c.py" not in out


def test_size_by_type(capsys):
    size_by_type(_files())

    out = capsys.readouterr().out
    assert "TOTAL SIZE BY TYPE" in out
    assert ".txt" in out


def test_oldest_newest(capsys):
    oldest_newest(_files())

    out = capsys.readouterr().out
    assert "Oldest" in out
    assert "Newest" in out


def test_oldest_newest_handles_empty(capsys):
    oldest_newest([])

    assert capsys.readouterr().out == ""


def test_empty_folders(tmp_path, capsys):
    (tmp_path / "empty").mkdir()
    full = tmp_path / "full"
    full.mkdir()
    (full / "file.txt").write_text("x")

    empties = empty_folders(tmp_path)

    assert [path.name for path in empties] == ["empty"]
    assert "EMPTY FOLDERS" in capsys.readouterr().out


def test_empty_folders_none_found(tmp_path, capsys):
    (tmp_path / "file.txt").write_text("x")

    assert empty_folders(tmp_path) == []
    assert "No empty folders" in capsys.readouterr().out


def test_empty_folders_rejects_missing_path(tmp_path):
    with pytest.raises(ScanError):
        empty_folders(tmp_path / "missing")

"""Tests for :mod:`dirmap.core.scanner`."""

from datetime import datetime

import pytest

from dirmap.core.scanner import scan_directory
from dirmap.errors import ScanError


def test_collects_files_sorted_by_size(tmp_path):
    (tmp_path / "small.txt").write_text("a")
    (tmp_path / "large.bin").write_bytes(b"x" * 10)
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "medium.BIN").write_bytes(b"x" * 5)

    files = scan_directory(tmp_path)

    assert [file["name"] for file in files] == ["large.bin", "medium.BIN", "small.txt"]
    assert [file["size_bytes"] for file in files] == [10, 5, 1]
    assert all(isinstance(file["modified"], datetime) for file in files)


def test_lowercases_suffix(tmp_path):
    (tmp_path / "READ.ME").write_text("hello")

    files = scan_directory(tmp_path)

    assert files[0]["suffix"] == ".me"


def test_ignores_directories(tmp_path):
    (tmp_path / "folder").mkdir()
    (tmp_path / "file.txt").write_text("x")

    files = scan_directory(tmp_path)

    assert [file["name"] for file in files] == ["file.txt"]


def test_rejects_missing_folder(tmp_path):
    with pytest.raises(ScanError):
        scan_directory(tmp_path / "missing")


def test_rejects_file_path(tmp_path):
    path = tmp_path / "file.txt"
    path.write_text("x")

    with pytest.raises(ScanError, match="Not a folder"):
        scan_directory(path)


def test_reports_unreadable_files(tmp_path, monkeypatch):
    (tmp_path / "file.txt").write_text("x")
    errors = []

    def raise_oserror(path):
        raise OSError("boom")

    monkeypatch.setattr("dirmap.core.scanner._build_record", raise_oserror)

    files = scan_directory(
        tmp_path,
        on_error=lambda path, exc: errors.append((path, exc)),
    )

    assert files == []
    assert len(errors) == 1

"""Tests for :mod:`dirmap.reporting.exporter`."""

import json

import pytest

from dirmap.errors import ExportError
from dirmap.reporting.exporter import export_csv, export_json


def _files():
    return [
        {
            "name": "a.txt",
            "suffix": ".txt",
            "size_bytes": 1,
            "path": "a.txt",
            "modified": "2024-01-01",
        }
    ]


def test_export_csv_creates_parent_and_writes(tmp_path, capsys):
    target = tmp_path / "nested" / "report.csv"

    export_csv(_files(), filename=str(target))

    header = target.read_text(encoding="utf-8").splitlines()[0]
    assert header == "name,suffix,size_bytes,path,modified"
    assert "Saved Files" in capsys.readouterr().out


def test_export_json_serializes_modified(tmp_path, capsys):
    target = tmp_path / "report.json"

    export_json(_files(), filename=str(target))

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data[0]["modified"] == "2024-01-01"
    assert "Saved to" in capsys.readouterr().out


def test_export_rejects_unwritable_target(tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("not a folder")

    with pytest.raises(ExportError):
        export_csv(_files(), filename=str(blocker / "report.csv"))

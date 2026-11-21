"""The standalone spec on synthetic replay folders (tiny fake files, no game data)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from heat3d_ext_riot import cli, standalone_spec
from heat3d_ext_riot.app import entry, paths, update
from heat3d_ext_riot.app import spec as app_spec


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")
    update.AUTO_THIS_RUN = False


def folders(tmp_path: Path, monkeypatch) -> tuple[Path, Path]:
    lol, val = tmp_path / "lol" / "Replays", tmp_path / "val" / "Demos"
    lol.mkdir(parents=True)
    (lol / "EUW1-1.rofl").write_bytes(b"x")
    monkeypatch.setattr(cli, "replay_folders", lambda: [("League of Legends", lol), ("VALORANT", val)])
    return lol, val


def test_find(tmp_path, monkeypatch):
    lol, val = folders(tmp_path, monkeypatch)
    g = {s.key: s for s in standalone_spec.SPEC.games}
    assert g["lol"].find(None) == lol
    assert g["valorant"].find(None) is None  # no folder there yet
    assert g["valorant"].find(str(lol)) == lol  # a folder chosen is taken as it is
    assert g["lol"].find(str(tmp_path / "nothing")) is None


def test_tasks(tmp_path, monkeypatch):
    lol, _ = folders(tmp_path, monkeypatch)
    levels = tmp_path / "levels"
    listing, convert = standalone_spec.SPEC.tasks
    assert listing.argv({}, levels) == ["heat3d-riot-replays", "list"]
    src, out = convert.inputs
    assert src.default(levels) == str(lol)
    assert out.default(levels) == str(paths.data_dir() / "matches" / "riot")
    assert convert.argv({"src": "r", "out": "o"}, levels) == ["heat3d-riot-replays", "convert", "r", "-o", "o"]
    assert convert.argv({"src": "", "out": "o"}, levels) == ["heat3d-riot-replays", "convert", "-o", "o"]


def test_no_maps_nothing_to_extract(tmp_path, monkeypatch, capsys):
    folders(tmp_path, monkeypatch)
    assert entry.main(standalone_spec.SPEC, ["status", "--json"]) == 0
    games = {g["game"]: g for g in json.loads(capsys.readouterr().out)["games"]}
    assert games["lol"]["found"] and not games["valorant"]["found"] and games["lol"]["maps"] == []
    assert entry.main(standalone_spec.SPEC, ["extract", "--new", "--progress-json"]) == 0
    assert json.loads(capsys.readouterr().out.splitlines()[-1]) == {"event": "done", "ok": 0, "failed": 0}

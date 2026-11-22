"""The match facts read from a replay's header and metadata alone - on the made-up files of test_replays."""

from __future__ import annotations

import pytest
from test_replays import rofl1, rofl2, vrf

from heat3d_ext_riot.replay_info import info

KEYS = {"map", "map_title", "mode", "date", "duration_s", "players", "teams", "outcome", "game_version"}


@pytest.mark.parametrize("make, version, game_id", [(rofl1, "14.9.580.2108", 7123456789), (rofl2, "15.3.659.6012", None)])
def test_league_metadata_gives_players_teams_and_the_winner(tmp_path, make, version, game_id):
    f = tmp_path / "match.rofl"
    f.write_bytes(make())
    r = info(f)
    assert KEYS <= set(r)
    assert r["game"] == "League of Legends"
    assert r["game_version"] == version
    assert r["game_id"] == game_id
    assert r["duration_s"] == 1800.0
    assert r["map"] is None and r["mode"] is None and r["date"] is None  # the file does not say
    assert [(p["name"], p["team"], p["champion"], p["kills"], p["won"]) for p in r["players"]] == [
        ("Someone#EUW", "100", "Ahri", 7, True), ("Other#EUW", "200", "Zed", 3, False)]
    assert r["teams"] == [{"id": "100", "name": "Blue", "kills": 7}, {"id": "200", "name": "Red", "kills": 3}]
    assert r["outcome"] == {"winner": "100", "result": "Blue victory"}


def test_valorant_info_block_and_header(tmp_path):
    f = tmp_path / "match.vrf"
    f.write_bytes(vrf())
    r = info(f)
    assert KEYS <= set(r)
    assert r["game"] == "VALORANT"
    assert r["map"] == "/Game/Maps/Ascent/Ascent" and r["map_title"] == "Ascent"
    assert r["match_id"] == "0a1b2c3d-1111-2222-3333-444455556666"
    assert r["agents"] == ["add6443a-41bd-e414-f6ad-e58d267f4e95"]
    assert r["date"] == "2023-11-14T22:13:20+00:00"
    assert r["duration_s"] == 2100.0
    assert r["game_version"] == "release-13.01"
    assert r["players"] == [] and r["outcome"] is None


def test_an_encrypted_valorant_replay_gives_its_info_block(tmp_path):
    f = tmp_path / "match.vrf"
    f.write_bytes(vrf(encrypted=1))
    r = info(f)
    assert r["encrypted"] is True and r["map"] is None and r["duration_s"] == 2100.0
    assert r["game_version"] == "999"


def test_other_files_are_refused(tmp_path):
    for name, raw in (("junk.rofl", b"not a replay at all" * 10), ("short.rofl", b"RIOT\x00\x00" + bytes(10)),
                      ("empty.vrf", b""), ("cut.rofl", b"RIOT\x02\x00" + bytes(20) + b"\xff\xff\xff\x7f")):
        f = tmp_path / name
        f.write_bytes(raw)
        with pytest.raises(ValueError):
            info(f)

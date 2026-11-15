"""League of Legends and Valorant replays: only what each file carries in the open - on made-up files."""

from __future__ import annotations

import csv
import json
import struct

import pytest

from heat3d_ext_riot import cli
from heat3d_ext_riot.replays import VRF_MAGIC, read_rofl, read_vrf

PLAYERS = [
    {"RIOT_ID_GAME_NAME": "Someone", "RIOT_ID_TAG_LINE": "EUW", "PUUID": "p1", "SKIN": "Ahri", "TEAM": "100",
     "TEAM_POSITION": "MIDDLE", "CHAMPIONS_KILLED": "7", "NUM_DEATHS": "2", "ASSISTS": "9", "GOLD_EARNED": "12345",
     "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS": "23456", "WIN": "Win"},
    {"RIOT_ID_GAME_NAME": "Other", "RIOT_ID_TAG_LINE": "EUW", "PUUID": "p2", "SKIN": "Zed", "TEAM": "200",
     "TEAM_POSITION": "MIDDLE", "CHAMPIONS_KILLED": "3", "NUM_DEATHS": "6", "ASSISTS": "1", "GOLD_EARNED": "9000",
     "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS": "15000", "WIN": "Fail"},
]
META = {"gameLength": 1800000, "lastGameChunkId": 30, "lastKeyFrameId": 15, "statsJson": json.dumps(PLAYERS)}


def rofl1(game_id: int = 7123456789) -> bytes:
    """ROFL1 as roflxd.cs reads it: magic, signature, lengths, metadata JSON, payload header."""
    meta = json.dumps({**META, "gameVersion": "14.9.580.2108"}).encode()
    header_len = 288
    meta_off = header_len
    payload_off = meta_off + len(meta)
    payload = struct.pack("<QIIIIII", game_id, 1800000, 15, 30, 2, 3, 60000) + struct.pack("<H", 4) + b"QUJD"
    lengths = struct.pack("<HIIIIII", header_len, 0, meta_off, len(meta), payload_off, len(payload), payload_off + len(payload))
    return b"RIOT\x00\x00" + bytes(256) + lengths + meta + payload


def rofl2() -> bytes:
    """ROFL2: version near the start, the metadata at the end with its length in the last four bytes."""
    meta = json.dumps(META).encode()
    head = b"RIOT\x02\x00" + bytes(8) + b"15.3.659.6012\x00\x00" + bytes(40)
    return head + b"\x28\xb5\x2f\xfd" + bytes(64) + meta + struct.pack("<i", len(meta))


def _fstring(text: str) -> bytes:
    raw = text.encode("latin-1") + b"\x00"
    return struct.pack("<i", len(raw)) + raw


def _event(group: str, words: list[int], seconds: float, time_ms: int) -> bytes:
    payload = struct.pack("<I", 1) + b"".join(struct.pack("<I", w) for w in words)
    payload += _fstring(f"EReplayEventGroup::{group}") + struct.pack("<f", seconds)
    return _fstring(f"ev-{time_ms}") + _fstring(group) + _fstring("") + struct.pack("<IIi", time_ms, time_ms, len(payload)) + payload


def vrf(encrypted: int = 0) -> bytes:
    """A replay in the layout vrfkit documents: the info block, then type/size chunks."""
    info = struct.pack("<II", VRF_MAGIC, 7) + struct.pack("<i", 1) + bytes(20)
    info += struct.pack("<iII", 2100000, 21, 999) + _fstring("Valorant replay")
    info += struct.pack("<IqII", 0, int((1_700_000_000 + 62135596800) * 1e7), 1, encrypted) + struct.pack("<i", 0)
    header = (struct.pack("<I", 0x2CF5A13D) + _fstring("++Ares-Core+release-13.01") + bytes(16)
              + _fstring("/Game/Maps/Ascent/Ascent") + b'{"matchID":"0a1b2c3d-1111-2222-3333-444455556666",'
              b'"playerLoadouts":{"x":{"characterId":"add6443a-41bd-e414-f6ad-e58d267f4e95"}}}')
    chunks = struct.pack("<Ii", 0, len(header)) + header
    for ev in (_event("roundStarted", [], 0.0, 1000), _event("characterDeath", [11, 22], 31.5, 32500),
               _event("spikePlanted", [11], 70.0, 71000), _event("roundStarted", [], 120.0, 121000)):
        chunks += struct.pack("<Ii", 3, len(ev)) + ev
    chunks += struct.pack("<Ii", 1, 4) + b"\x00\x01\x02\x03"  # replay data: not read
    return info + chunks


def _tiles(buf: bytes, sections) -> bool:
    """The parts, in file order, are the whole file."""
    return b"".join(buf[start:end] for _, start, end, _ in sorted(sections, key=lambda s: s[1])) == buf


def test_both_league_containers_give_the_box_score():
    for buf, version in ((rofl1(), "14.9.580.2108"), (rofl2(), "15.3.659.6012")):
        r = read_rofl(buf)
        assert r["version"] == version
        assert r["length_ms"] == 1800000
        assert [p["SKIN"] for p in r["players"]] == ["Ahri", "Zed"]
        assert _tiles(buf, r["sections"])
    assert read_rofl(rofl1())["game_id"] == 7123456789
    assert [s[0] for s in read_rofl(rofl2())["sections"]] == ["body", "metadata", "metadata_length"]
    with pytest.raises(ValueError):
        read_rofl(b"not a replay" + bytes(300))


def test_every_part_of_a_league_replay_is_named_and_the_chunks_left_unread():
    import struct as st

    # A ROFL1 with a chunk table of one keyframe and one chunk after its payload header, and their bytes.
    meta = json.dumps({**META, "gameVersion": "14.9.580.2108"}).encode()
    meta_off = 288
    ph_off = meta_off + len(meta)
    ph = st.pack("<QIIIIII", 7123456789, 1800000, 1, 1, 2, 3, 60000) + st.pack("<H", 4) + b"QUJD"
    payload_off = ph_off + len(ph)
    table = st.pack("<IBIII", 1, 2, 5, 0, 0) + st.pack("<IBIII", 1, 1, 3, 2, 5)
    data = b"KEYFR" + b"CHK"
    lengths = st.pack("<HIIIIII", 288, 0, meta_off, len(meta), ph_off, len(ph), payload_off)
    buf = b"RIOT\x00\x00" + bytes(256) + lengths + meta + ph + table + data + b"??"
    r = read_rofl(buf)
    kinds = [x[0] for x in r["sections"]]
    assert kinds == ["magic", "signature", "lengths", "metadata", "payload_header", "chunk_header", "chunk_header",
                     "keyframe", "chunk", "unknown"]
    assert _tiles(buf, r["sections"])
    # The encrypted chunks: named, nothing read of them.
    assert [x[3] for x in r["sections"] if x[0] in ("keyframe", "chunk", "unknown")] == [None, None, None]
    assert r["payload"]["keyframe_interval"] == 60000 and r["payload"]["encryption_key"] == "QUJD"
    assert r["chunks"] == [{"id": 1, "type": "keyframe", "length": 5, "next_chunk_id": 0, "offset": 0},
                           {"id": 1, "type": "chunk", "length": 3, "next_chunk_id": 2, "offset": 5}]


def test_a_valorant_replay_gives_its_open_facts_and_timeline():
    r = read_vrf(vrf())
    assert r["map"] == "/Game/Maps/Ascent/Ascent"
    assert r["match_id"] == "0a1b2c3d-1111-2222-3333-444455556666"
    assert r["agents"] == ["add6443a-41bd-e414-f6ad-e58d267f4e95"]
    assert [e["event"] for e in r["events"]] == ["round_start", "kill", "spike_planted", "round_start"]
    kill = r["events"][1]
    assert kill["words"] == [11, 22] and kill["seconds"] == pytest.approx(31.5)
    # An encrypted replay is walked, nothing read inside.
    locked = read_vrf(vrf(encrypted=1))
    assert locked["encrypted"] and locked["events"] == [] and locked["map"] is None
    assert [x[0] for x in locked["sections"]] == ["info", "header", "event", "event", "event", "event", "replay_data"]


def test_every_chunk_of_a_valorant_replay_is_named():
    buf = vrf() + b"\x09\x00\x00\x00\xff\x00\x00\x00cut"  # a chunk cut short at the end
    r = read_vrf(buf)
    assert [x[0] for x in r["sections"]] == ["info", "header", "event roundStarted", "event characterDeath",
                                              "event spikePlanted", "event roundStarted", "replay_data", "trailing"]
    assert _tiles(buf, r["sections"])
    assert r["info"]["network_version"] == 21 and r["info"]["name"] == "Valorant replay"
    assert r["info"]["changelist"] == 999
    assert r["events"][1]["id"] == "ev-32500" and r["events"][1]["time_ms"] == 32500


def test_convert_writes_the_reading_and_a_table_per_replay(tmp_path, capsys):
    folder = tmp_path / "replays"
    folder.mkdir()
    (folder / "EUW1-7123456789.rofl").write_bytes(rofl1())
    (folder / "match.vrf").write_bytes(vrf())
    (folder / "notes.txt").write_text("not a replay")
    out = tmp_path / "out"
    assert cli.main(["convert", str(folder), "-o", str(out)]) == 0
    doc = json.loads((out / "EUW1-7123456789.rofl.json").read_text(encoding="utf-8"))
    assert doc["format"] == cli.FORMAT and doc["game"] == "League of Legends" and doc["kind"] == "rofl"
    assert doc["game_id"] == 7123456789 and doc["file"] == "EUW1-7123456789.rofl"
    # The reading as read_rofl gives it, the parts as lists.
    assert doc["sections"] == json.loads(json.dumps(read_rofl(rofl1())["sections"]))
    with (out / "EUW1-7123456789.rofl.players.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [r["SKIN"] for r in rows] == ["Ahri", "Zed"] and rows[0]["CHAMPIONS_KILLED"] == "7"
    v = json.loads((out / "match.vrf.json").read_text(encoding="utf-8"))
    assert v["game"] == "VALORANT" and v["map"] == "/Game/Maps/Ascent/Ascent"
    with (out / "match.vrf.events.csv").open(encoding="utf-8") as f:
        events = list(csv.DictReader(f))
    assert [e["event"] for e in events] == ["round_start", "kill", "spike_planted", "round_start"]
    assert events[1]["words"] == "11 22"
    assert "match.vrf.json" in capsys.readouterr().out


def test_exit_status_says_what_went_wrong(tmp_path, monkeypatch, capsys):
    out = str(tmp_path / "out")
    assert cli.main(["convert", str(tmp_path / "empty"), "-o", out]) == 2
    bad = tmp_path / "broken.rofl"
    bad.write_bytes(b"not a replay")
    assert cli.main(["convert", str(bad), "-o", out]) == 2
    assert "not a League of Legends or VALORANT replay" in capsys.readouterr().err
    good = tmp_path / "EUW1-1.rofl"
    good.write_bytes(rofl2())
    assert cli.main(["convert", str(bad), str(good), "-o", out]) == 1


def test_list_looks_where_the_games_save_replays(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "me"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    assert [f for _, f in cli.replay_folders()] == [
        tmp_path / "me" / "Documents" / "League of Legends" / "Replays",
        tmp_path / "local" / "VALORANT" / "Saved" / "Demos",
    ]
    assert cli.main(["list"]) == 2
    demos = tmp_path / "local" / "VALORANT" / "Saved" / "Demos"
    demos.mkdir(parents=True)
    (demos / "match.vrf").write_bytes(vrf())
    assert cli.main(["list"]) == 0
    assert "match.vrf" in capsys.readouterr().out

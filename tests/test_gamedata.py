"""The game-file catalogues on synthetic files (a tiny pak with a .locres, a fake League folder)."""

from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest

from heat3d_ext_riot import gamedata, standalone_spec


@pytest.fixture(autouse=True)
def _no_riot(monkeypatch):
    monkeypatch.setattr(gamedata, "riot_running", lambda: [])


def fstring(s: str) -> bytes:
    b = s.encode("latin-1") + b"\0"
    return struct.pack("<i", len(b)) + b


def make_locres(tables: dict[str, dict[str, str]]) -> bytes:
    strings: list[str] = []
    body = bytearray(struct.pack("<I", len(tables)))
    for ns, keys in tables.items():
        body += struct.pack("<I", 0) + fstring(ns) + struct.pack("<I", len(keys))
        for k, v in keys.items():
            if v not in strings:
                strings.append(v)
            body += struct.pack("<I", 0) + fstring(k) + struct.pack("<Ii", 0, strings.index(v))
    head_len = 16 + 1 + 8 + 4
    arr = struct.pack("<i", len(strings)) + b"".join(fstring(s) + struct.pack("<i", 1) for s in strings)
    entries = sum(len(k) for k in tables.values())
    return gamedata.LOCRES + bytes([3]) + struct.pack("<q", head_len + len(body)) + struct.pack("<I", entries) \
        + bytes(body) + arr


def entry(payload: bytes, *, encrypted: bool = False) -> bytes:
    """One stored (uncompressed) pak entry: offset, size, size, no compression, hash, flags, block size."""
    return struct.pack("<qqqI", 0, len(payload), len(payload), 0) + b"\0" * 20 + bytes([1 if encrypted else 0]) \
        + struct.pack("<I", 0) + payload


def make_pak(*entries: bytes) -> bytes:
    data = b"".join(entries)
    index = len(data)
    footer = b"\0" * 16 + b"\x01" + struct.pack("<IIqq", gamedata.PAK_MAGIC, 11, index, 0) + b"\0" * 20
    return data + b"INDEX(encrypted, not read)" + footer


TABLES = {
    "Wushu_Strings": {"DisplayName": "Jett", "Ability_Q_DisplayName": "Updraft", "Ability_E_DisplayName": "Tailwind",
                      "Ability_X_DisplayName": "Blade Storm", "DisplayName_AllCaps": "JETT"},
    "Hunter_StringTable": {"DisplayName": "Sova", "GrenadeAbility_DisplayName": "Owl Drone",
                           "Ability1_DisplayName": "Shock Bolt", "Ultimate_DisplayName": "Hunter's Fury"},
    "AssaultRifleStringTable": {"AssaultRifle_AK_DisplayName": "Vandal"},
    "UI_Strings": {"DisplayName": "Settings"},
}


def test_locres_round_trip():
    assert gamedata.locres(make_locres(TABLES)) == TABLES


def test_pak_walk_skips_encrypted_entries():
    loc = make_locres(TABLES)
    pak = make_pak(entry(b"secret", encrypted=True), entry(loc))
    assert gamedata.pak_entries(pak, None) == [loc]


def test_valorant_catalogue():
    cat = gamedata.valorant_catalog(TABLES, game_build="1")
    ids = gamedata.item_ids(cat)
    assert ids["agent"] == ["jett", "sova"]
    assert ids["ability"] == ["jett-e", "jett-q", "jett-x", "sova-1", "sova-grenade", "sova-ultimate"]
    jett = next(i for i in cat["items"] if i["id"] == "jett")
    assert jett["codename"] == "Wushu" and len(jett["abilities"]) == 3


def valorant_install(tmp_path: Path) -> Path:
    game = tmp_path / "VALORANT" / "live"
    pak = game / gamedata.TEXT_PAK
    pak.parent.mkdir(parents=True)
    pak.write_bytes(make_pak(entry(make_locres(TABLES))))
    return game


def lol_install(tmp_path: Path) -> Path:
    game = tmp_path / "League of Legends"
    champs = gamedata.champions_dir(game)
    champs.mkdir(parents=True)
    for n in ("Ahri", "Ahri.en_US", "MonkeyKing", "Common"):
        (champs / f"{n}.wad.client").write_bytes(b"RW")
    (game / "Game" / "content-metadata.json").write_text(json.dumps({"version": "16.22.1"}))
    return game


def test_installs_from_riot_records(tmp_path, monkeypatch):
    val, lol = valorant_install(tmp_path), lol_install(tmp_path)
    meta = tmp_path / "ProgramData" / "Riot Games" / "Metadata"
    for product, path in (("valorant.live", val), ("league_of_legends.live", lol)):
        (meta / product).mkdir(parents=True)
        (meta / product / f"{product}.product_settings.yaml").write_text(
            f'product_install_full_path: "{path.as_posix()}"\nproduct_install_root: "x"\n')
    monkeypatch.setenv("ProgramData", str(tmp_path / "ProgramData"))
    assert gamedata.install_dir("valorant") == val
    assert gamedata.install_dir("lol") == lol


def test_league_champions(tmp_path):
    game = lol_install(tmp_path)
    assert gamedata.lol_champions(game) == ["Ahri", "MonkeyKing"]
    cat = gamedata.lol_catalog(game)
    assert cat["gameBuild"] == "16.22.1" and gamedata.item_ids(cat) == {"champion": ["ahri", "monkeyking"]}


def test_content_hooks(tmp_path, monkeypatch):
    val, lol = valorant_install(tmp_path), lol_install(tmp_path)
    monkeypatch.setattr(gamedata, "install_dir", lambda g: {"valorant": val, "lol": lol}[g])
    monkeypatch.setattr(gamedata, "decompressor", lambda given=None: None)
    monkeypatch.setattr(standalone_spec, "GameSpec", type("Kit", (), {"__dataclass_fields__": {
        "contents": 1, "extract_content": 1, "catalog_items": 1, "extracted_items": 1}}))
    for key, kinds in (("valorant", {"agent", "ability"}), ("lol", {"champion"})):
        h = standalone_spec._content_hooks(key)
        (c,) = h["contents"](tmp_path)
        assert c.kind == "catalog"
        out = tmp_path / "levels" / key
        assert h["extract_content"](tmp_path, c, out, lambda t: None) == [out / "catalog.json"]
        assert set(h["catalog_items"](tmp_path)) == kinds
        assert h["extracted_items"](out) == h["catalog_items"](tmp_path)


def test_hooks_are_plain_functions_before_the_kit_has_them(tmp_path, monkeypatch):
    """Called directly (as the kit will), whatever the kit version."""
    val = valorant_install(tmp_path)
    monkeypatch.setattr(gamedata, "install_dir", lambda g: val)
    monkeypatch.setattr(gamedata, "decompressor", lambda given=None: None)
    monkeypatch.setattr(standalone_spec, "GameSpec", type("Any", (), {"__dataclass_fields__": {
        "contents": 1, "extract_content": 1, "catalog_items": 1, "extracted_items": 1}}))
    h = standalone_spec._content_hooks("valorant")
    assert gamedata.item_ids(gamedata.valorant_from_install(val, None))["agent"] == ["jett", "sova"]
    assert h["catalog_items"](tmp_path)["agent"] == ["jett", "sova"]


def test_nothing_read_while_riot_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(gamedata, "riot_running", lambda: ["valorant.exe"])
    with pytest.raises(RuntimeError, match="running"):
        gamedata.not_running()
    assert gamedata.main(["--game", "lol", "--lol", str(lol_install(tmp_path)), "-o", str(tmp_path)]) == 1
    assert not (tmp_path / "lol" / "catalog.json").exists()

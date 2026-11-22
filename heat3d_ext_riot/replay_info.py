"""
What a League of Legends (.rofl) or VALORANT (.vrf) replay says about its
match, read without converting it: only the parts that describe the match are
read from the file, with the layouts `replays` reads them by.

* .rofl, ROFL1: the lengths after the signature, the metadata JSON they point
  to (game length, version, the box score) and the payload header's game id.
* .rofl, ROFL2: the version near the start and the metadata JSON at the end
  (its length in the last four bytes).
* .vrf: the info block (length, changelist, when it was recorded) and the
  header chunk after it (map, match id, agents, the build's branch). An
  encrypted replay gives the info block only.
"""

from __future__ import annotations

import json
import os
import re
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .replays import ROFL1, ROFL2, VRF_MAGIC, _fstring, _header

#: League's two sides as the box score numbers them.
LOL_TEAMS = {"100": "Blue", "200": "Red"}
#: VALORANT's maps: the folder under /Game/Maps/ -> the name players know.
VRF_MAPS = {
    "Ascent": "Ascent", "Bonsai": "Split", "Duality": "Bind", "Triad": "Haven", "Port": "Icebox", "Foxtrot": "Breeze",
    "Canyon": "Fracture", "Pitt": "Pearl", "Jam": "Lotus", "Juliett": "Sunset", "Infinity": "Abyss",
}  # fmt: skip
#: Never read more than this of one part (a metadata block or a header chunk).
MAX_PART = 64 << 20


def _result(game: str, **fields: Any) -> dict[str, Any]:
    out = {"game": game, "map": None, "map_title": None, "mode": None, "date": None, "duration_s": None,
           "players": [], "teams": [], "outcome": None, "game_version": None}
    out.update(fields)
    return out


def _int(v: Any) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _read_at(f: Any, at: int, n: int, size: int) -> bytes:
    if at < 0 or n < 0 or n > MAX_PART or at + n > size:
        raise ValueError("a part of the replay lies outside the file")
    f.seek(at)
    return f.read(n)


# --------------------------------------------------------------------- League


def _rofl(f: Any, size: int) -> dict[str, Any]:
    head = f.read(288)
    game_id = None
    if head[:6] == ROFL1:
        if len(head) < 288:
            raise ValueError("the replay ends inside its header")
        _hl, _fl, meta_off, meta_len, ph_off, _ph_len, _po = struct.unpack_from("<HIIIIII", head, 262)
        meta = json.loads(_read_at(f, meta_off, meta_len, size).decode("utf-8"))
        if ph_off + 8 <= size:
            (game_id,) = struct.unpack("<Q", _read_at(f, ph_off, 8, size))
        version = meta.get("gameVersion") or None
    elif head[:6] == ROFL2:
        f.seek(size - 4)
        (n,) = struct.unpack("<i", f.read(4))
        if n <= 0 or n > size - 4:
            raise ValueError("no metadata at the end of the replay")
        meta = json.loads(_read_at(f, size - 4 - n, n, size).decode("utf-8"))
        version = head[14:29].split(b"\x00")[0].decode("utf-8", errors="replace").strip() or None
    else:
        raise ValueError("not a League of Legends replay")
    if not isinstance(meta, dict):
        raise ValueError("the replay's metadata is not an object")
    stats = meta.get("statsJson", "[]")
    rows = json.loads(stats) if isinstance(stats, str) else stats
    rows = [p for p in rows if isinstance(p, dict)] if isinstance(rows, list) else []

    players = []
    kills: dict[str, int] = {}
    winners: set[str] = set()
    for p in rows:
        name = p.get("RIOT_ID_GAME_NAME") or p.get("NAME") or None
        if name and p.get("RIOT_ID_TAG_LINE"):
            name = f"{name}#{p['RIOT_ID_TAG_LINE']}"
        team = str(p["TEAM"]) if p.get("TEAM") not in (None, "") else None
        k = _int(p.get("CHAMPIONS_KILLED"))
        players.append({"name": name, "team": team, "champion": p.get("SKIN") or None,
                        "position": p.get("TEAM_POSITION") or p.get("INDIVIDUAL_POSITION") or None,
                        "kills": k, "deaths": _int(p.get("NUM_DEATHS")), "assists": _int(p.get("ASSISTS")),
                        "level": _int(p.get("LEVEL")), "won": p["WIN"] == "Win" if p.get("WIN") else None})
        if team is not None:
            kills[team] = kills.get(team, 0) + (k or 0)
            if p.get("WIN") == "Win":
                winners.add(team)
    teams = [{"id": t, "name": LOL_TEAMS.get(t), "kills": kills[t]} for t in sorted(kills)]
    outcome = None
    if len(winners) == 1:
        (w,) = winners
        outcome = {"winner": w, "result": f"{LOL_TEAMS.get(w, w)} victory"}
    length = meta.get("gameLength")
    return _result("League of Legends", game_id=game_id,
                   duration_s=length / 1000 if isinstance(length, (int, float)) and length > 0 else None,
                   players=players, teams=teams, outcome=outcome, game_version=version)


# -------------------------------------------------------------------- VALORANT


def _vrf(f: Any, size: int) -> dict[str, Any]:
    head = f.read(min(size, 1 << 16))
    (magic,) = struct.unpack_from("<I", head, 0)
    if magic != VRF_MAGIC:
        raise ValueError("not a VALORANT replay")
    # The info block, field by field as `replays.read_vrf` reads it.
    at = 8
    (versions,) = struct.unpack_from("<i", head, at)
    at += 4 + max(0, versions) * 20
    length_ms, _network, changelist = struct.unpack_from("<iII", head, at)
    at += 12
    _name, at = _fstring(head, at)
    _live, ticks, _compressed, encrypted = struct.unpack_from("<IqII", head, at)
    at += 20
    (key_len,) = struct.unpack_from("<i", head, at)
    at += 4 + max(0, key_len)
    found: dict[str, Any] = {"map": None, "match_id": None, "agents": []}
    branch = mode = None
    if not encrypted and at + 8 <= size:
        f.seek(at)
        kind, n = struct.unpack("<Ii", f.read(8))
        if kind == 0:
            chunk = _read_at(f, at + 8, n, size)
            _header(chunk, found)
            text = chunk.decode("latin-1")
            m = re.search(r"\+\+Ares-Core\+([A-Za-z0-9_.-]+)", text)
            branch = m.group(1) if m else None
            m = re.search(r"/Game/GameModes/([A-Za-z0-9_]+)/", text)
            mode = m.group(1) if m else None
    date = None
    if ticks > 0:
        date = datetime.fromtimestamp(ticks / 1e7 - 62135596800, timezone.utc).isoformat()
    title = VRF_MAPS.get(found["map"].split("/")[3]) if found["map"] and found["map"].count("/") >= 3 else None
    return _result("VALORANT", match_id=found["match_id"], map=found["map"], map_title=title, mode=mode, date=date,
                   duration_s=length_ms / 1000 if length_ms > 0 else None, agents=found["agents"],
                   encrypted=bool(encrypted), game_version=branch or (str(changelist) if changelist else None))


def info(path: Path) -> dict[str, Any]:
    """
    The match as the replay's header and metadata describe it. Keys are None
    (or empty) where the file does not say. Raises ValueError for a file that
    is neither a League of Legends nor a VALORANT replay.
    """
    path = Path(path)
    size = os.path.getsize(path)
    with path.open("rb") as f:
        magic = f.read(8)
        f.seek(0)
        try:
            if magic[:4] == b"RIOT":
                return _rofl(f, size)
            if len(magic) >= 4 and struct.unpack_from("<I", magic)[0] == VRF_MAGIC:
                return _vrf(f, size)
        except (struct.error, UnicodeDecodeError, json.JSONDecodeError, IndexError) as e:
            raise ValueError(f"{path.name}: a replay this reader cannot read ({e})") from e
    raise ValueError(f"{path.name} is not a League of Legends or VALORANT replay")

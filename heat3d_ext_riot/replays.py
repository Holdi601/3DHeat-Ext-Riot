"""
League of Legends and VALORANT replays: what of them can be read as it is.

Both games save replays to the player's disk, and both protect what is inside:
the moment-to-moment game data is obfuscated, and differently with every patch,
to keep it from being used to cheat. That part is not decoded here. What
each file carries in the open is read, and
every part of the file is named by its byte range (`sections`), with what is
read of it, so that a user of the result can keep every part whole (3DHeat's
converter rule, docs/converters.md in the viewer's repository).

League of Legends (.rofl)
-------------------------
`%USERPROFILE%\\Documents\\League of Legends\\Replays\\*.rofl`. Both container
versions carry the end-of-game box score as plain JSON (`statsJson`): for each
of the ten players the champion, kills, deaths, assists, gold, damage to
champions, items, team, role, win, their Riot ID, and every other number the
game totals (over a hundred per player). ROFL1 (patch 14.9 and before) has it
after a fixed header (`RIOT\\0\\0`, a 256-byte signature, then the lengths);
ROFL2 (14.11 on, `RIOT\\2\\0`) at the end of the file, its length in the last
four bytes (stated by a Riot engineer, ReplayBook issue 299). ROFL1's payload
header (game id, length, chunk and keyframe counts, the chunk key's length) and
its table of chunks (id, type, length, next chunk, offset) are in the open and
read; the chunks themselves are encrypted, and left unread. Layouts from
roflxd.cs (MIT).

Positions are not in the file in the open. The 3DHeat Watcher can fetch the
match's official timeline from Riot's Match-V5 API with the player's own Riot
developer key; that is not this reader's part.

VALORANT (.vrf)
---------------
`%LOCALAPPDATA%\\VALORANT\\Saved\\Demos\\*.vrf`, an Unreal Engine local replay
(layout from vrfkit, Apache-2.0, and ValorantReplayParser, MIT). In the open:
the replay's info block (length, network version, changelist, its name, when it
was recorded, whether it is compressed or encrypted), the map, the match id and
the agents picked (in the header), and the server's own event timeline - kills
(killer and victim as network ids, not names), rounds starting, spikes planted,
defused and exploding, ultimates used, sides switching - each with its time,
id and metadata. Positions, names, scores and everything else are in the
obfuscated stream (the replay data and checkpoint chunks), which is not read.
"""

from __future__ import annotations

import json
import re
import struct
from typing import Any


def _gaps(sections: list[tuple[str, int, int]], size: int) -> list[tuple[str, int, int]]:
    """
    A file's parts in order, with every stretch no part covers added as
    `unknown`: kept whole, so that the parts together are the whole file.
    Parts that overlap an earlier one are cut to what is new of them.
    """
    out: list[tuple[str, int, int]] = []
    at = 0
    for kind, start, end in sorted((s for s in sections if s[2] > s[1]), key=lambda s: (s[1], s[2])):
        start = max(start, at)
        end = min(end, size)
        if end <= start:
            continue
        if start > at:
            out.append(("unknown", at, start))
        out.append((kind, start, end))
        at = end
    if at < size:
        out.append(("unknown", at, size))
    return out


# --------------------------------------------------------------------- League

ROFL1 = b"RIOT\x00\x00"
ROFL2 = b"RIOT\x02\x00"
#: ROFL1's chunk table entry: id, type (1 chunk, 2 keyframe), length, next chunk id, offset from the data's start.
_CHUNK = struct.Struct("<IBIII")
_CHUNK_TYPES = {1: "chunk", 2: "keyframe"}


def read_rofl(buf: bytes) -> dict[str, Any]:
    """
    The plain parts of a .rofl: game length, version, each player's box score,
    the whole metadata; for ROFL1 also the payload header and the chunk
    table. `sections` names every part of the file by its byte range, each
    with what is read of it (`decoded`), so each can be kept whole.
    """
    sections: list[tuple[str, int, int]] = []
    decoded: dict[tuple[str, int], Any] = {}
    payload: dict[str, Any] = {}
    chunks: list[dict[str, Any]] = []
    if buf[:6] == ROFL1:
        header_len, file_len, meta_off, meta_len, ph_off, ph_len, payload_off = struct.unpack_from("<HIIIIII", buf, 262)
        meta = json.loads(buf[meta_off : meta_off + meta_len].decode("utf-8"))
        sections += [("magic", 0, 6), ("signature", 6, 262), ("lengths", 262, 288), ("metadata", meta_off, meta_off + meta_len)]
        decoded[("lengths", 262)] = {"header_length": header_len, "file_length": file_len, "metadata_offset": meta_off,
                                     "metadata_length": meta_len, "payload_header_offset": ph_off,
                                     "payload_header_length": ph_len, "payload_offset": payload_off}
        decoded[("magic", 0)] = {"container": 1}
        game_id = None
        if ph_off + 34 <= len(buf):
            game_id, length, keyframes, nchunks, end_startup, start_game, interval, key_len = struct.unpack_from(
                "<QIIIIIIH", buf, ph_off)
            key = buf[ph_off + 34 : ph_off + 34 + key_len]
            payload = {"game_id": game_id, "game_length": length, "keyframe_count": keyframes, "chunk_count": nchunks,
                       "end_startup_chunk_id": end_startup, "start_game_chunk_id": start_game,
                       "keyframe_interval": interval, "encryption_key_length": key_len,
                       "encryption_key": key.decode("latin-1")}
            sections.append(("payload_header", ph_off, ph_off + max(ph_len, 34 + key_len)))
            decoded[("payload_header", ph_off)] = payload
            table = payload_off
            data_start = payload_off + _CHUNK.size * (keyframes + nchunks)
            for i in range(keyframes + nchunks):
                at = table + i * _CHUNK.size
                if at + _CHUNK.size > len(buf):
                    break
                cid, ctype, clen, nxt, coff = _CHUNK.unpack_from(buf, at)
                entry = {"id": cid, "type": _CHUNK_TYPES.get(ctype, ctype), "length": clen, "next_chunk_id": nxt,
                         "offset": coff}
                chunks.append(entry)
                sections.append(("chunk_header", at, at + _CHUNK.size))
                decoded[("chunk_header", at)] = entry
                start = data_start + coff
                # The chunk's bytes: encrypted, kept whole.
                sections.append((str(_CHUNK_TYPES.get(ctype, f"chunk type {ctype}")), start, start + clen))
        version = meta.get("gameVersion", "")
        container = 1
    elif buf[:6] == ROFL2:
        (n,) = struct.unpack_from("<i", buf, len(buf) - 4)
        if n <= 0 or n > len(buf) - 4:
            raise ValueError("no metadata at the end of the replay")
        meta_off = len(buf) - 4 - n
        meta = json.loads(buf[meta_off : len(buf) - 4].decode("utf-8"))
        version = buf[14:29].split(b"\x00")[0].decode("utf-8", errors="replace").strip()
        game_id = None
        container = 2
        # Before the metadata: the game itself, in a layout not published; only the version is read of it.
        sections += [("body", 0, meta_off), ("metadata", meta_off, len(buf) - 4), ("metadata_length", len(buf) - 4, len(buf))]
        decoded[("body", 0)] = {"container": 2, "version": version}
        decoded[("metadata_length", len(buf) - 4)] = {"metadata_length": n}
    else:
        raise ValueError("not a League of Legends replay")
    decoded[("metadata", meta_off)] = {k: v for k, v in meta.items() if k != "statsJson"}
    stats = meta.get("statsJson", "[]")
    players = json.loads(stats) if isinstance(stats, str) else stats
    return {
        "container": container,
        "version": version,
        "length_ms": meta.get("gameLength"),
        "game_id": game_id,
        "players": players if isinstance(players, list) else [],
        "metadata": meta,
        "payload": payload,
        "chunks": chunks,
        "sections": [(kind, start, end, decoded.get((kind, start))) for kind, start, end in _gaps(sections, len(buf))],
    }


# -------------------------------------------------------------------- Valorant

VRF_MAGIC = 0x43F4EFDD
_GROUP = b"EReplayEventGroup::"
#: The chunk types of an Unreal local replay.
VRF_CHUNKS = {0: "header", 1: "replay_data", 2: "checkpoint", 3: "event"}


def _fstring(buf: bytes, at: int) -> tuple[str, int]:
    """An Unreal FString: an int32 length (negative: UTF-16), then the characters with their terminator."""
    (n,) = struct.unpack_from("<i", buf, at)
    at += 4
    if n == 0:
        return "", at
    if n > 0:
        raw = buf[at : at + n]
        return raw.split(b"\x00")[0].decode("latin-1"), at + n
    size = -n * 2
    return buf[at : at + size].decode("utf-16-le", errors="replace").split("\x00")[0], at + size


def read_vrf(buf: bytes) -> dict[str, Any]:
    """
    The open parts of a Valorant replay: header facts and the event timeline.

    The replay's info block is read field by field (vrfkit's layout); the chunks
    after it are walked by their type and size. Inside the header chunk the map
    and the match's own JSON are looked up by what they look like, not by offset:
    the fields before them change between builds, and a reader that guessed an
    offset would read a wrong map with confidence.

    An encrypted replay is walked the same way, its chunks' contents left
    unread. `sections` names every part of the file by its byte range, each with
    what is read of it, so each can be kept whole.
    """
    (magic, file_version) = struct.unpack_from("<II", buf, 0)
    if magic != VRF_MAGIC:
        raise ValueError("not an Unreal replay")
    at = 8
    (versions,) = struct.unpack_from("<i", buf, at)
    custom = [buf[at + 4 + i * 20 : at + 24 + i * 20].hex() for i in range(max(0, versions))]
    at += 4 + max(0, versions) * 20
    length_ms, network, changelist = struct.unpack_from("<iII", buf, at)
    at += 12
    friendly, at = _fstring(buf, at)
    live, ticks, compressed, encrypted = struct.unpack_from("<IqII", buf, at)
    at += 20
    (key_len,) = struct.unpack_from("<i", buf, at)
    key = buf[at + 4 : at + 4 + max(0, key_len)]
    at += 4 + max(0, key_len)
    info = {"magic": magic, "file_version": file_version, "custom_versions": custom, "length_ms": length_ms,
            "network_version": network, "changelist": changelist, "name": friendly, "is_live": bool(live),
            "timestamp_ticks": ticks, "compressed": bool(compressed), "encrypted": bool(encrypted),
            "encryption_key_length": key_len, "encryption_key": key.hex()}
    out: dict[str, Any] = {
        "file_version": file_version,
        "length_ms": length_ms,
        "name": friendly,
        "recorded_unix": ticks / 1e7 - 62135596800 if ticks > 0 else None,
        "encrypted": bool(encrypted),
        "info": info,
        "map": None,
        "match_id": None,
        "agents": [],
        "events": [],
        "sections": [("info", 0, at, info)],
    }
    while at + 8 <= len(buf):
        kind, size = struct.unpack_from("<Ii", buf, at)
        if size < 0 or at + 8 + size > len(buf):
            break
        start = at
        at += 8
        chunk = buf[at : at + size]
        at += size
        name = VRF_CHUNKS.get(kind, f"chunk {kind}")
        decoded: Any = None
        if not encrypted and kind == 0:
            _header(chunk, out)
            decoded = {k: out[k] for k in ("map", "match_id", "agents")}
        elif not encrypted and kind == 3:
            ev = _event(chunk)
            if ev:
                out["events"].append(ev)
                decoded = ev
                name = f"event {ev['group']}"
        out["sections"].append((name, start, at, decoded))
    if at < len(buf):
        # After the last whole chunk: a chunk cut short, or bytes the layout does not describe.
        out["sections"].append(("trailing", at, len(buf), None))
    return out


def _header(chunk: bytes, out: dict[str, Any]) -> None:
    text = chunk.decode("latin-1")
    m = re.search(r"/Game/Maps/[A-Za-z0-9_/]+", text)
    if m:
        out["map"] = m.group(0)
    m = re.search(r'"matchI[Dd]"\s*:\s*"([0-9a-fA-F-]{8,})"', text)
    if m:
        out["match_id"] = m.group(1)
    out["agents"] = sorted(set(re.findall(r'"characterId"\s*:\s*"([0-9a-fA-F-]{36})"', text)))


#: The server's event groups, as the watcher names them.
EVENTS = {
    "characterDeath": "kill",
    "roundStarted": "round_start",
    "spikePlanted": "spike_planted",
    "spikeDefused": "spike_defused",
    "spikeExploded": "spike_exploded",
    "characterUltimateUsed": "ultimate",
    "switchTeams": "switch_sides",
}


def _event(chunk: bytes) -> dict[str, Any] | None:
    try:
        event_id, at = _fstring(chunk, 0)
        group, at = _fstring(chunk, at)
        meta, at = _fstring(chunk, at)
        time1, time2, size = struct.unpack_from("<IIi", chunk, at)
        at += 12
        payload = chunk[at : at + max(0, size)]
    except struct.error:
        return None
    mark = payload.find(_GROUP)
    if mark < 4:
        return None
    end = payload.find(b"\x00", mark)
    name = payload[mark + len(_GROUP) : end].decode("latin-1")
    words_end = mark - 4  # the FString's length sits before its text
    words = list(struct.unpack_from(f"<{max(0, (words_end - 4) // 4)}I", payload, 4)) if words_end > 4 else []
    seconds = None
    if end + 5 <= len(payload):
        (seconds,) = struct.unpack_from("<f", payload, end + 1)
    return {"group": name, "event": EVENTS.get(name, name), "time_ms": time1, "end_ms": time2, "seconds": seconds,
            "words": words, "chunk_group": group, "id": event_id, "metadata": meta}

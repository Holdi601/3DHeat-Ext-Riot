"""
heat3d-riot-replays catalog: what the installed games name, read from their files on disk (never from a
running game, its client or its anti-cheat; nothing encrypted is read).

    heat3d-riot-replays catalog [--game lol|valorant] [-o <levels>] [--oodle <dll>]

VALORANT: agents and their abilities, from the English text table of the install
(`ShooterGame/Content/Paks/en_US_Text-WindowsClient.pak`). The archive's file index is
encrypted and is not read: the archive is walked entry by entry from its start (each
entry: offset, size, size unpacked, compression, hash, the compressed blocks, an
encryption flag, the block size), only entries that are not encrypted are read, and their
Oodle blocks are unpacked with an Oodle library you name (`--oodle` or `HEAT3D_OODLE`; the
game ships none to load). The text table is Unreal's `.locres` (version 3): namespaces of
keys and the shared strings. An agent is a namespace holding `DisplayName` and ability
names (`Ability1_DisplayName`, `GrenadeAbility_DisplayName`, `Ultimate_DisplayName`,
`Ability_Q_DisplayName` ...); the namespace is the agent's working name ("Wushu" for Jett).

League of Legends: the champions, one archive each under `Game/DATA/FINAL/Champions`
(`<Champion>.wad.client`, the language archives beside them skipped), by their file names
(the game's working names: `MonkeyKing` is Wukong). Items need the game's hashed data tables
and are not read yet.

Both write the viewer's catalogue format (`3dheat-catalog`, version 1) to
`<levels>/<game>/catalog.json`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
from pathlib import Path
from typing import Callable

from . import __version__

#: Riot's install records: `<ProgramData>/Riot Games/Metadata/<product>/<product>.product_settings.yaml`.
PRODUCTS = {"lol": "league_of_legends.live", "valorant": "valorant.live"}
DEFAULT_DIRS = {"lol": "League of Legends", "valorant": "VALORANT"}
TEXT_PAK = Path("ShooterGame") / "Content" / "Paks" / "en_US_Text-WindowsClient.pak"
LOCRES = bytes.fromhex("0E147475674A03FC4A15909DC3377F1B")
PAK_MAGIC = 0x5A6F12E1
ABILITY_KEY = re.compile(r"^(Ability\w*|GrenadeAbility|Ultimate|PassiveAbility)_DisplayName$")

Decompress = Callable[[bytes, int], bytes]


#: Riot's programs: while one runs, no game file is read.
RIOT_PROGRAMS = {"valorant.exe", "valorant-win64-shipping.exe", "league of legends.exe", "leagueclient.exe",
                 "leagueclientux.exe", "riotclientservices.exe", "riot client.exe"}


def riot_running() -> list[str]:
    """The Riot programs running now (Windows: the task list's names; elsewhere none are looked for)."""
    if sys.platform != "win32":
        return []
    import subprocess

    try:
        r = subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True, timeout=20,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.SubprocessError):
        return []
    names = {line.split('","')[0].strip('"').lower() for line in r.stdout.splitlines() if line.startswith('"')}
    return sorted(names & RIOT_PROGRAMS)


def not_running() -> None:
    running = riot_running()
    if running:
        raise RuntimeError("a Riot program is running (" + ", ".join(running) + "); close it and try again: "
                           "game files are read only while no Riot program runs")


# ---------------------------------------------------------------------------------------------- installs


def _metadata_dir() -> Path:
    return Path(os.environ.get("ProgramData", r"C:\ProgramData")) / "Riot Games" / "Metadata"


def install_dir(game: str) -> Path | None:
    """The game's install folder: Riot's install record (read only), else `<drive>:/Riot Games/<game>`."""
    product = PRODUCTS[game]
    settings = _metadata_dir() / product / f"{product}.product_settings.yaml"
    candidates: list[Path] = []
    try:
        for line in settings.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r'\s*product_install_full_path:\s*"?([^"]+?)"?\s*$', line)
            if m:
                candidates.append(Path(m.group(1)))
    except OSError:
        pass
    if sys.platform == "win32":
        candidates += [Path(f"{d}:/Riot Games") / DEFAULT_DIRS[game] for d in "CDEFGH"]
    for c in candidates:
        if _is_install(game, c):
            return c
    return None


def _is_install(game: str, p: Path) -> bool:
    try:
        if game == "valorant":
            return (p / "live" / TEXT_PAK).is_file() or (p / TEXT_PAK).is_file()
        return (p / "Game" / "DATA" / "FINAL" / "Champions").is_dir()
    except OSError:
        return False


def text_pak(valorant: Path) -> Path:
    live = valorant / "live" / TEXT_PAK
    return live if live.is_file() else valorant / TEXT_PAK


def champions_dir(lol: Path) -> Path:
    return lol / "Game" / "DATA" / "FINAL" / "Champions"


# --------------------------------------------------------------------------------------------- the pak


def pak_entries(data: bytes, decompress: Decompress | None) -> list[bytes]:
    """
    The unencrypted entries of an Unreal pak (version 8 to 11), walked from its start up to the index
    (the footer says where it starts). Entries the pak marks encrypted are skipped, never decrypted.
    """
    tail = data[-256:]
    at = tail.rfind(struct.pack("<I", PAK_MAGIC))
    if at < 0:
        raise ValueError("not an Unreal pak (no footer)")
    version = struct.unpack_from("<I", tail, at + 4)[0]
    index = struct.unpack_from("<q", tail, at + 8)[0]
    if not 8 <= version <= 11:
        raise ValueError(f"pak version {version} is not read")
    out: list[bytes] = []
    p = 0
    while p + 53 <= index:
        # offset, size, size unpacked, compression, hash[20], (blocks), flags, block size
        _, size, raw, method = struct.unpack_from("<qqqI", data, p)
        blocks: list[tuple[int, int]] = []
        q = p + 48
        if method:
            n = struct.unpack_from("<I", data, q)[0]
            if not 0 < n <= 1 << 20:
                break
            blocks = [struct.unpack_from("<qq", data, q + 4 + 16 * i) for i in range(n)]
            q += 4 + 16 * n
        flags, block_size = data[q], struct.unpack_from("<I", data, q + 1)[0]
        head = q + 5 - p
        if size <= 0 or raw <= 0:
            break
        end = p + blocks[-1][1] if blocks else p + head + size
        if not flags & 1:  # encrypted entries are skipped
            if not method:
                out.append(data[p + head:p + head + size])
            elif decompress is not None and block_size > 0:
                body = bytearray()
                for i, (s, e) in enumerate(blocks):
                    body += decompress(data[p + s:p + e], min(block_size, raw - block_size * i))
                out.append(bytes(body))
        if end <= p:
            break
        p = end
    return out


# ------------------------------------------------------------------------------------------- the locres


def _fstring(b: bytes, p: int) -> tuple[str, int]:
    n = struct.unpack_from("<i", b, p)[0]
    p += 4
    if n < 0:
        return b[p:p - 2 * n].decode("utf-16-le", "replace").rstrip("\0"), p - 2 * n
    return b[p:p + n].decode("latin-1").rstrip("\0"), p + n


def locres(b: bytes) -> dict[str, dict[str, str]]:
    """An Unreal `.locres` (versions 2 and 3): namespace -> key -> text."""
    if b[:16] != LOCRES:
        raise ValueError("not a .locres")
    version = b[16]
    if version < 2:
        raise ValueError(f".locres version {version} is not read")
    strings_at = struct.unpack_from("<q", b, 17)[0]
    p = 25 + (4 if version >= 3 else 0)
    q = strings_at
    count = struct.unpack_from("<i", b, q)[0]
    q += 4
    strings = []
    for _ in range(count):
        s, q = _fstring(b, q)
        strings.append(s)
        q += 4  # how often the string is used
    out: dict[str, dict[str, str]] = {}
    namespaces = struct.unpack_from("<I", b, p)[0]
    p += 4
    for _ in range(namespaces):
        ns, p = _fstring(b, p + 4)
        keys = struct.unpack_from("<I", b, p)[0]
        p += 4
        table = out.setdefault(ns, {})
        for _ in range(keys):
            key, p = _fstring(b, p + 4)
            idx = struct.unpack_from("<i", b, p + 4)[0]
            p += 8
            if 0 <= idx < len(strings):
                table[key] = strings[idx]
    return out


# -------------------------------------------------------------------------------------------- catalogues


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _slot(key: str) -> str:
    """`Ability_Q_DisplayName` -> "q", `GrenadeAbility_DisplayName` -> "grenade", `Ultimate_...` -> "ultimate"."""
    k = key[: -len("_DisplayName")]
    if k == "GrenadeAbility":
        return "grenade"
    if k == "PassiveAbility":
        return "passive"
    if k == "Ultimate":
        return "ultimate"
    return k[len("Ability"):].strip("_").lower() or "ability"


def valorant_catalog(tables: dict[str, dict[str, str]], *, game_build: str = "", source: str = "") -> dict:
    agents: dict[str, dict] = {}
    abilities: dict[str, dict] = {}
    for ns, t in sorted(tables.items()):
        name = (t.get("DisplayName") or "").strip()
        keys = sorted(k for k in t if ABILITY_KEY.match(k) and t[k].strip())
        if not name or len(keys) < 2:
            continue
        aid = _slug(name)
        codename = re.sub(r"_?String(s|Table)$", "", ns, flags=re.I)
        agent = agents.setdefault(aid, {"id": aid, "kind": "agent", "name": name, "codename": codename,
                                        "abilities": [], "aliases": [ns]})
        for k in keys:
            iid = f"{aid}-{_slug(_slot(k))}"
            if iid in abilities:
                continue
            abilities[iid] = {"id": iid, "kind": "ability", "name": t[k].strip(), "agent": aid, "slot": _slot(k)}
            agent["abilities"].append(iid)
    items = sorted(agents.values(), key=lambda i: i["id"]) + sorted(abilities.values(), key=lambda i: i["id"])
    return {"format": "3dheat-catalog", "version": 1, "game": "valorant", "gameBuild": game_build,
            "source": source, "items": items}


def valorant_from_install(game: Path, decompress: Decompress, source: str = "") -> dict:
    data = text_pak(game).read_bytes()
    tables: dict[str, dict[str, str]] = {}
    for body in pak_entries(data, decompress):
        if body[:16] == LOCRES:
            for ns, t in locres(body).items():
                tables.setdefault(ns, {}).update(t)
    return valorant_catalog(tables, game_build=valorant_build(game) or "", source=source)


def valorant_build(game: Path) -> str | None:
    """The text archive's size and date, which change with each patch (the install keeps no plain version)."""
    try:
        st = text_pak(game).stat()
    except OSError:
        return None
    return f"{st.st_size}-{int(st.st_mtime)}"


def lol_champions(game: Path) -> list[str]:
    """The champions' working names: `<Champion>.wad.client` without the language archives (`<C>.en_US.wad.client`)."""
    out = []
    try:
        files = sorted(champions_dir(game).glob("*.wad.client"))
    except OSError:
        return []
    for f in files:
        stem = f.name[: -len(".wad.client")]
        if "." not in stem and stem.lower() != "common":
            out.append(stem)
    return out


def lol_build(game: Path) -> str | None:
    try:
        meta = json.loads((game / "Game" / "content-metadata.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    v = meta.get("version") if isinstance(meta, dict) else None
    return str(v) if v else None


def lol_catalog(game: Path, source: str = "") -> dict:
    items = [{"id": c.lower(), "kind": "champion", "name": c, "aliases": [c]} for c in lol_champions(game)]
    return {"format": "3dheat-catalog", "version": 1, "game": "lol", "gameBuild": lol_build(game) or "",
            "source": source, "items": items}


def plural(kind: str) -> str:
    return kind[:-1] + "ies" if kind.endswith("y") else kind + "s"


def item_ids(catalog: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for it in catalog.get("items", []):
        out.setdefault(it["kind"], []).append(it["id"])
    return {k: sorted(v) for k, v in out.items()}


def write(catalog: dict, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(catalog, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(out)
    return out


def decompressor(given: str | None = None) -> Decompress:
    from . import oodle

    oodle.load(given)
    return oodle.decompress


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="heat3d-riot-replays catalog", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", choices=("lol", "valorant"), action="append",
                    help="the game (default: both that are installed)")
    ap.add_argument("-o", "--out", help="the levels folder (default: HEAT3D_LEVELS); writes <out>/<game>/catalog.json")
    ap.add_argument("--oodle", help="VALORANT: path of an oo2core_9_win64.dll from software you have installed "
                    "(or set HEAT3D_OODLE)")
    ap.add_argument("--lol", help="League of Legends' folder (default: Riot's install record)")
    ap.add_argument("--valorant", help="VALORANT's folder (default: Riot's install record)")
    args = ap.parse_args(argv)
    levels = Path(args.out or os.environ.get("HEAT3D_LEVELS") or ".")
    source = f"heat3d-riot-replays {__version__}"
    try:
        not_running()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1
    code = 0
    for g in args.game or ["lol", "valorant"]:
        folder = getattr(args, g)
        game = Path(folder) if folder else install_dir(g)
        if game is None or not _is_install(g, game):
            if args.game:
                print(f"{g}: not found; name its folder with --{g}", file=sys.stderr)
                code = 1
            continue
        try:
            cat = lol_catalog(game, source) if g == "lol" else \
                valorant_from_install(game, decompressor(args.oodle), source)
        except Exception as e:  # one game failing does not stop the other
            print(f"{g}: {type(e).__name__}: {e}", file=sys.stderr)
            code = 1
            continue
        path = write(cat, levels / g / "catalog.json")
        counts = ", ".join(f"{len(v)} {plural(k)}" for k, v in sorted(item_ids(cat).items()))
        print(f"{path}: {counts}")
    return code

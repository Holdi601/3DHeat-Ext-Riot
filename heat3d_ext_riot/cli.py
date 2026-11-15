"""
heat3d-riot-replays list                               where League of Legends and VALORANT save replays, and the replays there
heat3d-riot-replays convert [REPLAY|FOLDER ...] -o OUT what each .rofl and .vrf carries in the open, into OUT

Exit status: 0 done, 1 a replay failed, 2 nothing to read (no replay found, not a
League of Legends or VALORANT replay).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import struct
import sys
from pathlib import Path
from typing import Any

from . import __version__

PROG = "heat3d-riot-replays"
#: What the JSON written for each replay is; the 3DHeat Watcher reads it.
FORMAT = "heat3d-riot-replay/1"
#: Each game's replays: its name, the file pattern, and the reader's kind.
GAMES = {".rofl": ("League of Legends", "rofl"), ".vrf": ("VALORANT", "vrf")}


def say(text: str) -> None:
    print(f"{PROG}: {text}", file=sys.stderr)


def replay_folders() -> list[tuple[str, Path]]:
    """Where the games save replays: League's `Documents/League of Legends/Replays`, VALORANT's `Saved/Demos`."""
    home = Path(os.environ.get("USERPROFILE", str(Path.home())))
    local = Path(os.environ.get("LOCALAPPDATA", str(home / "AppData" / "Local")))
    return [("League of Legends", home / "Documents" / "League of Legends" / "Replays"),
            ("VALORANT", local / "VALORANT" / "Saved" / "Demos")]


def replays_in(paths: list[str]) -> tuple[list[Path], list[Path]]:
    """The replays to read (each file given, each folder's `.rofl` and `.vrf`), and the folders looked in."""
    folders = [Path(p) for p in paths] if paths else [f for _, f in replay_folders()]
    found: list[Path] = []
    for p in folders:
        if p.is_file():
            found.append(p)
        elif p.is_dir():
            found += sorted(f for f in p.iterdir() if f.is_file() and f.suffix.lower() in GAMES)
    return found, folders


def read(path: Path) -> dict[str, Any]:
    """One replay, read: what it carries in the open, and every part of it by its byte range."""
    from .replays import read_rofl, read_vrf

    game, kind = GAMES.get(path.suffix.lower(), (None, None))
    buf = path.read_bytes()
    if kind is None:
        # Not named as either: told apart by its first bytes.
        kind = "rofl" if buf[:4] == b"RIOT" else "vrf"
        game = "League of Legends" if kind == "rofl" else "VALORANT"
    r = read_rofl(buf) if kind == "rofl" else read_vrf(buf)
    return {"format": FORMAT, "tool": {"name": PROG, "version": __version__}, "file": path.name, "size": len(buf),
            "game": game, "kind": kind, **r}


def _csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns: list[str] = []
    for row in rows:
        columns += [k for k in row if k not in columns]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)


def write(r: dict[str, Any], out: Path) -> list[Path]:
    """`<file>.json`, the whole reading; and a table: League's box score, VALORANT's event timeline."""
    out.mkdir(parents=True, exist_ok=True)
    doc = out / f"{r['file']}.json"
    doc.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    written = [doc]
    if r["kind"] == "rofl" and r["players"]:
        table = out / f"{r['file']}.players.csv"
        _csv(table, [{k: v for k, v in p.items()} for p in r["players"] if isinstance(p, dict)])
        written.append(table)
    elif r["kind"] == "vrf" and r["events"]:
        table = out / f"{r['file']}.events.csv"
        _csv(table, [{"event": e["event"], "group": e["group"], "seconds": e["seconds"], "time_ms": e["time_ms"],
                      "end_ms": e["end_ms"], "words": " ".join(str(w) for w in e["words"]), "id": e["id"],
                      "metadata": e["metadata"]} for e in r["events"]])
        written.append(table)
    return written


def cmd_list(args) -> int:
    total = 0
    for game, folder in replay_folders():
        found = sorted(f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in GAMES) if folder.is_dir() else []
        print(f"{game}: {folder}{'' if folder.is_dir() else ' (not there: no replay saved yet)'}")
        for f in found:
            print(f"  {f.name:36s} {f.stat().st_size / 1e6:8.1f} MB")
        total += len(found)
    print(f"{total} replay(s)")
    return 0 if total else 2


def cmd_convert(args) -> int:
    files, folders = replays_in(args.replay)
    if not files:
        say(f"no replay (.rofl, .vrf) found in {', '.join(str(f) for f in folders)}")
        return 2
    out = Path(args.out)
    failed = unread = done = 0
    for path in files:
        try:
            r = read(path)
        except (ValueError, IndexError, struct.error) as e:
            # A file of another kind, or too short for the layout it starts like.
            say(f"{path}: not a League of Legends or VALORANT replay this reader understands ({e})")
            unread += 1
            continue
        except Exception as e:  # noqa: BLE001 - one bad replay does not stop the next
            say(f"{path}: {type(e).__name__}: {e}")
            failed += 1
            continue
        for f in write(r, out):
            print(f)
        done += 1
    if failed or (unread and done):
        return 1
    return 0 if done else 2


def main(argv: list[str] | None = None) -> int:
    try:
        import heat3d_update

        heat3d_update.startup("heat3d_ext_riot")
    except Exception:  # an update check never stops a conversion
        pass
    ap = argparse.ArgumentParser(prog=PROG, description="What League of Legends and VALORANT replays carry in the open")
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="where League of Legends and VALORANT save replays, and the replays there")
    p.set_defaults(run=cmd_list)

    p = sub.add_parser("convert", help="each replay's open parts: <file>.json and a table (.csv)")
    p.add_argument("replay", nargs="*", help="a .rofl or .vrf replay, or a folder of them (default: both games' "
                   "replay folders)")
    p.add_argument("-o", "--out", required=True, help="the folder to write to")
    p.set_defaults(run=cmd_convert)

    args = ap.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())

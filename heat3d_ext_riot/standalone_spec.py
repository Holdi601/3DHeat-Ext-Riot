"""
The standalone app's description of this tool (app/spec.py): the folders League
of Legends and VALORANT save replays in (found where the games put them, or the
folder you choose), and reading their open parts as tasks. A replay reader has
no maps; its content (kit contract 2026-11-28) is each installed game's catalogue
(gamedata.py: VALORANT's agents and abilities, League's champions), found through
Riot's install records, so new agents, abilities and champions are listed by id. `python -m heat3d_ext_riot.standalone_spec` runs the app from a
checkout; the release executables run the same.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import GameSpec, Input, MapSource, Replays, Spec, Task, game_folders


def _usual(game: str) -> list[Path]:
    from .cli import replay_folders

    out = [f for name, f in replay_folders() if name == game]
    if game == "League of Legends" and sys.platform.startswith("linux"):
        # A Wine/Lutris prefix under ~/Games keeps the Windows user's Documents inside it.
        games = Path.home() / "Games"
        try:
            out += sorted(games.glob("*/drive_c/users/*/Documents/League of Legends/Replays")) if games.is_dir() else []
        except OSError:
            pass
    return out


def _finder(game: str, windows_only: bool = False):
    def find(given: str | None) -> Path | None:
        if given:
            return Path(given) if Path(given).is_dir() else None
        if windows_only and sys.platform != "win32":
            return None
        return paths.first(_usual(game), lambda p: p.is_dir())

    return find


def _convert(v: dict[str, str], levels: Path) -> list[str]:
    return ["heat3d-riot-replays", "convert", *([v["src"]] if v.get("src") else []), "-o", v["out"]]


def _src(levels: Path) -> str:
    found = game_folders(SPEC)
    p = found.get("lol") or found.get("valorant")
    return str(p) if p else ""

def _replay_info(path: Path) -> dict:
    """`info <replay> --json`: the header only (replay_info.py)."""
    from .replay_info import info

    return info(path)


# ------------------------------------------------------------- content (kit contract 2026-11-28)


def _content_source(cid: str, title: str, sources: list[Path], kind: str, note: str = "") -> MapSource:
    """A MapSource with `kind`, also with a kit that has no `kind` field yet (it is then an attribute)."""
    try:
        return MapSource(cid, title, sources, note=note, kind=kind)  # type: ignore[call-arg]
    except TypeError:
        m = MapSource(cid, title, sources, note=note)
        m.kind = kind  # type: ignore[attr-defined]
        return m


def _install(key: str) -> Path | None:
    from .gamedata import install_dir

    return install_dir(key)


def _sources(key: str, game: Path) -> list[Path]:
    from . import gamedata

    if key == "valorant":
        pak = gamedata.text_pak(game)
        return [pak] if pak.is_file() else []
    meta = game / "Game" / "content-metadata.json"
    return [meta] if meta.is_file() else []


def _content_hooks(key: str) -> dict:
    title = "Agents and abilities" if key == "valorant" else "Champions"

    def contents(_found: Path) -> list[MapSource]:
        game = _install(key)
        files = _sources(key, game) if game else []
        return [_content_source("catalog", title, files, "catalog", "catalog.json")] if files else []

    def catalogue(game: Path) -> dict:
        from . import gamedata

        source = f"heat3d-riot-replays {__version__}"
        gamedata.not_running()
        if key == "lol":
            return gamedata.lol_catalog(game, source)
        return gamedata.valorant_from_install(game, gamedata.decompressor(), source)

    def extract_content(_found: Path, m: MapSource, out: Path, log) -> list[Path]:
        from . import gamedata

        game = _install(key)
        if m.id != "catalog" or game is None:
            raise ValueError(f"{key}: no install for {m.id}")
        cat = catalogue(game)
        path = gamedata.write(cat, out / "catalog.json")
        log(f"{key} catalogue: " + ", ".join(f"{len(v)} {gamedata.plural(k)}" for k, v in sorted(gamedata.item_ids(cat).items())))
        return [path]

    def catalog_items(_found: Path) -> dict[str, list[str]]:
        from . import gamedata

        game = _install(key)
        return gamedata.item_ids(catalogue(game)) if game else {}

    def extracted_items(out: Path) -> dict[str, list[str]]:
        import json

        from . import gamedata

        try:
            return gamedata.item_ids(json.loads((out / "catalog.json").read_text(encoding="utf-8")))
        except (OSError, ValueError, KeyError):
            return {}

    hooks = dict(contents=contents, extract_content=extract_content, catalog_items=catalog_items,
                 extracted_items=extracted_items)
    known = getattr(GameSpec, "__dataclass_fields__", {})
    return {k: v for k, v in hooks.items() if k in known}


SPEC = Spec(
    id="heat3d-riot",
    name="3DHeat Riot",
    repo="Holdi601/3DHeat-Ext-Riot",
    version=__version__,
    tools={"heat3d-riot-replays": "heat3d_ext_riot.cli:main"},
    default_tool="heat3d-riot-replays",
    description="What League of Legends and VALORANT replays carry in the open, for the 3DHeat viewer",
    module="heat3d_ext_riot.standalone_spec",
    games=[
        GameSpec(key="lol", label="League of Legends", find=_finder("League of Legends"), subdir="lol",
                 platforms=("windows-x64", "linux-x64", "macos-arm64"), **_content_hooks("lol")),
        GameSpec(key="valorant", label="VALORANT", find=_finder("VALORANT", windows_only=True), subdir="valorant",
                 platforms=("windows-x64",), **_content_hooks("valorant")),
    ],
    tasks=[
        Task("list", "List replay folders and replays", [], lambda v, levels: ["heat3d-riot-replays", "list"],
             help="where the games save replays, and the replays there"),
        Task("convert", "Convert replays",
             [Input("src", "Folder with .rofl or .vrf replays", "folder", default=_src),
              Input("out", "Where the results go", "folder",
                    default=lambda levels: str(paths.data_dir() / "matches" / "riot"))],
             _convert,
             help="each replay's open parts: <replay>.json and a table (.csv)"),
    ],
    min_free_gb=0.5,
    replays=Replays("riot", (".rofl", ".vrf"), lambda r, out: ["heat3d-riot-replays", "convert", str(r), "-o", str(out)], info=_replay_info),
    notice="Not affiliated with or endorsed by Riot Games.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))

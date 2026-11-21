"""
The standalone app's description of this tool (app/spec.py): the folders League
of Legends and VALORANT save replays in (found where the games put them, or the
folder you choose), and reading their open parts as tasks. A replay reader has
no maps. `python -m heat3d_ext_riot.standalone_spec` runs the app from a
checkout; the release executables run the same.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import GameSpec, Input, Spec, Task, game_folders


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
        GameSpec(key="lol", label="League of Legends", find=_finder("League of Legends"),
                 platforms=("windows-x64", "linux-x64", "macos-arm64")),
        GameSpec(key="valorant", label="VALORANT", find=_finder("VALORANT", windows_only=True),
                 platforms=("windows-x64",)),
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
    notice="Not affiliated with or endorsed by Riot Games.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))

"""Write docs/cli-reference.md from the code itself, so the reference cannot drift.

The options come from the program's own `--help`; the output's fields from
the code's own names.

    python tools/gen_docs_reference.py          # rewrite the page
    python tools/gen_docs_reference.py --check  # exit 1 when the page is stale
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "cli-reference.md"
COMMAND = "heat3d-riot-replays"
VERBS = ["list", "convert"]


def run(args):
    env = dict(os.environ, HEAT3D_NO_UPDATE="1", COLUMNS="88", PYTHONIOENCODING="utf-8",
               PYTHONPATH=str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    r = subprocess.run([sys.executable, "-m", "heat3d_ext_riot"] + args, capture_output=True, text=True,
                       env=env, encoding="utf-8", cwd=ROOT)
    return (r.stdout or r.stderr).rstrip()


def outputs():
    sys.path.insert(0, str(ROOT))
    from heat3d_ext_riot import cli, replays as r
    events = ", ".join(f"`{k}` -> `{v}`" for k, v in r.EVENTS.items())
    chunks = ", ".join(f"{k} `{v}`" for k, v in r.VRF_CHUNKS.items())
    return ["### `<file>.json`", "", f"`format`: `{cli.FORMAT}`; then `tool`, `file`, `size`, `game` "
            f"({', '.join(g for g, _ in cli.GAMES.values())}), `kind` ({', '.join(k for _, k in cli.GAMES.values())}), "
            "and the reading. `sections`: `[name, start, end, what was read or null]`, in file order, together the whole file.", "",
            "### VALORANT", "", f"Chunk types: {chunks}. Event groups, as named in the output: {events}; "
            "any other group under its own name.", "",
            "### League of Legends", "", "ROFL1 chunk table entry: `id`, `type` (" + ", ".join(
                f"{k} `{v}`" for k, v in r._CHUNK_TYPES.items()) + "), `length`, `next_chunk_id`, `offset`.", ""]


def build():
    out = ["---", "title: Command reference", "nav_order: 90", "---", "", "# Command reference", "",
           "Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.",
           "The other pages explain each command step by step.", "",
           f"## `{COMMAND}`", "", "```text", run(["--help"]), "```", ""]
    for v in VERBS:
        out += [f"## `{v}`", "", "```text", run([v, "--help"]), "```", ""]
    out += ["## Output", ""]
    return "\n".join(out + outputs())


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding="utf-8") == text else 1)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT))

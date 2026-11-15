---
title: Command reference
nav_order: 90
---

# Command reference

Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.
The other pages explain each command step by step.

## `heat3d-riot-replays`

```text
usage: heat3d-riot-replays [-h] [--version] {list,convert} ...

What League of Legends and VALORANT replays carry in the open

positional arguments:
  {list,convert}
    list          where League of Legends and VALORANT save replays, and the replays
                  there
    convert       each replay's open parts: <file>.json and a table (.csv)

options:
  -h, --help      show this help message and exit
  --version       show program's version number and exit
```

## `list`

```text
usage: heat3d-riot-replays list [-h]

options:
  -h, --help  show this help message and exit
```

## `convert`

```text
usage: heat3d-riot-replays convert [-h] -o OUT [replay ...]

positional arguments:
  replay         a .rofl or .vrf replay, or a folder of them (default: both games'
                 replay folders)

options:
  -h, --help     show this help message and exit
  -o, --out OUT  the folder to write to
```

## Output

### `<file>.json`

`format`: `heat3d-riot-replay/1`; then `tool`, `file`, `size`, `game` (League of Legends, VALORANT), `kind` (rofl, vrf), and the reading. `sections`: `[name, start, end, what was read or null]`, in file order, together the whole file.

### VALORANT

Chunk types: 0 `header`, 1 `replay_data`, 2 `checkpoint`, 3 `event`. Event groups, as named in the output: `characterDeath` -> `kill`, `roundStarted` -> `round_start`, `spikePlanted` -> `spike_planted`, `spikeDefused` -> `spike_defused`, `spikeExploded` -> `spike_exploded`, `characterUltimateUsed` -> `ultimate`, `switchTeams` -> `switch_sides`; any other group under its own name.

### League of Legends

ROFL1 chunk table entry: `id`, `type` (1 `chunk`, 2 `keyframe`), `length`, `next_chunk_id`, `offset`.

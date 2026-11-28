---
title: Command reference
nav_order: 90
---

# Command reference

Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.
The other pages explain each command step by step.

## `heat3d-riot-replays`

```text
usage: heat3d-riot-replays [-h] [--version] {list,convert,catalog} ...

What League of Legends and VALORANT replays carry in the open

positional arguments:
  {list,convert,catalog}
    list                where League of Legends and VALORANT save replays, and the
                        replays there
    convert             each replay's open parts: <file>.json and a table (.csv)
    catalog             the installed games' agents, abilities and champions (catalog
                        --help)

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
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

## `catalog`

```text
usage: heat3d-riot-replays catalog [-h] [--game {lol,valorant}] [-o OUT]
                                   [--oodle OODLE] [--lol LOL] [--valorant VALORANT]

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

options:
  -h, --help            show this help message and exit
  --game {lol,valorant}
                        the game (default: both that are installed)
  -o, --out OUT         the levels folder (default: HEAT3D_LEVELS); writes
                        <out>/<game>/catalog.json
  --oodle OODLE         VALORANT: path of an oo2core_9_win64.dll from software you
                        have installed (or set HEAT3D_OODLE)
  --lol LOL             League of Legends' folder (default: Riot's install record)
  --valorant VALORANT   VALORANT's folder (default: Riot's install record)
```

## Output

### `<file>.json`

`format`: `heat3d-riot-replay/1`; then `tool`, `file`, `size`, `game` (League of Legends, VALORANT), `kind` (rofl, vrf), and the reading. `sections`: `[name, start, end, what was read or null]`, in file order, together the whole file.

### VALORANT

Chunk types: 0 `header`, 1 `replay_data`, 2 `checkpoint`, 3 `event`. Event groups, as named in the output: `characterDeath` -> `kill`, `roundStarted` -> `round_start`, `spikePlanted` -> `spike_planted`, `spikeDefused` -> `spike_defused`, `spikeExploded` -> `spike_exploded`, `characterUltimateUsed` -> `ultimate`, `switchTeams` -> `switch_sides`; any other group under its own name.

### League of Legends

ROFL1 chunk table entry: `id`, `type` (1 `chunk`, 2 `keyframe`), `length`, `next_chunk_id`, `offset`.

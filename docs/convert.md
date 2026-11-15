---
title: "Reading: convert"
nav_order: 3
---

# Reading: `convert`

```bash
heat3d-riot-replays convert [<replay> or <folder> ...] -o <folder>
```

reads each `.rofl` and `.vrf` replay and writes what it carries in the open
into the `-o` folder. Without a replay it reads every one in both games'
folders ([list](list.md) shows which); a folder given reads each `.rofl` and
`.vrf` in it. Code:
[`heat3d_ext_riot/replays.py`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/heat3d_ext_riot/replays.py).

| Option | Does |
|---|---|
| `<replay>` or `<folder>` | what to read; several may be given (default: both games' replay folders) |
| `-o`, `--out FOLDER` | where the results go (required); made when missing |

For each replay it prints the files it wrote:

```text
out\EUW1-7123456789.rofl.json
out\EUW1-7123456789.rofl.players.csv
```

## League of Legends (.rofl)

Both container versions carry the end-of-game box score as plain JSON in the
file (`statsJson`): for each of the ten players the champion, kills, deaths,
assists, gold, damage to champions, items, team, role, win, their Riot ID, and
every other number the game totals - over a hundred per player.

| Container | Patches | Read |
|---|---|---|
| ROFL1 (`RIOT` 0 0) | 14.9 and before | the metadata JSON (game length, version, last chunk and keyframe ids, the box score); the lengths block; the payload header (game id, game length, keyframe and chunk counts, startup and game start chunk ids, keyframe interval, the chunk key as it is stored); the chunk table (id, type, length, next chunk, offset) |
| ROFL2 (`RIOT` 2 0) | 14.11 on | the metadata JSON at the end of the file, its length in the last four bytes; the version string near the start |

**Not read:** the game itself. ROFL1's chunks and keyframes and ROFL2's body
are encrypted, and the packets inside them obfuscated anew with every patch.
They are named by their byte range (`keyframe`, `chunk`, `body`) and left as
they are.

## VALORANT (.vrf)

A VALORANT replay is an Unreal Engine local replay: an info block, then chunks
by type and size.

| Part | Read |
|---|---|
| the info block | every field: file version, custom versions, length, network version, changelist, name, live flag, recording time, compressed and encrypted flags, the key as stored |
| the header chunk | the map, the match id and the agents picked - looked up by their form, not by an offset that changes between builds |
| each event chunk | id, group, metadata, start and end time, and of its data the event's name, its time in seconds and the numbers before it: a kill's killer and victim as network ids (not names), rounds starting, spikes planted, defused and exploding, ultimates used, sides switching |

**Not read:** positions, names, scores, abilities, every frame of the game -
they are in the replay data and checkpoint chunks, which are obfuscated. Of an
encrypted replay, the chunks are walked and named, nothing inside them read.

## What comes out

| File | Holds |
|---|---|
| `<file>.json` | everything read. `format` (`heat3d-riot-replay/1`), `tool`, `file`, `size`, `game`, `kind` (`rofl` or `vrf`), and the reading: League's `container`, `version`, `length_ms`, `game_id`, `players` (the box score), `metadata`, `payload`, `chunks`; VALORANT's `file_version`, `length_ms`, `name`, `recorded_unix`, `encrypted`, `info`, `map`, `match_id`, `agents`, `events` |
| `<file>.players.csv` | League: the box score, a row per player, every field as the game wrote it |
| `<file>.events.csv` | VALORANT: the event timeline, a row per event |

`sections` in the JSON lists every part of the file in order as
`[name, start, end, what was read of it]` - the last `null` for a part left
unread - and the parts together are the whole file, with any stretch no
known part covers named `unknown` (League) or `trailing` (VALORANT). Fields:
[Command reference](cli-reference.md#output).

## Using it

These files have no positions: they are tables to read, in a spreadsheet or a
script. The 3DHeat Watcher runs this tool on every replay the games save and
makes a session of it; for a League match, with your own Riot developer key in
its settings, it also fetches the match's official timeline from Riot's
Match-V5 API - every player's position once a minute and every kill where it
happened - which the 3DHeat viewer draws on the map
([League of Legends replays in the Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)).
That fetch is the Watcher's, not this tool's: this tool reads files only.

## How it was checked

On replays built field by field to the layouts in roflxd.cs (MIT) and vrfkit
(Apache-2.0), including a cut-short chunk and an encrypted VALORANT replay; no
real replay was available to check against. The reader checks before reading
and refuses what does not match, rather than guess.

## Messages and exit status

| Message | Exit | Means |
|---|---|---|
| the files written | 0 | done |
| `heat3d-riot-replays: no replay (.rofl, .vrf) found in ...` | 2 | nothing to read where it looked |
| `heat3d-riot-replays: <file>: not a League of Legends or VALORANT replay this reader understands (...)` | 2 | another kind of file, or a layout this tool does not know; among others that were read: 1 |
| `heat3d-riot-replays: <file>: <error>` | 1 | that replay failed; the others are still read |

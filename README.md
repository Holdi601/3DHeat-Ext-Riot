# 3DHeat Riot: what League of Legends and VALORANT replays carry in the open

**What is it?** This tool reads League of Legends (`.rofl`) and VALORANT
(`.vrf`) replays and writes out what each file carries in the open: League's
end-of-game box score for all ten players and the replay's header; VALORANT's
map, match id, agents and the server's timeline of kills, rounds and spikes.

**Why would I use it?** To keep your matches' numbers - every player's
kills, deaths, gold, damage and a hundred more per League game, every round
and kill of a VALORANT game - as plain tables, for your own statistics or the
[3DHeat](https://github.com/Holdi601/3DHeat) tools.

**Example:** `heat3d-riot-replays convert EUW1-7123456789.rofl -o out` ->
`out/EUW1-7123456789.rofl.json` (everything read) and
`out/EUW1-7123456789.rofl.players.csv` (the box score, a row per player).

**Documentation:** [holdi601.github.io/3DHeat-Ext-Riot](https://holdi601.github.io/3DHeat-Ext-Riot/),
a page per command with step-by-step use and example output. Part of
[3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)).

**What it does not do:** read positions or anything else of the game itself.
That part of a replay is encrypted. This tool reads only the unencrypted parts
of your own `.rofl` and `.vrf` files; it breaks no encryption and does no
deobfuscation - those parts are named by their place in the file and left unread -
and it ships no Riot assets: no game file, art, map, logo or data of the
games.

## The standalone program

No Python needed: download the file for your system (Windows, Linux and macOS) from the
[latest release](https://github.com/Holdi601/3DHeat-Ext-Riot/releases/latest), check it against `SHA256SUMS`, unpack it and start `heat3d-riot`. Its window
finds the replay folders, converts the replays there (or in any folder you pick),
and asks before it updates itself. `heat3d-riot --help` lists its commands (`heat3d-riot heat3d-riot-replays ...` runs every command below).
The 3DHeat app's Extractors panel can install and update it for you. See
[the install page](https://holdi601.github.io/3DHeat-Ext-Riot/before-you-start.html).

## Quick start for new users (Python)

You need: Windows, [Python](https://www.python.org/downloads/) 3.10 or later
("Add python.exe to PATH" ticked in its installer), and replays saved by the
games: in League of Legends' match history pick a match and click its download
button (it lands in `Documents\League of Legends\Replays\*.rofl`); in VALORANT,
Career, pick a match and download its replay (`%LOCALAPPDATA%\VALORANT\Saved\Demos\*.vrf`).
The tool finds both folders by itself. Nothing else is needed, no Git either.

1. Install the tool (one line, in PowerShell or a command prompt):

   ```bash
   python -m pip install https://github.com/Holdi601/3DHeat-Ext-Riot/archive/refs/tags/v0.1.0.zip
   ```

2. List the replays both games saved, then read them (or name one file; a
   League replays folder moved in the client's settings is given the same way):

   ```bash
   heat3d-riot-replays list
   heat3d-riot-replays convert -o out
   heat3d-riot-replays convert EUW1-7123456789.rofl -o out
   ```

3. The output lands in the `-o` folder, per replay named after the file:
   `out\<file>.json` (everything read) and a table, `out\<file>.players.csv`
   for League (the box score, a row per player) or `out\<file>.events.csv`
   for VALORANT (the event timeline). `convert` prints each file it wrote.
4. These have no positions, so they are tables to read, not to draw: open the
   `.csv` in a spreadsheet. For a League match on the map in the
   [3DHeat viewer](https://github.com/Holdi601/3DHeat#quick-start), the
   [3DHeat Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)
   runs this tool and adds the match's positions from Riot's API (with your own
   Riot developer key); open what it writes with **Source -> Files...** and
   **Load file** in the viewer (download it with **Code -> Download ZIP**, unpack, double-click
   `start.bat`, which offers to install [Node.js](https://nodejs.org/) when it
   is missing and opens Chrome or Edge at `http://127.0.0.1:5273`).

When a new release is out, the tool says so when it starts and offers to
update itself (`python -m heat3d_ext_riot.update` does the same).

## Install from a checkout

New to the command line? Read [Before you start](https://holdi601.github.io/3DHeat-Ext-Riot/before-you-start.html) first.

1. Install Python 3.10 or later. Nothing else is needed.
2. `git clone https://github.com/Holdi601/3DHeat-Ext-Riot` (or download the
   ZIP) and open a terminal in that folder.
3. Install the command and check where your replays are:

```bash
python -m pip install -e .        # installs the heat3d-riot-replays command
heat3d-riot-replays list          # where both games save replays, and the ones there
```

## Commands

| Command | Does | Page |
|---|---|---|
| `list` | where League of Legends (`Documents\League of Legends\Replays`) and VALORANT (`%LOCALAPPDATA%\VALORANT\Saved\Demos`) save replays, and the replays there | [list](https://holdi601.github.io/3DHeat-Ext-Riot/list.html) |
| `convert [REPLAY or FOLDER ...] -o OUT` | each replay's open parts into `OUT`; without a replay, every one in both games' folders | [convert](https://holdi601.github.io/3DHeat-Ext-Riot/convert.html) |

```bash
heat3d-riot-replays convert EUW1-7123456789.rofl -o out   # one replay
heat3d-riot-replays convert -o out                        # every replay both games saved
```

Exit status: 0 done; 1 a replay failed; 2 nothing to read - no replay found, or
a file that is not a replay this tool understands (the message says which).
Every option, as the program prints it: [Command reference](https://holdi601.github.io/3DHeat-Ext-Riot/cli-reference.html).

## What comes out, and using it

Per replay, named after the file:

- `<file>.json` - everything read: for League the game length, version, game
  id, every player's box score (`players`), the whole metadata, ROFL1's
  payload header and chunk table; for VALORANT the info block, the map, the
  match id, the agents and every event (kill with killer and victim as network
  ids, round start, spike planted, defused, exploded, ultimate, side switch).
  `sections` names every part of the file by its byte range with what was read
  of it, the unread parts included.
- `<file>.players.csv` (League) - the box score, a row per player, every field
  the game totals; `<file>.events.csv` (VALORANT) - the event timeline.

These have no positions, so they are tables to read, not to draw: open the CSV
in a spreadsheet. For a League match on the map in the 3DHeat viewer, the
3DHeat Watcher runs this tool and, with your own Riot developer key, adds the
match's official timeline from Riot's API - every player's position once a
minute and every kill where it happened
([League of Legends replays in the Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)).

## Terms

3DHeat Riot is not affiliated with or endorsed by Riot Games. League of Legends,
VALORANT and related names and trademarks belong to their owners. The tool reads
the replay files the games wrote on your computer, only what they carry in the
open, and talks to no server; nothing of the games is shipped or redistributed,
and what it writes stays on your machine ([Terms and
licence](https://holdi601.github.io/3DHeat-Ext-Riot/terms.html)).

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn on
a rights holder's request - on its own, without affecting the viewer or the
other tools.

Rights holders: open an issue at
[3DHeat-Ext-Riot/issues](https://github.com/Holdi601/3DHeat-Ext-Riot/issues) -
we respond quickly and remove anything on request.

## Tests

```bash
python -m pip install -e .[test]
python -m pytest
```

On made-up files only: no replay is part of this repository.

## Licence

MIT ([`LICENSE`](LICENSE)). What it uses and consulted: [`LICENSES.md`](LICENSES.md).

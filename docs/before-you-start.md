---
title: Before you start
nav_order: 1.5
---

# Before you start

New to the command line? This page takes you from nothing to a first run.
It takes about ten minutes, once.

## The standalone program (no Python needed)

Each [release](https://github.com/Holdi601/3DHeat-Ext-Riot/releases/latest) has a ready-to-run program for Windows, Linux and macOS
(`heat3d-riot-<version>-windows-x64.zip`, `...-linux-x64.tar.gz`, `...-macos-arm64.tar.gz`), with a
`SHA256SUMS` file to check the download. Unpack it anywhere and start `heat3d-riot` (on macOS the
first start may need *Open* from the right-click menu, as the program is not notarised).

Started without arguments it opens a window that:

- finds the folders the games keep replays in (League of Legends on Windows and macOS,
  VALORANT on Windows), or lets you choose one;
- says what is missing (the game, free disk space);
- lists what the replays there carry and converts them, as the commands below do (by default
  into the 3DHeat data folder's `matches/riot`);
- checks for updates and asks before installing one, unless you tick *Update automatically*.

The same program runs every command below: `heat3d-riot heat3d-riot-replays --help`. For scripts:
`heat3d-riot --check --json` says what is found and missing, and `heat3d-riot status --json` what is found
(a replay reader has no maps; `extract` has nothing to do). The 3DHeat app's Extractors panel installs,
updates and starts it for you.

The window walks through four steps (find the game, choose, work, done) in the 3DHeat look, dark or light. On Windows the program opens only its window, with no console window; in a terminal it prints as usual, and `heat3d-riot-cli.cmd` in the same folder makes the terminal wait for it and pass on its exit code.

Replays from the command line: `heat3d-riot convert <replay>... -o <folder> [--progress-json]` converts them (one JSON line per replay with `--progress-json`), and `heat3d-riot info <replay> --json` prints what a replay says about its match (map, mode, date, length, players, teams, result, game version), read from its header without converting it. The 3DHeat Library uses both.

## 1. Install Python

This tool needs **Python 3.10 or later**.

- **Windows:** download Python from [python.org/downloads](https://www.python.org/downloads/)
  and run the installer. On its first screen, tick **Add python.exe to PATH**,
  then click **Install Now**.
- **macOS and Linux:** Python 3 is often there already. Where these pages say
  `python`, type `python3`.

## 2. Get this tool

Open [github.com/Holdi601/3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot), click the
green **Code** button, then **Download ZIP**, and unzip it into a folder of your
choice. If you use git: `git clone https://github.com/Holdi601/3DHeat-Ext-Riot`.

## 3. Open a terminal in that folder

A terminal is a window where you type commands.

- **Windows:** open the folder in Explorer, click into the address bar, type
  `powershell` and press Enter. A blue or black window opens, already in that
  folder.
- **macOS:** open **Terminal**, type `cd ` (with a space), drag the folder into
  the window and press Enter.

`cd` means "change folder": `cd C:\Tools\3DHeat-Ext-Riot` goes to that folder.

## 4. Install the tool

Type this and press Enter:

```bash
python -m pip install -e .
```

You should see, at the end: `Successfully installed heat3d-ext-riot-...`.
The tool needs nothing but Python itself.

## 5. Save a replay and run it

In League of Legends, open your match history, pick a match and click the
download button; in VALORANT, open Career, pick a match and download its
replay. Then:

```bash
heat3d-riot-replays list
```

You should see something like:

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

Next: [Reading: convert](convert.md).

## How to read the commands on these pages

| You see | It means |
|---|---|
| `<file>` | a placeholder: type your own value instead, without the `< >` |
| `[REPLAY ...]` | optional: leave it out, or type it as shown |
| `# a note` | a comment for you: do not type it |
| `"C:\My Files\x"` | put a path that has spaces in quotes |

## When something goes wrong

| The message | What to do |
|---|---|
| `'python' is not recognized` | Python is not installed, or the PATH box was not ticked: install it again and tick it (or type `py` instead of `python`). |
| `'heat3d-riot-replays' is not recognized` | Run step 4 again in the tool's folder, or type `python -m heat3d_ext_riot` instead of `heat3d-riot-replays`: it does the same. |
| `no replay (.rofl, .vrf) found in ...` | Save a replay in the game first (step 5), or give the replay's path to `convert`. |
| `... not a League of Legends or VALORANT replay this reader understands` | The file is something else, or cut short; a replay in a layout this tool does not know is refused the same way. |
| anything else | Read the last line of the message, then open an issue on GitHub with it. |

Every command also ends with an **exit status**: 0 means it worked, 2 that
there was nothing to read, 1 that a replay failed. To see it, type
`echo $LASTEXITCODE` in PowerShell or `echo $?` on macOS and Linux.

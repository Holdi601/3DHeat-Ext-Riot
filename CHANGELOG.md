# Changelog

## 0.3.0

- Its own icon: the 3DHeat cube with a text badge for its game (letters in 3DHeat's colours), as the
  program, window, taskbar and docs icon.
- A new window: the 3DHeat look in dark and light (follows the system, switchable), the logo and
  icon, sharp at any display scaling. Four steps: find the game (each requirement with its fix),
  choose (maps ticked when there is something to do, filters, search; jobs with their fields
  inline), work (progress, time left, cancel), done (open in 3DHeat, open the output folder, and
  for a failure what went wrong and what to do, copy details, report a problem).
- No console window on Windows: the program is a window program. From a terminal it still prints
  as before; `heat3d-riot-cli.cmd` beside it waits for it in a terminal and passes its exit code.
- The update offer in the same look: Update now / Later / Skip this version, and "Update
  automatically" from the dialog.
- CI draws every page and dialog of the window (on Linux under a virtual display) and checks the
  Windows build is a window program.
- `heat3d-riot convert <replay>... -o <out> [--progress-json]` and `heat3d-riot info <replay> --json` (what the
  replay says about its match, read from its header without converting it), the same verbs in every
  3DHeat replay reader; the old command lines work as before.

## 0.2.0

- A standalone program for Windows, Linux and macOS (no Python needed), built by CI with a `SHA256SUMS` file.
  Without arguments it opens a window: what is found and what is missing, and the conversions as buttons.
- `status --json` and `--check --json` for the 3DHeat app's Extractors panel; a replay reader has no maps, so
  `extract` has nothing to do.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).

## 0.1.0

- First version, moved out of the 3DHeat Watcher (its `lol-replays` and
  `valorant-replays` adapters now run this tool): what League of Legends
  (`.rofl`, both containers) and VALORANT (`.vrf`) replays carry in the open -
  the end-of-game box score, the header facts and ROFL1's chunk table; the
  map, match id, agents and the server's event timeline of a VALORANT replay -
  with every part of the file named by its byte range. Nothing encrypted or
  obfuscated is read. `list` says where both games save replays; `convert`
  writes `<file>.json` and a table (`.players.csv`, `.events.csv`).
- Installs with one pip line from the release zip, no Git needed; a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-Riot](https://holdi601.github.io/3DHeat-Ext-Riot/)):

| Feature | Page |
|---|---|
| Installing, a first run | [Before you start](docs/before-you-start.md) |
| Where replays are, saving one (`list`) | [Finding replays: list](docs/list.md) |
| Reading (`convert`), what comes out, what is not read | [Reading: convert](docs/convert.md) |
| What is read and what is not, the Riot API key, the licence | [Terms and licence](docs/terms.md) |
| Every option and field, generated | [Command reference](docs/cli-reference.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |

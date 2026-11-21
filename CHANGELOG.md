# Changelog

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

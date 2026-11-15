# Changelog

## 0.1.0

- First version, moved out of the 3DHeat Watcher (its `lol-replays` and
  `valorant-replays` adapters now run this tool): what League of Legends
  (`.rofl`, both containers) and VALORANT (`.vrf`) replays carry in the open -
  the end-of-game box score, the header facts and ROFL1's chunk table; the
  map, match id, agents and the server's event timeline of a VALORANT replay -
  with every part of the file named by its byte range. Nothing encrypted or
  obfuscated is read. `list` says where both games save replays; `convert`
  writes `<file>.json` and a table (`.players.csv`, `.events.csv`).

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-Riot](https://holdi601.github.io/3DHeat-Ext-Riot/)):

| Feature | Page |
|---|---|
| Installing, a first run | [Before you start](docs/before-you-start.md) |
| Where replays are, saving one (`list`) | [Finding replays: list](docs/list.md) |
| Reading (`convert`), what comes out, what is not read | [Reading: convert](docs/convert.md) |
| Riot's terms, what is read and what is not, the Riot API key | [Terms and licence](docs/terms.md) |
| Every option and field, generated | [Command reference](docs/cli-reference.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |

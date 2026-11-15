---
title: Home
nav_order: 1
---

# 3DHeat Riot

**What is it?** This tool reads League of Legends (`.rofl`) and VALORANT
(`.vrf`) replays and writes out **what each file carries in the open**:
League's end-of-game box score for all ten players and the replay's header;
VALORANT's map, match id, agents and the server's timeline of kills, rounds and
spikes. It is one of the tools around the [3DHeat](https://github.com/Holdi601/3DHeat)
viewer ([documentation](https://holdi601.github.io/3DHeat/)).

**Why would I use it?** To keep your matches' numbers as plain tables - every
League player's kills, deaths, gold, damage and a hundred more, every round and
kill of a VALORANT game - for your own statistics, or for the 3DHeat Watcher,
which runs this tool on every replay you save.

**Example:** `heat3d-riot-replays convert EUW1-7123456789.rofl -o out` ->
`out/EUW1-7123456789.rofl.json` and `out/EUW1-7123456789.rofl.players.csv`.

**What it does not do:** read positions or the game itself. That part of a
replay is encrypted and obfuscated against cheating, and getting through it
would mean taking the game apart, which Riot's terms forbid. This tool breaks
no encryption and undoes no obfuscation ([Terms](terms.md)).

## Quick start

New to the command line? Read [Before you start](before-you-start.md) first.
You need Python 3.10 or later, nothing else. Run these in the folder you cloned
or unzipped:

```bash
python -m pip install -e .                  # installs the heat3d-riot-replays command
heat3d-riot-replays list                    # where both games save replays, the ones there
heat3d-riot-replays convert -o out          # every replay there, read
```

`convert` prints each file it wrote. Open the `.csv` in a spreadsheet, or
read the `.json` ([Reading: convert](convert.md)).

## Pages

| Page | What it covers |
|---|---|
| [Before you start](before-you-start.md) | Python, a terminal, a first run |
| [Finding replays: list](list.md) | where both games save replays, saving one, what `list` prints |
| [Reading: convert](convert.md) | what is read of each file, what comes out, what is not read |
| [Terms and licence](terms.md) | Riot's terms, what is read and what never is, the Riot API key |
| [Command reference](cli-reference.md) | every option and field, generated from the code |
| [Maintaining these docs](maintaining.md) | the release checklist |

## Related

- The 3DHeat viewer: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentation at [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- The 3DHeat Watcher runs this tool on every replay the games save; for League,
  with your own Riot developer key, it adds the match's official timeline with
  positions: [League of Legends replays](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html),
  [VALORANT replays](https://holdi601.github.io/3DHeat-Watcher/game-valorant-replays.html).
- League of Legends while you play (Riot's Live Client Data API):
  [the Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-live.html).

## The 3DHeat tools

| Tool | What it does | Code | Docs |
|---|---|---|---|
| 3DHeat viewer | shows the data: heatmaps, race analysis, match review | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | levels and courses from a game's own files | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | lap telemetry, and levels rebuilt from gameplay video | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | an Unreal Editor plugin: a level as one `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike 2 demos and maps | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | records what games publish while you play | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | War Thunder replays | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | World of Tanks replays | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | World of Warships replays | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | Squad server demos | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | DCS World maps as 3D levels | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | IL-2 Sturmovik maps as 3D levels | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | the Dota 2 map as a 3D level | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | Dota 2 replays as tables | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | League of Legends and VALORANT replays: what they carry in the open | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | Forza courses, races and cars from your own install | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | Battlefield levels (Frostbite) as 3D levels | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | BeamNG.drive courses | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | Assetto Corsa Rally stages as courses | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | Arma Reforger worlds (Enfusion) as 3D levels | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | Rainbow Six Siege match replays | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |

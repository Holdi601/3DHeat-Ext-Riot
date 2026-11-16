---
title: "Replays finden: list"
nav_order: 2
lang: "de"
source: list.md
source_hash: "0d13db1af26d"
nav_exclude: true
search_exclude: true
---
# Replays finden: `list` {#finding-replays-list}

```bash
heat3d-riot-replays list
```

gibt aus, wo League of Legends und VALORANT Replays speichern, und jedes Replay dort mit
seiner Größe. Ohne angegebenes Replay liest [`convert`](convert.md) die, die `list` zeigt.

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

## Wo die Replays liegen {#where-replays-are}

| Spiel | Ordner | Eins speichern |
|---|---|---|
| League of Legends | `%USERPROFILE%\Documents\League of Legends\Replays\*.rofl` | die Matchhistorie im Client: ein Match auswählen und auf den Download-Button klicken. Die Datei heißt `<platform>-<game id>.rofl`, z. B. `EUW1-7123456789.rofl` |
| VALORANT | `%LOCALAPPDATA%\VALORANT\Saved\Demos\*.vrf` | Karriere: ein Match auswählen, dessen Replay herunterladen |

League lässt dich den Replay-Ordner in den Einstellungen des Clients verschieben
(Replays); gib diesen Ordner dann an `convert`. Ein Replay, das dir jemand schickt,
funktioniert genauso: Gib seinen Pfad an `convert`.

## Meldungen und Exit-Status {#messages-and-exit-status}

| Meldung | Exit | Bedeutet |
|---|---|---|
| `<game>: <folder> (not there: no replay saved yet)` | - | dieses Spiel hat auf diesem Rechner noch kein Replay gespeichert |
| `0 replay(s)` | 2 | keiner der beiden Ordner hat ein Replay |
| `<n> replay(s)` | 0 | gefunden |

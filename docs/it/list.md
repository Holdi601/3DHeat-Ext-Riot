---
title: "Trovare i replay: list"
nav_order: 2
lang: "it"
source: list.md
source_hash: "0d13db1af26d"
nav_exclude: true
search_exclude: true
---
# Trovare i replay: `list` {#finding-replays-list}

```bash
heat3d-riot-replays list
```

stampa dove League of Legends e VALORANT salvano i replay, e ogni replay presente con la sua dimensione.
Senza un replay indicato, [`convert`](convert.md) legge quelli che `list` mostra.

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

## Dove sono i replay {#where-replays-are}

| Gioco | Cartella | Come salvarne uno |
|---|---|---|
| League of Legends | `%USERPROFILE%\Documents\League of Legends\Replays\*.rofl` | la cronologia delle partite del client: scegli una partita, clicca sul pulsante di download. Il file si chiama `<platform>-<game id>.rofl`, ad esempio `EUW1-7123456789.rofl` |
| VALORANT | `%LOCALAPPDATA%\VALORANT\Saved\Demos\*.vrf` | Career: scegli una partita, scarica il suo replay |

League permette di spostare la sua cartella dei replay nelle impostazioni del client (Replays); indica poi quella
cartella a `convert`. Un replay che qualcuno ti manda funziona allo stesso modo: dai il suo percorso a `convert`.

## Messaggi e stato di uscita {#messages-and-exit-status}

| Messaggio | Uscita | Significa |
|---|---|---|
| `<game>: <folder> (not there: no replay saved yet)` | - | quel gioco non ha ancora salvato alcun replay su questo computer |
| `0 replay(s)` | 2 | nessuna delle due cartelle contiene un replay |
| `<n> replay(s)` | 0 | trovati |

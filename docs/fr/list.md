---
title: "Trouver les replays : list"
nav_order: 2
lang: "fr"
source: list.md
source_hash: "0d13db1af26d"
nav_exclude: true
search_exclude: true
---
# Trouver les replays : `list` {#finding-replays-list}

```bash
heat3d-riot-replays list
```

affiche où League of Legends et VALORANT sauvegardent les replays, et chaque replay
qui s'y trouve avec sa taille. Sans replay donné, [`convert`](convert.md) lit ceux
que `list` affiche.

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

## Où sont les replays {#where-replays-are}

| Jeu | Dossier | Sauvegarder un replay |
|---|---|---|
| League of Legends | `%USERPROFILE%\Documents\League of Legends\Replays\*.rofl` | l'historique de parties du client : choisissez une partie, cliquez sur le bouton de téléchargement. Le fichier s'appelle `<platform>-<game id>.rofl`, par exemple `EUW1-7123456789.rofl` |
| VALORANT | `%LOCALAPPDATA%\VALORANT\Saved\Demos\*.vrf` | Carrière : choisissez une partie, téléchargez son replay |

League vous permet de déplacer son dossier de replays dans les réglages du client (Replays) ;
donnez alors ce dossier à `convert`. Un replay que quelqu'un vous envoie fonctionne de la même façon :
donnez son chemin à `convert`.

## Messages et code de sortie {#messages-and-exit-status}

| Message | Sortie | Signification |
|---|---|---|
| `<game>: <folder> (not there: no replay saved yet)` | - | ce jeu n'a encore sauvegardé aucun replay sur cette machine |
| `0 replay(s)` | 2 | aucun des deux dossiers ne contient de replay |
| `<n> replay(s)` | 0 | trouvés |

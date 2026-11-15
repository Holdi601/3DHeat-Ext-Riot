---
title: "Finding replays: list"
nav_order: 2
---

# Finding replays: `list`

```bash
heat3d-riot-replays list
```

prints where League of Legends and VALORANT save replays, and each replay
there with its size. Without a replay given, [`convert`](convert.md) reads the
ones `list` shows.

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

## Where replays are

| Game | Folder | Saving one |
|---|---|---|
| League of Legends | `%USERPROFILE%\Documents\League of Legends\Replays\*.rofl` | the client's match history: pick a match, click the download button. The file is named `<platform>-<game id>.rofl`, e.g. `EUW1-7123456789.rofl` |
| VALORANT | `%LOCALAPPDATA%\VALORANT\Saved\Demos\*.vrf` | Career: pick a match, download its replay |

League lets you move its replays folder in the client's settings (Replays);
give that folder to `convert` then. A replay anyone sends you works the same:
give its path to `convert`.

## Messages and exit status

| Message | Exit | Means |
|---|---|---|
| `<game>: <folder> (not there: no replay saved yet)` | - | that game saved no replay on this machine yet |
| `0 replay(s)` | 2 | neither folder has a replay |
| `<n> replay(s)` | 0 | found |

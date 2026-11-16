---
title: "Encontrar repeticiones: list"
nav_order: 2
lang: "es"
source: list.md
source_hash: "0d13db1af26d"
nav_exclude: true
search_exclude: true
---
# Encontrar repeticiones: `list` {#finding-replays-list}

```bash
heat3d-riot-replays list
```

imprime dónde guardan repeticiones League of Legends y VALORANT, y cada repetición que hay allí con su tamaño. Sin repetición indicada, [`convert`](convert.md) lee las que muestra `list`.

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

## Dónde están las repeticiones {#where-replays-are}

| Juego | Carpeta | Cómo guardar una |
|---|---|---|
| League of Legends | `%USERPROFILE%\Documents\League of Legends\Replays\*.rofl` | el historial de partidas del cliente: elige una partida, haz clic en el botón de descarga. El archivo se llama `<platform>-<game id>.rofl`, p. ej. `EUW1-7123456789.rofl` |
| VALORANT | `%LOCALAPPDATA%\VALORANT\Saved\Demos\*.vrf` | Carrera: elige una partida, descarga su repetición |

League permite mover su carpeta de repeticiones en los ajustes del cliente (Replays);
indica esa carpeta a `convert` entonces. Una repetición que alguien te envíe funciona igual:
indica su ruta a `convert`.

## Mensajes y código de salida {#messages-and-exit-status}

| Mensaje | Salida | Significa |
|---|---|---|
| `<game>: <folder> (not there: no replay saved yet)` | - | ese juego todavía no guardó ninguna repetición en este equipo |
| `0 replay(s)` | 2 | ninguna de las dos carpetas tiene una repetición |
| `<n> replay(s)` | 0 | encontradas |

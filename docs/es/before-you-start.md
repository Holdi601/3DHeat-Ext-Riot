---
title: Antes de empezar
nav_order: 1.5
lang: "es"
source: before-you-start.md
source_hash: "81c92d0ec0c5"
nav_exclude: true
search_exclude: true
---
# Antes de empezar {#before-you-start}

¿Nuevo en la línea de comandos? Esta página te lleva de cero a una primera ejecución.
Lleva unos diez minutos, una sola vez.

## 1. Instalar Python {#install-python}

Esta herramienta necesita **Python 3.10 o posterior**.

- **Windows:** descarga Python desde [python.org/downloads](https://www.python.org/downloads/)
  y ejecuta el instalador. En su primera pantalla, marca **Add python.exe to PATH**
  y luego haz clic en **Install Now**.
- **macOS y Linux:** Python 3 suele estar ya instalado. Donde estas páginas dicen
  `python`, escribe `python3`.

## 2. Obtener esta herramienta {#get-this-tool}

Abre [github.com/Holdi601/3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot), haz clic en el
botón verde **Code** y luego en **Download ZIP**, y descomprímela en una carpeta a tu elección. Si usas git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Riot`.

## 3. Abrir una terminal en esa carpeta {#open-a-terminal-in-that-folder}

Una terminal es una ventana donde escribes comandos.

- **Windows:** abre la carpeta en el Explorador, haz clic en la barra de direcciones, escribe
  `powershell` y pulsa Intro. Se abre una ventana azul o negra, ya en esa carpeta.
- **macOS:** abre **Terminal**, escribe `cd ` (con un espacio), arrastra la carpeta a
  la ventana y pulsa Intro.

`cd` significa "cambiar de carpeta": `cd C:\Tools\3DHeat-Ext-Riot` va a esa carpeta.

## 4. Instalar la herramienta {#install-the-tool}

Escribe esto y pulsa Intro:

```bash
python -m pip install -e .
```

Al final deberías ver: `Successfully installed heat3d-ext-riot-...`.
La herramienta no necesita nada más que el propio Python.

## 5. Guardar una repetición y ejecutarla {#save-a-replay-and-run-it}

En League of Legends, abre tu historial de partidas, elige una partida y haz clic en el
botón de descarga; en VALORANT, abre Carrera, elige una partida y descarga su
repetición. Después:

```bash
heat3d-riot-replays list
```

Deberías ver algo como:

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

Siguiente: [Lectura: convert](convert.md).

## Cómo leer los comandos de estas páginas {#how-to-read-the-commands-on-these-pages}

| Ves | Significa |
|---|---|
| `<file>` | un marcador: escribe tu propio valor en su lugar, sin los `< >` |
| `[REPLAY ...]` | opcional: déjalo fuera, o escríbelo tal como se muestra |
| `# a note` | un comentario para ti: no lo escribas |
| `"C:\My Files\x"` | pon entre comillas una ruta que tenga espacios |

## Cuando algo sale mal {#when-something-goes-wrong}

| El mensaje | Qué hacer |
|---|---|
| `'python' is not recognized` | Python no está instalado, o no se marcó la casilla PATH: instálalo de nuevo y márcala (o escribe `py` en lugar de `python`). |
| `'heat3d-riot-replays' is not recognized` | Repite el paso 4 en la carpeta de la herramienta, o escribe `python -m heat3d_ext_riot` en lugar de `heat3d-riot-replays`: hace lo mismo. |
| `no replay (.rofl, .vrf) found in ...` | Guarda antes una repetición en el juego (paso 5), o indica la ruta de la repetición a `convert`. |
| `... not a League of Legends or VALORANT replay this reader understands` | El archivo es otra cosa, o está cortado; una repetición con un diseño que esta herramienta no conoce se rechaza igual. |
| cualquier otra cosa | Lee la última línea del mensaje y luego abre una incidencia en GitHub con ella. |

Cada comando también termina con un **código de salida**: 0 significa que funcionó, 2 que
no había nada que leer, 1 que una repetición falló. Para verlo,
escribe `echo $LASTEXITCODE` en PowerShell o `echo $?` en macOS y Linux.

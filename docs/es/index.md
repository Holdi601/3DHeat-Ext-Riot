---
title: Inicio
nav_order: 1
lang: "es"
source: index.md
source_hash: "7d4b8345cc71"
nav_exclude: true
search_exclude: true
permalink: /es/
---
# 3DHeat Riot {#dheat-riot}

**¿Qué es?** Esta herramienta lee repeticiones de League of Legends (`.rofl`) y VALORANT
(`.vrf`) y escribe **lo que cada archivo contiene a la vista**: la tabla de estadísticas de final de partida de los diez jugadores de League y la cabecera de la repetición; el mapa, el id de la partida, los agentes y la línea de tiempo de eventos del servidor de VALORANT (muertes, rondas y espigas). Es una de las herramientas que rodean al visor de [3DHeat](https://github.com/Holdi601/3DHeat)
([documentación](https://holdi601.github.io/3DHeat/)).

**¿Para qué sirve?** Para guardar los números de tus partidas como tablas sencillas: asesinatos, muertes, oro, daño y cien cosas más de cada jugador de League, cada ronda y cada muerte de una partida de VALORANT, para tus propias estadísticas, o para el Watcher de 3DHeat, que ejecuta esta herramienta con cada repetición que guardes.

**Ejemplo:** `heat3d-riot-replays convert EUW1-7123456789.rofl -o out` ->
`out/EUW1-7123456789.rofl.json` y `out/EUW1-7123456789.rofl.players.csv`.

**Lo que no hace:** leer posiciones ni el juego en sí. Esa parte de una repetición está cifrada y ofuscada contra las trampas, y atravesarla supondría desmontar el juego, lo que prohíben las condiciones de Riot. Esta herramienta no rompe ningún cifrado ni deshace ninguna ofuscación ([Términos](terms.md)).

## Inicio rápido {#quick-start}

¿Nuevo en la línea de comandos? Lee primero [Antes de empezar](before-you-start.md).
Necesitas Python 3.10 o posterior, nada más. Ejecuta esto en la carpeta que clonaste
o descomprimiste:

```bash
python -m pip install -e .                  # installs the heat3d-riot-replays command
heat3d-riot-replays list                    # where both games save replays, the ones there
heat3d-riot-replays convert -o out          # every replay there, read
```

`convert` imprime cada archivo que escribe. Abre el `.csv` en una hoja de cálculo, o
lee el `.json` ([Lectura: convert](convert.md)).

## Páginas {#pages}

| Página | Qué cubre |
|---|---|
| [Antes de empezar](before-you-start.md) | Python, una terminal, una primera ejecución |
| [Encontrar repeticiones: list](list.md) | dónde guardan repeticiones ambos juegos, cómo guardar una, qué imprime `list` |
| [Lectura: convert](convert.md) | qué se lee de cada archivo, qué sale, qué no se lee |
| [Términos y licencia](terms.md) | las condiciones de Riot, qué se lee y qué nunca, la clave de API de Riot |
| [Referencia de comandos](../cli-reference.md) | cada opción y campo, generados desde el código |
| [Mantener estas páginas](maintaining.md) | la lista de comprobación de cada versión |

## Relacionado {#related}

- El visor de 3DHeat: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentación en [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- El Watcher de 3DHeat ejecuta esta herramienta con cada repetición que guardan los juegos; para League,
  con tu propia clave de desarrollador de Riot, añade la línea de tiempo oficial de la partida con posiciones:
  [repeticiones de League of Legends](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html),
  [repeticiones de VALORANT](https://holdi601.github.io/3DHeat-Watcher/game-valorant-replays.html).
- League of Legends mientras juegas (la API de datos del cliente en directo de Riot):
  [el Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-live.html).

## Las herramientas de 3DHeat {#the-3dheat-tools}

| Herramienta | Qué hace | Código | Documentación |
|---|---|---|---|
| visor de 3DHeat | muestra los datos: mapas de calor, análisis de carrera, revisión de partidas | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | niveles y recorridos a partir de los archivos propios de un juego | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | telemetría de vueltas, y niveles reconstruidos a partir de vídeo de juego | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | un plugin del editor de Unreal: un nivel como un único `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | demos y mapas de Counter-Strike 2 | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | registra lo que publican los juegos mientras juegas | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | repeticiones de War Thunder | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | repeticiones de World of Tanks | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | repeticiones de World of Warships | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | demos de servidores de Squad | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | mapas de DCS World como niveles 3D | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | mapas de IL-2 Sturmovik como niveles 3D | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | el mapa de Dota 2 como nivel 3D | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | repeticiones de Dota 2 como tablas | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | repeticiones de League of Legends y VALORANT: lo que contienen a la vista | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | recorridos, carreras y coches de Forza desde tu propia instalación | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | niveles de Battlefield (Frostbite) como niveles 3D | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | recorridos de BeamNG.drive | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | tramos de Assetto Corsa Rally como recorridos | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | mundos de Arma Reforger (Enfusion) como niveles 3D | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | repeticiones de partidas de Rainbow Six Siege | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |

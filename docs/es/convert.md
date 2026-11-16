---
title: "Lectura: convert"
nav_order: 3
lang: "es"
source: convert.md
source_hash: "2a11c2db4829"
nav_exclude: true
search_exclude: true
---
# Lectura: `convert` {#reading-convert}

```bash
heat3d-riot-replays convert [<replay> or <folder> ...] -o <folder>
```

lee cada repetición `.rofl` y `.vrf` y escribe lo que contiene a la vista en la carpeta indicada con `-o`. Sin repetición, lee todas las de las carpetas de ambos juegos ([list](list.md) muestra cuáles son); una carpeta indicada lee cada `.rofl` y `.vrf` que contenga. Código:
[`heat3d_ext_riot/replays.py`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/heat3d_ext_riot/replays.py).

| Opción | Hace |
|---|---|
| `<replay>` o `<folder>` | qué leer; se pueden indicar varios (por defecto: las carpetas de repeticiones de ambos juegos) |
| `-o`, `--out FOLDER` | dónde van los resultados (obligatorio); se crea si no existe |

Por cada repetición imprime los archivos que escribió:

```text
out\EUW1-7123456789.rofl.json
out\EUW1-7123456789.rofl.players.csv
```

## League of Legends (.rofl) {#league-of-legends-rofl}

Ambas versiones del contenedor guardan la tabla de estadísticas de final de partida como JSON sin cifrar dentro del archivo (`statsJson`): para cada uno de los diez jugadores, el campeón, las muertes, las asistencias, el oro, el daño a campeones, los objetos, el equipo, el rol, la victoria, su Riot ID, y cada otro número que el juego totaliza: más de cien por jugador.

| Contenedor | Parches | Lectura |
|---|---|---|
| ROFL1 (`RIOT` 0 0) | 14.9 y anteriores | el JSON de metadatos (duración de la partida, versión, los ids del último fragmento y del último fotograma clave, la tabla de estadísticas); el bloque de longitudes; la cabecera de la carga (id de la partida, duración, número de fotogramas clave y de fragmentos, ids de los fragmentos de inicio y de comienzo de partida, intervalo de fotogramas clave, la clave del fragmento tal como está guardada); la tabla de fragmentos (id, tipo, longitud, siguiente fragmento, desplazamiento) |
| ROFL2 (`RIOT` 2 0) | 14.11 en adelante | el JSON de metadatos al final del archivo, su longitud en los últimos cuatro bytes; la cadena de versión cerca del principio |

**No se lee:** la partida en sí. Los fragmentos y los fotogramas clave de ROFL1 y el cuerpo de ROFL2 están cifrados, y los paquetes que contienen se ofuscan de nuevo con cada parche. Se nombran por su rango de bytes (`keyframe`, `chunk`, `body`) y se dejan como están.

## VALORANT (.vrf) {#valorant-vrf}

Una repetición de VALORANT es una repetición local de Unreal Engine: un bloque de información, y luego fragmentos por tipo y tamaño.

| Parte | Lectura |
|---|---|
| el bloque de información | cada campo: versión del archivo, versiones personalizadas, longitud, versión de red, changelist, nombre, indicador de en directo, hora de grabación, indicadores de comprimido y cifrado, la clave tal como está guardada |
| el fragmento de cabecera | el mapa, el id de la partida y los agentes elegidos, buscados por su forma y no por un desplazamiento que cambia entre versiones |
| cada fragmento de evento | id, grupo, metadatos, hora de inicio y de fin, y de sus datos el nombre del evento, su hora en segundos y los números que lo preceden: quién mató y quién murió como ids de red (no nombres), inicio de rondas, espigas plantadas, desactivadas y explosionadas, ultimates usadas, cambios de bando |

**No se lee:** las posiciones, los nombres, las puntuaciones, las habilidades, cada fotograma de la partida: están en los fragmentos de datos de repetición y de puntos de control, que están ofuscados. De una repetición cifrada se recorren y nombran los fragmentos, pero no se lee nada dentro de ellos.

## Qué sale {#what-comes-out}

| Archivo | Contiene |
|---|---|
| `<file>.json` | todo lo leído. `format` (`heat3d-riot-replay/1`), `tool`, `file`, `size`, `game`, `kind` (`rofl` o `vrf`), y la lectura: en League, `container`, `version`, `length_ms`, `game_id`, `players` (la tabla de estadísticas), `metadata`, `payload`, `chunks`; en VALORANT, `file_version`, `length_ms`, `name`, `recorded_unix`, `encrypted`, `info`, `map`, `match_id`, `agents`, `events` |
| `<file>.players.csv` | League: la tabla de estadísticas, una fila por jugador, cada campo tal como lo escribió el juego |
| `<file>.events.csv` | VALORANT: la línea de tiempo de eventos, una fila por evento |

`sections` en el JSON enumera cada parte del archivo en orden como
`[name, start, end, what was read of it]` - el último `null` para una parte no leída - y las partes juntas son el archivo entero, con cualquier tramo que ningún bloque conocido cubra marcado como `unknown` (League) o `trailing` (VALORANT). Campos:
[Referencia de comandos](../cli-reference.md#output).

## Cómo usarlo {#using-it}

Estos archivos no tienen posiciones: son tablas para leer, en una hoja de cálculo o en un script. El Watcher de 3DHeat ejecuta esta herramienta con cada repetición que guardan los juegos y crea una sesión con ella; en una partida de League, con tu propia clave de desarrollador de Riot en sus ajustes, también descarga la línea de tiempo oficial de la partida desde la API Match-V5 de Riot: la posición de cada jugador una vez por minuto y cada muerte en el lugar donde ocurrió, que el visor de 3DHeat dibuja sobre el mapa ([repeticiones de League of Legends en el Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)). Esa descarga es del Watcher, no de esta herramienta: esta herramienta solo lee archivos.

## Cómo se comprobó {#how-it-was-checked}

Con repeticiones construidas campo por campo según los diseños de roflxd.cs (MIT) y vrfkit (Apache-2.0), incluido un fragmento cortado y una repetición de VALORANT cifrada; no había ninguna repetición real con la que comparar. El lector comprueba antes de leer y rechaza lo que no encaja, en lugar de adivinar.

## Mensajes y código de salida {#messages-and-exit-status}

| Mensaje | Salida | Significa |
|---|---|---|
| los archivos escritos | 0 | listo |
| `heat3d-riot-replays: no replay (.rofl, .vrf) found in ...` | 2 | no hay nada que leer donde se buscó |
| `heat3d-riot-replays: <file>: not a League of Legends or VALORANT replay this reader understands (...)` | 2 | otro tipo de archivo, o un diseño que esta herramienta no conoce; entre los que se leyeron: 1 |
| `heat3d-riot-replays: <file>: <error>` | 1 | esa repetición falló; las demás se siguen leyendo |

---
title: Términos y licencia
nav_order: 8
lang: "es"
source: terms.md
source_hash: "2427841ba70b"
nav_exclude: true
search_exclude: true
---
# Términos y licencia {#terms-and-licence}

## Los juegos y las repeticiones de Riot {#riots-games-and-replays}

3DHeat Riot no está afiliado a Riot Games ni respaldado por Riot Games. League of Legends, VALORANT y los nombres y marcas relacionados pertenecen a sus propietarios. Esta herramienta no incluye ningún recurso de Riot (ningún archivo del juego, arte, modelo, mapa, sonido, logotipo ni dato de ninguno de los dos juegos) y no se comunica con ningún servidor: lee los archivos de repetición que los juegos escribieron en tu equipo, fuera del juego, y no cambia nada en él. Lo que escribe se queda en tu equipo.

## Qué se lee, y qué nunca {#what-is-read-and-what-never-is}

Ambos juegos protegen lo que hay dentro de sus repeticiones: los datos de juego momento a momento están cifrados y ofuscados, y de forma distinta con cada parche, para impedir que se usen para hacer trampas. Esta herramienta:

- lee **solo lo que cada archivo contiene a la vista**: el JSON de metadatos sin cifrar de un `.rofl` (la tabla de estadísticas de final de partida), su cabecera y su tabla de fragmentos; el bloque de información de un `.vrf`, el mapa, el id de la partida y los agentes de su cabecera, y los fragmentos de eventos del servidor;
- **no rompe ningún cifrado y no deshace ninguna ofuscación**, y no contiene ninguna clave, ningún descifrado ni código tomado de los juegos;
- nombra las partes protegidas por su lugar en el archivo y las deja sin leer.

Una clave que el propio archivo guarda a la vista (la clave de fragmento de una repetición ROFL1) se copia en la lectura tal como está guardada, como parte de la cabecera; no se descifra nada con ella.

## La clave de API de Riot {#the-riot-api-key}

La herramienta no necesita cuenta ni clave. Las posiciones de una partida de League vienen de la API Match-V5 de Riot, no del archivo: el Watcher de 3DHeat puede descargar la línea de tiempo de una partida con **tu propia** clave de desarrollador de Riot (una clave personal está pensada para "showing (self) player stats"). Esa descarga es del Watcher; está desactivada sin una clave, y esta herramienta no envía nada a ningún sitio.

## Un proyecto propio {#its-own-project}

Cada lector de un juego es un pequeño proyecto propio, con su propio archivo de licencia, sus versiones y su gestor de incidencias, así que puede instalarse, actualizarse, mantenerse (o retirarse a petición de un titular de derechos) por sí solo, sin afectar al visor ni a las demás herramientas.

Titulares de derechos: abran una incidencia en [3DHeat-Ext-Riot/issues](https://github.com/Holdi601/3DHeat-Ext-Riot/issues); respondemos con rapidez y retiramos cualquier cosa que se nos pida.

## Licencia y fuentes {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSE)).
Solo necesita la biblioteca estándar de Python; las pruebas necesitan pytest (MIT). Escrito para
este proyecto, primero como parte del Watcher de 3DHeat. Los diseños de archivo se tomaron como hechos de
roflxd.cs (MIT), vrfkit (Apache-2.0) y ValorantReplayParser
(MIT), y de una descripción de ROFL2 de un ingeniero de Riot (ReplayBook, incidencia 299);
no se copió ningún código. Ver
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSES.md).

---
title: Termini e licenza
nav_order: 8
lang: "it"
source: terms.md
source_hash: "2427841ba70b"
nav_exclude: true
search_exclude: true
---
# Termini e licenza {#terms-and-licence}

## I giochi e i replay di Riot {#riots-games-and-replays}

3DHeat Riot non è affiliato a Riot Games né approvato da Riot Games. League of Legends, VALORANT e i nomi e i
marchi correlati appartengono ai rispettivi proprietari. Questo strumento non include alcuna risorsa di Riot -
nessun file di gioco, opera grafica, modello, mappa, suono, logo o dato di nessuno dei due giochi - e non parla con
nessun server: legge i file di replay che i giochi hanno scritto sul tuo computer, al di fuori del gioco, e non
modifica nulla al suo interno. Ciò che scrive resta sul tuo computer.

## Cosa viene letto, e cosa non lo sarà mai {#what-is-read-and-what-never-is}

Entrambi i giochi proteggono ciò che c'è dentro i loro replay: i dati di gioco momento per momento sono cifrati e
offuscati, e in modo diverso a ogni patch, per impedire che vengano usati per barare. Questo strumento:

- legge **solo ciò che ogni file contiene in chiaro** - i metadati JSON in chiaro di un `.rofl` (il riepilogo di fine
  partita), la sua intestazione e la tabella dei chunk; il blocco di informazioni di un `.vrf`, la mappa, l'id della
  partita e gli agenti nella sua intestazione, e i chunk di evento del server;
- **non rompe alcuna cifratura e non annulla alcun offuscamento**, e non contiene alcuna chiave, alcuna decifratura né
  alcun codice ricavato dai giochi;
- nomina le parti protette in base alla loro posizione nel file e le lascia non lette.

Una chiave che il file stesso memorizza in chiaro (la chiave di chunk di un replay ROFL1) viene copiata nella lettura
così come è memorizzata, come parte dell'intestazione; con essa non si decifra nulla.

## La chiave API di Riot {#the-riot-api-key}

Lo strumento non richiede alcun account né alcuna chiave. Le posizioni di una partita di League arrivano dall'API
Match-V5 di Riot, non dal file: il 3DHeat Watcher può scaricare la cronologia di una partita con la **tua** chiave da
sviluppatore Riot (una chiave personale è pensata per "showing (self) player stats"). Quel download
è del Watcher, è disattivato senza una chiave, e questo strumento non invia nulla da nessuna parte.

## Un progetto a sé {#its-own-project}

Ogni lettore di un gioco è un piccolo progetto a sé, con il proprio file di licenza, i propri rilasci e il proprio
tracker delle issue, così può essere installato, aggiornato, mantenuto - o ritirato su richiesta di un titolare dei
diritti - da solo, senza toccare il visualizzatore o gli altri strumenti.

Titolari dei diritti: aprite una issue su
[3DHeat-Ext-Riot/issues](https://github.com/Holdi601/3DHeat-Ext-Riot/issues) - rispondiamo in fretta e rimuoviamo
qualsiasi cosa su richiesta.

## Licenza e fonti {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSE)).
Richiede solo la libreria standard di Python; i test richiedono pytest (MIT). Scritto per questo progetto, prima come
parte del 3DHeat Watcher. I layout dei file sono stati presi come fatti da roflxd.cs (MIT), vrfkit (Apache-2.0) e
ValorantReplayParser (MIT), e dalla descrizione di ROFL2 di un ingegnere di Riot (ReplayBook issue 299);
nessun codice è stato copiato. Vedi
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSES.md).

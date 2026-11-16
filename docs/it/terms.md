---
title: Termini e licenza
nav_order: 8
lang: "it"
source: terms.md
source_hash: "b8ab95d59a93"
nav_exclude: true
search_exclude: true
---
# Termini e licenza {#terms-and-licence}

## I giochi e i replay di Riot {#riots-games-and-replays}

League of Legends e VALORANT appartengono a Riot Games, che non approva questo progetto. Questo
strumento non include alcuna risorsa di Riot - nessun file di gioco, opera grafica, modello, mappa,
suono, logo o dato di nessuno dei due giochi - e non parla con nessun server: legge i tuoi file di
replay sul tuo computer, al di fuori del gioco, e non modifica nulla al suo interno. Ciò che scrive è tuo da conservare;
usare lo strumento è una tua decisione, secondo i termini che hai accettato per i giochi.

## Cosa viene letto, e cosa non lo sarà mai {#what-is-read-and-what-never-is}

Entrambi i giochi proteggono ciò che c'è dentro i loro replay: i dati di gioco momento per momento sono cifrati
e offuscati, e in modo diverso a ogni patch, per impedire che vengano usati per barare. Arrivarci vorrebbe dire
smontare il client di gioco, cosa che i Termini di Servizio di Riot vietano (sezioni 3.1 e 7.1). Quindi questo strumento:

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

## Perché un pacchetto a sé {#why-a-separate-package}

Se Riot un giorno chiedesse di ritirarlo, andrebbe ritirato da solo, e il visualizzatore, il Watcher e gli altri
strumenti restano.

## Licenza e fonti {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSE)).
Richiede solo la libreria standard di Python; i test richiedono pytest (MIT). Scritto per questo progetto, prima come
parte del 3DHeat Watcher. I layout dei file sono stati presi come fatti da roflxd.cs (MIT), vrfkit (Apache-2.0) e
ValorantReplayParser (MIT), e dalla descrizione di ROFL2 di un ingegnere di Riot (ReplayBook issue 299);
nessun codice è stato copiato. Vedi
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSES.md).

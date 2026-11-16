---
title: "Lettura: convert"
nav_order: 3
lang: "it"
source: convert.md
source_hash: "2a11c2db4829"
nav_exclude: true
search_exclude: true
---
# Lettura: `convert` {#reading-convert}

```bash
heat3d-riot-replays convert [<replay> or <folder> ...] -o <folder>
```

legge ogni replay `.rofl` e `.vrf` e scrive ciò che contiene in chiaro nella cartella `-o`.
Senza un replay legge ogni file presente nelle cartelle di entrambi i giochi ([list](list.md) mostra quali);
una cartella indicata legge ogni `.rofl` e `.vrf` che contiene. Codice:
[`heat3d_ext_riot/replays.py`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/heat3d_ext_riot/replays.py).

| Opzione | Fa |
|---|---|
| `<replay>` o `<folder>` | cosa leggere; se ne possono indicare più d'uno (predefinito: le cartelle dei replay di entrambi i giochi) |
| `-o`, `--out FOLDER` | dove vanno i risultati (obbligatorio); viene creata se manca |

Per ogni replay stampa i file che ha scritto:

```text
out\EUW1-7123456789.rofl.json
out\EUW1-7123456789.rofl.players.csv
```

## League of Legends (.rofl) {#league-of-legends-rofl}

Entrambe le versioni del contenitore portano nel file il riepilogo di fine partita come JSON in chiaro
(`statsJson`): per ognuno dei dieci giocatori il campione, uccisioni, morti, assist, oro, danno ai
campioni, oggetti, squadra, ruolo, vittoria, il loro Riot ID, e ogni altro numero che il gioco totalizza -
oltre cento per giocatore.

| Contenitore | Patch | Lettura |
|---|---|---|
| ROFL1 (`RIOT` 0 0) | 14.9 e precedenti | il JSON dei metadati (durata della partita, versione, id dell'ultimo chunk e del keyframe, il riepilogo); il blocco delle lunghezze; l'intestazione del payload (id della partita, durata, numero di keyframe e chunk, id dei chunk di avvio e di inizio partita, intervallo dei keyframe, la chiave del chunk così come è memorizzata); la tabella dei chunk (id, tipo, lunghezza, chunk successivo, offset) |
| ROFL2 (`RIOT` 2 0) | 14.11 e successive | il JSON dei metadati alla fine del file, la sua lunghezza negli ultimi quattro byte; la stringa di versione vicino all'inizio |

**Non letto:** la partita stessa. I chunk e i keyframe di ROFL1 e il corpo di ROFL2 sono cifrati, e i pacchetti
al loro interno sono offuscati di nuovo a ogni patch. Vengono nominati dal loro intervallo di byte (`keyframe`,
`chunk`, `body`) e lasciati così come sono.

## VALORANT (.vrf) {#valorant-vrf}

Un replay di VALORANT è un replay locale di Unreal Engine: un blocco di informazioni, poi chunk per tipo e dimensione.

| Parte | Lettura |
|---|---|
| il blocco di informazioni | ogni campo: versione del file, versioni personalizzate, durata, versione di rete, changelist, nome, flag di diretta, ora di registrazione, flag di compressione e cifratura, la chiave così come è memorizzata |
| il chunk di intestazione | la mappa, l'id della partita e gli agenti scelti - cercati per la loro forma, non per un offset che cambia tra una build e l'altra |
| ogni chunk di evento | id, gruppo, metadati, ora di inizio e di fine, e dei suoi dati il nome dell'evento, il suo tempo in secondi e i numeri che lo precedono: l'assassino e la vittima di un'uccisione come id di rete (non nomi), round che iniziano, spike piazzate, disinnescate ed esplose, ultimate usate, lati che si scambiano |

**Non letto:** posizioni, nomi, punteggi, abilità, ogni frame della partita - sono nei dati del replay e nei chunk di
checkpoint, che sono offuscati. Di un replay cifrato, i chunk vengono percorsi e nominati, senza leggere nulla al loro interno.

## Cosa esce {#what-comes-out}

| File | Contiene |
|---|---|
| `<file>.json` | tutto ciò che è stato letto. `format` (`heat3d-riot-replay/1`), `tool`, `file`, `size`, `game`, `kind` (`rofl` o `vrf`), e la lettura: per League `container`, `version`, `length_ms`, `game_id`, `players` (il riepilogo), `metadata`, `payload`, `chunks`; per VALORANT `file_version`, `length_ms`, `name`, `recorded_unix`, `encrypted`, `info`, `map`, `match_id`, `agents`, `events` |
| `<file>.players.csv` | League: il riepilogo, una riga per giocatore, ogni campo come lo ha scritto il gioco |
| `<file>.events.csv` | VALORANT: la cronologia degli eventi, una riga per evento |

`sections` nel JSON elenca ogni parte del file in ordine come `[name, start, end, what was read of it]` - l'ultimo
`null` per una parte non letta - e le parti insieme sono l'intero file; ogni tratto che nessuna parte nota copre è
nominato `unknown` (League) o `trailing` (VALORANT). Campi: [Riferimento dei comandi](../cli-reference.md#output).

## Come usarlo {#using-it}

Questi file non hanno posizioni: sono tabelle da leggere, in un foglio di calcolo o in uno script. Il 3DHeat Watcher
lancia questo strumento su ogni replay che i giochi salvano e ne ricava una sessione; per una partita di League,
con la tua chiave da sviluppatore Riot nelle sue impostazioni, scarica anche la cronologia ufficiale della partita
dall'API Match-V5 di Riot - la posizione di ogni giocatore una volta al minuto e ogni uccisione nel punto in cui è
avvenuta - che il visualizzatore 3DHeat disegna sulla mappa
([replay di League of Legends nel Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)).
Quel download è del Watcher, non di questo strumento: questo strumento legge solo file.

## Come è stato verificato {#how-it-was-checked}

Su replay costruiti campo per campo secondo i formati di roflxd.cs (MIT) e vrfkit (Apache-2.0), incluso un
chunk troncato e un replay VALORANT cifrato; non era disponibile alcun replay reale con cui confrontarsi. Il
lettore controlla prima di leggere e rifiuta ciò che non corrisponde, invece di indovinare.

## Messaggi e stato di uscita {#messages-and-exit-status}

| Messaggio | Uscita | Significa |
|---|---|---|
| i file scritti | 0 | fatto |
| `heat3d-riot-replays: no replay (.rofl, .vrf) found in ...` | 2 | nulla da leggere dove è stato cercato |
| `heat3d-riot-replays: <file>: not a League of Legends or VALORANT replay this reader understands (...)` | 2 | un altro tipo di file, oppure un formato che questo strumento non conosce; tra gli altri che sono stati letti: 1 |
| `heat3d-riot-replays: <file>: <error>` | 1 | quel replay è fallito; gli altri vengono comunque letti |

---
title: Prima di iniziare
nav_order: 1.5
lang: "it"
source: before-you-start.md
source_hash: "81c92d0ec0c5"
nav_exclude: true
search_exclude: true
---
# Prima di iniziare {#before-you-start}

Non hai mai usato la riga di comando? Questa pagina ti porta da zero a una prima esecuzione.
Richiede circa dieci minuti, una volta sola.

## 1. Installa Python {#install-python}

Questo strumento richiede **Python 3.10 o successivo**.

- **Windows:** scarica Python da [python.org/downloads](https://www.python.org/downloads/)
  ed esegui il programma di installazione. Nella sua prima schermata spunta **Add python.exe to PATH**,
  poi clicca su **Install Now**.
- **macOS e Linux:** Python 3 spesso c'è già. Dove queste pagine dicono
  `python`, scrivi `python3`.

## 2. Ottieni questo strumento {#get-this-tool}

Apri [github.com/Holdi601/3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot), clicca sul
pulsante verde **Code**, poi su **Download ZIP**, e decomprimilo in una cartella a tua scelta.
Se usi git: `git clone https://github.com/Holdi601/3DHeat-Ext-Riot`.

## 3. Apri un terminale in quella cartella {#open-a-terminal-in-that-folder}

Un terminale è una finestra in cui scrivi i comandi.

- **Windows:** apri la cartella in Esplora risorse, clicca nella barra degli indirizzi, scrivi
  `powershell` e premi Invio. Si apre una finestra blu o nera, già in quella cartella.
- **macOS:** apri **Terminale**, scrivi `cd ` (con lo spazio), trascina la cartella nella
  finestra e premi Invio.

`cd` significa "cambia cartella": `cd C:\Tools\3DHeat-Ext-Riot` va in quella cartella.

## 4. Installa lo strumento {#install-the-tool}

Scrivi questo e premi Invio:

```bash
python -m pip install -e .
```

Alla fine dovresti vedere: `Successfully installed heat3d-ext-riot-...`.
Lo strumento non richiede altro che Python stesso.

## 5. Salva un replay ed eseguilo {#save-a-replay-and-run-it}

In League of Legends, apri la cronologia delle tue partite, scegline una e clicca sul
pulsante di download; in VALORANT, apri Career, scegli una partita e scarica il suo
replay. Poi:

```bash
heat3d-riot-replays list
```

Dovresti vedere qualcosa del genere:

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

Avanti: [Lettura: convert](convert.md).

## Come leggere i comandi di queste pagine {#how-to-read-the-commands-on-these-pages}

| Vedi | Significa |
|---|---|
| `<file>` | un segnaposto: scrivi invece il tuo valore, senza i `< >` |
| `[REPLAY ...]` | facoltativo: omettilo, oppure scrivilo come mostrato |
| `# a note` | un commento per te: non scriverlo |
| `"C:\My Files\x"` | metti tra virgolette un percorso che contiene spazi |

## Quando qualcosa va storto {#when-something-goes-wrong}

| Il messaggio | Cosa fare |
|---|---|
| `'python' is not recognized` | Python non è installato, oppure non era spuntata la casella PATH: installalo di nuovo e spuntala (o scrivi `py` al posto di `python`). |
| `'heat3d-riot-replays' is not recognized` | Esegui di nuovo il passo 4 nella cartella dello strumento, oppure scrivi `python -m heat3d_ext_riot` al posto di `heat3d-riot-replays`: fa la stessa cosa. |
| `no replay (.rofl, .vrf) found in ...` | Salva prima un replay nel gioco (passo 5), oppure dai a `convert` il percorso del replay. |
| `... not a League of Legends or VALORANT replay this reader understands` | Il file è un altro tipo, oppure è troncato; un replay in un formato che questo strumento non conosce viene rifiutato allo stesso modo. |
| qualsiasi altra cosa | Leggi l'ultima riga del messaggio, poi apri una segnalazione su GitHub con quella riga. |

Ogni comando termina anche con uno **stato di uscita**: 0 significa che ha funzionato, 2 che
non c'era nulla da leggere, 1 che un replay è fallito. Per vederlo, scrivi
`echo $LASTEXITCODE` in PowerShell oppure `echo $?` su macOS e Linux.

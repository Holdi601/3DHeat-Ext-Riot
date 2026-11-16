---
title: Vor dem Start
nav_order: 1.5
lang: "de"
source: before-you-start.md
source_hash: "81c92d0ec0c5"
nav_exclude: true
search_exclude: true
---
# Vor dem Start {#before-you-start}

Neu in der Kommandozeile? Diese Seite führt dich von null bis zu einem ersten Lauf.
Es dauert einmal etwa zehn Minuten.

## 1. Python installieren {#install-python}

Dieses Werkzeug braucht **Python 3.10 oder neuer**.

- **Windows:** Lade Python von [python.org/downloads](https://www.python.org/downloads/)
  herunter und starte das Installationsprogramm. Setze auf dessen erster Seite den Haken
  bei **python.exe zu PATH hinzufügen** (englisch: **Add python.exe to PATH**) und klicke
  auf **Jetzt installieren** (englisch: **Install Now**).
- **macOS und Linux:** Python 3 ist oft schon vorhanden. Wo diese Seiten `python`
  schreiben, tippe `python3`.

## 2. Dieses Werkzeug holen {#get-this-tool}

Öffne [github.com/Holdi601/3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot),
klicke auf den grünen Button **Code** und dann auf **Download ZIP**, und entpacke es in
einen Ordner deiner Wahl. Wenn du git benutzt: `git clone https://github.com/Holdi601/3DHeat-Ext-Riot`.

## 3. Ein Terminal in diesem Ordner öffnen {#open-a-terminal-in-that-folder}

Ein Terminal ist ein Fenster, in das du Befehle tippst.

- **Windows:** Öffne den Ordner im Explorer, klicke in die Adressleiste, tippe
  `powershell` und drücke Enter. Ein blaues oder schwarzes Fenster öffnet sich, schon in
  diesem Ordner.
- **macOS:** Öffne **Terminal**, tippe `cd ` (mit einem Leerzeichen), ziehe den Ordner in
  das Fenster und drücke Enter.

`cd` heißt „Ordner wechseln“: `cd C:\Tools\3DHeat-Ext-Riot` geht in diesen Ordner.

## 4. Das Werkzeug installieren {#install-the-tool}

Tippe dies und drücke Enter:

```bash
python -m pip install -e .
```

Am Ende solltest du sehen: `Successfully installed heat3d-ext-riot-...`.
Das Werkzeug braucht außer Python selbst nichts.

## 5. Ein Replay speichern und ausführen {#save-a-replay-and-run-it}

In League of Legends öffnest du deine Matchhistorie, wählst ein Match und klickst auf den
Download-Button; in VALORANT öffnest du **Karriere**, wählst ein Match und lädst dessen
Replay herunter. Dann:

```bash
heat3d-riot-replays list
```

Du solltest etwa so etwas sehen:

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

Weiter: [Lesen: convert](convert.md).

## So liest du die Befehle auf diesen Seiten {#how-to-read-the-commands-on-these-pages}

| Du siehst | Es bedeutet |
|---|---|
| `<file>` | ein Platzhalter: tippe stattdessen deinen eigenen Wert, ohne die `< >` |
| `[REPLAY ...]` | optional: lass es weg, oder tippe es wie gezeigt |
| `# a note` | ein Kommentar für dich: nicht mittippen |
| `"C:\My Files\x"` | einen Pfad mit Leerzeichen in Anführungszeichen setzen |

## Wenn etwas schiefgeht {#when-something-goes-wrong}

| Die Meldung | Was zu tun ist |
|---|---|
| `'python' is not recognized` | Python ist nicht installiert, oder das PATH-Kästchen war nicht angehakt: installiere es noch einmal und hake es an (oder tippe `py` statt `python`). |
| `'heat3d-riot-replays' is not recognized` | Führe Schritt 4 im Ordner des Werkzeugs noch einmal aus, oder tippe `python -m heat3d_ext_riot` statt `heat3d-riot-replays`: das tut dasselbe. |
| `no replay (.rofl, .vrf) found in ...` | Speichere zuerst ein Replay im Spiel (Schritt 5), oder gib den Pfad des Replays an `convert`. |
| `... not a League of Legends or VALORANT replay this reader understands` | Die Datei ist etwas anderes oder abgeschnitten; ein Replay in einem Format, das dieses Werkzeug nicht kennt, wird genauso abgelehnt. |
| alles andere | Lies die letzte Zeile der Meldung und eröffne damit ein Issue auf GitHub. |

Jeder Befehl endet außerdem mit einem **Exit-Status**: 0 heißt, es hat geklappt; 2, dass
es nichts zu lesen gab; 1, dass ein Replay fehlschlug. Um ihn zu sehen, tippe
`echo $LASTEXITCODE` in PowerShell oder `echo $?` unter macOS und Linux.

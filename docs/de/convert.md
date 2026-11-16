---
title: "Lesen: convert"
nav_order: 3
lang: "de"
source: convert.md
source_hash: "2a11c2db4829"
nav_exclude: true
search_exclude: true
---
# Lesen: `convert` {#reading-convert}

```bash
heat3d-riot-replays convert [<replay> or <folder> ...] -o <folder>
```

liest jede `.rofl`- und `.vrf`-Replay-Datei und schreibt, was sie offen enthält, in den
Ordner `-o`. Ohne angegebenes Replay liest es jede aus den Ordnern beider Spiele
([list](list.md) zeigt, welche das sind); ein angegebener Ordner liest jede `.rofl`- und
`.vrf`-Datei darin. Code:
[`heat3d_ext_riot/replays.py`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/heat3d_ext_riot/replays.py).

| Option | Tut |
|---|---|
| `<replay>` oder `<folder>` | was gelesen wird; mehrere sind möglich (Standard: die Replay-Ordner beider Spiele) |
| `-o`, `--out FOLDER` | wohin die Ergebnisse kommen (Pflicht); der Ordner wird angelegt, wenn er fehlt |

Für jedes Replay gibt es die Dateien aus, die es geschrieben hat:

```text
out\EUW1-7123456789.rofl.json
out\EUW1-7123456789.rofl.players.csv
```

## League of Legends (.rofl) {#league-of-legends-rofl}

Beide Containerversionen tragen die Endstatistik (Box Score) als einfaches JSON in der
Datei (`statsJson`): für jeden der zehn Spieler den Champion, Kills, Tode, Assists, Gold,
Schaden an Champions, Items, Team, Rolle, Sieg, seine Riot-ID und jede andere Zahl, die das
Spiel summiert – über hundert pro Spieler.

| Container | Patches | Gelesen |
|---|---|---|
| ROFL1 (`RIOT` 0 0) | 14.9 und früher | die Metadaten-JSON (Spieldauer, Version, Ids des letzten Chunks und Keyframes, die Endstatistik); der Längenblock; der Payload-Header (Spiel-ID, Spieldauer, Anzahl der Keyframes und Chunks, Ids der Start- und Spielbeginn-Chunks, Keyframe-Intervall, der Chunk-Schlüssel wie gespeichert); die Chunk-Tabelle (Id, Typ, Länge, nächster Chunk, Offset) |
| ROFL2 (`RIOT` 2 0) | 14.11 an | die Metadaten-JSON am Dateiende, ihre Länge in den letzten vier Bytes; die Versionszeichenkette nahe dem Anfang |

**Nicht gelesen:** das Spiel selbst. Die Chunks und Keyframes von ROFL1 und der Körper
von ROFL2 sind verschlüsselt, und die Pakete darin werden mit jedem Patch neu verschleiert.
Sie werden nach ihrem Byte-Bereich benannt (`keyframe`, `chunk`, `body`) und unverändert
gelassen.

## VALORANT (.vrf) {#valorant-vrf}

Ein VALORANT-Replay ist ein lokales Replay der Unreal Engine: ein Info-Block, dann Chunks
nach Typ und Größe.

| Teil | Gelesen |
|---|---|
| der Info-Block | jedes Feld: Dateiversion, benutzerdefinierte Versionen, Länge, Netzwerkversion, Changelist, Name, Live-Flag, Aufnahmezeit, Flags für komprimiert und verschlüsselt, der Schlüssel wie gespeichert |
| der Header-Chunk | die Karte, die Match-ID und die gewählten Agenten – gefunden über ihre Form, nicht über einen Offset, der sich zwischen Builds ändert |
| jeder Event-Chunk | Id, Gruppe, Metadaten, Start- und Endzeit, und aus seinen Daten der Name des Events, seine Zeit in Sekunden und die Zahlen davor: der Killer und das Opfer eines Kills als Netzwerk-IDs (nicht Namen), Runden, die beginnen, Spikes, die gelegt, entschärft und detoniert werden, benutzte Ultimates, Seitenwechsel |

**Nicht gelesen:** Positionen, Namen, Ergebnisse, Fähigkeiten, jeder Frame des Spiels –
sie stehen in den Replay-Daten- und Checkpoint-Chunks, die verschleiert sind. Bei einem
verschlüsselten Replay werden die Chunks durchlaufen und benannt, nichts in ihnen gelesen.

## Was herauskommt {#what-comes-out}

| Datei | Enthält |
|---|---|
| `<file>.json` | alles Gelesene. `format` (`heat3d-riot-replay/1`), `tool`, `file`, `size`, `game`, `kind` (`rofl` oder `vrf`), und die Lesung: bei League `container`, `version`, `length_ms`, `game_id`, `players` (die Endstatistik), `metadata`, `payload`, `chunks`; bei VALORANT `file_version`, `length_ms`, `name`, `recorded_unix`, `encrypted`, `info`, `map`, `match_id`, `agents`, `events` |
| `<file>.players.csv` | League: die Endstatistik, eine Zeile pro Spieler, jedes Feld so, wie das Spiel es schrieb |
| `<file>.events.csv` | VALORANT: die Ereigniszeitleiste, eine Zeile pro Ereignis |

`sections` in der JSON listet jeden Teil der Datei in Reihenfolge auf, als
`[name, start, end, what was read of it]` – das letzte `null` für einen ungelesenen Teil.
Die Teile zusammen ergeben die ganze Datei; ein Stück, das kein bekannter Teil abdeckt,
heißt `unknown` (League) oder `trailing` (VALORANT). Felder:
[Befehlsreferenz](../cli-reference.md#output).

## Verwenden {#using-it}

Diese Dateien haben keine Positionen: Es sind Tabellen zum Lesen, in einer
Tabellenkalkulation oder einem Skript. Der 3DHeat Watcher führt dieses Werkzeug bei jedem
Replay aus, das die Spiele speichern, und macht daraus eine Session. Bei einem
League-Match holt er mit deinem eigenen Riot-Developer-Schlüssel in seinen Einstellungen
außerdem die offizielle Zeitleiste des Matches aus Riots Match-V5-API – die Position jedes
Spielers einmal pro Minute und jeden Kill dort, wo er passierte. Der 3DHeat-Viewer zeichnet
sie auf der Karte ([League-of-Legends-Replays im Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)).
Dieser Abruf gehört dem Watcher, nicht diesem Werkzeug: Dieses Werkzeug liest nur Dateien.

## Wie es geprüft wurde {#how-it-was-checked}

An Replays, die Feld für Feld nach den Layouts in roflxd.cs (MIT) und vrfkit
(Apache-2.0) gebaut wurden, einschließlich eines abgeschnittenen Chunks und eines
verschlüsselten VALORANT-Replays; ein echtes Replay zum Vergleichen war nicht verfügbar.
Der Leser prüft vor dem Lesen und lehnt ab, was nicht passt, statt zu raten.

## Meldungen und Exit-Status {#messages-and-exit-status}

| Meldung | Exit | Bedeutet |
|---|---|---|
| die geschriebenen Dateien | 0 | fertig |
| `heat3d-riot-replays: no replay (.rofl, .vrf) found in ...` | 2 | nichts zu lesen, wo gesucht wurde |
| `heat3d-riot-replays: <file>: not a League of Legends or VALORANT replay this reader understands (...)` | 2 | eine andere Dateiart oder ein Format, das dieses Werkzeug nicht kennt; unter den anderen, die gelesen wurden: 1 |
| `heat3d-riot-replays: <file>: <error>` | 1 | dieses Replay ist fehlgeschlagen; die anderen werden trotzdem gelesen |

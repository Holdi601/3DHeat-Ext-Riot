---
title: Start
nav_order: 1
lang: "de"
source: index.md
source_hash: "54b97b5bbcb6"
nav_exclude: true
search_exclude: true
permalink: /de/
---
# 3DHeat Riot {#dheat-riot}

**Was ist das?** Dieses Werkzeug liest League-of-Legends- (`.rofl`) und VALORANT-Replays
(`.vrf`) und schreibt aus, **was jede Datei offen enthält**: die Endstatistik von League für
alle zehn Spieler und den Header des Replays; bei VALORANT die Karte, die Match-ID, die
Agenten und die Zeitleiste des Servers mit Kills, Runden und Spikes. Es ist eines der
Werkzeuge rund um den [3DHeat](https://github.com/Holdi601/3DHeat)-Viewer
([Dokumentation](https://holdi601.github.io/3DHeat/)).

**Wozu brauche ich das?** Um die Zahlen deiner Matches als einfache Tabellen zu behalten –
jede Kill-, Tod-, Gold- und Schadenszahl jedes League-Spielers und hundert weitere, jede
Runde und jeden Kill eines VALORANT-Spiels – für deine eigene Statistik oder für den
3DHeat Watcher, der dieses Werkzeug bei jedem Replay ausführt, das du speicherst.

**Beispiel:** `heat3d-riot-replays convert EUW1-7123456789.rofl -o out` ->
`out/EUW1-7123456789.rofl.json` und `out/EUW1-7123456789.rofl.players.csv`.

**Was es nicht tut:** Positionen oder das Spiel selbst lesen. Dieser Teil eines Replays ist
verschlüsselt; dieses Werkzeug bricht keine Verschlüsselung und hebt keine Verschleierung auf
([Bedingungen und Lizenz](terms.md)).

**Ein eigenes Projekt:** Jeder Spiel-Leser ist ein eigenes kleines Projekt mit eigener Lizenzdatei,
eigenen Releases und eigenem Issue-Tracker. So lässt er sich für sich allein installieren,
aktualisieren, pflegen – oder auf Wunsch eines Rechteinhabers zurückziehen –, ohne den Viewer oder
die anderen Werkzeuge zu berühren.

## Schnellstart {#quick-start}

Du brauchst Windows, Python 3.10 oder neuer (im Installer "Add python.exe to PATH"
ankreuzen) und Replays, die die Spiele gespeichert haben: Der Match-Verlauf von League
of Legends (ein Match wählen, auf seinen Download-Button klicken) speichert nach
`Documents\League of Legends\Replays`, die Karriere von VALORANT (ein Match wählen, sein
Replay herunterladen) nach `%LOCALAPPDATA%\VALORANT\Saved\Demos`. Das Werkzeug findet
beide von selbst ([Replays finden: list](list.md)). Sonst nichts, auch kein Git. Neu in
der Kommandozeile? Lies zuerst [Vor dem Start](before-you-start.md).

```bash
python -m pip install https://github.com/Holdi601/3DHeat-Ext-Riot/archive/refs/tags/v0.1.0.zip
heat3d-riot-replays list                    # wo beide Spiele Replays speichern, die Replays dort
heat3d-riot-replays convert -o out          # jedes Replay dort, gelesen
heat3d-riot-replays convert EUW1-7123456789.rofl -o out   # oder ein Replay
```

`convert` schreibt je Replay, nach der Datei benannt, `out\<file>.json` (alles Gelesene)
und eine Tabelle: `out\<file>.players.csv` für League (die Spielstatistik, eine Zeile pro
Spieler), `out\<file>.events.csv` für VALORANT (die Ereignis-Zeitleiste); es gibt jede
Datei aus, die es schreibt ([Lesen: convert](convert.md)).

Diese Dateien haben keine Positionen, sie sind also Tabellen zum Lesen, nicht zum Zeichnen:
Öffne die `.csv` in einer Tabellenkalkulation. Für ein League-Match auf der Karte im
[3DHeat-Viewer](https://github.com/Holdi601/3DHeat#quick-start) führt der
[3DHeat Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html) dieses
Werkzeug aus und fügt die Positionen des Matches aus Riots API hinzu (mit deinem eigenen
Riot-Entwicklerschlüssel); öffne, was er schreibt, im Viewer mit **Quelle -> Dateien...** und
**Datei laden** (herunterladen mit **Code -> Download ZIP**, entpacken, `start.bat` doppelklicken; es
bietet an, Node.js zu installieren, wenn es fehlt, und öffnet `http://127.0.0.1:5273`).

Wenn ein neues Release erscheint, sagt das Werkzeug es beim Start und bietet an, sich
selbst zu aktualisieren (`python -m heat3d_ext_riot.update` macht dasselbe).

## Seiten {#pages}

| Seite | Was sie behandelt |
|---|---|
| [Vor dem Start](before-you-start.md) | Python, ein Terminal, ein erster Lauf |
| [Replays finden: list](list.md) | wo beide Spiele Replays speichern, eins speichern, was `list` ausgibt |
| [Lesen: convert](convert.md) | was von jeder Datei gelesen wird, was herauskommt, was nicht gelesen wird |
| [Bedingungen und Lizenz](terms.md) | was gelesen wird und was nie, der Riot-API-Schlüssel, die Lizenz |
| [Befehlsreferenz](../cli-reference.md) | jede Option und jedes Feld, aus dem Code erzeugt |
| [Diese Dokumentation pflegen](maintaining.md) | die Checkliste für ein Release |

## Verwandtes {#related}

- Der 3DHeat-Viewer: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  Dokumentation unter [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- Der 3DHeat Watcher führt dieses Werkzeug bei jedem Replay aus, das die Spiele speichern;
  für League bringt er mit deinem eigenen Riot-Developer-Schlüssel die offizielle Zeitleiste
  des Matches mit Positionen:
  [League-of-Legends-Replays](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html),
  [VALORANT-Replays](https://holdi601.github.io/3DHeat-Watcher/game-valorant-replays.html).
- League of Legends während des Spiels (Riots Live Client Data API):
  [der Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-live.html).

## Die 3DHeat-Werkzeuge {#the-3dheat-tools}

| Werkzeug | Was es tut | Code | Dokumentation |
|---|---|---|---|
| 3DHeat viewer | zeigt die Daten: Heatmaps, Rennanalyse, Match-Auswertung | [3DHeat](https://github.com/Holdi601/3DHeat) | [Doku](https://holdi601.github.io/3DHeat/) |
| GameFiles | Level und Strecken aus den eigenen Dateien eines Spiels | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [Doku](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | Rundentelemetrie und aus Spielvideos nachgebaute Level | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [Doku](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | ein Plugin für den Unreal Editor: ein Level als eine `.glb`-Datei | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [Doku](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike-2-Demos und -Karten | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [Doku](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | nimmt auf, was Spiele veröffentlichen, während du spielst | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [Doku](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | War-Thunder-Replays | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [Doku](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | World-of-Tanks-Replays | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [Doku](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | World-of-Warships-Replays | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [Doku](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | Squad-Server-Demos | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [Doku](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | DCS-World-Karten als 3D-Level | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [Doku](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | IL-2-Sturmovik-Karten als 3D-Level | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [Doku](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | die Dota-2-Karte als 3D-Level | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [Doku](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | Dota-2-Replays als Tabellen | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [Doku](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | League-of-Legends- und VALORANT-Replays: was sie offen enthalten | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [Doku](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | Forza-Strecken, Rennen und Autos aus deiner eigenen Installation | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [Doku](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | Battlefield-Level (Frostbite) als 3D-Level | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [Doku](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | BeamNG.drive-Strecken | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [Doku](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | Assetto-Corsa-Rally-Etappen als Strecken | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [Doku](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | Arma-Reforger-Welten (Enfusion) als 3D-Level | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [Doku](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | Rainbow-Six-Siege-Match-Replays | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [Doku](https://holdi601.github.io/3DHeat-Ext-R6/) |

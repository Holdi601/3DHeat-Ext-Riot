---
title: Bedingungen und Lizenz
nav_order: 8
lang: "de"
source: terms.md
source_hash: "b8ab95d59a93"
nav_exclude: true
search_exclude: true
---
# Bedingungen und Lizenz {#terms-and-licence}

## Riots Spiele und Replays {#riots-games-and-replays}

League of Legends und VALORANT gehören Riot Games, das dieses Projekt nicht unterstützt.
Dieses Werkzeug liefert kein Riot-Asset mit – keine Spieldatei, keine Grafik, kein Modell,
keine Karte, kein Sound, kein Logo und keine Daten eines der beiden Spiele – und spricht mit
keinem Server. Es liest deine eigenen Replay-Dateien auf deinem Rechner, außerhalb des Spiels,
und ändert darin nichts. Was es schreibt, gehört dir zum Behalten; das Werkzeug zu benutzen ist
deine Entscheidung, unter den Bedingungen, die du für die Spiele akzeptiert hast.

## Was gelesen wird und was nie {#what-is-read-and-what-never-is}

Beide Spiele schützen, was in ihren Replays steckt: Die Spieldaten im Moment-zu-Moment-Ablauf
sind verschlüsselt und verschleiert, und zwar bei jedem Patch anders, damit man sie nicht zum
Betrügen nutzen kann. Sie zu knacken hieße, den Spiel-Client auseinanderzunehmen, was Riots
Nutzungsbedingungen verbieten (Abschnitte 3.1 und 7.1). Deshalb tut dieses Werkzeug Folgendes:

- liest **nur, was jede Datei offen enthält** – die einfachen JSON-Metadaten einer `.rofl`
  (die Endstatistik), ihren Header und ihre Chunk-Tabelle; bei einer `.vrf` den Info-Block, die
  Karte, die Match-ID und die Agenten in ihrem Header und die Event-Chunks des Servers;
- **bricht keine Verschlüsselung und hebt keine Verschleierung auf** und enthält keinen
  Schlüssel, keine Entschlüsselung und keinen Code aus den Spielen;
- benennt die geschützten Teile nach ihrem Platz in der Datei und lässt sie ungelesen.

Ein Schlüssel, den die Datei selbst offen speichert (der Chunk-Schlüssel eines ROFL1-Replays),
wird so, wie er gespeichert ist, als Teil des Headers in die Lesung übernommen. Damit wird
nichts entschlüsselt.

## Der Riot-API-Schlüssel {#the-riot-api-key}

Das Werkzeug braucht kein Konto und keinen Schlüssel. Die Positionen eines League-Matches kommen
nicht aus der Datei, sondern aus Riots Match-V5-API: Der 3DHeat Watcher kann die Zeitleiste eines
Matches mit **deinem eigenen** Riot-Developer-Schlüssel abrufen (ein persönlicher Schlüssel ist
für „showing (self) player stats“ gedacht). Dieser Abruf gehört dem Watcher, er ist ohne Schlüssel
ausgeschaltet, und dieses Werkzeug sendet nichts irgendwohin.

## Warum ein eigenes Paket {#why-a-separate-package}

Wenn Riot jemals verlangt, dass es verschwindet, geht es allein, und der Viewer, der Watcher und
die anderen Werkzeuge bleiben.

## Lizenz und Quellen {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSE)).
Braucht nur Pythons Standardbibliothek; die Tests brauchen pytest (MIT). Entstanden für dieses
Projekt, zuerst als Teil des 3DHeat Watcher. Die Dateiaufbauten wurden als Fakten aus roflxd.cs
(MIT), vrfkit (Apache-2.0) und ValorantReplayParser (MIT) übernommen sowie aus der Beschreibung
von ROFL2 durch einen Riot-Ingenieur (ReplayBook Issue 299); es wurde kein Code kopiert. Siehe
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSES.md).

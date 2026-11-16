---
title: Home
nav_order: 1
lang: "it"
source: index.md
source_hash: "7d4b8345cc71"
nav_exclude: true
search_exclude: true
permalink: /it/
---
# 3DHeat Riot {#dheat-riot}

**Che cos'è?** Questo strumento legge i replay di League of Legends (`.rofl`) e VALORANT
(`.vrf`) e scrive **ciò che ogni file contiene in chiaro**: il riepilogo di fine partita di League per tutti
e dieci i giocatori e l'intestazione del replay; per VALORANT la mappa, l'id della partita, gli agenti e la
cronologia del server di uccisioni, round e spike. È uno degli strumenti intorno al visualizzatore
[3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)).

**Perché usarlo?** Per conservare i numeri delle tue partite come tabelle semplici - uccisioni, morti, oro, danno e
un centinaio di altri dati di ogni giocatore di League, ogni round e ogni uccisione di una partita di VALORANT - per
le tue statistiche, oppure per il 3DHeat Watcher, che lancia questo strumento su ogni replay che salvi.

**Esempio:** `heat3d-riot-replays convert EUW1-7123456789.rofl -o out` ->
`out/EUW1-7123456789.rofl.json` e `out/EUW1-7123456789.rofl.players.csv`.

**Cosa non fa:** leggere le posizioni o la partita stessa. Quella parte di un replay è cifrata e offuscata contro
i bari, e arrivarci significherebbe smontare il gioco, cosa che i termini di Riot vietano. Questo strumento non
rompe alcuna cifratura e non annulla alcun offuscamento ([Termini](terms.md)).

## Avvio rapido {#quick-start}

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).
Ti serve solo Python 3.10 o successivo, nient'altro. Esegui questi comandi nella cartella in cui hai clonato
o decompresso lo strumento:

```bash
python -m pip install -e .                  # installa il comando heat3d-riot-replays
heat3d-riot-replays list                    # dove entrambi i giochi salvano i replay, quelli presenti
heat3d-riot-replays convert -o out          # tutti i replay presenti, letti
```

`convert` stampa ogni file che ha scritto. Apri il `.csv` in un foglio di calcolo, oppure leggi il `.json`
([Lettura: convert](convert.md)).

## Pagine {#pages}

| Pagina | Cosa contiene |
|---|---|
| [Prima di iniziare](before-you-start.md) | Python, un terminale, una prima esecuzione |
| [Trovare i replay: list](list.md) | dove entrambi i giochi salvano i replay, come salvarne uno, cosa stampa `list` |
| [Lettura: convert](convert.md) | cosa viene letto di ogni file, cosa esce, cosa non viene letto |
| [Termini e licenza](terms.md) | i termini di Riot, cosa viene letto e cosa non lo sarà mai, la chiave API di Riot |
| [Riferimento dei comandi](../cli-reference.md) | ogni opzione e campo, generati dal codice |
| [Manutenzione di questa documentazione](maintaining.md) | la lista di controllo per ogni rilascio |

## Collegamenti {#related}

- Il visualizzatore 3DHeat: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentazione su [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- Il 3DHeat Watcher lancia questo strumento su ogni replay salvato dai giochi; per League, con la tua chiave
  da sviluppatore Riot, aggiunge la cronologia ufficiale della partita con le posizioni:
  [replay di League of Legends](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html),
  [replay di VALORANT](https://holdi601.github.io/3DHeat-Watcher/game-valorant-replays.html).
- League of Legends mentre giochi (l'API Live Client Data di Riot):
  [il Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-live.html).

## Gli strumenti 3DHeat {#the-3dheat-tools}

| Strumento | Cosa fa | Codice | Documentazione |
|---|---|---|---|
| visualizzatore 3DHeat | mostra i dati: mappe di calore, analisi di gara, revisione delle partite | [3DHeat](https://github.com/Holdi601/3DHeat) | [documentazione](https://holdi601.github.io/3DHeat/) |
| GameFiles | livelli e percorsi dai file propri di un gioco | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [documentazione](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | telemetria dei giri, e livelli ricostruiti dal video di gioco | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [documentazione](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | un plugin per Unreal Editor: un livello come un unico `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [documentazione](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | demo e mappe di Counter-Strike 2 | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [documentazione](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | registra ciò che i giochi pubblicano mentre giochi | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [documentazione](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | replay di War Thunder | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [documentazione](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | replay di World of Tanks | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [documentazione](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | replay di World of Warships | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [documentazione](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | demo dei server di Squad | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | mappe di DCS World come livelli 3D | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [documentazione](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | mappe di IL-2 Sturmovik come livelli 3D | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [documentazione](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | la mappa di Dota 2 come livello 3D | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | replay di Dota 2 come tabelle | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [documentazione](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | replay di League of Legends e VALORANT: ciò che contengono in chiaro | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | percorsi, gare e auto di Forza dalla tua installazione | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | livelli di Battlefield (Frostbite) come livelli 3D | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | percorsi di BeamNG.drive | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [documentazione](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | tappe di Assetto Corsa Rally come percorsi | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [documentazione](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | mondi di Arma Reforger (Enfusion) come livelli 3D | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [documentazione](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | replay di partite di Rainbow Six Siege | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [documentazione](https://holdi601.github.io/3DHeat-Ext-R6/) |

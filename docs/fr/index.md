---
title: "Accueil"
nav_order: 1
lang: "fr"
source: index.md
source_hash: "7d4b8345cc71"
nav_exclude: true
search_exclude: true
permalink: /fr/
---
# 3DHeat Riot {#dheat-riot}

**Qu'est-ce que c'est ?** Cet outil lit les replays de League of Legends (`.rofl`) et de VALORANT
(`.vrf`) et écrit **ce que chaque fichier contient en clair** : le tableau de fin de partie de League pour les dix
joueurs et l'en-tête du replay ; pour VALORANT, la carte, l'identifiant du match, les agents et la chronologie
des éliminations, des manches et des spikes tenue par le serveur. C'est l'un des outils qui
entourent le visualiseur [3DHeat](https://github.com/Holdi601/3DHeat)
([documentation](https://holdi601.github.io/3DHeat/)).

**Pourquoi l'utiliser ?** Pour garder les chiffres de vos parties sous forme de tableaux simples - les
éliminations, morts, l'or, les dégâts et une centaine d'autres données de chaque joueur de League, chaque
manche et chaque élimination d'une partie de VALORANT - pour vos propres statistiques, ou pour le
3DHeat Watcher, qui lance cet outil sur chaque replay que vous sauvegardez.

**Exemple :** `heat3d-riot-replays convert EUW1-7123456789.rofl -o out` ->
`out/EUW1-7123456789.rofl.json` et `out/EUW1-7123456789.rofl.players.csv`.

**Ce qu'il ne fait pas :** lire les positions ou la partie elle-même. Cette partie d'un
replay est chiffrée et brouillée contre la triche, et la traverser voudrait dire démonter le jeu,
ce que les conditions de Riot interdisent. Cet outil ne casse aucun chiffrement et ne défait aucun
brouillage ([Conditions](terms.md)).

## Démarrage rapide {#quick-start}

Vous n'avez jamais utilisé la ligne de commande ? Lisez d'abord [Avant de commencer](before-you-start.md).
Il vous faut Python 3.10 ou plus récent, rien d'autre. Lancez ces commandes dans le dossier où vous avez
cloné ou décompressé l'outil :

```bash
python -m pip install -e .                  # installs the heat3d-riot-replays command
heat3d-riot-replays list                    # where both games save replays, the ones there
heat3d-riot-replays convert -o out          # every replay there, read
```

`convert` affiche chaque fichier qu'il écrit. Ouvrez les `.csv` dans un tableur, ou lisez le
`.json` ([Lecture : convert](convert.md)).

## Pages {#pages}

| Page | Ce qu'elle couvre |
|---|---|
| [Avant de commencer](before-you-start.md) | Python, un terminal, un premier lancement |
| [Trouver les replays : list](list.md) | où les deux jeux sauvegardent les replays, sauvegarder un replay, ce qu'affiche `list` |
| [Lecture : convert](convert.md) | ce qui est lu de chaque fichier, ce qui en sort, ce qui n'est pas lu |
| [Conditions et licence](terms.md) | les conditions de Riot, ce qui est lu et ce qui ne l'est jamais, la clé d'API Riot |
| [Référence des commandes](../cli-reference.md) | chaque option et chaque champ, générés à partir du code |
| [Entretien de ces documents](maintaining.md) | la liste de contrôle de publication |

## Liens utiles {#related}

- Le visualiseur 3DHeat : [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentation sur [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- Le 3DHeat Watcher lance cet outil sur chaque replay que les jeux sauvegardent ; pour League,
  avec votre propre clé de développeur Riot, il ajoute la chronologie officielle du match avec les
  positions : [replays de League of Legends](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html),
  [replays de VALORANT](https://holdi601.github.io/3DHeat-Watcher/game-valorant-replays.html).
- League of Legends pendant que vous jouez (l'API Live Client Data de Riot) :
  [le Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-live.html).

## Les outils 3DHeat {#the-3dheat-tools}

| Outil | Ce qu'il fait | Code | Documentation |
|---|---|---|---|
| Visualiseur 3DHeat | affiche les données : cartes de chaleur, analyse de course, revue de match | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | niveaux et parcours tirés des fichiers propres à un jeu | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | télémétrie de tour, et niveaux reconstruits à partir de vidéos de jeu | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | un plugin pour l'éditeur Unreal : un niveau en un seul `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | démos et cartes de Counter-Strike 2 | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | enregistre ce que les jeux publient pendant que vous jouez | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | replays de War Thunder | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | replays de World of Tanks | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | replays de World of Warships | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | démos de serveurs Squad | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | cartes de DCS World en niveaux 3D | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | cartes d'IL-2 Sturmovik en niveaux 3D | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | la carte de Dota 2 en niveau 3D | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | replays de Dota 2 en tableaux | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | replays de League of Legends et VALORANT : ce qu'ils contiennent en clair | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | parcours, courses et voitures de Forza à partir de votre propre installation | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | niveaux de Battlefield (Frostbite) en niveaux 3D | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | parcours de BeamNG.drive | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | épreuves d'Assetto Corsa Rally en parcours | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | mondes d'Arma Reforger (Enfusion) en niveaux 3D | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | replays de matchs Rainbow Six Siege | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |

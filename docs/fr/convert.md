---
title: "Lecture : convert"
nav_order: 3
lang: "fr"
source: convert.md
source_hash: "2a11c2db4829"
nav_exclude: true
search_exclude: true
---
# Lecture : `convert` {#reading-convert}

```bash
heat3d-riot-replays convert [<replay> or <folder> ...] -o <folder>
```

lit chaque replay `.rofl` et `.vrf` et écrit ce qu'il contient en clair
dans le dossier `-o`. Sans replay, il lit tous ceux des dossiers des deux jeux
([list](list.md) montre lesquels) ; un dossier donné lit chaque `.rofl` et
`.vrf` qu'il contient. Code :
[`heat3d_ext_riot/replays.py`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/heat3d_ext_riot/replays.py).

| Option | Fait |
|---|---|
| `<replay>` ou `<folder>` | ce qu'il faut lire ; on peut en donner plusieurs (par défaut : les dossiers de replays des deux jeux) |
| `-o`, `--out FOLDER` | où vont les résultats (obligatoire) ; créé s'il n'existe pas |

Pour chaque replay, il affiche les fichiers qu'il a écrits :

```text
out\EUW1-7123456789.rofl.json
out\EUW1-7123456789.rofl.players.csv
```

## League of Legends (.rofl) {#league-of-legends-rofl}

Les deux versions du conteneur portent le tableau de fin de partie en JSON brut dans le
fichier (`statsJson`) : pour chacun des dix joueurs, le champion, les éliminations, les morts,
les passes décisives, l'or, les dégâts aux champions, les objets, l'équipe, le rôle, la victoire, son
Riot ID, et chaque autre nombre que le jeu totalise - plus de cent par joueur.

| Conteneur | Patchs | Lu |
|---|---|---|
| ROFL1 (`RIOT` 0 0) | 14.9 et antérieurs | le JSON de métadonnées (durée de partie, version, identifiants du dernier morceau et de la dernière image clé, le tableau de fin de partie) ; le bloc des durées ; l'en-tête de la charge utile (identifiant de partie, durée, nombre d'images clés et de morceaux, identifiants des morceaux de démarrage et de début de partie, intervalle des images clés, la clé de morceau telle qu'elle est stockée) ; la table des morceaux (identifiant, type, longueur, morceau suivant, décalage) |
| ROFL2 (`RIOT` 2 0) | 14.11 et suivants | le JSON de métadonnées à la fin du fichier, sa longueur dans les quatre derniers octets ; la chaîne de version près du début |

**Non lu :** la partie elle-même. Les morceaux et images clés de ROFL1 et le corps de ROFL2
sont chiffrés, et les paquets qu'ils contiennent sont brouillés à nouveau à chaque patch.
Ils sont nommés par leur plage d'octets (`keyframe`, `chunk`, `body`) et laissés tels quels.

## VALORANT (.vrf) {#valorant-vrf}

Un replay VALORANT est un replay local d'Unreal Engine : un bloc d'informations, puis des morceaux
par type et par taille.

| Partie | Lue |
|---|---|
| le bloc d'informations | chaque champ : version du fichier, versions personnalisées, longueur, version réseau, numéro de changement, nom, indicateur de direct, date d'enregistrement, indicateurs compressé et chiffré, la clé telle qu'elle est stockée |
| le morceau d'en-tête | la carte, l'identifiant du match et les agents choisis - retrouvés par leur forme, non par un décalage qui change d'une version à l'autre |
| chaque morceau d'événement | identifiant, groupe, métadonnées, heure de début et de fin, et de ses données le nom de l'événement, son heure en secondes et les nombres qui la précèdent : le tueur et la victime d'une élimination en identifiants réseau (non en noms), les débuts de manche, les spikes posés, désamorcés et explosés, les ultimes utilisés, les changements de camp |

**Non lu :** les positions, les noms, les scores, les capacités, chaque image de la partie -
ils sont dans les données de replay et les morceaux de points de contrôle, qui sont brouillés. D'un
replay chiffré, les morceaux sont parcourus et nommés, rien à l'intérieur n'est lu.

## Ce qui en sort {#what-comes-out}

| Fichier | Contient |
|---|---|
| `<file>.json` | tout ce qui a été lu. `format` (`heat3d-riot-replay/1`), `tool`, `file`, `size`, `game`, `kind` (`rofl` ou `vrf`), et la lecture : pour League, `container`, `version`, `length_ms`, `game_id`, `players` (le tableau de fin de partie), `metadata`, `payload`, `chunks` ; pour VALORANT, `file_version`, `length_ms`, `name`, `recorded_unix`, `encrypted`, `info`, `map`, `match_id`, `agents`, `events` |
| `<file>.players.csv` | League : le tableau de fin de partie, une ligne par joueur, chaque champ tel que le jeu l'a écrit |
| `<file>.events.csv` | VALORANT : la chronologie des événements, une ligne par événement |

`sections` dans le JSON liste chaque partie du fichier dans l'ordre sous la forme
`[name, start, end, what was read of it]` - le dernier `null` pour une partie non lue - et les
parties ensemble forment tout le fichier, toute portion qu'aucune partie connue ne couvre
étant nommée `unknown` (League) ou `trailing` (VALORANT). Champs :
[Référence des commandes](../cli-reference.md#output).

## Utilisation {#using-it}

Ces fichiers n'ont pas de positions : ce sont des tableaux à lire, dans un tableur ou un
script. Le 3DHeat Watcher lance cet outil sur chaque replay que les jeux sauvegardent et en fait
une session ; pour une partie de League, avec votre propre clé de développeur Riot dans ses
réglages, il récupère aussi la chronologie officielle du match depuis l'API Match-V5 de Riot - la
position de chaque joueur une fois par minute et chaque élimination à l'endroit où elle a eu lieu - que
le visualiseur 3DHeat dessine sur la carte
([replays de League of Legends dans le Watcher](https://holdi601.github.io/3DHeat-Watcher/game-lol-replays.html)).
Cette récupération est celle du Watcher, non celle de cet outil : cet outil ne lit que des fichiers.

## Comment c'est vérifié {#how-it-was-checked}

Sur des replays construits champ par champ selon les structures de roflxd.cs (MIT) et vrfkit
(Apache-2.0), y compris un morceau tronqué et un replay VALORANT chiffré ; aucun vrai replay n'était
disponible pour comparer. Le lecteur vérifie avant de lire et refuse ce qui ne correspond pas,
au lieu de deviner.

## Messages et code de sortie {#messages-and-exit-status}

| Message | Sortie | Signification |
|---|---|---|
| les fichiers écrits | 0 | terminé |
| `heat3d-riot-replays: no replay (.rofl, .vrf) found in ...` | 2 | rien à lire là où il a cherché |
| `heat3d-riot-replays: <file>: not a League of Legends or VALORANT replay this reader understands (...)` | 2 | un autre type de fichier, ou une structure que cet outil ne connaît pas ; parmi ceux lus : 1 |
| `heat3d-riot-replays: <file>: <error>` | 1 | ce replay a échoué ; les autres sont tout de même lus |

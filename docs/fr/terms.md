---
title: "Conditions et licence"
nav_order: 8
lang: "fr"
source: terms.md
source_hash: "b8ab95d59a93"
nav_exclude: true
search_exclude: true
---
# Conditions et licence {#terms-and-licence}

## Les jeux et les replays de Riot {#riots-games-and-replays}

League of Legends et VALORANT appartiennent à Riot Games, qui ne soutient pas ce
projet. Cet outil n'embarque aucun élément de Riot - aucun fichier de jeu, illustration, modèle, carte,
son, logo ni donnée de l'un ou l'autre jeu - et ne parle à aucun serveur : il lit vos propres
fichiers de replay sur votre machine, en dehors du jeu, et ne modifie rien dedans. Ce qu'il écrit
vous appartient ; utiliser l'outil est votre décision, selon les conditions que vous avez acceptées pour les jeux.

## Ce qui est lu, et ce qui ne l'est jamais {#what-is-read-and-what-never-is}

Les deux jeux protègent ce qu'il y a dans leurs replays : les données de jeu, instant par instant, sont
chiffrées et brouillées, et différemment à chaque patch, pour empêcher qu'on s'en serve pour tricher.
Passer cette protection voudrait dire démonter le client du jeu, ce que les Conditions d'utilisation
de Riot interdisent (sections 3.1 et 7.1). Donc cet outil :

- lit **seulement ce que chaque fichier contient en clair** - les métadonnées JSON en clair d'un `.rofl`
  (le tableau de fin de partie), son en-tête et sa table des morceaux ; le bloc d'informations d'un `.vrf`,
  la carte, l'identifiant du match et les agents dans son en-tête, et les morceaux d'événements du serveur ;
- **ne casse aucun chiffrement et ne défait aucun brouillage**, et ne contient aucune clé, aucun
  déchiffrement ni aucun code tiré des jeux ;
- nomme les parties protégées par leur place dans le fichier et les laisse non lues.

Une clé que le fichier lui-même stocke en clair (la clé de morceau d'un replay ROFL1) est recopiée
dans la lecture telle qu'elle est stockée, comme partie de l'en-tête ; rien n'est déchiffré avec elle.

## La clé d'API Riot {#the-riot-api-key}

L'outil n'a besoin ni de compte ni de clé. Les positions d'une partie de League viennent de
l'API Match-V5 de Riot, non du fichier : le 3DHeat Watcher peut récupérer la chronologie d'un match avec
**votre propre** clé de développeur Riot (une clé personnelle est prévue pour « showing (self) player stats »). Cette récupération est celle du Watcher ; elle est désactivée sans clé, et cet outil n'envoie rien nulle part.

## Pourquoi un paquet à part {#why-a-separate-package}

Si Riot demande un jour qu'il disparaisse, il partira seul, et le visualiseur, le Watcher et
les autres outils resteront.

## Licence et sources {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSE)).
N'a besoin que de la bibliothèque standard de Python ; les tests ont besoin de pytest (MIT). Écrit pour
ce projet, d'abord dans le cadre du 3DHeat Watcher. Les structures de fichiers ont été retenues comme des faits
à partir de roflxd.cs (MIT), vrfkit (Apache-2.0) et ValorantReplayParser (MIT), et d'une description de
ROFL2 par un ingénieur de Riot (ReplayBook, ticket 299) ; aucun code n'a été copié. Voir
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSES.md).

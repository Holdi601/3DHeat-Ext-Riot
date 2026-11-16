---
title: "Avant de commencer"
nav_order: 1.5
lang: "fr"
source: before-you-start.md
source_hash: "81c92d0ec0c5"
nav_exclude: true
search_exclude: true
---
# Avant de commencer {#before-you-start}

Vous n'avez jamais utilisé la ligne de commande ? Cette page vous mène de zéro à un premier lancement.
Cela prend environ dix minutes, une seule fois.

## 1. Installer Python {#install-python}

Cet outil demande **Python 3.10 ou plus récent**.

- **Windows :** téléchargez Python sur [python.org/downloads](https://www.python.org/downloads/)
  et lancez l'installateur. Sur son premier écran, cochez **Add python.exe to PATH**,
  puis cliquez sur **Install Now**.
- **macOS et Linux :** Python 3 est souvent déjà là. Là où ces pages disent
  `python`, tapez `python3`.

## 2. Obtenir cet outil {#get-this-tool}

Ouvrez [github.com/Holdi601/3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot), cliquez sur le
bouton vert **Code**, puis sur **Download ZIP**, et décompressez-le dans le dossier de votre choix. Si vous utilisez git : `git clone https://github.com/Holdi601/3DHeat-Ext-Riot`.

## 3. Ouvrir un terminal dans ce dossier {#open-a-terminal-in-that-folder}

Un terminal est une fenêtre où vous tapez des commandes.

- **Windows :** ouvrez le dossier dans l'Explorateur, cliquez dans la barre d'adresse, tapez
  `powershell` et appuyez sur Entrée. Une fenêtre bleue ou noire s'ouvre, déjà dans ce
  dossier.
- **macOS :** ouvrez **Terminal**, tapez `cd ` (avec un espace), glissez le dossier dans la
  fenêtre et appuyez sur Entrée.

`cd` signifie « changer de dossier » : `cd C:\Tools\3DHeat-Ext-Riot` va dans ce dossier.

## 4. Installer l'outil {#install-the-tool}

Tapez ceci et appuyez sur Entrée :

```bash
python -m pip install -e .
```

Vous devez voir, à la fin : `Successfully installed heat3d-ext-riot-...`.
L'outil n'a besoin de rien d'autre que Python lui-même.

## 5. Sauvegarder un replay et le lancer {#save-a-replay-and-run-it}

Dans League of Legends, ouvrez votre historique de parties, choisissez une partie et cliquez sur le
bouton de téléchargement ; dans VALORANT, ouvrez Carrière, choisissez une partie et téléchargez
son replay. Ensuite :

```bash
heat3d-riot-replays list
```

Vous devez voir quelque chose comme :

```text
League of Legends: C:\Users\you\Documents\League of Legends\Replays
  EUW1-7123456789.rofl                    21.4 MB
VALORANT: C:\Users\you\AppData\Local\VALORANT\Saved\Demos
  0a1b2c3d-1111-2222-3333-444455556666.vrf  35.0 MB
2 replay(s)
```

Suite : [Lecture : convert](convert.md).

## Comment lire les commandes de ces pages {#how-to-read-the-commands-on-these-pages}

| Vous voyez | Cela signifie |
|---|---|
| `<file>` | un espace réservé : tapez votre propre valeur à la place, sans les `< >` |
| `[REPLAY ...]` | facultatif : omettez-le, ou tapez-le comme indiqué |
| `# a note` | un commentaire pour vous : ne le tapez pas |
| `"C:\My Files\x"` | mettez entre guillemets un chemin qui contient des espaces |

## Quand quelque chose ne va pas {#when-something-goes-wrong}

| Le message | Que faire |
|---|---|
| `'python' is not recognized` | Python n'est pas installé, ou la case PATH n'était pas cochée : réinstallez-le et cochez-la (ou tapez `py` au lieu de `python`). |
| `'heat3d-riot-replays' is not recognized` | Refaites l'étape 4 dans le dossier de l'outil, ou tapez `python -m heat3d_ext_riot` au lieu de `heat3d-riot-replays` : cela fait la même chose. |
| `no replay (.rofl, .vrf) found in ...` | Sauvegardez d'abord un replay dans le jeu (étape 5), ou donnez le chemin du replay à `convert`. |
| `... not a League of Legends or VALORANT replay this reader understands` | Le fichier est autre chose, ou il est tronqué ; un replay dans une structure que cet outil ne connaît pas est refusé de la même façon. |
| autre chose | Lisez la dernière ligne du message, puis ouvrez un ticket sur GitHub avec elle. |

Chaque commande se termine aussi par un **code de sortie** : 0 signifie que cela a marché, 2 qu'il
n'y avait rien à lire, 1 qu'un replay a échoué. Pour le voir, tapez
`echo $LASTEXITCODE` dans PowerShell, ou `echo $?` sous macOS et Linux.

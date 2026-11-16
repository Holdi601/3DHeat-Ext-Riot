---
title: "Entretien de ces documents"
nav_order: 91
lang: "fr"
source: maintaining.md
source_hash: "60ba5e33861f"
nav_exclude: true
search_exclude: true
---
# Entretien de ces documents {#maintaining-these-docs}

Une liste de contrôle à chaque publication, pour que les pages ne soient jamais en retard sur le code.

1. **Régénérer la référence.** `python tools/gen_docs_reference.py` réécrit
   [Référence des commandes](../cli-reference.md) à partir du `--help` du programme et de ses
   colonnes de sortie. `python tools/gen_docs_reference.py --check` se termine avec 1 lorsque
   la page validée est périmée.
2. **Lister ce qui a changé.** `git log v<VERSION>..HEAD --oneline`, où
   `<VERSION>` est la dernière version publiée (le fichier `VERSION` au moment de la publication). Donnez à chaque
   nouvelle fonctionnalité, option et colonne de sortie une place sur une page, et une
   ligne dans la section **Docs** de [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/CHANGELOG.md).
3. **Relecture indépendante.** Quelqu'un qui n'a pas écrit les pages relit le
   README et chaque page modifiée, images comprises, trois fois : comme un débutant qui n'a jamais
   utilisé de terminal, comme un enfant de huit ans, et comme un expert qui vérifie chaque
   option par rapport à `--help`. Les exemples n'utilisent que des noms et des chiffres inventés.
4. **Corriger** tout ce que la relecture trouve.
5. **Traductions.** Chaque page traduite enregistre le hash de la page anglaise dont elle est issue.
   Retraduisez les pages dont la source anglaise a changé, puis relisez chaque langue : texte clair,
   étiquettes de schéma correctes, mêmes mots que l'interface traduite du visualiseur.
6. **Lancer les tests** (`pytest`).
7. **Publier** seulement après le feu vert du propriétaire.

## Traductions : les commandes {#translations-the-commands}

Le site doit être traduit dans les 40 langues du visualiseur 3DHeat (pour l'instant : uniquement l'anglais). L'anglais est dans
`docs/`, chaque autre langue dans `docs/<lang>/` avec les mêmes noms de fichiers. `tools/docs_i18n.py` tient les comptes :

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Ne traduisez que ce que `todo` liste : gardez le Markdown, les liens, le code, les noms de fichiers et de
colonnes tels quels, traduisez les titres et les descriptions d'images, et utilisez les mots de la
visualiseur 3DHeat pour ses boutons et panneaux (son `src/i18n/locales/<lang>/`). Les pages de référence
générées et les images de terminal restent en anglais. Sur le site, une traduction périmée le signale et
renvoie à la page anglaise ; une traduction absente retombe sur l'anglais. Le menu des langues de
l'en-tête et la redirection de la page d'accueil selon la langue du navigateur viennent de `docs/_includes/`.

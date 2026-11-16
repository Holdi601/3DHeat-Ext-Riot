---
title: "Mantener estas páginas"
nav_order: 91
lang: "es"
source: maintaining.md
source_hash: "60ba5e33861f"
nav_exclude: true
search_exclude: true
---
# Mantener estas páginas {#maintaining-these-docs}

Una lista de comprobación para cada versión, para que las páginas nunca se queden atrás respecto al código.

1. **Regenerar la referencia.** `python tools/gen_docs_reference.py` reescribe
   [Referencia de comandos](../cli-reference.md) a partir del propio `--help` del programa y de
   sus columnas de salida. `python tools/gen_docs_reference.py --check` termina con 1 cuando
   la página confirmada está desactualizada.
2. **Listar lo que cambió.** `git log v<VERSION>..HEAD --oneline`, donde
   `<VERSION>` es la última versión publicada (el archivo `VERSION` en la publicación).
   Dale a cada nueva función, opción y columna de salida un lugar en una página, y una
   fila en la sección **Docs** de [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/CHANGELOG.md).
3. **Revisión independiente.** Alguien que no escribió las páginas lee el
   README y cada página cambiada, las imágenes incluidas, tres veces: como un principiante que nunca ha usado
   una terminal, como un niño de 8 años, y como un experto que comprueba cada opción contra
   `--help`. Los ejemplos usan solo nombres y números inventados.
4. **Corregir** todo lo que encuentre la revisión.
5. **Traducciones.** Cada página traducida registra el hash de la página inglesa de la que
   se hizo. Vuelve a traducir las páginas cuyo original en inglés cambió,
   y luego revisa cada idioma: texto claro, etiquetas correctas en los diagramas, las mismas
   palabras que la interfaz traducida del visor.
6. **Ejecutar las pruebas** (`pytest`).
7. **Publicar** solo con el visto bueno del propietario.

## Traducciones: los comandos {#translations-the-commands}

El sitio se va a traducir a los 40 idiomas del visor de 3DHeat (hasta ahora: solo inglés): el inglés en
`docs/`, cada otro idioma en `docs/<lang>/` con los mismos nombres de archivo. `tools/docs_i18n.py` lleva la contabilidad:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Traduce solo lo que lista `todo`: mantén el Markdown, los enlaces, el código, los nombres de archivo y de columnas tal como están,
traduce los títulos y las descripciones de las imágenes, y usa las palabras propias del visor de 3DHeat para sus botones
y paneles (su `src/i18n/locales/<lang>/`). Las páginas de referencia generadas y las imágenes de terminal siguen
en inglés. En el sitio, una traducción desactualizada lo indica y enlaza la página en inglés; una que falta
recurre al inglés. El menú de idiomas de la cabecera y la redirección por idioma del navegador de la página de inicio
vienen de `docs/_includes/`.

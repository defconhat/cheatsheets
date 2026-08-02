# 📌 Шпаргалки

Статический сайт со шпаргалками (горячие клавиши, команды, концепции)
по терминалу, DevOps, BigData и другим инструментам ежедневной работы.

**Адрес:** <https://defconhat.github.io/cheatsheets/>

## Что внутри

```
manuals/            ← исходники шпаргалок в Markdown (.md)
cheatsheets-site/   ← генератор статического сайта (Python)
  ├─ build.py         сборка мультистраничного сайта в docs/
  ├─ build_single.py  сборка одного standalone HTML-файла
  └─ assets/          style.css, search.js, page.js
docs/               ← собранный сайт (отдаёт GitHub Pages)
```

## Как пересобрать

```bash
cd cheatsheets-site
python build.py            # → соберёт ./docs (через SRC_DIR = ../manuals)
# или локально: python build.py собирает в _site, копируем в ../docs
```

Зависимости: `markdown`, `pygments`.

```bash
pip install markdown pygments
```

## Добавить новую шпаргалку

1. Положить `.md` в `manuals/`.
2. Добавить запись в список `CHEATSHEETS` в `cheatsheets-site/build.py`
   (slug, title, icon, desc, src, tags).
3. `python cheatsheets-site/build.py` и скопировать `_site/*` в `docs/`.
4. Закоммитить — GitHub Pages обновится автоматически.

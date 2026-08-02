#!/usr/bin/env python3
"""
Сборка сайта в ОДИН standalone HTML-файл (для расшаривания).
Всё встроено: CSS, JS, все 9 шпаргалок на отдельных "страницах" (через JS-роутинг).
Никаких внешних зависимостей — файл можно открыть офлайн где угодно.

Запуск:
    python build_single.py
Результат: _site_single/cheatsheets-standalone.html
"""
import re
import html
import base64
import datetime
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

from build import CHEATSHEETS, SRC_DIR, slugify, SITE_TITLE, SITE_SUBTITLE

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "_site_single"
OUT_FILE = OUT_DIR / "cheatsheets-standalone.html"
ASSETS = ROOT / "assets"


def md_to_html(md_text: str):
    """Конвертация Markdown → (html_body, toc)."""
    md = markdown.Markdown(
        extensions=["extra", "codehilite", "toc", "admonition", "sane_lists", "smarty"],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "highlight", "noclasses": False},
            "toc": {"permalink": "#", "permalink_title": "Ссылка", "slugify": slugify},
        },
    )
    return md.convert(md_text), md.toc


def read_asset(name: str) -> str:
    return (ASSETS / name).read_text(encoding="utf-8")


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Pygments CSS (светлая тёплая тема) ──
    formatter = HtmlFormatter(style="gruvbox-light", nobackground=True)
    pyg_css = formatter.get_style_defs(".highlight") + "\n.highlight pre { overflow-x: auto; }"

    style_css = read_asset("style.css")

    # ── Рендерим все шпаргалки → словарь slug → html ──
    pages = {}
    for cs in CHEATSHEETS:
        md_text = (SRC_DIR / cs["src"]).read_text(encoding="utf-8")
        body, toc = md_to_html(md_text)
        pages[cs["slug"]] = {"body": body, "toc": toc, "meta": cs}

    # ── Данные для JS (метаданные карточек) ──
    cards_json = json_dumps([{
        "slug": c["slug"], "title": c["title"], "icon": c["icon"],
        "desc": c["desc"], "tags": c["tags"],
    } for c in CHEATSHEETS])

    # ── Карточки для главной (статичный HTML, на случай отключённого JS) ──
    cards_html = "\n".join(
        f'<a class="card" href="#/{c["slug"]}" data-slug="{c["slug"]}">'
        f'<div class="card-icon">{c["icon"]}</div>'
        f'<div class="card-body"><h3>{html.escape(c["title"])}</h3>'
        f'<p>{html.escape(c["desc"])}</p>'
        f'<div class="tags">{"".join(f"<span class=\"tag\">{html.escape(t)}</span>" for t in c["tags"])}</div>'
        f'</div><div class="card-arrow">→</div></a>'
        for c in CHEATSHEETS
    )

    # ── Боковая навигация ──
    nav_items = "\n".join(
        f'<a href="#/{c["slug"]}" class="nav-item" data-slug="{c["slug"]}">'
        f'<span class="nav-ico">{c["icon"]}</span>{html.escape(c["title"])}</a>'
        for c in CHEATSHEETS
    )

    # ── Шаблон страницы-шпаргалки (скрытый, клонируется через JS) ──
    page_template = """<div class="layout" id="page-template" hidden>
  <aside class="sidebar">
    <a href="#/" class="brand">📌 Шпаргалки</a>
    <nav class="nav" id="page-nav"></nav>
  </aside>
  <main class="content">
    <article id="page-body"></article>
    <nav class="pagination">
      <a class="pager prev" id="page-prev"></a>
      <a class="pager next" id="page-next"></a>
    </nav>
  </main>
  <aside class="toc">
    <details open>
      <summary>📑 Оглавление</summary>
      <div class="toc-list" id="page-toc"></div>
    </details>
  </aside>
</div>"""

    stamp = datetime.datetime.now().strftime("%Y-%m-%d")

    # ── Итоговый HTML ──
    out = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(SITE_TITLE)}</title>
<style>
/* ====== Встроенные стили ====== */
{style_css}

/* ====== Pygments (подсветка кода) ====== */
{pyg_css}

/* ====== Специфичные стили для standalone ====== */
body {{ transition: opacity 0.15s; }}
#view-home {{ display: block; }}
#view-page {{ display: none; }}
body[data-view="page"] #view-home {{ display: none; }}
body[data-view="page"] #view-page {{ display: block; }}

/* Главная видна сразу (без JS тоже работает) */
#hero-main .grid #cards-static {{ }}

/* Скрыть шаблон страницы */
#page-template {{ display: none !important; }}

/* Подвал standalone */
.standalone-footer {{
  text-align: center;
  padding: 24px;
  color: var(--text-faint);
  font-size: 0.78rem;
  font-family: var(--font-mono);
  border-top: 1px solid var(--border);
}}
.standalone-footer a {{ color: var(--text-mute); }}
</style>
</head>
<body data-view="home">

<!-- ══════════════ ГЛАВНАЯ ══════════════ -->
<div id="view-home">
  <header class="hero" id="hero-main">
    <div class="hero-inner">
      <h1>📌 {html.escape(SITE_TITLE)}</h1>
      <p class="subtitle">{html.escape(SITE_SUBTITLE)}</p>
      <div class="search">
        <input type="search" id="search" placeholder="🔍 Поиск по {len(CHEATSHEETS)} шпаргалкам…" autocomplete="off">
      </div>
    </div>
  </header>
  <main class="grid" id="cards">
{cards_html}
  </main>
  <footer class="standalone-footer">
    📦 Standalone-сборка · {len(CHEATSHEETS)} шпаргалок · собрано {stamp}
  </footer>
</div>

<!-- ══════════════ СТРАНИЦА ШПАРГАЛКИ ══════════════ -->
<div id="view-page">
{page_template}
</div>

<button class="back-top" id="backTop" aria-label="Наверх">↑</button>

<script>
// ══════════════ Данные всех страниц ══════════════
const PAGES = {json_dumps(pages)};

// ══════════════ Хеш-роутинг (один файл, разные "страницы") ══════════════
(function () {{
  const body = document.body;
  const home = document.getElementById("view-home");
  const page = document.getElementById("view-page");
  const tpl = document.getElementById("page-template");

  // Карточки и навигация — на главных кликабельны через hash
  document.querySelectorAll('a[href^="#/"]').forEach(a => {{
    a.addEventListener("click", () => {{
      const slug = a.getAttribute("href").slice(2);
      if (PAGES[slug]) renderPage(slug);
    }});
  }});

  function renderPage(slug) {{
    const data = PAGES[slug];
    if (!data) {{ goHome(); return; }}

    // Заполняем шаблон
    const layout = tpl.cloneNode(true);
    layout.id = "page-layout";
    layout.hidden = false;
    layout.style.display = "grid";

    // Боковая навигация
    const navHtml = [{cards_json}].map(c => `
      <a href="#/${{c.slug}}" class="nav-item ${{c.slug === slug ? "active" : ""}}" data-slug="${{c.slug}}">
        <span class="nav-ico">${{c.icon}}</span>${{c.title}}
      </a>`).join("");
    layout.querySelector("#page-nav").innerHTML = navHtml;

    // Контент и TOC
    layout.querySelector("#page-body").innerHTML = data.body;
    layout.querySelector("#page-toc").innerHTML = data.toc;

    // Пагинация
    const order = [{cards_json}];
    const idx = order.findIndex(c => c.slug === slug);
    const prev = idx > 0 ? order[idx - 1] : null;
    const next = idx < order.length - 1 ? order[idx + 1] : null;
    const prevEl = layout.querySelector("#page-prev");
    const nextEl = layout.querySelector("#page-next");
    prevEl.style.visibility = prev ? "visible" : "hidden";
    nextEl.style.visibility = next ? "visible" : "hidden";
    if (prev) {{ prevEl.textContent = "← " + prev.title; prevEl.href = "#/" + prev.slug;
      prevEl.onclick = () => renderPage(prev.slug); }}
    if (next) {{ nextEl.textContent = next.title + " →"; nextEl.href = "#/" + next.slug;
      nextEl.onclick = () => renderPage(next.slug); }}

    // Навигация в сайдбаре
    layout.querySelectorAll('.nav-item').forEach(a => {{
      a.onclick = (e) => {{ const s = a.getAttribute("data-slug"); if (PAGES[s]) renderPage(s); }};
    }});

    // Заменяем содержимое
    page.innerHTML = "";
    page.appendChild(layout);

    body.dataset.view = "page";
    document.title = data.meta.title + " — {html.escape(SITE_TITLE)}";
    window.scrollTo(0, 0);
    location.hash = "/" + slug;
    initPageFeatures(layout);
  }}

  function goHome() {{
    body.dataset.view = "home";
    document.title = "{html.escape(SITE_TITLE)}";
    location.hash = "";
    window.scrollTo(0, 0);
  }}

  // Кнопка "наверх"
  const backTop = document.getElementById("backTop");
  window.addEventListener("scroll", () => {{
    backTop.classList.toggle("visible", window.scrollY > 400);
  }}, {{ passive: true }});
  backTop.onclick = () => window.scrollTo({{ top: 0, behavior: "smooth" }});

  // Восстановление состояния по hash при загрузке
  function route() {{
    const h = location.hash.slice(1);
    if (h.startsWith("/") && PAGES[h.slice(1)]) {{
      renderPage(h.slice(1));
    }} else {{
      goHome();
    }}
  }}
  window.addEventListener("hashchange", route);
  route();

  // ══════════════ Поиск (главная) ══════════════
  const searchInput = document.getElementById("search");
  if (searchInput) {{
    const cards = Array.from(document.querySelectorAll("#cards .card"));
    const indexed = cards.map(c => ({{ el: c, text: c.textContent.toLowerCase() }}));
    let noRes = null;
    searchInput.addEventListener("input", () => {{
      const q = searchInput.value.trim().toLowerCase();
      let visible = 0;
      indexed.forEach(({{ el, text }}) => {{
        const m = !q || text.includes(q);
        el.classList.toggle("hidden", !m);
        if (m) visible++;
      }});
      if (!noRes) {{
        noRes = document.createElement("div");
        noRes.className = "no-results";
        noRes.textContent = "Ничего не найдено 🤔";
        document.getElementById("cards").appendChild(noRes);
      }}
      noRes.style.display = visible === 0 ? "block" : "none";
    }});
    document.addEventListener("keydown", (e) => {{
      if (e.key === "/" && document.activeElement !== searchInput) {{
        e.preventDefault(); searchInput.focus();
      }}
      if (e.key === "Escape" && document.activeElement === searchInput) {{
        searchInput.value = ""; searchInput.dispatchEvent(new Event("input")); searchInput.blur();
      }}
    }});
  }}

  // ══════════════ Фичи страницы: копирование кода, TOC-подсветка ══════════════
  function initPageFeatures(layout) {{
    // Кнопка "копировать" у блоков кода
    layout.querySelectorAll("article pre").forEach(pre => {{
      if (pre.querySelector(".copy-btn")) return;
      const btn = document.createElement("button");
      btn.className = "copy-btn"; btn.textContent = "копировать";
      btn.onclick = async () => {{
        const code = pre.querySelector("code");
        const text = code ? code.textContent : pre.textContent;
        try {{
          await navigator.clipboard.writeText(text);
          btn.textContent = "✓ скопировано"; btn.classList.add("copied");
          setTimeout(() => {{ btn.textContent = "копировать"; btn.classList.remove("copied"); }}, 1500);
        }} catch {{
          btn.textContent = "ошибка"; setTimeout(() => btn.textContent = "копировать", 1500);
        }}
      }};
      pre.style.position = "relative"; pre.appendChild(btn);
    }});

    // Подсветка активного раздела в TOC при скролле
    const headings = Array.from(layout.querySelectorAll("article h2, article h3"));
    const tocLinks = Array.from(layout.querySelectorAll(".toc a[href^='#']"));
    if (headings.length && tocLinks.length) {{
      const obs = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            tocLinks.forEach(link => {{
              const active = link.getAttribute("href") === "#" + entry.target.id;
              link.style.color = active ? "var(--text)" : "";
              link.style.fontWeight = active ? "700" : "";
              link.style.borderLeftColor = active ? "var(--text-dim)" : "transparent";
            }});
          }}
        }});
      }}, {{ rootMargin: "-80px 0px -70% 0px" }});
      headings.forEach(h => h.id && obs.observe(h));
    }}

    // Навигация клавишами
    layout.tabIndex = 0;
    document.onkeydown = (e) => {{
      const tag = document.activeElement.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      const h = location.hash.slice(1);
      if (!h.startsWith("/")) return;
      const slug = h.slice(1);
      const order = [{cards_json}];
      const idx = order.findIndex(c => c.slug === slug);
      if ((e.ctrlKey || e.metaKey) && e.key === "ArrowLeft" && idx > 0)
        renderPage(order[idx-1].slug);
      if ((e.ctrlKey || e.metaKey) && e.key === "ArrowRight" && idx < order.length-1)
        renderPage(order[idx+1].slug);
    }};
  }}
}})();
</script>
</body>
</html>"""

    OUT_FILE.write_text(out, encoding="utf-8")
    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"✓ {OUT_FILE.name}  ({size_kb:.0f} KB)")
    print(f"\n✅ Standalone HTML: {OUT_FILE}")
    print(f"   Открыть: file://{OUT_FILE}")


def json_dumps(obj) -> str:
    """JSON без проблемных символов для встраивания в <script>."""
    import json
    return json.dumps(obj, ensure_ascii=False)


if __name__ == "__main__":
    build()

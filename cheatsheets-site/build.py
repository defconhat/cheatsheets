#!/usr/bin/env python3
"""
Генератор статического сайта со шпаргалками.
Конвертирует Markdown-файлы в HTML-страницы с подсветкой синтаксиса,
навигацией, оглавлением и поиском.

Запуск:
    python build.py
"""
import re
import html
import shutil
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

# ── Конфигурация ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT.parent / "manuals"         # ../manuals/  (где лежат .md)
OUT_DIR = ROOT / "_site"
ASSETS_DIR = OUT_DIR / "assets"

# Метаданные шпаргалок: slug, заголовок, эмодзи-иконка, описание, цвет
CHEATSHEETS = [
    {
        "slug": "yazi",
        "title": "Yazi",
        "icon": "📦",
        "desc": "Терминальный файловый менеджер на Rust",
        "color": "#7c3aed",
        "src": "yazi-hotkeys.md",
        "tags": ["файлы", "терминал", "rust"],
    },
    {
        "slug": "neovim",
        "title": "Neovim (LazyVim)",
        "icon": "📘",
        "desc": "Дистрибутив Neovim на базе lazy.nvim",
        "color": "#57b657",
        "src": "neovim-lazyvim-hotkeys.md",
        "tags": ["редактор", "vim", "lsp"],
    },
    {
        "slug": "niri",
        "title": "Niri",
        "icon": "🪟",
        "desc": "Scrollable-tiling Wayland compositor",
        "color": "#f59e0b",
        "src": "niri-hotkeys.md",
        "tags": ["wayland", "wm", "тайлинг"],
    },
    {
        "slug": "tmux",
        "title": "Tmux",
        "icon": "🪟",
        "desc": "Терминальный мультиплексор",
        "color": "#06b6d4",
        "src": "tmux-hotkeys.md",
        "tags": ["терминал", "сессии", "сплиты"],
    },
    {
        "slug": "bash",
        "title": "Bash",
        "icon": "🐚",
        "desc": "Скриптинг и использование оболочки",
        "color": "#eab308",
        "src": "bash-cheatsheet.md",
        "tags": ["shell", "скрипты", "автоматизация"],
    },
    {
        "slug": "git",
        "title": "Git",
        "icon": "🔀",
        "desc": "Контроль версий и workflow",
        "color": "#ef4444",
        "src": "git-cheatsheet.md",
        "tags": ["vcs", "github", "коммиты"],
    },
    {
        "slug": "terminal",
        "title": "Терминал Linux",
        "icon": "🖥️",
        "desc": "Базовые и продвинутые команды",
        "color": "#10b981",
        "src": "terminal-commands.md",
        "tags": ["cli", "linux", "команды"],
    },
    {
        "slug": "powershell",
        "title": "PowerShell",
        "icon": "💻",
        "desc": "Кроссплатформенная оболочка и скриптинг (Windows/Linux)",
        "color": "#0f7cbd",
        "src": "powershell-cheatsheet.md",
        "tags": ["shell", "windows", "скрипты", ".net"],
    },
    {
        "slug": "cmd",
        "title": "CMD (cmd.exe)",
        "icon": "🪟",
        "desc": "Классическая командная строка Windows",
        "color": "#71717a",
        "src": "cmd-cheatsheet.md",
        "tags": ["windows", "bat", "cmd"],
    },
    {
        "slug": "python",
        "title": "Python",
        "icon": "🐍",
        "desc": "Язык и стандартная библиотека",
        "color": "#71717a",
        "src": "python-cheatsheet.md",
        "tags": ["python", "язык", "stdlib"],
    },
    {
        "slug": "systemd",
        "title": "systemd",
        "icon": "⚙️",
        "desc": "Управление службами, таймеры, журналы",
        "color": "#71717a",
        "src": "systemd-cheatsheet.md",
        "tags": ["linux", "сервисы", "init"],
    },
    {
        "slug": "ssh",
        "title": "SSH",
        "icon": "🔐",
        "desc": "Удалённый доступ, ключи, туннели",
        "color": "#71717a",
        "src": "ssh-cheatsheet.md",
        "tags": ["сеть", "безопасность", "туннели"],
    },
    {
        "slug": "make-cmake",
        "title": "Make / CMake",
        "icon": "🔨",
        "desc": "Системы сборки для C/C++",
        "color": "#71717a",
        "src": "make-cmake-cheatsheet.md",
        "tags": ["сборка", "c/c++", "make"],
    },
    {
        "slug": "docker",
        "title": "Docker",
        "icon": "🐳",
        "desc": "Контейнеризация и docker-compose",
        "color": "#71717a",
        "src": "docker-cheatsheet.md",
        "tags": ["контейнеры", "devops", "compose"],
    },
    {
        "slug": "pacman",
        "title": "pacman / yay / paru",
        "icon": "📦",
        "desc": "Пакетный менеджер Arch / CachyOS + AUR",
        "color": "#71717a",
        "src": "pacman-yay-paru-cheatsheet.md",
        "tags": ["arch", "aur", "пакеты"],
    },
    {
        "slug": "spark",
        "title": "Apache Spark / PySpark",
        "icon": "⚡",
        "desc": "Распределённая обработка больших данных",
        "color": "#71717a",
        "src": "spark-cheatsheet.md",
        "tags": ["bigdata", "etl", "pyspark"],
    },
    {
        "slug": "markdown",
        "title": "Markdown",
        "icon": "📝",
        "desc": "Синтаксис разметки для README и документации",
        "color": "#71717a",
        "src": "markdown-cheatsheet.md",
        "tags": ["разметка", "docs", "readme"],
    },
    {
        "slug": "regex",
        "title": "Регулярные выражения",
        "icon": "🔍",
        "desc": "Шаблоны для поиска и замены",
        "color": "#71717a",
        "src": "regex-cheatsheet.md",
        "tags": ["regex", "поиск", "текст"],
    },
    {
        "slug": "jq-json",
        "title": "jq + JSON",
        "icon": "🔧",
        "desc": "Обработка JSON в командной строке",
        "color": "#71717a",
        "src": "jq-json-cheatsheet.md",
        "tags": ["json", "cli", "jq"],
    },
    {
        "slug": "awk-sed",
        "title": "awk / sed",
        "icon": "✂️",
        "desc": "Обработка и редактирование текста",
        "color": "#71717a",
        "src": "awk-sed-cheatsheet.md",
        "tags": ["текст", "sed", "awk"],
    },
    {
        "slug": "airflow",
        "title": "Apache Airflow",
        "icon": "🌪️",
        "desc": "Оркестрация ETL/ELT пайплайнов",
        "color": "#71717a",
        "src": "airflow-cheatsheet.md",
        "tags": ["etl", "оркестрация", "dag"],
    },
    {
        "slug": "http-curl",
        "title": "HTTP / curl",
        "icon": "🌐",
        "desc": "HTTP-протокол и запросы curl",
        "color": "#71717a",
        "src": "http-curl-cheatsheet.md",
        "tags": ["http", "curl", "api"],
    },
    {
        "slug": "yaml",
        "title": "YAML",
        "icon": "📄",
        "desc": "Формат данных для K8s, Compose, CI/CD",
        "color": "#71717a",
        "src": "yaml-cheatsheet.md",
        "tags": ["yaml", "конфиг", "k8s"],
    },
    {
        "slug": "vscode",
        "title": "VS Code",
        "icon": "💻",
        "desc": "Горячие клавиши и настройка редактора",
        "color": "#71717a",
        "src": "vscode-cheatsheet.md",
        "tags": ["редактор", "ide", "shortcuts"],
    },
    {
        "slug": "cron",
        "title": "cron",
        "icon": "⏰",
        "desc": "Планировщик задач в Linux",
        "color": "#71717a",
        "src": "cron-cheatsheet.md",
        "tags": ["расписание", "linux", "automation"],
    },
    {
        "slug": "fzf-zoxide",
        "title": "fzf + zoxide",
        "icon": "🔎",
        "desc": "Fuzzy-поиск и умный cd",
        "color": "#71717a",
        "src": "fzf-zoxide-cheatsheet.md",
        "tags": ["cli", "поиск", "навигация"],
    },
    {
        "slug": "minikube-k8s",
        "title": "Minikube / Kubernetes",
        "icon": "☸️",
        "desc": "Локальный K8s и kubectl",
        "color": "#71717a",
        "src": "minikube-k8s-cheatsheet.md",
        "tags": ["k8s", "kubernetes", "devops"],
    },
    {
        "slug": "cicd",
        "title": "GitLab CI / GitHub Actions",
        "icon": "🦊",
        "desc": "Непрерывная интеграция и доставка",
        "color": "#71717a",
        "src": "cicd-cheatsheet.md",
        "tags": ["ci/cd", "gitlab", "github"],
    },
    {
        "slug": "nginx",
        "title": "nginx",
        "icon": "🌐",
        "desc": "Веб-сервер и reverse-proxy",
        "color": "#71717a",
        "src": "nginx-cheatsheet.md",
        "tags": ["web", "proxy", "load-balancer"],
    },
    {
        "slug": "dbt",
        "title": "dbt",
        "icon": "🔧",
        "desc": "Трансформация данных в DWH",
        "color": "#71717a",
        "src": "dbt-cheatsheet.md",
        "tags": ["data", "etl", "dwh"],
    },
    {
        "slug": "kafka",
        "title": "Apache Kafka",
        "icon": "🐘",
        "desc": "Потоковая обработка событий",
        "color": "#71717a",
        "src": "kafka-cheatsheet.md",
        "tags": ["streaming", "bigdata", "events"],
    },
    {
        "slug": "prometheus-grafana",
        "title": "Prometheus / Grafana",
        "icon": "📊",
        "desc": "Сбор метрик и дашборды мониторинга",
        "color": "#71717a",
        "src": "prometheus-grafana-cheatsheet.md",
        "tags": ["мониторинг", "метрики", "dashboards"],
    },
    {
        "slug": "iceberg-nessie",
        "title": "Iceberg / Nessie",
        "icon": "🧊",
        "desc": "Table format + Git-подобный каталог для lakehouse",
        "color": "#71717a",
        "src": "iceberg-nessie-cheatsheet.md",
        "tags": ["lakehouse", "table-format", "bigdata"],
    },
    {
        "slug": "impala",
        "title": "Apache Impala",
        "icon": "🐬",
        "desc": "MPP SQL-движок для аналитики",
        "color": "#71717a",
        "src": "impala-cheatsheet.md",
        "tags": ["sql", "bigdata", "olap"],
    },
    {
        "slug": "terraform",
        "title": "Terraform",
        "icon": "🏗️",
        "desc": "Infrastructure as Code (облако, K8s)",
        "color": "#71717a",
        "src": "terraform-cheatsheet.md",
        "tags": ["iac", "облако", "devops"],
    },
    {
        "slug": "linux-internals",
        "title": "Linux Internals",
        "icon": "🐧",
        "desc": "procfs / sysfs / cgroups / namespaces",
        "color": "#71717a",
        "src": "linux-internals-cheatsheet.md",
        "tags": ["linux", "ядро", "cgroups"],
    },
    {
        "slug": "miscellaneous",
        "title": "Miscellaneous",
        "icon": "🧰",
        "desc": "SQL-трюки, CachyOS, Python, инструменты — сборник заметок",
        "color": "#71717a",
        "src": "miscellaneous-cheatsheet.md",
        "tags": ["заметки", "sql", "разное"],
    },
    {
        "slug": "python-automation-libs",
        "title": "Python: авт-ция (10 libs)",
        "icon": "🐍",
        "desc": "tqdm, Rich, sh, Watchdog, Loguru, IceCream и др.",
        "color": "#3b82f6",
        "src": "python-automation-libs.md",
        "tags": ["python", "автоматизация", "библиотеки"],
    },
    {
        "slug": "python-features",
        "title": "Python: 14 фич",
        "icon": "🐍",
        "desc": "overload, дженерики, match-case, протоколы, метаклассы и др.",
        "color": "#3b82f6",
        "src": "python-features.md",
        "tags": ["python", "typing", "синтаксис", "паттерны"],
    },
    {
        "slug": "eza",
        "title": "eza",
        "icon": "🌈",
        "desc": "Современная замена ls (форк exa) на Rust",
        "color": "#f59e0b",
        "src": "eza-cheatsheet.md",
        "tags": ["терминал", "ls", "rust", "файлы"],
    },
    {
        "slug": "dbeaver",
        "title": "DBeaver",
        "icon": "🗄️",
        "desc": "Универсальный GUI-клиент для БД (Postgres, MySQL, ClickHouse…)",
        "color": "#8b5cf6",
        "src": "dbeaver-cheatsheet.md",
        "tags": ["базы-данных", "sql", "gui", "postgres"],
    },
    {
        "slug": "zcode",
        "title": "ZCode",
        "icon": "🤖",
        "desc": "AI-агент для кодинга: команды, скиллы, MCP, плагины",
        "color": "#10b981",
        "src": "zcode-cheatsheet.md",
        "tags": ["ai", "агент", "cli", "автоматизация"],
    },
    {
        "slug": "warp",
        "title": "Warp",
        "icon": "🚀",
        "desc": "Терминал на Rust с блоками, AI и workflows",
        "color": "#06b6d4",
        "src": "warp-cheatsheet.md",
        "tags": ["терминал", "ai", "rust", "cli"],
    },
    {
        "slug": "agentic-ai-dev",
        "title": "Агентная разработка с ИИ",
        "icon": "🤝",
        "desc": "Паттерны работы с AI-агентами: ZCode, Claude Code, Cursor",
        "color": "#f59e0b",
        "src": "agentic-ai-dev.md",
        "tags": ["ai", "agentic", "best-practices", "workflow"],
    },
]

SITE_TITLE = "Шпаргалки"
SITE_SUBTITLE = "Горячие клавиши и команды для ежедневной работы"


# ── Утилиты ───────────────────────────────────────────────────────────────
_slug_re = re.compile(r"[^\w\u0400-\u04FF]+", re.UNICODE)

def slugify(text: str, separator: str = "-") -> str:
    """Unicode-aware slug для toc-расширения: (value, separator)."""
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    slug = _slug_re.sub(separator, text).strip(separator)
    return slug or "section"


def md_to_html(md_text: str):
    """Конвертация Markdown → (html, toc_html)."""
    md = markdown.Markdown(
        extensions=[
            "extra",        # tables, fenced_code, abbr, attr_list, def_list, footnotes
            "codehilite",   # подсветка синтаксиса через Pygments
            "toc",          # оглавление
            "admonition",
            "sane_lists",
            "smarty",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "css_class": "highlight",
                "noclasses": False,
            },
            "toc": {
                "permalink": "#",
                "permalink_title": "Ссылка",
                "slugify": slugify,    # ← наш кириллице-дружелюбный slugify
            },
        },
    )
    body = md.convert(md_text)
    toc = md.toc  # готовое оглавление с корректными ссылками на id
    return body, toc


# ── Шаблоны ───────────────────────────────────────────────────────────────
def head_html(title: str, active: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} — {SITE_TITLE}</title>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/pygments.css">
</head>
<body>"""


def card_html(cs: dict) -> str:
    tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in cs["tags"])
    return f"""        <a class="card" href="{cs['slug']}.html" style="--accent:{cs['color']}">
          <div class="card-icon">{cs['icon']}</div>
          <div class="card-body">
            <h3>{html.escape(cs['title'])}</h3>
            <p>{html.escape(cs['desc'])}</p>
            <div class="tags">{tags}</div>
          </div>
          <div class="card-arrow">→</div>
        </a>"""


def index_html() -> str:
    cards = "\n".join(card_html(cs) for cs in CHEATSHEETS)
    return f"""{head_html(SITE_TITLE)}
<header class="hero">
  <div class="hero-inner">
    <h1>📌 {SITE_TITLE}</h1>
    <p class="subtitle">{SITE_SUBTITLE}</p>
    <div class="search">
      <input type="search" id="search" placeholder="🔍 Поиск по {len(CHEATSHEETS)} шпаргалкам…" autocomplete="off">
    </div>
  </div>
</header>

<main class="grid" id="cards">
{cards}
</main>

<footer class="site-footer">
  <p>Сгенерировано из Markdown · {len(CHEATSHEETS)} шпаргалок ·
    <a href="https://yazi-rs.github.io">источники</a> в каждом файле</p>
</footer>

<script src="assets/search.js"></script>
</body>
</html>"""


def page_html(cs: dict) -> str:
    md_text = (SRC_DIR / cs["src"]).read_text(encoding="utf-8")
    body, toc_html = md_to_html(md_text)

    nav_items = "\n".join(
        f'<a href="{c["slug"]}.html" class="nav-item{" active" if c["slug"]==cs["slug"] else ""}">'
        f'<span class="nav-ico">{c["icon"]}</span>{html.escape(c["title"])}</a>'
        for c in CHEATSHEETS
    )

    prev_cs = next((c for c in reversed(CHEATSHEETS) if CHEATSHEETS.index(c) < CHEATSHEETS.index(cs)), None)
    next_cs = next((c for c in CHEATSHEETS if CHEATSHEETS.index(c) > CHEATSHEETS.index(cs)), None)

    prev_html = (f'<a class="pager prev" href="{prev_cs["slug"]}.html">← {html.escape(prev_cs["title"])}</a>'
                 if prev_cs else '<span></span>')
    next_html = (f'<a class="pager next" href="{next_cs["slug"]}.html">{html.escape(next_cs["title"])} →</a>'
                 if next_cs else '<span></span>')

    return f"""{head_html(cs["title"])}
<div class="layout">
  <aside class="sidebar">
    <a href="index.html" class="brand">📌 {SITE_TITLE}</a>
    <nav class="nav">
{nav_items}
    </nav>
  </aside>

  <main class="content">
    <article>
{body}
    </article>
    <nav class="pagination">
      {prev_html}
      {next_html}
    </nav>
  </main>

  <aside class="toc">
    <details open>
      <summary>📑 Оглавление</summary>
      <div class="toc-list">
{toc_html}
      </div>
    </details>
  </aside>
</div>

<button class="back-top" id="backTop" aria-label="Наверх">↑</button>

<script src="assets/search.js"></script>
<script src="assets/page.js"></script>
</body>
</html>"""


# ── Главный цикл ──────────────────────────────────────────────────────────
def build():
    # Очистка
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Pygments CSS (светлая тёплая тема под бумажную палитру)
    formatter = HtmlFormatter(style="gruvbox-light", nobackground=True)
    pyg_css = formatter.get_style_defs(".highlight")
    # добавить скролл для длинных блоков
    pyg_css += "\n.highlight pre { overflow-x: auto; }"
    (ASSETS_DIR / "pygments.css").write_text(pyg_css, encoding="utf-8")

    # Копируем статические ассеты (CSS, JS) из assets/ рядом с build.py
    src_assets = ROOT / "assets"
    for asset in src_assets.iterdir():
        if asset.is_file():
            shutil.copy2(asset, ASSETS_DIR / asset.name)
            print(f"✓ assets/{asset.name}")

    # Главнаscrf index
    (OUT_DIR / "index.html").write_text(index_html(), encoding="utf-8")
    print(f"✓ index.html")

    # Страницы
    for cs in CHEATSHEETS:
        (OUT_DIR / f"{cs['slug']}.html").write_text(page_html(cs), encoding="utf-8")
        print(f"✓ {cs['slug']}.html  ({cs['title']})")

    print(f"\n✅ Готово. Сайт в: {OUT_DIR}")
    print(f"   Открыть: file://{OUT_DIR}/index.html")


if __name__ == "__main__":
    build()

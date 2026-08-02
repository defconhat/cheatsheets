# 🤖 ZCode — шпаргалка

> **ZCode** — интерактивный AI-агент для кодинга в терминале. Работает с кодом через инструменты (Read/Write/Edit/Bash/Agent/…), поддерживает слэш-команды, скиллы, плагины, MCP, хуки и память сессий.
> Бинарник: `/usr/sbin/zcode`. Конфиг: `~/.zcode/`.

---

## 🚀 Запуск

```bash
zcode                       # запустить в текущей директории
zcode /path/to/project      # открыть конкретный проект
zcode --help                # справка CLI
```

При старте ZCode:
1. Загружает пользовательские настройки из `~/.zcode/AGENTS.md`.
2. Ищет `AGENTS.md` в проекте (от текущей директории вверх до корня репозитория).
3. Подключает MCP-серверы (user + workspace scope — авто-коннект).
4. Активирует скиллы/команды/хуки из `~/.zcode` и плагинов.

---

## ⌨️ Слэш-команды (вводятся в чат, начинаются с `/`)

| Команда | Назначение |
|---|---|
| `/help` | Справка по доступным командам |
| `/init` | Создать/обновить `AGENTS.md` для текущего проекта |
| `/clear` | Очистить контекст текущей сессии (начать заново) |
| `/compact` | **Сжать** длинную сессию в summary (контекст сохраняется, но сокращается) |
| `/memory` | Показать/редактировать сохранённую память проекта |
| `/remember <fact>` | Сохранить факт в память проекта |
| `/resume` | Продолжить прошлую сессию (`sess_*` ID) |
| `/agents` | Управление субагентами |
| `/mcp` | Статус MCP-серверов (подключённые/упавшие) |
| `/permissions` | Настройки разрешений инструментов |
| `/model` | Сменить модель (если подключено несколько провайдеров) |
| `/config` | Открыть конфигурацию |
| `/cost` | Потраченные токены/деньги за сессию |
| `/export` | Экспорт сессии |
| `/review` | Ревью изменений (часто из плагина) |
| `/<skill-name>` | Запустить конкретный скилл напрямую |

> Точный список зависит от версии и установленных плагинов. Ввод `/` показывает автодополнение.

---

## 📁 Структура конфигурации

```
~/.zcode/
├── AGENTS.md              # пользовательские инструкции (для всех проектов)
├── cli/
│   ├── config.json        # MCP, hooks, plugins enable/disable
│   ├── agents/            # сессии (sess_<uuid>/)
│   ├── commands/          # пользовательские слэш-команды (.md)
│   ├── skills/            # пользовательские скиллы
│   ├── plugins/
│   │   ├── cache/         # установленные плагины (из marketplace)
│   │   ├── marketplaces/  # добавленные маркетплейсы
│   │   └── known_marketplaces.json
│   ├── memories/          # память по проектам
│   ├── rollout/           # логи выполнения
│   ├── log/               # системные логи
│   └── exec/              # runtime
└── v2/
    ├── config.json        # провайдеры моделей
    ├── setting.json       # UI/поведение (locale, zoom, indexing…)
    ├── credentials.json   # API-ключи (зашифрованы)
    └── tasks-index.sqlite # индекс задач
```

### Workspace scope (в репозитории)
```
<repo>/
├── AGENTS.md              # инструкции проекта (версионируются с командой)
├── .zcode/
│   ├── config.json        # MCP/hooks для проекта
│   ├── commands/          # команды проекта
│   └── skills/            # скиллы проекта
└── .agents/               # совместимость с Claude/Codex/Cursor
    ├── mcp.json           # MCP-серверы (fallback)
    ├── commands/
    └── skills/
```

---

## 🎯 Пять типов расширений

| Ресурс | Форма | Где (user) | Где (workspace) |
|---|---|---|---|
| **Skills** | папка + `SKILL.md` | `~/.zcode/skills/` | `<repo>/.zcode/skills/` |
| **Commands** | `.md` файл | `~/.zcode/commands/` | `<repo>/.zcode/commands/` |
| **MCP** | JSON-объект | `~/.zcode/cli/config.json` → `mcp.servers` | `<repo>/.zcode/config.json` → `mcp.servers` |
| **Hooks** | объект в config | `~/.zcode/cli/config.json` → `hooks` | `<repo>/.zcode/config.json` → `hooks` |
| **Plugins** | папка + `plugin.json` | из marketplace | — |

### Совместимость с `.agents/`
ZCode читает `.agents/` как fallback — полезно для общих скиллов с Claude/Codex/Cursor.
Порядок в каждом scope: `.zcode` → `.agents`.

---

## 🔌 MCP (Model Context Protocol)

MCP-серверы дают агенту внешние инструменты (БД, API, браузер, файлы и т.д.).

### Добавление в `~/.zcode/cli/config.json`
```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
      },
      "postgres": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres",
                 "postgresql://user:pass@localhost/db"]
      }
    }
  }
}
```

### Поведение
- **Все scope авто-подключаются** при старте сессии (user, workspace, plugin).
- User переопределяет workspace при конфликте имён.
- Инструменты MCP появляются как `mcp__<server>__<tool>`.
- Статус: **Settings → MCP** или команда `/mcp`.
- ⚠️ Открывайте только доверенные проекты — workspace MCP подключается автоматически.

### Не подключается?
Использовать скилл **`/diagnosing-mcp`** — он ищет причину (bad command, timeout, untrusted).

---

## 🪝 Hooks

7 событий:
| Событие | Когда срабатывает |
|---|---|
| `SessionStart` | Старт сессии |
| `UserPromptSubmit` | Пользователь отправил промпт |
| `PreToolUse` | Перед вызовом инструмента |
| `PermissionRequest` | Запрос разрешения |
| `PostToolUse` | После успешного вызова |
| `PostToolUseFailure` | После ошибки инструмента |
| `Stop` | Агент завершил ответ |

### Конфигурация
```json
{
  "hooks": {
    "enabled": true,
    "SessionStart": [
      {
        "matcher": "*",
        "command": "echo 'session started' >> /tmp/zcode.log"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "echo 'Bash call: $TOOL_INPUT' >> /tmp/zcode.log"
      }
    ]
  }
}
```

> ⚠️ **Важно:** хуки из config требуют `hooks.enabled: true`. Хуки из плагинов включают runner автоматически.

### Не срабатывает хук?
Скилл **`/diagnosing-hooks`** — проверит matcher, executable, расширение файла.

---

## 🧩 Plugins

Плагин = папка с `.zcode-plugin/plugin.json`. Может содержать skills, commands, hooks, MCP, agents.

### Минимальный `plugin.json`
```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "skills": ["skills/my-skill"],
  "commands": ["commands/my-command.md"]
}
```

### Управление
- **Settings → Plugin Management** → вкладки **Installed** / **Discover**.
- Добавить marketplace: кнопка **`+`** на Discover (GitHub repo / Git URL / локальная папка / файл).
- Built-in плагин можно отключить, но не удалить.
- Состояние вкл/выкл хранится в `~/.zcode/cli/config.json` → `plugins`.

### Built-in плагины (поставляются с ZCode)
| Плагин | Что даёт |
|---|---|
| **zcode-guide** | Скиллы самодиагностики конфигурации |
| **document-skills** | Создание/правка DOCX и PDF |
| **skill-creator** | Создание новых скиллов |
| **android-emulator** | Разработка под Android |
| **ios-simulator** | Разработка под iOS |
| **restore-legacy-sessions** | Восстановление старых сессий |

---

## 📝 AGENTS.md — инструкции

Текстовый файл с правилами поведения агента в проекте. Загружается в контекст.

### Когда использовать
- **User scope** (`~/.zcode/AGENTS.md`): личные дефолты (язык ответов, стиль ревью).
- **Workspace scope** (`<repo>/AGENTS.md`): архитектура, конвенции коммитов, тесты — версионируется с кодом.

### Порядок загрузки
1. Сначала `~/.zcode/AGENTS.md` (базовые правила).
2. Затем `<repo>/AGENTS.md` (может сужать/переопределять).

### Пример `AGENTS.md` для проекта
```markdown
# Правила проекта

## Язык
- Отвечать на русском.

## Коммиты
- Формат: `feat:`, `fix:`, `docs:`, `refactor:`.
- Не больше 50 символов в заголовке.

## Тесты
- Перед PR обязательно запустить `pytest tests/`.
- Покрытие новых функций — не ниже 80%.

## Архитектура
- Слои: api → service → repository.
- Не обращаться к БД из api-слоя напрямую.
```

---

## 🧠 Память (Memory)

ZCode хранит сводку по проекту между сессиями.

```
~/.zcode/cli/memories/projects/<project-id>/
├── memory_summary.md      # краткая сводка (загружается всегда)
├── MEMORY.md              # индекс тем
├── topics/*.md            # типизированные памяти
└── rollout_summaries/*.md # детальные саммари
```

### Команды
- `/memory` — посмотреть текущую память.
- `/remember <fact>` — сохранить факт.
- В сессии: «запомни, что мы используем порт 4000» → агент добавит в память.

### Принципы (как агент использует память)
- Опциональна — не истина, а контекст.
- Секреты не раскрывать.
- Широкие сканы избегать — лучше продолжить без неё.

---

## 🛠️ Инструменты агента

| Инструмент | Назначение |
|---|---|
| **Read** | Чтение файла (или картинки) |
| **Write** | Создание/перезапись файла |
| **Edit** | Точная замена строк в файле |
| **Bash** | Выполнение команды в шелле |
| **Agent** | Запуск субагента для подзадачи |
| **TodoWrite** | Управление списком задач сессии |
| **WebFetch** | Загрузка URL + ответ на промпт |
| **WebSearch** | Поиск в интернете |
| **EnterPlanMode** | Переход в режим планирования |
| **ExitPlanMode** | Показ плана пользователю для одобрения |
| **AskUserQuestion** | Вопрос к пользователю при развилке |
| **TaskStop** | Остановка фоновой задачи |
| **SendMessage** | Сообщение другому локальному агенту |
| **ReadSessionContext** | Чтение контекста другой сессии |

---

## 🎭 Режимы разрешений

ZCode работает за permission-модом, выбранным пользователем:
- **Ask** — спрашивать перед каждым действием.
- **Auto-edit** — авто-редактирование файлов, спрашивать внешние действия.
- **Plan** — только планирование, без изменений.
- **Yolo** — всё автоматически (опасно ⚠️).

Хуки могут перехватывать вызовы инструментов (`PreToolUse`).

---

## 🩺 Самодиагностика (встроенные скиллы)

Если что-то не работает — вызови соответствующий скилл:

| Симптом | Скилл |
|---|---|
| MCP не подключается, инструменты пропали | `/diagnosing-mcp` |
| Скилл не находится/не триггерится | `/diagnosing-skills` |
| Слэш-команда пропала/не подставляет аргументы | `/diagnosing-commands` |
| Хук не срабатывает | `/diagnosing-hooks` |
| Плагин не виден/не ставится | `/diagnosing-plugins` |

Каждый скилл ведёт по сценарию: симптом → причина → проверка → фикс (и для пользователя через UI, и для агента через файлы).

---

## ⚡ Частые сценарии

### Добавить свой скилл
```bash
mkdir -p ~/.zcode/skills/my-skill
cat > ~/.zcode/skills/my-skill/SKILL.md <<'EOF'
---
name: my-skill
description: Запускать, когда пользователь просит сделать X
---

# My Skill

Инструкции агенту, что делать при срабатывании.
EOF
```

### Добавить свою слэш-команду
```bash
mkdir -p ~/.zcode/commands
cat > ~/.zcode/commands/deploy.md <<'EOF'
---
description: Задеплоить текущий проект
---

Запусти `make build && make deploy` и проверь логи на ошибки.
EOF
```
Теперь доступна как `/deploy`.

### Подключить PostgreSQL через MCP
Добавить в `~/.zcode/cli/config.json`:
```json
{
  "mcp": {
    "servers": {
      "postgres": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres",
                 "postgresql://user:pass@localhost:5432/mydb"]
      }
    }
  }
}
```
Перезапустить ZCode → `/mcp` проверить статус.

### Продолжить прерванную сессию
```bash
ls ~/.zcode/cli/agents/    # найти sess_<uuid>
```
В чате: `/resume` → выбрать нужную.

---

## 🆚 ZCode vs Claude Code vs Codex vs Cursor

| Что | ZCode | Claude Code | Codex | Cursor |
|---|---|---|---| standalone |
| Формат | standalone CLI | CLI | CLI | IDE |
| Скиллы/команды | `.zcode` + `.agents` | `.claude` | `.codex` | встроенные |
| MCP | ✅ авто-коннект | ✅ | ✅ | ⚠️ |
| Хуки (7 событий) | ✅ | ✅ | ⚠️ | ❌ |
| Память сессий | ✅ (`sess_*`) | ✅ | ⚠️ | ⚠️ |
| Совместимость | `.agents/` fallback | родной `.claude` | родной `.codex` | свой формат |

> ZCode читает `.agents/` для совместимости — скиллы из `~/.agents/skills/` работают одновременно в Claude Code, Codex и ZCode.

---

## 🔗 Источники

- Установленные плагины: `~/.zcode/cli/plugins/cache/zcode-plugins-official/`
- Гайд по конфигурации: скилл `zcode-configuration-guide`
- Диагностика: скиллы `diagnosing-*` (mcp, skills, commands, hooks, plugins)
- Бинарник: `/usr/sbin/zcode` (`zcode --help`)

# 💻 VS Code — шпаргалка по горячим клавишам и настройке

> **Visual Studio Code** (VS Code) — бесплатный редактор кода от Microsoft.
> Документация: https://code.visualstudio.com/docs

---

## 🔑 Главные сочетания

> Обозначение: `Ctrl` (Windows/Linux), `Cmd` (macOS).

### Command Palette (главное!)
| Клавиша | Действие |
|---|---|
| `Ctrl+Shift+P` / `Cmd+Shift+P` | **Command Palette** — поиск команд |
| `Ctrl+P` / `Cmd+P` | Быстрый поиск файлов |
| `Ctrl+Shift+O` | Перейти к символу в файле |
| `Ctrl+G` | Перейти к строке |
| `Ctrl+Tab` | Переключение вкладок |
| `Ctrl+,` | Открыть настройки |

> 💡 Command Palette — ваше всё. Забыли шорткат? Откройте палитру и начните печатать.

---

## 📁 Файлы и редактирование

### Базовое редактирование
| Клавиша | Действие |
|---|---|
| `Ctrl+S` | Сохранить |
| `Ctrl+Shift+S` | Сохранить как |
| `Ctrl+N` | Новый файл |
| `Ctrl+O` | Открыть файл |
| `Ctrl+W` / `Ctrl+F4` | Закрыть вкладку |
| `Ctrl+Shift+T` | Восстановить закрытую вкладку |
| `Ctrl+Z` | Отменить |
| `Ctrl+Y` / `Ctrl+Shift+Z` | Вернуть (redo) |
| `Ctrl+C` (без выделения) | Копировать строку |
| `Ctrl+X` (без выделения) | Вырезать строку |
| `Ctrl+V` | Вставить |
| `Ctrl+Shift+K` | Удалить строку |
| `Alt+↑` / `Alt+↓` | Переместить строку вверх/вниз |
| `Shift+Alt+↓` / `Shift+Alt+↑` | Дублировать строку |
| `Ctrl+Enter` | Новая строка ниже |
| `Ctrl+Shift+Enter` | Новая строка выше |
| `Ctrl+]` / `Ctrl+[` | Отступ вправо/влево |
| `Ctrl+/` | Закомментировать/раскомментировать |
| `Shift+Alt+A` | Блочный комментарий |
| `Ctrl+K Ctrl+C` | Закомментировать строку |
| `Ctrl+K Ctrl+U` | Раскомментировать строку |
| `Home` / `End` | В начало/конец строки |
| `Ctrl+Home` / `Ctrl+End` | В начало/конец файла |

### Мульти-курсор
| Клавиша | Действие |
|---|---|
| `Alt+Click` | Добавить курсор |
| `Ctrl+Alt+↑` / `Ctrl+Alt+↓` | Курсор в каждой строке выше/ниже |
| `Ctrl+D` | Выделить следующее совпадение |
| `Ctrl+Shift+L` | Выделить ВСЕ совпадения |
| `Ctrl+K Ctrl+D` | Пропустить текущее (следующее) |
| `Shift+Alt+I` | Курсор в конце каждой строки выделения |
| `Ctrl+U` | Отменить последний курсор |
| `Alt+→` / `Alt+←` | По словам |
| `Ctrl+Shift+\` | К парной скобке |
| `Ctrl+L` | Выделить строку |

### Выделение
| Клавиша | Действие |
|---|---|
| `Shift+→/←` | Посимвольно |
| `Ctrl+Shift+→/←` | По словам |
| `Shift+↓/↑` | По строкам |
| `Ctrl+A` | Выделить всё |
| `Ctrl+Shift+Home/End` | До начала/конца файла |
| `Ctrl+K Ctrl+B` | Расширить выделение |

---

## 🔍 Поиск и замена

| Клавиша | Действие |
|---|---|
| `Ctrl+F` | Поиск в файле |
| `Ctrl+H` | Замена |
| `F3` / `Enter` | Следующее совпадение |
| `Shift+F3` / `Shift+Enter` | Предыдущее |
| `Alt+Enter` | Выделить все совпадения (мультикурсор) |
| `Ctrl+Shift+F` | Поиск по всем файлам |
| `Ctrl+Shift+H` | Замена по всем файлам |
| `Ctrl+D` | Выделить следующее + мультикурсор |

### Опции поиска
| Опция | Что |
|---|---|
| `Aa` | Case-sensitive (учитывать регистр) |
| `\b` | Whole word (целое слово) |
| `.*` | Regex |
| `↕` | Preserve case в замене |
| `ab|ac` | Заменить в выделении |

---

## 🗂️ Боковая панель и навигация

| Клавиша | Действие |
|---|---|
| `Ctrl+B` | Скрыть/показать боковую панель |
| `Ctrl+Shift+E` | Explorer (файлы) |
| `Ctrl+Shift+F` | Поиск |
| `Ctrl+Shift+G` | Source Control (Git) |
| `Ctrl+Shift+D` | Run and Debug |
| `Ctrl+Shift+X` | Extensions |
| `Ctrl+Shift+U` | Output panel |
| `Ctrl+Shift+M` | Problems (ошибки) |
| `Ctrl+Shift+J` | Раскрыть/свернуть поиск |
| `Ctrl+\` | Разделить редактор |
| `Ctrl+K Ctrl+→/←` | Перейти в соседнюю группу |
| `Ctrl+1/2/3` | Фокус на группу 1/2/3 |
| `Ctrl+Shift+PageUp` | Вкладку влево |
| `Ctrl+Shift+PageDown` | Вкладку вправо |
| `Ctrl+K Ctrl+Shift+Enter` | Закрепить вкладку |
| `Ctrl+Shift+P` → "View: Toggle Zen Mode" | Дзен-режим |
| `F11` | Полноэкранный режим |

---

## 🖥️ Терминал и панель

| Клавиша | Действие |
|---|---|
| `Ctrl+`` ` ` | Открыть/закрыть терминал |
| `Ctrl+Shift+`` ` ` | Новый терминал |
| `Ctrl+Shift+C` | Разделить терминал |
| `Ctrl+Shift+M` | Переключить фокус (терминал ↔ редактор) |
| `Ctrl+Shift+Backspace` | Удалить терминал |
| `Ctrl+Shift+D` (в терминале) | Закрыть |
| `Alt+Z` | Перенос слов в терминале |

### Встроенный терминал
- Поддержка bash/zsh/fish/PowerShell/cmd.
- Интеграция с shell: `code .` открывает VS Code в текущем каталоге.
- Профили терминала: `terminal.integrated.profiles.linux`.
- Дефолтный: `terminal.integrated.defaultProfile.linux`.

---

## 🌐 Git-интеграция

| Клавиша / Команда | Действие |
|---|---|
| `Ctrl+Shift+G` | Source Control view |
| В поле сообщения + `Ctrl+Enter` | Commit |
| `…` → Commit All | Закоммитить всё |
| `…` → Discard All Changes | Отменить изменения |
| `…` → Stash Changes | Спрятать изменения |
| Клик на файле в Changes | Diff view |
| `Stage` / `Unstage` | Добавить/убрать из staging |
| `git blame` (встроенный) | Навести на строку |
| Hover → Git lens | Кто изменил строку |
| `Ctrl+Shift+G G` | Откройте Git Graph (если установлен) |

### Встроенные git-команды
- Command Palette → `Git: Clone`, `Git: Pull`, `Git: Push`.
- `Git: Checkout To...` — сменить ветку.
- `Git: Commit` — закоммитить.
- `Git: Stash`, `Git: Pop Stash`.

---

## 🐛 Дебаггер

| Клавиша | Действие |
|---|---|
| `F5` | Start debugging |
| `Shift+F5` | Stop |
| `Ctrl+Shift+F5` | Restart |
| `F9` | Toggle breakpoint |
| `F10` | Step over |
| `F11` | Step into |
| `Shift+F11` | Step out |
| `F5` | Continue |
| Hover по переменной | Посмотреть значение |
| `Watch` panel | Добавить выражение |
| `Call Stack` | Стек вызовов |

### launch.json
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

---

## 🎨 Emmet (HTML/CSS)

| Abbreviation | Результат |
|---|---|
| `!` | HTML5 boilerplate |
| `div.class` | `<div class="class"></div>` |
| `div#id` | `<div id="id"></div>` |
| `ul>li*3` | `<ul>` с 3 `<li>` |
| `a:link` | `<a href="http://"></a>` |
| `p*2` | два `<p>` |
| `nav>ul>li*5>a` | Вложенная структура |
| `.wrapper>h1+p*3` | div + h1 + 3 p |
| `m10` | `margin: 10px;` |
| `p10-20` | `padding: 10px 20px;` |
| `w100p` | `width: 100%;` |
| `d:f` | `display: flex;` |

Emmet работает в HTML, CSS, JSX, Vue, Svelte.

---

## 🔤 Сниппеты

### Свои сниппеты
`Ctrl+Shift+P` → `Preferences: Configure User Snippets` → выбор языка.

```json
// python.json
{
  "Print": {
    "prefix": "pp",
    "body": [
      "print(f\"${1:var} = {$1}\")"
    ],
    "description": "Debug print"
  },
  "Main": {
    "prefix": "main",
    "body": [
      "if __name__ == \"__main__\":",
      "    ${1:main()}"
    ]
  }
}
```

Переменные в сниппетах:
- `${1:default}` — placeholder с значением по умолчанию.
- `${2:second}` — следующий курсор.
- `$0` — финальная позиция курсора.
- `${1|opt1,opt2,opt3|}` — выбор из списка.
- `$CLIPBOARD`, `$TM_FILENAME`, `$CURRENT_YEAR` и т.д.

---

## ⚙️ Настройки

### settings.json
`Ctrl+,` → иконка `Open Settings (JSON)` в правом верхнем углу.

```json
{
  // Общее
  "editor.fontSize": 14,
  "editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "editor.minimap.enabled": false,
  "editor.wordWrap": "on",
  "editor.stickyScroll.enabled": true,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": "active",
  "editor.inlineSuggest.enabled": true,

  // Files
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/__pycache__": true
  },
  "files.associations": {
    "*.md": "markdown",
    "*.json": "jsonc"
  },
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  // Search
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.git": true
  },

  // Terminal
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.fontFamily": "JetBrains Mono",
  "terminal.integrated.scrollback": 10000,
  "terminal.integrated.defaultProfile.linux": "zsh",

  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },

  // Тема
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "workbench.startupEditor": "none",
  "workbench.editor.labelFormat": "short",
  "window.title": "${dirty}${activeEditorShort}${separator}${rootName}",
  "window.zoomLevel": 1,

  // Git
  "git.enableSmartCommit": true,
  "git.confirmSync": false,
  "git.autofetch": true,
  "gitlens.currentLine.enabled": true,

  // Расширения
  "editor.linkedEditing": true,        // менять парные теги одновременно
  "liveServer.settings.donotShowInfoMsg": true,
  "errorLens.enabled": true
}
```

### keybindings.json
`Ctrl+K Ctrl+S` → иконка открытия.

```json
[
  {
    "key": "ctrl+shift+up",
    "command": "editor.action.copyLinesUpAction",
    "when": "editorTextFocus && !editorReadonly"
  },
  {
    "key": "ctrl+shift+down",
    "command": "editor.action.copyLinesDownAction",
    "when": "editorTextFocus && !editorReadonly"
  },
  {
    "key": "ctrl+e",
    "command": "workbench.action.quickOpen"
  }
]
```

---

## 🧩 Must-have расширения

### Общее
| Расширение | Назначение |
|---|---|
| **Prettier** | Форматирование (JS/TS/CSS/HTML/MD/YAML) |
| **ESLint** | Линтер JS/TS |
| **EditorConfig** | Уважать `.editorconfig` |
| **Path Intellisense** | Автодополнение путей |
| **Error Lens** | Ошибки прямо в строке |
| **Material Icon Theme** | Иконки файлов |
| **One Dark Pro** / **Tokyo Night** | Темы |
| **TODO Highlight** | Подсветка TODO/FIXME |
| **TODO Tree** | Дерево TODO |
| **Code Spell Checker** | Проверка орфографии |

### Python
| Расширение | Назначение |
|---|---|
| **Python** | Официальное (Microsoft) |
| **Pylance** | Type checker (быстрый) |
| **Ruff** | Линтер+форматер (рекомендуется!) |
| **Black Formatter** | Альтернативный форматер |
| **Jupyter** | Ноутбуки .ipynb |

### Git
| Расширение | Назначение |
|---|---|
| **GitLens** | Blame, история, многофункциональный |
| **Git Graph** | Визуализация графа коммитов |
| **GitHub Pull Requests** | PR из VS Code |
| **GitLab Workflow** | GitLab интеграция |

### Веб
| Расширение | Назначение |
|---|---|
| **Live Server** | Локальный сервер с автообновлением |
| **Tailwind CSS IntelliSense** | Автодополнение Tailwind |
| **Auto Rename Tag** | Переименование парных тегов |
| **CSS Peek** | Переход к CSS-определению |

### Инструменты
| Расширение | Назначение |
|---|---|
| **Docker** | Управление контейнерами |
| **Remote - SSH** | Разработка на удалённом сервере |
| **Remote - Containers** | Dev Containers |
| **Database Client** | JDBC (MySQL/PostgreSQL) |
| **REST Client** | `.http` файлы |
| **Thunder Client** | Postman внутри VS Code |
| **YAML** | Поддержка YAML + схемы |
| **Markdown All in One** | Markdown-помощники |
| **Markdown Preview Enhanced** | Расширенное превью |
| **Draw.io Integration** | Диаграммы |
| **Ascii Tree Generator** | Деревья каталогов |

### Remote Development
```bash
# Установить pack
code --install-extension ms-vscode-remote.vscode-remote-extensionpack
```
- **Remote - SSH** — редактировать файлы на сервере.
- **Remote - Containers** — dev в Docker-контейнере.
- **Remote - WSL** — Windows Subsystem for Linux.
- **Remote - Tunnels** — удалённый доступ через туннели.

---

## ⚙️ tasks.json и launch.json

### tasks.json — автоматизация
`.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Python",
      "type": "shell",
      "command": "python",
      "args": ["${file}"],
      "group": {"kind": "build", "isDefault": true},
      "problemMatcher": []
    },
    {
      "label": "Test",
      "type": "shell",
      "command": "pytest",
      "group": "test"
    }
  ]
}
```
`Ctrl+Shift+B` — запустить build task.

---

## 🌍 Пользовательская синхронизация

**Settings Sync** — синхронизация настроек между машинами через GitHub/Microsoft.

`Ctrl+Shift+P` → `Settings Sync: Turn On`.

Синхронизирует:
- Настройки (`settings.json`)
- Горячие клавиши (`keybindings.json`)
- Расширения
- Сниппеты
- UI состояние
- Профили

---

## 🚀 CLI: `code`

```bash
# Установить команду `code` в PATH
# (Cmd+Shift+P → "Shell Command: Install 'code' command in PATH")

# Использование
code .                              # открыть текущий каталог
code file.py                        # открыть файл
code -r file.py                     # открыть в текущем окне
code -n .                           # в новом окне
code -d file1 file2                 # diff
code -g file.py:10:5                # перейти к строке 10, колонке 5
code --install-extension ms-python.python   # установить расширение
code --list-extensions              # список расширений
code --uninstall-extension name
code --diff a.txt b.txt             # сравнить файлы
code -w file.txt                    # ждать закрытия (для git)
```

### Экспорт расширений
```bash
code --list-extensions > extensions.txt
# Установка на новой машине:
cat extensions.txt | xargs -L1 code --install-extension
```

---

## 🪤 Частые ошибки

1. **Расширения вместо конфигурации** — не ставьте 100 расширений.
2. **Форматирование** — настройте `formatOnSave` под каждый язык.
3. **`code .` не работает** — установите shell-команду.
4. **Sync включает мусор** — отключите рабочие расширения в Settings Sync.
5. **Тяжёлые расширения** — Prettier, ESLint замедляют большие проекты.
6. **Terminal профиль** — задайте правильный shell (zsh, not bash).
7. **`.vscode/` в репозитории** — некоторые настройки можно шарить, секреты — нельзя.
8. **Python interpreter** — выберите правильный в Command Palette.
9. **Забыли `gitlens`** — самая полезная git-интеграция.
10. **Auto Save** — может мешать автосборке.

---

## 🔗 Полезные ссылки

- Документация: https://code.visualstudio.com/docs
- Hotkeys (Windows): https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf
- Hotkeys (macOS): https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf
- Hotkeys (Linux): https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf
- Marketplace: https://marketplace.visualstudio.com
- Awesome VSCode: https://github.com/viatsko/awesome-vscode
- My top extensions: https://vscode.pro

---

## 💡 Полезные советы

1. **Command Palette** (`Ctrl+Shift+P`) — узнавайте команды по имени.
2. **Quick Open** (`Ctrl+P`) — быстрее, чем навигация по дереву.
3. **Settings Sync** — один раз настройте, и на всех машинах одинаково.
4. **`code .`** — открывает проект в текущем каталоге.
5. **`formatOnSave`** — настройте, чтобы код всегда был отформатирован.
6. **`editor.linkedEditing`** — менять парные HTML-теги одновременно.
7. **Snippets** — для часто повторяющегося кода.
8. **Emmet** — мощно для HTML/CSS (`!`, `div.class`).
9. **Мультикурсор** (`Ctrl+D`, `Alt+Click`) — для массовых правок.
10. **Zen Mode** — для фокусировки (двойной `Esc` для выхода).
11. **Terminal + `code`** — интеграция shell.
12. **Remote - SSH** — редактируйте код на сервере как локально.
13. **`.vscode/settings.json`** в проекте — для командных настроек.
14. **Profiles** — разные наборы расширений для разных задач.
15. **Dev Containers** — изолированная среда разработки в Docker.

---

*Сгенерировано как шпаргалка. VS Code огромен —
углубляйтесь через https://code.visualstudio.com/docs и `Ctrl+Shift+P`*

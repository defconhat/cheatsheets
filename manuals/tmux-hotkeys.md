# 🪟 Tmux — шпаргалка по горячим клавишам и командам

> **tmux** — терминальный мультиплексор: несколько окон/панелей в одном терминале,
> сессии переживают закрытие терминала.
> Дом: https://github.com/tmux/tmux · Мануал: `man tmux`

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **server** | Фоновый процесс tmux, хранит все сессии |
| **session** | Независимый набор окон (то, что «переживает» отключение) |
| **window** | Вкладка внутри сессии (как вкладка браузера) |
| **pane** | Область внутри окна (сплит) |
| **prefix** | Клавиша-модификатор перед командой. По умолчанию **`Ctrl-b`** |
| **attach** | Подключиться к существующей сессии |

Далее обозначение: **`C-b`** = нажмите `Ctrl-b`, отпустите, затем следующую клавишу.

---

## 🚀 Запуск и сессии

| Команда / Клавиша | Действие |
|---|---|
| `tmux` | Запустить новую сессию |
| `tmux new -s имя` | Новая сессия с именем |
| `tmux ls` | Список сессий |
| `tmux a` / `tmux attach` | Подключиться к последней сессии |
| `tmux a -t имя` | Подключиться к конкретной сессии |
| `tmux kill-session -t имя` | Убить сессию |
| `tmux kill-server` | Убить все сессии (весь сервер) |
| `tmux source ~/.tmux.conf` | Перечитать конфиг |
| `C-b d` | Отключиться от сессии (detach) |
| `C-b s` | Список сессий (интерактивно) |
| `C-b $` | Переименовать текущую сессию |
| `C-b (` / `C-b )` | Предыдущая / следующая сессия |
| `C-b L` | Переключиться на последнюю активную сессию |

---

## 🖼️ Окна (windows)

| Клавиша | Действие |
|---|---|
| `C-b c` | Создать окно |
| `C-b ,` | Переименовать окно |
| `C-b &` | Закрыть окно (с подтверждением) |
| `C-b n` / `C-b p` | Следующее / предыдущее окно |
| `C-b 0..9` | Перейти к окну №0..9 |
| `C-b w` | Список окон (интерактивно) |
| `C-b f` | Найти окно по заголовку/содержимому |
| `C-b .` | Перейти к окну по номеру |
| `C-b M-n` / `C-b M-p` | Следующее/пред. окно с alert'ом |
| `swap-window -t -1` (в prompt) | Поменять окна местами |

---

## ▦ Панели (panes — сплиты)

| Клавиша | Действие |
|---|---|
| `C-b %` | Разделить по вертикали (right) |
| `C-b "` | Разделить по горизонтали (below) |
| `C-b o` | Следующая панель (по кругу) |
| `C-b q` | Показать номера панелей (затем цифру — перейти) |
| `C-b ↑↓←→` | Перейти к панели в направлении |
| `C-b {` / `C-b }` | Поменять панели местами |
| `C-b x` | Закрыть панель (с подтверждем) |
| `C-b z` | Zoom (на весь экран / обратно) |
| `C-b Space` | Следующий layout (раскладка панелей) |
| `C-b !` | Вынести панель в отдельное окно |
| `C-b ;` | Последняя активная панель |
| `Resize: `C-b Ctrl-↑↓←→` | Изменить размер панели (зажав prefix) |
| `resize-pane -L 10` (в prompt) | На 10 влево |

### Layout'ы (по `C-b Space`)
- **even-horizontal** — все в ряд слева направо
- **even-vertical** — все в столбик
- **main-horizontal** — большое сверху, мелкие внизу
- **main-vertical** — большое слева, мелкие справа
- **tiled** — сетка

---

## 📜 Копирование и режим прокрутки

По умолчанию режим копирования — **emacs-стиль** (можно поменять на vi в конфиге).

| Клавиша | Действие |
|---|---|
| `C-b [` | Войти в режим копирования (copy mode) |
| `C-b PgUp` | То же (сразу прокрутка вверх) |
| В copy mode: | |
| `↑ ↓` / `PgUp PgDn` | Перемещение |
| `Ctrl-u` / `Ctrl-d` | Пол-страницы |
| `Ctrl-b` / `Ctrl-f` | Страница |
| `g` / `G` | В начало / конец буфера |
| `/` | Поиск вперёд |
| `?` | Поиск назад |
| `n` / `N` | Следующее / предыдущее совпадение |
| `Space` (emacs) / `v` (vi) | Начать выделение |
| `Enter` | Скопировать выделение |
| `q` / `Esc` | Выйти из copy mode |
| `C-b ]` | Вставить из буфера tmux |
| `C-b =` | Список буферов (выбрать) |
| `C-b #` | Список буферов |
| `save-buffer <file>` (в prompt) | Сохранить буфер в файл |

### Копирование в системный буфер обмена
Нужна интеграция с `xclip`/`wl-copy`. Пример для Wayland в `~/.tmux.conf`:
```tmux
# Копировать выделение в буфер Wayland
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "wl-copy"
bind-key -T copy-mode    y send-keys -X copy-pipe-and-cancel "wl-copy"
```

---

## 🎛️ Prompt и команды tmux (после `C-b :`)

| Команда | Действие |
|---|---|
| `:source ~/.tmux.conf` | Перечитать конфиг |
| `:new-session -s имя` | Новая сессия |
| `:new-window -n имя` | Новое окно |
| `:split-window -h` | Сплит вертикальный |
| `:split-window -v` | Сплит горизонтальный |
| `:kill-session` | Убить сессию |
| `:kill-window` | Убить окно |
| `:kill-pane` | Убить панель |
| `:resize-pane -L 10` | Ресайз влево на 10 |
| `:move-window -t 2` | Переместить окно на индекс 2 |
| `:swap-window -t -1` | Сдвинуть окно влево |
| `:clock-mode` | Часы (большие) |
| `:clear-history` | Очистить историю прокрутки панели |
| `:capture-pane -p` | Захватить содержимое панели в буфер |

---

## ⚙️ Конфигурация `~/.tmux.conf`

Базовый полезный конфиг:
```tmux
# --- Основное ---
set -g default-terminal "tmux-256color"
set -ga terminal-overrides ",xterm-256color:Tc"   # true color
set -g mouse on                                    # мышь (скролл, сплиты)
set -g history-limit 50000                         # размер истории
set -g base-index 1                                # окна с 1, а не с 0
setw -g pane-base-index 1                          # панели с 1
set -g renumber-windows on                         # перенумерация после закрытия
set -g escape-time 0                               # убрать задержку Esc

# --- Префикс на Ctrl-a (удобнее) ---
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# --- Vi-стиль в copy mode ---
setw -g mode-keys vi
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "wl-copy"

# --- Интуитивные сплиты (как в редакторах) ---
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# --- Перенавигация панелей как в vim (Alt+hjkl) ---
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# --- Перезагруз конфига ---
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# --- Тема ---
set -g status-style "bg=default,fg=white"
set -g status-left "#[fg=green,bold][#S] "
set -g status-right "#[fg=cyan]%Y-%m-%d #[fg=yellow]%H:%M "
set -g status-interval 5
setw -g window-status-current-style "fg=black,bg=cyan,bold"
```

После правки — `prefix + r` (если добавили бинд) или `:source ~/.tmux.conf`.

---

## 🖱️ Мышь

Включить:
```tmux
set -g mouse on
```
Что работает:
- **Скролл** — автоматически входит в copy mode.
- **Клик по панели** — переключение.
- **Drag по границе** — изменение размера.
- **Drag по окну** — перемещение между окнами.
Временно отключить мышь: `prefix` затем `M` (или `:set mouse off`).

---

## 🧩 Плагины (через TPM)

**TPM** — Tmux Plugin Manager: https://github.com/tmux-plugins/tpm

Установка:
```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

В конец `~/.tmux.conf`:
```tmux
# --- Плагины ---
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'      # sane defaults
set -g @plugin 'tmux-plugins/tmux-resurrect'     # сохранение сессий
set -g @plugin 'tmux-plugins/tmux-continuum'     # автосохранение
set -g @plugin 'tmux-plugins/tmux-yank'          # системный буфер обмена
set -g @plugin 'tmux-plugins/tmux-pain-control'  # удобные сплиты
set -g @plugin 'dracula/tmux'                     # тема Dracula

# auto-restore + autosave
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'

# MUST be at the very bottom
run '~/.tmux/plugins/tpm/tmux'
```

Установить плагины: `prefix + I` (большое I). Обновить: `prefix + U`.

### Полезные плагины
| Плагин | Что делает |
|---|---|
| `tmux-sensible` | Разумные настройки по умолчанию |
| `tmux-resurrect` | Сохраняет/восстанавливает сессии после ребута |
| `tmux-continuum` | Автосохранение + autorrestore |
| `tmux-yank` | Копирование в системный буфер |
| `tmux-pain-control` | Удобное управление панелями |
| `tmux-fzf` | FZF-интерфейс для tmux |
| `tmux-floax` | Плавающий scratch-терминал |
| `dracula/tmux` / `catppuccin/tmux` | Темы |

---

## 🐚 Скриптинг tmux

tmux отлично автоматизируется. Примеры:

### Скрипт создания dev-окружения
```bash
#!/bin/bash
# dev-setup.sh
SESSION="dev"

tmux new-session -d -s "$SESSION" -n 'editor'
tmux send-keys -t "$SESSION:editor" 'nvim .' C-m

tmux new-window -t "$SESSION" -n 'server'
tmux send-keys -t "$SESSION:server" 'npm run dev' C-m

tmux split-window -t "$SESSION:server" -v
tmux send-keys -t "$SESSION:server" 'tail -f log.txt' C-m

tmux new-window -t "$SESSION" -n 'git'
tmux send-keys -t "$SESSION:git" 'lazygit' C-m

tmux attach-session -t "$SESSION"
```

### Полезные команды для скриптов
| Команда | Действие |
|---|---|
| `tmux new-session -d -s имя` | Создать detached-сессию |
| `tmux send-keys 'cmd' C-m` | Послать команду + Enter в панель |
| `tmux send-keys -t target 'cmd' C-m` | В конкретную панель/окно |
| `tmux split-window -h -t session` | Разделить |
| `tmux select-layout -t session tiled` | Сетка |
| `tmux setw -t session synchronize-pane on` | Синхронный ввод во все панели |
| `tmux list-windows -a -F '#{session_name}'` | Имена сессий |
| `tmux display-message -p '#{pane_current_path}'` | Текущий путь панели |

---

## ⌨️ Внутри сессии: статус-бар и подсказки

| Клавиша | Действие |
|---|---|
| `C-b ?` | Полный список биндингов (встроенная справка!) |
| `C-b t` | Показать часы (большими цифрами) |
| `C-b :` | Командная строка tmux |
| `C-b r` (если настроен) | Перезагрузить конфиг |
| `C-b [` | Copy mode / прокрутка истории |
| `C-b ~` | Показать сообщения tmux |
| `C-b i` | Информация о текущем окне |
| `C-b r` | Refresh-client (если глюки с размером) |

---

## 💡 Полезные советы

1. **`prefix + ?`** — лучший способ вспомнить биндинги.
2. **Detach** (`C-b d`) — оставляет процессы работать; вернуться через `tmux a`.
3. **`tmux a -t имя`** — подключиться к конкретной сессии по имени.
4. **SSH + tmux** — на сервере всегда работайте в tmux: при обрыве связи
   сессия сохранится, переподключились через `tmux a -d`.
5. **`-d`** при attach — отключить других клиентов (`tmux a -d -t имя`).
6. **`synchronize-pane`** — ввод одной команды во все панели сразу
   (массовое управление серверами):
   `:setw synchronize-pane on` / `off`.
7. **Масштабирование панели** — `C-b z` для работы в одной панели на весь экран.
8. **Мышь** — `set -g mouse on` сильно упрощает жизнь.
9. **rename-window** — `C-b ,` помогает не путаться в окнах.
10. **Renumber windows** — `set -g renumber-windows on` автоматически сдвигает
    индексы после закрытия окна.
11. **`tmux kill-server`** — когда «всё сломалось» (убивает все сессии).
12. **true color** — `terminal-overrides ",*:Tc"` для корректных цветов
    в редакторах.
13. **SSH-мультиплексирование**: `ssh user@host -t "tmux a -t main \|\| tmux new -s main"`
    — подключение к существующей сессии или создание новой.

---

## 🔗 Ссылки

- Официальный сайт: https://github.com/tmux/tmux
- Мануал: `man tmux` (очень подробный)
- TPM (plugin manager): https://github.com/tmux-plugins/tpm
- tmux-resurrect: https://github.com/tmux-plugins/tmux-resurrect
- Awesome tmux: https://github.com/rothgar/awesome-tmux
- Книга: *tmux 2: Productive Mouse-Free Development* (Brian Hogan)
- Шпаргалка: https://tmuxcheatsheet.com

---

*Сгенерировано как шпаргалка. tmux имеет огромный функционал —
актуальные биндинги смотрите через `C-b ?` и `man tmux`.*

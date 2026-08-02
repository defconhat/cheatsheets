# 🪟 Niri — шпаргалка по горячим клавишам

> **Niri** — scrollable-tiling Wayland compositor.
> Окна выкладываются в бесконечную горизонтальную «ленту» — не перекрывают друг друга.
> Дом: https://github.com/YaLTeR/niri · Документация: https://github.com/YaLTeR/niri/wiki
>
> ⚠️ В конфиге используются ключи-модификаторы:
> `Mod` = Super (Windows key) — по умолчанию в niri.
> Сменить можно в `config.kdl` (`modifier = "Super"` → `"Alt"` и т.п.)

---

## 🪟 Главное — концепция ленты

- Окна в одном workspace расположены **в ряд по горизонтали** (scrollable tiling).
- Переключаетесь между ними, прокручивая ленту влево/вправо.
- Нет «стека» и перекрытий — каждое окно видно целиком.
- Workspaces независимы, у каждого своя лента.

---

## 🚀 Запуск / управление сессией

| Клавиша | Действие |
|---|---|
| `niri` | Запустить niri (если вручную) |
| `Mod+Shift+E` / `Mod+Ctrl+Esc` (настраивается) | Выйти из сессии (выход/перезагрузка compositor'а) |
| `Mod+Shift+/` (`?`) | Показать шпаргалку (встроенный overview hotkeys) |
| `Mod+Shift+P` | Power menu (если настроено) |
| `niri msg action --help` | Список доступных действий через CLI |

---

## 🖼️ Окна

| Клавиша | Действие |
|---|---|
| `Mod+T` | Открыть терминал (по умолчанию `alacritty`) |
| `Mod+D` | Запустить приложение (лаунчер, обычно `fuzzel`/`wofi`/`anyrun`) |
| `Mod+Q` | Закрыть окно |
| `Mod+Shift+H` / `Mod+Shift+L` | Переместить окно влево/вправо по ленте |
| `Mod+H` / `Mod+L` (или `←`/`→`) | Фокус на окно влево/вправо |
| `Mod+K` / `Mod+J` (или `↑`/`↓`) | Перемещение фокуса в столбцах (если окна в столбце) |
| `Mod+Ctrl+H/L` | Поменять окно местами влево/вправо |
| `Mod+R` | Войти в режим resize (изменить ширину) |
| `Mod+F` (или `Mod+M`) | Полноэкранный режим (maximize column) |
| `Mod+C` | Центрировать столбец (centre column) |
| `Mod+-` / `Mod+=` | Уменьшить / увеличить ширину столбца |
| `Mod+W` | Wide column (растянуть столбец) |
| `Mod+[` / `Mod+]` | Move window to column left / right |
| `Mod+Shift+↑/↓` | Сдвинуть окно вверх/вниз внутри столбца |

---

## 🖥️ Workspaces (виртуальные рабочие столы)

| Клавиша | Действие |
|---|---|
| `Mod+1` … `Mod+9` / `Mod+0` | Перейти на workspace №1–10 (по умолчанию 10) |
| `Mod+Tab` (или `Mod+Left/Right` в некоторых конфигах) | Предыдущий / следующий workspace |
| `Mod+Shift+1..0` | Переместить окно на workspace №1–10 |
| `Mod+Wheel` | Переключение workspaces колесом мыши |
| `Mod+Scroll` на фоне | Переключение workspaces колесом |

---

## 📜 Прокрутка ленты / обзор

| Клавиша | Действие |
|---|---|
| `Mod+O` (overview) | Обзор всех окон/workspaces (как Expo) |
| `Mod+Shift+←` / `→` | Прокрутить ленту влево / вправо |
| `Mod+PgUp` / `Mod+PgDn` | Прокрутить ленту |

---

## 🪟 Floating / Fullscreen

| Клавиша | Действие |
|---|---|
| `Mod+Shift+F` / `Mod+V` | Toggle floating (поверх ленты) |
| `Mod+F` | Toggle maximize (полная ширина столбца) |
| `Mod+Shift+Space` | Toggle column width preset (у некоторых конфигов) |

---

## 🔊 Мультимедиа клавиши (если настроены)

| Клавиша | Действие |
|---|---|
| `XF86AudioRaiseVolume` | Громкость + |
| `XF86AudioLowerVolume` | Громкость − |
| `XF86AudioMute` | Mute |
| `XF86AudioPlay/Pause` | Play/Pause |
| `XF86AudioNext` / `Prev` | Следующий / предыдущий трек |
| `XF86MonBrightnessUp/Down` | Яркость монитора + / − |
| `Print` / `Mod+Print` | Скриншот (через `grim` / `grimblast` / `satty`) |

---

## 🖱️ Мышь

| Действие | Эффект |
|---|---|
| `Mod+ЛКМ` (drag) | Переместить окно (move) |
| `Mod+ПКМ` (drag) | Изменить размер окна (resize) |
| `Mod+Колесо` | Переключение workspaces |

---

## 🛠️ CLI — `niri msg`

Управление niri из терминала (скрипты, keybind'ы, ибар'ы):

| Команда | Действие |
|---|---|
| `niri msg action focus-window-left` | Фокус влево |
| `niri msg action focus-window-right` | Фокус вправо |
| `niri msg action focus-workspace-down` | Следующий workspace |
| `niri msg action move-column-left/right` | Двигать столбец |
| `niri msg action close-window` | Закрыть окно |
| `niri msg action maximize-column` | Maximize |
| `niri msg action do-screen-transition` | Эффект перехода |
| `niri msg workspaces` | Вывести список workspaces (для status bar) |
| `niri msg focused-window` | Информация об активном окне |
| `niri msg event-stream` | Поток событий (для waybar/пагинация) |
| `niri validate` | Проверить конфиг на ошибки |
| `niri msg version` | Версия niri |

---

## ⚙️ Конфигурация

Расположение: `~/.config/niri/config.kdl` (формат KDL)

Пример фрагмента:
```kdl
// Модификатор по умолчанию
Mod T  { spawn "alacritty"; }
Mod D  { spawn "fuzzel"; }
Mod Q  { close-window; }
Mod Shift+E { quit; }

// Фокус
Mod H { focus-column-left; }
Mod L { focus-column-right; }
Mod K { focus-window-up; }
Mod J { focus-window-down; }

// Workspaces
Mod 1 { focus-workspace 1; }
Mod 2 { focus-workspace 2; }
Mod Shift+1 { move-column-to-workspace 1; }

// Скриншот
Print { spawn "grimblast" "copy" "area"; }

// Громкость
XF86AudioRaiseVolume { spawn "wpctl" "set-volume" "@DEFAULT_AUDIO_SINK@" "5%+"; }
XF86AudioMute        { spawn "wpctl" "set-mute"   "@DEFAULT_AUDIO_SINK@" "toggle"; }
```

Проверка конфига:
```bash
niri validate
```

Изменения применяются **на лету** — niri автоматически перезагружает конфиг при сохранении файла.

---

## 🧩 Типичный стек с niri

| Компонент | Что | Примеры |
|---|---|---|
| Бар | status bar | `waybar`, `ironbar`, `fnott` |
| Лаунчер | запуск приложений | `fuzzel`, `wofi`, `anyrun`, `tofi` |
| Уведомления | notification daemon | `mako`, `dunst`, `swaync` |
| Обои | wallpaper | `swaybg`, `swww`, `hyprpaper`-like |
| Скриншоты | screenshot | `grim` + `slurp`, `grimblast`, `satty` |
| Блокировка экрана | lockscreen | `swaylock`, `hyprlock` |
| Idle | энергосбережение | `swayidle` |
| Polkit | авторизация | `polkit-gnome`, `hyprpolkitagent` |

---

## 💡 Полезные советы

1. **Встроенный overview** — `Mod+Shift+/` (или `Mod+O`) показывает все
   столбцы/окна текущего workspace.
2. **Нет overlays/stacking** — не пытайтесь делать «плавающие» окна как в
   i3/sway; используйте floating-режим (`Mod+Shift+F`) для диалогов.
3. **Многомониторность** — каждый монитор имеет свой набор workspaces.
4. **Анимации** настраиваются в секции `environment` / `animations`.
5. **niri ipc** — `niri msg event-stream` даёт JSON-поток для waybar.
6. **waybar**: используйте модуль `custom/niri` или `niri/workspaces` —
   есть готовые примеры в репо niri.
7. **Проверка конфига** перед перезапуском — `niri validate`.
8. **Документация по всем action'ам** — `niri msg action --help` и
   https://github.com/YaLTeR/niri/wiki/Configuration:-Key-Bindings
9. **Шпаргалку внутри niri** можно вывести в floating окне через конфиг —
   смотрите раздел Hotkey-Overlay в wiki.
10. **Скрипт быстрого переключения раскладки** — `swaywsr`,
    `kbd-switcher`, или `hyprctl`-аналог через `niri msg`.

---

## 🔗 Ссылки

- Niri GitHub: https://github.com/YaLTeR/niri
- Wiki (конфиг): https://github.com/YaLTeR/niri/wiki
- Key bindings: https://github.com/YaLTeR/niri/wiki/Configuration:-Key-Bindings
- Default config: https://github.com/YaLTeR/niri/wiki/Configuration:-Sample-Config
- Сообщество / примеры: https://github.com/sorchix/niri-config (и др.)

---

*Сгенерировано как шпаргалка. Niri активно развивается —
актуальные action'ы смотрите через `niri msg action --help` и в wiki.*

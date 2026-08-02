# 📘 Neovim (LazyVim) — шпаргалка по горячим клавишам

> **LazyVim** — готовый дистрибутив Neovim на базе менеджера `lazy.nvim`.
> Дом: https://lazyvim.github.io · Репо: https://github.com/LazyVim/LazyVim
>
> Лидер `<leader>` по умолчанию = **Пробел** (`Space`)
> Локальный лидер `\` (редко используется)

---

## 🚀 Первый запуск и базовые команды

| Команда | Действие |
|---|---|
| `nvim` | Открыть Neovim |
| `nvim файл` | Открыть файл |
| `:Lazy` | Открыть менеджер плагинов (установка, обновление) |
| `:LazyHealth` | Проверка здоровья LazyVim |
| `:checkhealth` | Диагностика Neovim и плагинов |
| `:Mason` | Менеджер LSP/форматеров/линтеров (установка инструментов) |
| `:LazyExtras` | Дополнительные модули LazyVim (языки, инструменты) |
| `:q` / `:q!` | Выйти / выйти без сохранения |
| `:w` / `:wq` / `:x` | Сохранить / сохранить+выйти / сохранить (только если есть изменения) |

---

## ✨ Режимы (вставка, обычный, визуальный)

| Клавиша | Действие |
|---|---|
| `i` | Вставка перед курсором |
| `I` | Вставка в начале строки |
| `a` | Вставка после курсора |
| `A` | Вставка в конце строки |
| `o` | Новая строка снизу + режим вставки |
| `O` | Новая строка сверху + режим вставки |
| `Esc` / `jk` / `kj` | Выйти из вставки (LazyVim по умолчанию remap `jk`/`kj`) |
| `v` | Визуальный режим (побуквенно) |
| `V` | Визуальный режим (по строкам) |
| `Ctrl-v` | Визуальный блочный режим |
| `R` | Замена (replace mode) |

---

## 🧭 Навигация по курсору

| Клавиша | Действие |
|---|---|
| `h j k l` | Влево / вниз / вверх / вправо |
| `w` / `b` | Вперёд / назад по словам |
| `e` / `ge` | Конец слова вперёд / назад |
| `0` | В начало строки |
| `^` | К первому непустому символу |
| `$` | В конец строки |
| `gg` | В начало файла |
| `G` | В конец файла |
| `{` / `}` | Между абзацами |
| `%` | К парной скобке |
| `*` / `#` | Следующее / предыдущее совпадение слова под курсором |
| `Ctrl-o` / `Ctrl-i` | Назад / вперёд по jump-list |

---

## 📜 Прокрутка и окна

| Клавиша | Действие |
|---|---|
| `Ctrl-d` / `Ctrl-u` | Пол-страницы вниз / вверх |
| `Ctrl-f` / `Ctrl-b` | Страница вниз / вверх |
| `Ctrl-e` / `Ctrl-y` | Прокрутка на строку без движения курсора |
| `zz` / `zt` / `zb` | Центр / верх / низ экрана (курсор) |
| `H` / `M` / `L` | Верх / середина / низ экрана |

### Разделение окон

| Клавиша | Действие |
|---|---|
| `<leader>-` (`Space -`) | Горизонтальный сплит |
| `<leader>\|` (`Space \|`) | Вертикальный сплит |
| `Ctrl-h/j/k/l` | Перейти в окно влево/вниз/вверх/вправо |
| `Ctrl-↑/↓/←/→` | Изменить размер окна (LazyVim) |
| `<leader>=` | Сделать окна равными |
| `<leader>wd` (`Space w d`) | Закрыть окно |
| `<leader>wo` | Закрыть все кроме текущего (only) |

---

## 🗂️ Буферы (lazy.nvim / bufferline.nvim)

| Клавиша | Действие |
|---|---|
| `<leader>bb` (`Space b b`) | Список буферов (Bufferline/Telescope) |
| `<S-h>` / `<S-l>` (`Shift-h/l`) | Предыдущий / следующий буфер |
| `[b` / `]b` | Предыдущий / следующий буфер |
| `<leader>bd` | Закрыть буфер |
| `<leader>bo` | Закрыть все кроме текущего |
| `<leader>bl` | Перейти к последнему буферу |
| `<leader>` + `1..9` | Перейти к вкладке bufferline №1..9 |

---

## 🔭 Telescope (поиск и fuzzy-finder) — `<leader>f`

| Клавиша | Действие |
|---|---|
| `<leader><Space>` (`Space Space`) | Найти файлы (Find Files) |
| `<leader>ff` | Найти файлы |
| `<leader>fr` | Недавние файлы (Recent) |
| `<leader>fg` | Поиск по содержимому файлов (live grep, ripgrep) |
| `<leader>fw` | Поиск слова под курсором |
| `<leader>fb` | Буферы |
| `<leader>fc` | Найти в конфиге Neovim |
| `<leader>fh` | Справка Neovim (`:help`) |
| `<leader>fk` | Поиск по keymap'ам |
| `<leader>fo` | Опции |
| `<leader>ft` | Темы оформления |
| `<leader>fd` | Диагностики (document) |
| `<leader>s` … | Группа поисков (s = search, например `<leader>ss` — символы) |

**Внутри Telescope:**
| Клавиша | Действие |
|---|---|
| `Ctrl-j` / `Ctrl-k` | Вниз / вверх |
| `Enter` | Выбрать |
| `Ctrl-v` / `Ctrl-x` / `Ctrl-t` | Открыть в вертикальном/горизонтальном сплите/вкладке |
| `Ctrl-q` | Отправить в quickfix |
| `Esc` | Закрыть |

---

## 🧭 NeoTree (файловое дерево) — `<leader>e`

| Клавиша | Действие |
|---|---|
| `<leader>e` (`Space e`) | Открыть / закрыть файловое дерево |
| Внутри дерева: | |
| `?` | Подсказка по клавишам |
| `Enter` / `o` | Открыть файл / каталог |
| `a` | Создать файл/каталог |
| `d` | Удалить |
| `r` | Переименовать |
| `c` / `p` | Копировать / вставить |
| `m` | Переместить |
| `y` | Скопировать путь |
| `H` | Показать/скрыть скрытые файлы |
| `R` | Обновить (refresh) |
| `<` / `>` | Сменить источник (files / buffers / git) |
| `g?` | Полная справка NeoTree |

---

## 💻 Терминал (toggleterm / встроенный)

| Клавиша | Действие |
|---|---|
| `<C-/>` / `<C-_>` | Открыть/закрыть плавающий терминал (LazyVim default) |
| `<leader>ft` (`Space f t`) | Открыть терминал |
| `<Esc><Esc>` (двойной) | Выйти из режима терминала в Normal |

---

## 🧠 LSP (языковой сервер) — `gr` и `K`

| Клавиша | Действие |
|---|---|
| `K` | Hover (документация под курсором) |
| `gd` | Перейти к определению (Go to Definition) |
| `gD` | Перейти к объявлению (Declaration) |
| `gi` | Перейти к реализации (Implementation) |
| `gr` | References (ссылки) — через Telescope |
| `gI` | Go to Implementation |
| `gy` | Go to Type Definition |
| `<leader>ca` | Code Action (предложения/quickfix) |
| `<leader>cr` | Rename (переименовать символ) |
| `<leader>cf` | Format (форматировать буфер/диапазон) |
| `<leader>cd` | Показать диагностику в строке |
| `]d` / `[d` | Следующая / предыдущая диагностика |
| `]e` / `[e` | Следующая / предыдущая ошибка |
| `<leader>ll` | Открыть Trouble (список диагностик) |

---

## 🔁 Git

| Клавиша | Действие |
|---|---|
| `<leader>gg` (`Space g g`) | LazyGit (TUI-клиент git) — рекомендуемый способ |
| `<leader>gf` | LazyGit для текущего файла |
| `]h` / `[h` | Следующий / предыдущий hunk (gitsigns) |
| `<leader>ghs` | Stage hunk |
| `<leader>ghu` | Undo stage hunk |
| `<leader>ghr` | Reset hunk |
| `<leader>ghp` | Preview hunk |
| `<leader>ghb` | Blame line |

---

## ✂️ Редактирование текста

| Клавиша | Действие |
|---|---|
| `dd` | Удалить строку (и в буфер) |
| `cc` | Изменить строку |
| `dw` / `cw` | Удалить / изменить слово |
| `D` | Удалить до конца строки |
| `C` | Изменить до конца строки |
| `x` | Удалить символ |
| `u` | Отменить (undo) |
| `Ctrl-r` | Вернуть (redo) |
| `.` | Повторить последнее действие |
| `y` / `yy` | Скопировать (yank) / строку |
| `p` / `P` | Вставить после / перед курсором |
| `>>` / `<<` | Сдвинуть строку вправо / влево |
| `gv` | Восстановить последнее выделение |

---

## ✂️ LazyVim extras: мини-команды

| Клавиша | Действие |
|---|---|
| `<leader>xl` (`Space x l`) | Открыть Location List (Trouble) |
| `<leader>xx` | Список диагностик (Trouble) |
| `<leader>xX` | Диагностики только буфера |
| `<leader>cs` | Toggle Outline (символы файла) |
| `<leader>co` | Other (переключить источник/окно) |
| `<leader>;` | Открыть командную историю |
| `<leader>/` | Поиск в текущем буфере (buffer grep) |

---

## 🧩 Плагины (управление)

| Команда | Действие |
|---|---|
| `:Lazy` | Главная панель плагинов |
| `:Lazy install` | Установить плагины |
| `:Lazy update` | Обновить все плагины |
| `:Lazy sync` | Синхронизировать (install + update + clean) |
| `:Lazy clean` | Удалить неиспользуемые плагины |
| `:Lazy profile` | Профилирование загрузки |
| `:Lazy log` | Логи изменений |
| `:Lazy load <name>` | Загрузить плагин вручную |
| `:Mason` | Менеджер инструментов (LSP, format, lint) |
| `:MasonInstall <tool>` | Установить инструмент |
| `:MasonUpdate` | Обновить реестр/инструменты |

---

## ⚙️ Настройка LazyVim

Расположение: `~/.config/nvim/`

| Файл | Назначение |
|---|---|
| `init.lua` | Точка входа (bootstrap lazy.nvim) |
| `lua/config/options.lua` | Опции Neovim |
| `lua/config/keymaps.lua` | Глобальные keymap'ы |
| `lua/config/autocmds.lua` | Автокоманды |
| `lua/plugins/` | Свои плагины (один файл на плагин/группу) |

### Пример своего плагина (`lua/plugins/example.lua`)
```lua
return {
  -- добавить плагин
  { "f-person/gitblame.nvim", event = "BufRead" },

  -- переопределить существующий (Comment.nvim)
  {
    "numToStr/Comment.nvim",
    opts = function(_, opts)
      opts.toggler = { line = "<leader>cc", block = "<leader>bc" }
    end,
  },

  -- отключить плагин из LazyVim
  { "folke/noice.nvim", enabled = false },
}
```

### Пример своего keymap'а (`lua/config/keymaps.lua`)
```lua
-- быстрое сохранение
vim.keymap.set("n", "<leader>w", "<cmd>w<cr>", { desc = "Save file" })
-- выйти без сохранения
vim.keymap.set("n", "<leader>qq", "<cmd>qa!<cr>", { desc = "Quit all" })
```

### Опции (`lua/config/options.lua`)
```lua
-- размер таба
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
-- относительные номера строк
vim.opt.relativenumber = true
-- системный буфер
vim.opt.clipboard = "unnamedplus"
```

---

## 🎨 Темы и красота

| Клавиша / Команда | Действие |
|---|---|
| `<leader>ft` (`Space f t`) | Превью и выбор темы |
| `:Telescope colorscheme` | То же через Telescope |
| Варианты в LazyVim по умолчанию: | `tokyonight`, `catppuccin`, `habamax` |

Поставить тему навсегда в `lua/plugins/theme.lua`:
```lua
return {
  { "catppuccin/nvim", name = "catppuccin", priority = 1000 },
  { "LazyVim/LazyVim", opts = { colorscheme = "catppuccin" } },
}
```

---

## 💡 Полезные советы

1. **`:LazyExtras`** — включите модули под ваши языки (`lang.python`,
   `lang.rust`, `lang.go`, `lang.typescript` и т.д.).
2. **`:checkhealth`** после установки — проверит, что все LSP/инструменты
   работают.
3. **`:Mason** — поставьте `lua-language-server`, `stylua`, `prettierd`,
   `eslint_d`, `ruff`, `pyright` под ваши задачи.
4. **Какой LSP активен?** — `:LspInfo` (или `:checkhealth lsp`).
5. **Откаты** — LazyVim использует `lazy.nvim` с лок-файлом, обновления
   безопасны; откатить плагин можно в `:Lazy log`.
6. **Быстрый поиск файла** — `<leader><leader>` (Find Files) и **live grep**
   — `<leader>fg` (нужен установленный `ripgrep`).
7. **Диагностики в одном списке** — `<leader>xx` (плагин `trouble.nvim`).
8. **Форматирование при сохранении** — LazyVim включает форматconform.nvim
   автоматически; проверить: `:ConformInfo`.
9. **Про замену `Ctrl-h/j/k/l`** на навигацию по окнам — это builtin LazyVim,
   но `Ctrl-l` в терминале конфликтует, имейте в виду.
10. **Docs:** https://lazyvim.github.io/keymaps — официальный и всегда
    актуальный список.

---

## 🔗 Ссылки

- LazyVim: https://lazyvim.github.io
- lazy.nvim: https://github.com/folke/lazy.nvim
- Telescope: https://github.com/nvim-telescope/telescope.nvim
- Mason: https://github.com/Williamboman/mason.nvim
- NeoTree: https://github.com/nvim-neo-tree/neo-tree.nvim
- Trouble: https://github.com/folke/trouble.nvim
- LazyGit: https://github.com/jesseduffield/lazygit

---

*Сгенерировано как шпаргалка. LazyVim постоянно развивается —
актуальный список биндингов смотрите на https://lazyvim.github.io/keymaps
или через `:Telescope keymaps` (`<leader>fk`).*

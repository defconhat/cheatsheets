# 🌈 eza — шпаргалка (замена ls)

> **eza** — современная замена `ls` на Rust (форк `exa`, который больше не развивается).
> Цветной вывод, git-статус, древовидный режим, иконки. Дом: https://github.com/eza-community/eza

---

## 📦 Установка

```bash
# Arch / CachyOS
sudo pacman -S eza

# macOS
brew install eza

# Debian/Ubuntu (новые версии — через cargo или eza-форум)
sudo apt install eza           # может быть старая
cargo install eza              # самая свежая

# Через Rust
cargo install eza
```

### Алиас вместо `ls` (рекомендуется в `~/.zshrc` / `~/.bashrc`)
```bash
alias ls="eza --group-directories-first --icons"
alias ll="eza -l --group-directories-first --icons --git"
alias la="eza -la --group-directories-first --icons --git"
alias lt="eza --tree --level=2 --icons"
alias lh="eza -la --icons | grep '^-'"
```

---

## 🔑 Базовый вывод

| Флаг | Что делает |
|---|---|
| `eza` | Листинг текущей папки (как `ls`) |
| `eza <dir>` | Листинг указанной папки |
| `eza -1` | Один файл на строку |
| `eza -a` | Показать скрытые (точкой) |
| `eza -A` | Все, кроме `.` и `..` |
| `eza -d` | Показать сами директории, а не их содержимое |
| `eza -D` | Только директории |
| `eza -f` | Только файлы |

### Длинный формат (`-l`)
```bash
eza -l                # подробный листинг
eza -l --header       # с заголовками колонок
eza -l --number       # с числовыми UID/GID
eza -l --links        # число хардлинков
eza -l --blocks       # добавить колонку блоков
```

| Колонка | Что значит |
|---|---|
| mode | права доступа |
| links | кол-во хардлинков |
| user / group | владелец |
| size | размер (`--smart-size` или `-h`) |
| modified | дата изменения |
| name | имя (с иконкой если `--icons`) |

---

## 🌳 Дерево (tree)

```bash
eza --tree                    # дерево текущей папки
eza --tree --level=2          # глубина 2
eza --tree --level=3 -a       # со скрытыми
eza -T --level=1 -D           # только директории, 1 уровень
eza --tree -I "node_modules|.git"   # игнорить папки
```

| Флаг | Действие |
|---|---|
| `--tree` / `-T` | Включить древовидный режим |
| `--level=N` | Макс. глубина |
| `--ignore-glob` | Игнорировать по glob |
| `--recurse` | Рекурсивный листинг (списком, не деревом) |

---

## 🎨 Иконки и цвета

```bash
eza --icons                    # добавить иконки файлов
eza --icons=auto               # только если терминал поддерживает
eza --color=always             # форсировать цвет
eza --color=never              # без цвета (для pipe)
eza --color-scale all          # шкала цвета по размеру
eza --colour-scale-mode fixed  # фикс. шкала
```

> ⚠️ Для иконок нужен Nerd Font в терминале (например JetBrainsMono Nerd Font).

---

## 🔀 Git-интеграция

```bash
eza -l --git                   # колонка git-статуса
eza -l --git-repos             # статус репозитория целиком
eza -l --git-repos --git-repos-no-status  # без детального статуса
```

| Символ | Значение |
|---|---|
| `-` | не изменён |
| `N` | новый (untracked) |
| `M` | модифицированный |
| `U` | обновлённый/неразрешённый |
| `C` | скопированный |
| `D` | удалённый |
| `?` | игнорируемый |

Также `eza` показывает у репозитория: текущую ветку, сколько коммитов вперед/назад от `origin`.

---

## 📊 Сортировка

```bash
eza -l --sort=size             # по размеру
eza -l --sort=size --reverse   # крупные внизу
eza -l --sort=modified         # по дате изменения
eza -l --sort=accessed         # по дате доступа
eza -l --sort=created          # по дате создания
eza -l --sort=extension        # по расширению
eza -l --sort=name             # по имени (дефолт)
eza -l --sort=none             # без сортировки
eza -l --sort=inode            # по inode
eza -l --sort=version          # по версии (v1, v2, v10)
```

### Группировка
```bash
eza -l --group-directories-first   # папки сверху
eza -l --group-directories-last    # папки снизу
eza -l --reverse                   # обратный порядок
```

---

## 📐 Размер и время

```bash
eza -l --bytes                # размер в байтах (без суффиксов)
eza -l --binary               | размер в KiB/MiB (1024)
eza -l -h                     # human-readable (KB, MB)
eza -l --smart-size           # авто: байты/KB/MB по ситуации
eza -l --time-style=long-iso  # формат времени
eza -l --time-style=full-iso  # полный ISO
eza -l --time-style=custom "%Y-%m-%d %H:%M"  # свой формат
```

| Флаг времени | какую дату показывать |
|---|---|
| `-m` / `--modified` | дата изменения (по умолчанию) |
| `-u` / `--accessed` | дата доступа |
| `-U` / `--created` | дата создания |
| `--changed` | когда менялись метаданные |

---

## 🔗 Доп. метаданные

```bash
eza -l --extended              # расширенные атрибуты (xattr)
eza -l --security-context      | SELinux context
eza -l --context               | колонка контекста (безопасность)
eza -l --mounts                | точка монтирования
```

---

## 🧰 Частые комбинации (one-liners)

```bash
# Быстрый обзор проекта
eza -l --git --icons --group-directories-first

# Только что изменилось (как watch)
eza -l --sort=modified --reverse | head

# Показать самый большой файл в директории
eza -l --sort=size --reverse --oneline | tail -1

# Дерево без мусора (для разработки)
eza --tree --level=2 -I "node_modules|.git|target|dist|build"

# Список недавно изменённых файлов (рекурсивно)
eza -l --sort=modified --reverse -R | head -50
```

---

## ⚙️ Конфиг по умолчанию

eza читает переменные окружения для дефолтных флагов:

```bash
# ~/.zshrc или ~/.bashrc
export EZA_STANDARD_OPTIONS="--group-directories-first --icons"
export EZA_LONG_OPTIONS="--git --header --smart-size"
export EZA_TREE_OPTIONS="--level=2"
```

---

## 🆚 eza vs exa vs ls

| Что | `ls` | `exa` | `eza` |
|---|---|---|---|
| Цвет | базовый | ✅ детальный | ✅ детальный + шкала |
| Git-статус | ❌ | ✅ | ✅ |
| Иконки (Nerd) | ❌ | ⚠️ патч | ✅ нативно |
| Дерево | ❌ (`tree` отдельно) | ✅ | ✅ |
| Сортировка | базовая | ✅ расшир. | ✅ расшир. |
| Поддержка | активная | ❌ заброшен | ✅ активная (форк exa) |
| Скорость (Rust) | C | Rust | Rust |

> `eza` — прямой преемник `exa`. Если стоит `exa`, переходите на `eza`.

---

## 💡 Сравнение выводов

```
$ ls -l
-rw-r--r-- 1 user user 1234 Jan 6 10:30 file.txt

$ eza -l --icons --git
.rw-r--r-- 1.2k user  6 Jan 10:30 📄 file.txt  -M
```

Цвета: директории — синий, исполняемые — зелёный, ссылки — голубой, `*.md` — особый, скрытые — серый.

---

## 🔗 Источники

- GitHub: https://github.com/eza-community/eza
- Документация: https://github.com/eza-community/eza/blob/main/man/eza.1.md
- Сравнение с exa: https://github.com/eza-community/eza#features

# 📦 pacman / yay / paru — шпаргалка (Arch / CachyOS)

> **pacman** — пакетный менеджер Arch Linux.
> **yay** / **paru** — AUR-хелперы (AUR = Arch User Repository).
> Документация: https://wiki.archlinux.org/title/Pacman

---

## 🚀 pacman — базовые команды

### Установка
```bash
sudo pacman -S <package>              # установить
sudo pacman -S nginx postgresql       # несколько
sudo pacman -S --needed <pkg>         # не переустанавливать если есть
sudo pacman -S "$(pacman -Slq)"       # интерактивно выбрать (НЕ делать!)
sudo pacman -U package.tar.zst        # установить локальный файл
sudo pacman -U https://example.com/pkg.tar.zst   # по URL
```

### Удаление
```bash
sudo pacman -R <package>              # удалить (оставить зависимости)
sudo pacman -Rs <package>             # + неиспользуемые зависимости
sudo pacman -Rns <package>            # + конфиги (рекомендуется!)
sudo pacman -Rdd <package>            # без проверки зависимостей (ОПАСНО)
sudo pacman -Rns $(pacman -Qdtq)      # удалить все пакеты-сироты
```

### Обновление системы
```bash
sudo pacman -Sy                       # обновить БД пакетов (БЕЗ обновления)
sudo pacman -Su                       # обновить пакеты
sudo pacman -Syu                      # ⭐ обновить БД + пакеты (СТАНДАРТ)
sudo pacman -Syyu                     # принудительно обновить БД (если зеркало устарело)
sudo pacman -Syyu --needed base-devel # ...
```

> ⚠️ **НИКОГДА** не делайте `pacman -Sy <pkg>` (обновить БД без обновления пакетов) —
> это приведёт к partial upgrade и сломает систему.
> Только `pacman -Syu` для обновления.

### Поиск
```bash
pacman -Ss <name>                     # искать в репозиториях
pacman -Ss "^python-"                 # regex
pacman -Ss editor                     # по слову
pacman -Qs <name>                     # искать среди установленных
pacman -F <filename>                  # в каком пакете файл
pacman -Fy                            # обновить базу файлов (сначала)
sudo pacman -Fy && pacman -F nginx.conf
```

### Информация
```bash
pacman -Si <package>                  # инфо о пакете в репозитории
pacman -Qi <package>                  # инфо об установленном
pacman -Qil <package>                 # файлы установленного пакета
pacman -Ql <package>                  # список файлов пакета
pacman -Qo /path/to/file             # какому пакету принадлежит файл
pacman -Qo $(which nginx)
pacman -Qdt                           # пакеты-сироты
pacman -Qet                           # явно установленные
pacman -Qm                            # пакеты не из репозиториев (AUR)
pacman -Qn                            # пакеты из официальных репозиториев
```

### Списки
```bash
pacman -Q                             # все установленные
pacman -Qe                            # явно установленные (не зависимости)
pacman -Qeq                           # только имена
pacman -Q | wc -l                     # сколько пакетов
```

---

## 📋 Мнемоника флагов pacman

| Буква | Что значит |
|---|---|
| **S** | **S**ync (репозиторий: установить/искать/скачать) |
| **Q** | **Q**uery (локальная база установленных) |
| **R** | **R**emove (удалить) |
| **U** | **U**pgrade/URL (установить из файла) |
| **F** | **F**iles (поиск файлов) |

Дополнительные модификаторы:
| Флаг | Значение |
|---|---|
| `y` | refresh (обновить базу) |
| `u` | sysupgrade (обновить пакеты) |
| `s` | search (искать) |
| `i` | info (информация) |
| `l` | list (список файлов) |
| `o` | owns (кому принадлежит файл) |
| `e` | explicit (явно установленные) |
| `t` | orphan (сироты) / deps-tree |
| `n` | native (из официальных репо) |
| `m` | foreign (AUR/внешние) |
| `d` | deps (зависимости) |
| `c` | cascade / config |
| `n` | nosave (не сохранять конфиги) |

---

## 🔧 pacman.conf

Файл: `/etc/pacman.conf`

```ini
[options]
HoldPkg = pacman glibc
Architecture = auto
CheckSpace
Color                    # цветной вывод
VerbosePkgLists
ParallelDownloads = 5    # параллельная загрузка (ускоряет!)

# Репозитории
[core]
Include = /etc/pacman.d/mirrorlist

[extra]
Include = /etc/pacman.d/mirrorlist

[multilib]               # 32-бит (для Steam, Wine)
Include = /etc/pacman.d/mirrorlist

# CachyOS repo (если у вас CachyOS)
[cachyos]
Include = /etc/pacman.d/cachyos-mirrorlist
```

### Полезные опции
```ini
Color
ILoveCandy              # прогресс-бар в виде Pac-Man (пасхалка)
ParallelDownloads = 10  # быстрее загрузка
VerbosePkgLists         # подробный список
```

---

## 🪞 Зеркала (mirrorlist)

```bash
# Файл: /etc/pacman.d/mirrorlist
# Обновить список зеркал:
sudo reflector --latest 50 --protocol https --sort rate \
    --save /etc/pacman.d/mirrorlist

# CachyOS:.rate-mirrors
rate-mirrors cachyos | sudo tee /etc/pacman.d/cachyos-mirrorlist

# Проверить статус зеркал
curl -s "https://archlinux.org/mirrors/status/" | head

# Тест скорости
rankmirrors -n 6 /etc/pacman.d/mirrorlist
```

---

## 💾 Кэш пакетов и чистка

```bash
ls /var/cache/pacman/pkg/              # кэш
du -sh /var/cache/pacman/pkg/          # размер кэша

# paccache (из pacman-contrib) — РЕКОМЕНДУЕТСЯ
sudo paccache -r                       # оставить последние 3 версии
sudo paccache -rk1                     # оставить только 1 (последнюю)
sudo paccache -ruk0                    # удалить кэш удалённых пакетов
sudo paccache -v                       # подробнее

# Авто-чистка (systemd timer)
sudo systemctl enable --now paccache.timer

# Полная очистка кэша (ОСТОРОЖНО!)
sudo pacman -Sc                        # удалить кэш удалённых пакетов
sudo pacman -Scc                       # удалить ВЕСЬ кэш
```

---

## 🆘 Восстановление / откат

### Откат пакета из кэша
```bash
# Найти старую версию в кэше
ls /var/cache/pacman/pkg/python-3.12*

# Установить конкретную версию
sudo pacman -U /var/cache/pacman/pkg/python-3.12.0-1-x86_64.pkg.tar.zst
```

### Архив пакетов (если кэша нет)
```bash
# https://archive.archlinux.org/packages/
sudo pacman -U https://archive.archlinux.org/packages/p/python/python-3.12.0-1-x86_64.pkg.tar.zst
```

### Система не загружается после обновления
```bash
# 1. Загрузиться с Arch ISO (USB)
# 2. Примонтировать корень
sudo mount /dev/sda2 /mnt

# 3. Чрутнуться
sudo arch-chroot /mnt

# 4. Откатить проблемный пакет из кэша
sudo pacman -U /var/cache/pacman/pkg/broken-package-1.0-1.pkg.tar.zst

# 5. Если pacman сломан — временно игнорировать
sudo pacman -Syu --ignore broken-package
```

### Игнорировать пакет при обновлении
```bash
sudo pacman -Syu --ignore python
sudo pacman -Syu --ignore python,linux
# Или в pacman.conf:
# IgnorePkg = python
```

---

## 🌟 yay / paru — AUR-хелперы

### Установка yay/paru
```bash
# paru (рекомендуется, на Rust)
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/paru.git
cd paru && makepkg -si

# yay
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si
```

### Базовое использование (как pacman, но с AUR!)
```bash
paru <name>                           # поиск + установка интерактивно
paru -S <package>                     # установить (из репо или AUR)
paru -S firefox-developer-edition     # AUR-пакет
yay -S visual-studio-code-bin

# Обновление
paru -Syu                             # репо + AUR
paru -Sua                             # только AUR
paru -Syu --devel                     # + VCS-пакеты (git/svn)
paru                                  # = paru -Syu (по умолчанию)

# Поиск
paru <name>                           # интерактивный поиск
paru -Ss <name>                       # найти в репо + AUR
paru -Sa <name>                       # только AUR

# Информация
paru -Si <package>                    # инфо
paru -Ps                              # статистика системы

# Удаление
paru -Rns <package>                   # с зависимостями и конфигами
paru -Rns $(paru -Qdtq)               # удалить сироты
paru -c                               # очистить кэш + сироты
```

### Особенности AUR-хелперов
```bash
# Редактирование PKGBUILD перед сборкой
paru -S <pkg> --edit
yay -S <pkg> --edit

# Не спрашивать подтверждения
paru -S <pkg> --noconfirm
yay -S <pkg> --noconfirm

# Скачать исходники без установки
paru -G <pkg>                         # в текущий каталог
paru -Gcd <pkg>                       # + показать diff
yay -G <pkg>

# Показать зависимости
paru -Pi <pkg>
```

### paru.conf / yay.conf
```ini
# ~/.config/paru/paru.conf
[options]
RemoveMake = yes                      # удалять make-зависимости
SkipReview                            # не показывать PKGBUILD (осторожно!)
CleanAfter = yes                      # удалять файлы сборки
Provides = yes                        # учитывать Provides
PgpFetch = yes                        # авто-импорт PGP-ключей
SudoLoop = yes                        # держать sudo активным

[bin]
fm = nnn                              # файловый менеджер для review
```

---

## 🔍 AUR (Arch User Repository)

AUR — пользовательский репозиторий. Пакеты там **НЕ бинарные** — это скрипты `PKGBUILD`,
которые собирают пакет из исходников.

### Ручная установка из AUR (без хелпера)
```bash
# 1. Установить зависимости
sudo pacman -S --needed base-devel git

# 2. Клонировать
git clone https://aur.archlinux.org/package-name.git
cd package-name

# 3. ПРОЧИТАТЬ PKGBUILD! (безопасность!)
cat PKGBUILD

# 4. Собрать пакет
makepkg -si                           # -s установка зависимостей, -i установить
```

### Команды makepkg
```bash
makepkg                               # собрать пакет
makepkg -s                            # + установить зависимости
makepkg -i                            # + установить собранный
makepkg -si                           # оба
makepkg -o                            # только скачать исходники
makepkg -f                            # пересобрать
makepkg -c                            # очистить после
makepkg -G                            # получить исходники + PKGBUILD
makepkg --skipinteg                   # пропустить проверки (ОПАСНО!)
makepkg --sign                        # подписать пакет
```

### Безопасность AUR
- **Всегда читайте PKGBUILD** перед установкой! Внутри может быть что угодно.
- Проверяйте `Votes` и `Popularity` — популярные пакеты безопаснее.
- `Orphaned` пакеты (без мейнтейнера) — риск.
- `Maintainer` с хорошей репутацией — доверие выше.
- `Last Updated` — старые пакеты могут не собираться.

### Поиск на aur.archlinux.org
```bash
# Через API
curl -s "https://aur.archlinux.org/rpc/?v=5&type=search&arg=neovim" | jq

# Проверить статус пакета
paru -Si <pkg>                        # локально
```

---

## 📊 pacman tips & tricks

### Что занимает место?
```bash
expac -H M '%m\t%n' | sort -h         # пакеты по размеру
pacman -Qi | awk '/^Name/{n=$3} /^Installed Size/{print $4" "n}' | sort -h
```

### Самые новые установленные
```bash
expac --timefmt='%Y-%m-%d %H:%M' '%l\t%n' | sort | tail -20
```

### Зависимости (дерево)
```bash
pactree <package>                     # дерево зависимостей
pactree -r <package>                  # обратное дерево (кто зависит)
pacdeps <package>
```

### Кто установил пакет?
```bash
# Лог установки
grep " installed <package>" /var/log/pacman.log
```

### Экспорт списка пакетов
```bash
pacman -Qqe > pkglist.txt             # явно установленные
# Восстановление на новой системе:
sudo pacman -S --needed - < pkglist.txt
```

### Сравнение файлов (.pacnew)
```bash
# Когда pacman создаёт .pacnew (не перезаписывает ваш конфиг)
sudo pacdiff                          # интерактивное слияние
# Инструменты: pacdiff, vimdiff, meld
```

---

## 🐛 Частые проблемы

### "conflicting files"
```bash
# Файл принадлежит другому пакету
sudo pacman -S <pkg> --overwrite 'path/to/file'
sudo pacman -S <pkg> --overwrite '*'
```

### "invalid or corrupted package"
```bash
sudo pacman -Sy archlinux-keyring     # обновить ключи
sudo pacman-key --init
sudo pacman-key --populate archlinux cachyos
sudo pacman -Syyu
```

### Ключи (GPG)
```bash
sudo pacman-key --init
sudo pacman-key --populate archlinux
sudo pacman-key --refresh-keys
sudo pacman-key --recv-keys <KEYID>
sudo pacman-key --lsign-key <KEYID>
```

### Зеркало устарело
```bash
sudo pacman -Syy                      # принудительно обновить базу
sudo reflector --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist
```

### "failed to commit transaction (failed to allocate memory)"
```bash
# Закройте приложения или добавьте swap
sudo swapon /swapfile
sudo pacman -Syu
```

### База данных заблокирована
```bash
sudo rm /var/lib/pacman/db.lck        # удалить lock-файл
```

### Сборка AUR падает (out of memory)
```bash
# makepkg компилирует в /tmp (в RAM)
# Перенесите в диск:
sudo vim /etc/makepkg.conf
# BUILDDIR=/tmp/makepkg → BUILDDIR=/var/tmp/makepkg

# Или добавьте swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## ⚙️ CachyOS особенности

CachyOS использует оптимизированные репозитории:

```bash
# Репозитории CachyOS (в /etc/pacman.conf)
[cachyos]                             # оптимизированные пакеты
[cachyos-v3]                          # v3 (AVX2, для новых CPU)
[cachyos-core-v3]                     # ядро v3
```

### Специфичные команды CachyOS
```bash
# Управление ядром
sudo cachyos-rate-mirrors             # обновить зеркала
cachy-bugreport                       # отчёт для баг-репорта

# Утилиты CachyOS
chwd                                  # CachyOS Hardware Detection
sudo cachyos-kernel-manager           # GUI для управления ядром

# Оптимизация (CPU governor)
sudo cachyos-settings-manager

# Hello / Welcome app
cachyhello                            # приветственное приложение
```

### Выбор ядра
```bash
# CachyOS предлагает несколько ядер:
# linux-cachyos          — BORE scheduler (по умолчанию, рекомендуется)
# linux-cachyos-bore     — BORE
# linux-cachyos-eevdf    — EEVDF
# linux-cachyos-lts      — LTS
# linux-cachyos-bore-lts — LTS + BORE
# linux-zen              — Zen (vanilla)
# linux                  — vanilla

sudo pacman -S linux-cachyos linux-cachyos-headers
```

---

## 🆚 pacman vs apt vs dnf

| Действие | pacman (Arch) | apt (Debian/Ubuntu) | dnf (Fedora) |
|---|---|---|---|
| Установить | `pacman -S` | `apt install` | `dnf install` |
| Удалить | `pacman -Rns` | `apt remove` / `purge` | `dnf remove` |
| Обновить список | `pacman -Sy` | `apt update` | `dnf check-update` |
| Обновить пакеты | `pacman -Su` | `apt upgrade` | `dnf upgrade` |
| Полное обновление | `pacman -Syu` | `apt update && upgrade` | `dnf upgrade` |
| Поиск | `pacman -Ss` | `apt search` | `dnf search` |
| Инфо | `pacman -Si` | `apt show` | `dnf info` |
| Список файлов пакета | `pacman -Ql` | `dpkg -L` | `rpm -ql` |
| Кому принадлежит файл | `pacman -Qo` | `dpkg -S` | `rpm -qf` |

---

## 🪤 Частые ошибки и грабли

1. **`pacman -Sy <pkg>`** — НЕЛЬЗЯ. Только `-Syu`. Иначе partial upgrade.
2. **AUR без проверки** — всегда читайте PKGBUILD.
3. **`makepkg` от root** — нельзя. Только обычный пользователь.
4. **Удаление csrf** — `pacman -Rdd` без проверки может сломать систему.
5. **Игнорирование `linux`** — ядро надо обновлять вместе с системой.
6. **Забытый `.pacnew`** — проверяйте после обновлений (`pacdiff`).
7. **AUR для критичного софта** — AUR не получает автообновления безопасности.
8. **Кэш переполнен** — `/var/cache/pacman/pkg/` разрастается. `paccache -r`.
9. **Зеркала не синхронны** — `pacman -Syyu` если "target not found".
10. **Чистка `pacman -Scc`** — удалит кэш, не сможете откатиться.

---

## 🔗 Полезные ссылки

- Arch Wiki: Pacman: https://wiki.archlinux.org/title/Pacman
- Arch Wiki: AUR: https://wiki.archlinux.org/title/Arch_User_Repository
- Arch Wiki: makepkg: https://wiki.archlinux.org/title/Makepkg
- Arch Package Search: https://archlinux.org/packages
- AUR: https://aur.archlinux.org
- Arch Linux Archive: https://archive.archlinux.org
- CachyOS Wiki: https://wiki.cachyos.org
- pacman rosetta (сравнение): https://wiki.archlinux.org/title/Pacman/Rosetta

---

## 💡 Полезные советы

1. **`pacman -Syu`** — единственный правильный способ обновления.
2. **`-Rns`** для удаления — с зависимостями и конфигами.
3. **paru/yay** — почти как pacman, но с AUR. `paru` (= без флагов) обновляет всё.
4. **Чистите кэш**: `sudo paccache -r` или включите `paccache.timer`.
5. **Чистите сироты**: `paru -Rns $(paru -Qdtq)`.
6. **Зеркала**: `reflector` или `rate-mirrors` регулярно.
7. **Читайте новости**: https://archlinux.org/news перед крупными обновлениями.
8. **`.pacnew`**: `sudo pacdiff` после обновлений.
9. **Резервная копия списка пакетов**: `pacman -Qqe > pkglist.txt`.
10. **Не используйте AUR для base-системы** — только для пользовательского софта.
11. **`paru -Ps`** — статистика: сколько пакетов, сколько из AUR и т.д.
12. **`pactree`** — для понимания зависимостей сложных пакетов.
13. **CachyOS**: используйте `linux-cachyos` (BORE scheduler) для лучшей отзывчивости.
14. **HoldPkg** в pacman.conf — критичные пакеты (pacman, glibc) спросят подтверждение.
15. **`CheckSpace`** в pacman.conf — проверяет, есть ли место перед установкой.

---

*Сгенерировано как шпаргалка. pacman прост, но Arch требует понимания —
углубляйтесь через https://wiki.archlinux.org/ и `pacman --help`*

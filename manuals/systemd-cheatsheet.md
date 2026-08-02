# ⚙️ systemd — шпаргалка по управлению службами

> **systemd** — система инициализации (init) и менеджер служб в современных Linux.
> Заменяет SysV init. Управляет сервисами, таймерами, сокетами, монтированием.
> Документация: https://systemd.io · `man systemd`

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **unit (юнит)** | Любой ресурс, которым управляет systemd (service, timer, socket...) |
| **target** | Группа юнитов (аналог runlevel: `multi-user.target`, `graphical.target`) |
| **service** | Служба/демон (как `nginx.service`) |
| **timer** | Запуск по расписанию (замена cronу) |
| **socket** | Сокет-активация (сокет создаётся до запуска службы) |
| **journal** | Логи systemd (`journalctl`) |
| **machine-id** | Уникальный ID машины |

Команды управления: **`systemctl`** (юниты) и **`journalctl`** (логи).

---

## 🚀 systemctl — управление службами

### Базовые операции с сервисом
| Команда | Действие |
|---|---|
| `systemctl status nginx` | Статус службы (жива ли, последние логи) |
| `systemctl start nginx` | Запустить |
| `systemctl stop nginx` | Остановить |
| `systemctl restart nginx` | Перезапустить |
| `systemctl reload nginx` | Перечитать конфиг (без остановки) |
| `systemctl try-restart nginx` | Перезапустить только если была запущена |
| `systemctl reload-or-restart nginx` | reload если поддерживает, иначе restart |

### Управление автозапуском
| Команда | Действие |
|---|---|
| `systemctl enable nginx` | Включить автозапуск при загрузке |
| `systemctl disable nginx` | Отключить автозапуск |
| `systemctl enable --now nginx` | Включить автозапуск + запустить сейчас |
| `systemctl disable --now nginx` | Отключить автозапуск + остановить |
| `systemctl is-enabled nginx` | Проверить автозапуск (`enabled`/`disabled`) |
| `systemctl is-active nginx` | Запущена ли сейчас (`active`/`inactive`) |
| `systemctl is-failed nginx` | В ошибочном состоянии? |
| `systemctl reenable nginx` | disable + enable (применить изменения symlink) |
| `systemctl preset nginx` | Применить default-политику дистрибутива |

### Маскировка (запрет)
```bash
systemctl mask nginx         # жёстко запретить (нельзя даже запустить вручную)
systemctl unmask nginx       # снять запрет
```

> Разница: `disable` убирает только автозапуск, но службу можно запустить
> вручную. `mask` делает юнит недоступным совсем (ссылка на `/dev/null`).

---

## 📋 Просмотр юнитов

### Списки
```bash
systemctl list-units                      # все активные юниты
systemctl list-units --all                # включая неактивные
systemctl list-units --type=service       # только сервисы
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=failed
systemctl list-units --type=mount         # точки монтирования
systemctl list-units --type=socket        # сокеты
systemctl list-units --type=timer         # таймеры
systemctl list-unit-files                 # все установленные (не только активные)
systemctl list-unit-files --type=service --state=enabled
systemctl list-sockets                    # сокеты с активацией
systemctl list-timers                     # все таймеры (как cron)
systemctl list-dependencies nginx         # дерево зависимостей
systemctl list-jobs                       # текущие jobs
```

### Поиск и проверка
```bash
systemctl status nginx                    # статус + последние логи
systemctl status nginx.service -l         # + полный вывод логов
systemctl cat nginx                       # показать сам файл юнита
systemctl show nginx                      # все свойства (machine-readable)
systemctl show nginx -p ExecStart         # конкретное свойство
systemctl show -p ActiveState nginx       # только активное состояние
systemctl list-dependencies nginx         # что требует
systemctl list-dependencies --reverse nginx   # кто требует nginx
```

---

## 🖥️ Управление системой (машиной)

| Команда | Действие |
|---|---|
| `systemctl reboot` | Перезагрузка |
| `systemctl poweroff` | Выключение |
| `systemctl halt` | Остановить систему |
| `systemctl suspend` | Ждущий режим (S3) |
| `systemctl hibernate` | Гибернация (на диск) |
| `systemctl hybrid-sleep` | Гибридный сон |
| `systemctl suspend-then-hibernate` | Сон → потом гибернация |
| `systemctl rescue` | Однопользовательский режим (rescue) |
| `systemctl emergency` | Аварийный режим (минимум) |
| `systemctl default` | Запустить default target |
| `systemctl get-default` | Текущий target по умолчанию |
| `systemctl set-default multi-user.target` | Загружаться в текстовом режиме |
| `systemctl set-default graphical.target` | Загружаться в графическом режиме |

### Targets (аналоги runlevel)
| Target | Runlevel | Описание |
|---|---|---|
| `poweroff.target` | 0 | Выключение |
| `rescue.target` | 1 | Однопользовательский |
| `multi-user.target` | 3 | Многопользовательский (текстовый) |
| `graphical.target` | 5 | Графический |
| `reboot.target` | 6 | Перезагрузка |

---

## 📝 Создание собственного сервиса

### Расположение файлов юнитов
| Путь | Приоритет | Назначение |
|---|---|---|
| `/etc/systemd/system/` | высокий | Администратор (override'ы тут) |
| `/run/systemd/system/` | средний | Runtime |
| `/usr/lib/systemd/system/` | низкий | Пакетный менеджер |
| `~/.config/systemd/user/` | — | Пользовательские сервисы |

> Чтобы изменить пакетный юнит, используйте `systemctl edit nginx` —
> создаст drop-in файл в `/etc/systemd/system/nginx.service.d/`.

### Базовый пример `.service`
```ini
[Unit]
Description=My Python App
Documentation=https://myapp.example.com
After=network-online.target
Wants=network-online.target
# After — после чего запускать
# Requires — жёсткая зависимость (упадёт — упадёт и этот)
# Wants — мягкая зависимость
# Conflicts — с чем конфликтует

[Service]
Type=simple                      # simple/forking/oneshot/notify/dbus
User=myapp                       # от какого пользователя
Group=myapp
WorkingDirectory=/opt/myapp
Environment="NODE_ENV=production"
EnvironmentFile=-/etc/myapp/env  # файл с переменными (- = необязательно)
ExecStart=/usr/bin/python3 /opt/myapp/main.py
ExecStartPre=/usr/bin/install -d /var/log/myapp
ExecStartPost=/usr/bin/touch /var/run/myapp.started
ExecStop=/usr/bin/kill -TERM $MAINPID
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure               # no/on-failure/always/on-abnormal
RestartSec=5s
TimeoutStartSec=30
TimeoutStopSec=30
KillMode=control-group
KillSignal=SIGTERM

# Жёстение/ограничения (sandboxing)
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/myapp /var/log/myapp
ReadOnlyPaths=/etc/myapp
CapabilityBoundingSet=
AmbientCapabilities=
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6
RestrictNamespaces=true
LockPersonality=true
RestrictRealtime=true
RestrictSUIDSGID=true
SystemCallFilter=@system-service
SystemCallArchitectures=native

[Install]
WantedBy=multi-user.target       # в каком target'е активировать
```

### Типы служб (Type=)
| Тип | Описание |
|---|---|
| `simple` | Процесс не разветвляется, считается запущенным сразу (по умолчанию) |
| `exec` | Как simple, но ждёт `execve()` (3.0+) |
| `forking` | Классический демон: разветвляется, родитель выходит |
| `oneshot` | Одноразовая задача, выполняется и завершается |
| `notify` | Служба сама сигнализирует о готовности через sd_notify |
| `idle` | Запуск когда idle (для терминалов) |
| `dbus` | Готова когда имя D-Bus приобретено |

### Полный цикл установки сервиса
```bash
# 1. Создать файл
sudo nano /etc/systemd/system/myapp.service

# 2. Перечитать конфигурацию systemd
sudo systemctl daemon-reload

# 3. Включить автозапуск + запустить
sudo systemctl enable --now myapp

# 4. Проверить статус
sudo systemctl status myapp
sudo journalctl -u myapp -f      # смотреть логи

# 5. Если правки в файле — снова daemon-reload + restart
sudo systemctl daemon-reload
sudo systemctl restart myapp
```

### Drop-in (переопределение части юнита)
```bash
# Создаёт override в /etc/systemd/system/nginx.service.d/override.conf
systemctl edit nginx

# Полный файл (не только override)
systemctl edit --full nginx

# После правки:
systemctl daemon-reload
systemctl restart nginx
```

Пример override (перезапуск при падении + лимит файлов):
```ini
# /etc/systemd/system/nginx.service.d/override.conf
[Service]
Restart=always
RestartSec=5s
LimitNOFILE=65536
```

---

## ⏰ Таймеры (замена cronу)

systemd timers мощнее cron'а: зависимости, условия, точность, логи в journal.

### Пример `.timer`
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=*-*-* 03:00:00          # ежедневно в 3:00
Persistent=true                    # запустить пропущенное (если ПК был выключен)
AccuracySec=1min                   # точность

# Альтернативы OnCalendar:
# OnBootSec=5min              # через 5 минут после загрузки
# OnUnitActiveSec=1h          # каждый час после активации
# OnUnitInactiveSec=30min     # через 30 минут после деактивации
# OnCalendar=weekly           # раз в неделю
# OnCalendar=Mon *-*-* 03:00:00  # по понедельникам
# OnCalendar=*:0/15           # каждые 15 минут

[Install]
WantedBy=timers.target
```

### Таймер + сервис
```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Run backup script

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

```bash
# Установка
sudo systemctl enable --now backup.timer
systemctl list-timers               # проверить
systemctl list-timers backup.timer
systemctl start backup.service      # запустить вручную (без таймера)
systemctl status backup.timer
```

### Сравнение синтаксиса OnCalendar с cron
```
cron:        */15 * * * *      (каждые 15 мин)
OnCalendar:  *:0/15            (то же)
cron:        0 3 * * *         (каждый день в 3:00)
OnCalendar:  *-*-* 03:00:00
cron:        0 0 * * 0         (воскресенье в полночь)
OnCalendar:  Sun *-*-* 00:00:00
```

### Пользовательские таймеры
```bash
# В ~/.config/systemd/user/mytask.timer и mytask.service
systemctl --user daemon-reload
systemctl --user enable --now mytask.timer
systemctl --user list-timers

# Чтобы работали после выхода:
loginctl enable-linger $USER
```

---

## 📜 journalctl — чтение логов

### Базовый просмотр
```bash
journalctl                          # все логи (с самого начала)
journalctl -b                       # с последней загрузки
journalctl -b -1                    # с предпоследней загрузки
journalctl --list-boots             # список загрузок
journalctl -k                       # только ядро (kernel, =dmesg)
journalctl -f                       # следить в реальном времени (tail -f)
journalctl -n 50                    # последние 50 строк
journalctl -n 50 -f                 # последние + следить
journalctl --no-pager               # без пейджера (для пайпов)
journalctl -r                       # в обратном порядке (новые сверху)
journalctl -o cat                   # только сообщение (без метаданных)
journalctl -o json                  # в JSON
journalctl -o json-pretty
journalctl -o short-iso             # формат ISO-времени
journalctl -o verbose               # подробно
```

### Фильтрация
```bash
# По сервису
journalctl -u nginx                 # только nginx
journalctl -u nginx -u php-fpm      # несколько
journalctl -u nginx.service
journalctl _COMM=nginx              # по имени исполняемого

# По времени
journalctl --since today
journalctl --since "2024-01-15" --until "2024-01-16"
journalctl --since "09:00" --until "10:00"
journalctl --since "1 hour ago"
journalctl --since yesterday
journalctl --since "3 days ago"

# По приоритету (syslog)
journalctl -p err                   # ошибки и хуже
journalctl -p warning
journalctl -p 3                     # числом: 0-7
# 0=emerg 1=alert 2=crit 3=err 4=warning 5=notice 6=info 7=debug

# По процессу/пользователю
journalctl _PID=1234
journalctl _UID=1000
journalctl _GID=100
journalctl _COMM=bash

# Комбинированный фильтр
journalctl -u nginx -p err --since yesterday
journalctl -u nginx --since "2 hours ago" | grep ERROR
```

### Очистка логов
```bash
journalctl --disk-usage             # сколько занимают логи
journalctl --vacuum-size=100M       # оставить только 100 МБ
journalctl --vacuum-time=2weeks     # удалить логи старше 2 недель
journalctl --vacuum-files=10        # оставить 10 файлов

# Постоянная настройка в /etc/systemd/journald.conf:
# SystemMaxUse=500M
# MaxRetentionSec=1month
sudo systemctl restart systemd-journald
```

### Логирование в journal из скрипта
```bash
logger "Моё сообщение"                       # базово
logger -t myapp "Запущен"                    # с тегом
logger -p user.err "Ошибка валидации"        # с приоритетом
echo "текст" | logger -t myscript            # из пайпа
```

```python
# Из Python
import logging.handlers
handler = logging.handlers.SysLogHandler(address="/dev/log")
logger = logging.getLogger("myapp")
logger.addHandler(handler)
logger.error("Something went wrong")
```

---

## 🔌 Сокет-активация

Сокет создаётся заранее, служба запускается при первом подключении.

```ini
# /etc/systemd/system/myapp.socket
[Unit]
Description=My App Socket

[Socket]
ListenStream=8080            # порт TCP
# ListenDatagram=8080        # UDP
# ListenStream=/tmp/myapp.sock   # UNIX-сокет

[Install]
WantedBy=sockets.target
```

```ini
# /etc/systemd/system/myapp.service
[Service]
ExecStart=/usr/bin/myapp
```

```bash
sudo systemctl enable --now myapp.socket
# myapp.service запустится автоматически при подключении к порту 8080
```

Примеры: `sshd.socket`, `cups.socket`, `docker.socket`.

---

## 🏠 Пользовательские сервисы (--user)

systemd может управлять сервисами от обычного пользователя (без sudo).

```bash
# Расположение
~/.config/systemd/user/

# Команды (с --user)
systemctl --user status myapp
systemctl --user start myapp
systemctl --user enable myapp
systemctl --user list-units
systemctl --user list-timers
systemctl --user daemon-reload

# Логи
journalctl --user -u myapp
journalctl --user -f

# Чтобы сервисы работали когда пользователь не залогинен:
loginctl enable-linger $USER
loginctl disable-linger $USER
loginctl show-user $USER
```

Пример пользовательского сервиса (например, синхронизация):
```ini
# ~/.config/systemd/user/sync.service
[Unit]
Description=Sync files

[Service]
Type=oneshot
ExecStart=/home/me/bin/sync.sh
```

```ini
# ~/.config/systemd/user/sync.timer
[Unit]
Description=Run sync every hour

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h

[Install]
WantedBy=timers.target
```

---

## 🌐 hostnamectl, localectl, timedatectl, loginctl

### hostnamectl — имя хоста
```bash
hostnamectl                          # информация о системе
hostnamectl set-hostname myserver
hostnamectl set-hostname --pretty "My Production Server"
hostnamectl set-icon-name computer
hostnamectl set-chassis server       # desktop/laptop/server/vm/container
```

### localectl — локаль и раскладка
```bash
localectl status
localectl list-locales
localectl set-locale LANG=ru_RU.UTF-8
localectl set-locale LC_TIME=en_US.UTF-8
localectl list-keymaps
localectl set-keymap us              # раскладка в консоли
localectl set-x11-keymap us         # в X11/Wayland
localectl set-x11-keymap us,ru "" "grp:alt_shift_toggle"
```

### timedatectl — время и часовой пояс
```bash
timedatectl status                   # текущее состояние
timedatectl list-timezones
timedatectl set-timezone Europe/Moscow
timedatectl set-time "2024-01-15 14:30:00"
timedatectl set-ntp true             # включить синхронизацию (chronyd/systemd-timesyncd)
timedatectl set-ntp false
```

### loginctl — сессии и пользователи
```bash
loginctl list-sessions               # активные сессии
loginctl list-users
loginctl session-status $SID
loginctl user-status $USER
loginctl lock-session                # заблокировать
loginctl terminate-session $SID
loginctl kill-user $USER
loginctl enable-linger $USER         # запускать --user сервисы без логина
```

---

## 🔧 Анализ производительности

### systemd-analyze
```bash
systemd-analyze                       # время загрузки
systemd-analyze time
systemd-analyze blame                 # топ медленных юнитов
systemd-analyze critical-chain        # критический путь загрузки
systemd-analyze critical-chain nginx  # для конкретного сервиса
systemd-analyze plot > boot.svg       # график загрузки (SVG!)
systemd-analyze calendar "Mon *-*-* 09:00"   # проверить выражение timer
systemd-analyze calendar "*:0/15"     # расшифровать OnCalendar
systemd-analyze log-level debug       # уровень логирования systemd
systemd-analyze cat-config            # показать все конфиги
systemd-analyze verify /etc/systemd/system/myapp.service   # проверить файл
```

### Пример вывода blame
```
$ systemd-analyze blame
3.215s NetworkManager-wait-online.service
1.890s dev-sda1.device
 820ms systemd-journal-flush.service
 450ms udisks2.service
```

---

## 🛠️ systemd-cgls, systemd-cgtop — cgroups

systemd управляет всеми процессами через **cgroups** (control groups).

```bash
systemd-cgls                  # дерево процессов по cgroups
systemd-cgls systemd.slice    # конкретная slice
systemd-cgtop                 # top по cgroups (CPU, память, I/O)
systemd-cgls /user.slice      # пользовательские процессы

# Посмотреть cgroup процесса
cat /proc/$PID/cgroup
ps -o pid,cgroup -p $PID
```

### Убить все процессы службы
```bash
systemctl kill nginx
systemctl kill --signal=SIGKILL nginx
systemctl kill --kill-who=control nginx
```

---

## 🔍 Отладка и траблшутинг

### Сервис не запускается
```bash
# 1. Статус + последние логи
systemctl status nginx
systemctl status nginx -l         # полный вывод

# 2. Подробные логи
journalctl -u nginx -n 50 --no-pager
journalctl -u nginx -f            # следить

# 3. Проверить синтаксис файла
systemd-analyze verify /etc/systemd/system/myapp.service

# 4. Проверить зависимости
systemctl list-dependencies myapp
systemctl list-dependencies --reverse myapp

# 5. Запустить вручную (ту же команду, что в ExecStart)
/usr/bin/python3 /opt/myapp/main.py

# 6. Включить debug systemd
systemd-analyze log-level debug
journalctl -f
systemd-analyze log-level info     # вернуть обратно
```

### Режим rescue / emergency (если не загружается)
```bash
# В GRUB нажмите 'e', добавьте в строку linux:
systemd.unit=rescue.target         # однопользовательский
systemd.unit=emergency.target      # минимальный (только root)
# или
init=/bin/bash                     # совсем базово
```

### Конфликт/порт занят
```bash
# Кто слушает порт?
ss -tlnp | grep :80
sudo lsof -i :80
sudo fuser 80/tcp

# Найти процесс
ps aux | grep nginx
systemctl status <pid>
```

### Recovery после изменений
```bash
# Если сломали загрузку через bad unit:
# 1. Загрузиться в rescue mode
# 2. Переименовать/удалить проблемный юнит
# 3. systemctl daemon-reload
# 4. reboot
```

---

## 📦 Логирование и лог-уровни

### Syslog priorities
| Код | Имя | Когда использовать |
|---|---|---|
| 0 | emerg | Система неработоспособна |
| 1 | alert | Требует немедленного действия |
| 2 | crit | Критическая ошибка |
| 3 | err | Ошибка |
| 4 | warning | Предупреждение |
| 5 | notice | Важное нормальное событие |
| 6 | info | Информационное |
| 7 | debug | Отладочное |

### Дебаг конкретной службы
```bash
# Включить debug через override
sudo systemctl edit myapp
```
```ini
[Service]
Environment=SYSTEMD_LOG_LEVEL=debug
```
```bash
sudo systemctl restart myapp
journalctl -u myapp -f
```

---

## 🌍 Переменные окружения в сервисах

```ini
[Service]
Environment="KEY1=value1" "KEY2=value2"
EnvironmentFile=/etc/myapp/env.conf
# В env.conf:
# KEY=value
# (без export, построчно)
```

```bash
# Просмотр переменных запущенного процесса
systemctl show myapp -p Environment
cat /proc/$(systemctl show -p MainPID --value myapp)/environ | tr '\0' '\n'
```

---

## 🧩 networkd, resolved, timesyncd

systemd включает набор системных демонов:

### systemd-networkd — сеть
```bash
systemctl status systemd-networkd
# Конфиги в /etc/systemd/network/
# *.network — настройки интерфейсов
# *.link — параметры устройств
# *.netdev — виртуальные устройства
networkctl status
networkctl list
networkctl reload
```

### systemd-resolved — DNS
```bash
systemctl status systemd-resolved
resolvectl status
resolvectl query example.com        # DNS-запрос
resolvectl domain                   # домены
# /etc/resolv.conf → symlink на /run/systemd/resolve/stub-resolv.conf
```

### systemd-timesyncd — NTP
```bash
systemctl status systemd-timesyncd
timedatectl status                  # показывает NTP service
timedatectl timesync-status
timedatectl show-timesync
```

---

## 📊 Полезные команды одной строкой

```bash
# Все упавшие сервисы
systemctl --failed
systemctl list-units --state=failed

# Перезапустить все включённые сервисы
systemctl list-units --type=service --state=running --no-legend | awk '{print $1}' | xargs systemctl restart

# Найти самые медленно запускающиеся
systemd-analyze blame | head -20

# Топ потребления CPU службами
systemd-cgtop

# Все таймеры как cron
systemctl list-timers --all

# Логи за сегодня с ошибками
journalctl --since today -p err

# Список всех юнитов, которые перезапускаются при падении
systemctl list-unit-files --type=service | grep enabled | awk '{print $1}' | \
    xargs -I{} sh -c 'systemctl show {} -p Restart | grep -q "no" || echo {}'
```

---

## 🆚 Сравнение с традиционными командами

| Традиция | systemd | Примечание |
|---|---|---|
| `service nginx start` | `systemctl start nginx` | |
| `service nginx status` | `systemctl status nginx` | |
| `chkconfig nginx on` | `systemctl enable nginx` | RHEL/CentOS |
| `update-rc.d nginx enable` | `systemctl enable nginx` | Debian |
| `/etc/init.d/nginx restart` | `systemctl restart nginx` | |
| `tail -f /var/log/nginx.log` | `journalctl -u nginx -f` | централизованно |
| `cron` | `systemctl list-timers` | timers мощнее |
| `runlevel` | `systemctl get-default` | |
| `telinit 3` | `systemctl isolate multi-user.target` | |
| `halt`/`reboot`/`poweroff` | `systemctl halt/reboot/poweroff` | (алиасы работают) |
| `hostname` | `hostnamectl` | |
| `date` | `timedatectl` | |
| `locale` | `localectl` | |

---

## 🪤 Частые ошибки и грабли

1. **Забыть `daemon-reload`** после правки `.service` файла — изменения не применятся.
2. **`enable` не запускает сервис** — только `enable --now` или отдельно `start`.
3. **`ExecStart` с путями** — всегда полные пути (`/usr/bin/python3`, не `python3`).
4. **Environment в кавычках** — `Environment="A=1" "B=2"`, не построчно.
5. **Type=forking без PIDFile** — systemd не узнает главный процесс.
6. **`Restart=always` для oneshot** — приведёт к зацикливанию.
7. **`User=` без absolute paths** — относительные пути ломаются.
8. **Привилегии в user-сервисах** — `--user` сервисы не могут биндить порты <1024.
9. **`systemctl edit` vs `--full`** — `edit` создаёт override (не затирает оригинал).
10. **`mask` vs `disable`** — `mask` полностью запрещает юнит.
11. **Логи в /var/log** — некоторые сервисы пишут сами, не в journal.
12. **`After=` vs `Requires=`** — After только порядок, Requires — зависимость.
13. **Сетевые сервисы без `After=network.target`** — могут стартовать до сети.

---

## 🔗 Полезные ссылки

- Официальный сайт: https://systemd.io
- man pages: `man systemd`, `man systemctl`, `man journalctl`, `man systemd.service`
- systemd по-русски: https://wiki.archlinux.org/title/Systemd_(Русский)
- Lennart's blog (автор): https://0pointer.net/blog/
- systemd-by-example: https://systemd-by-example.com
- Песочница юнитов: https://wiki.archlinux.org/title/Systemd#Sandboxing

---

## 💡 Полезные советы

1. **`systemctl status` без аргументов** — обзор системы (топ активных юнитов).
2. **`-b` в journalctl** — только с этой загрузки, спасает от спама историей.
3. **`--since`/`--until`** в journalctl — мощнее, чем grep по времени.
4. **`journalctl -p err`** — только ошибки, для быстрого траблшутинга.
5. **`systemd-analyze verify file.service`** — проверяйте новые юниты перед установкой.
6. **`systemctl edit`** — не правьте `/usr/lib/systemd/system/` напрямую (затрётся обновлением).
7. **`enable-linger`** — для user-сервисов, чтобы работали без активной сессии.
8. **`PrivateTmp=true`** — изолирует `/tmp` сервиса (безопасность).
9. **`ProtectSystem=strict`** — делает `/` read-only (только для чтения).
10. **`RestrictAddressFamilies`** — ограничивает сетевые вызовы сервиса.
11. **Timers вместо cron** — логи в journal, зависимости, условия, точность.
12. **`systemd-cgtop`** — мониторинг ресурсов по cgroups (кто жрёт CPU/RAM).
13. **`systemd-analyze blame`** — для оптимизации времени загрузки.
14. **Drop-in файлы** — переопределяйте части юнита, не трогая оригинал.
15. **`Type=notify`** — для сервисов, которые должны точно знать о готовности.

---

*Сгенерировано как шпаргалка. systemd огромен —
углубляйтесь через `man systemd`, `man systemd.service` и https://systemd.io*

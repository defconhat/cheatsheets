# 🐧 Linux Internals — шпаргалка (procfs / sysfs / cgroups / namespaces)

> Внутреннее устройство Linux: виртуальные ФС, контроль ресурсов, изоляция.
> То, на чём строятся Docker, systemd, top, ps и другие инструменты.
> Документация: `man proc` · `man sysfs` · https://www.kernel.org/doc/html/latest/admin-guide

---

## 📁 /proc — procfs (процессы и ядро)

Виртуальная файловая система: **информация о процессах и ядре**.
Не занимает места на диске — генерируется на лету.

### Процессы

```
/proc/<pid>/            # информация о процессе
├── cmdline             # команда запуска (с аргументами, \0-разделитель)
├── cwd → /path         # симлинк на текущий каталог
├── exe → /path         # симлинк на исполняемый файл
├── environ             # переменные окружения (\0-разделитель)
├── status              # статус (читаемо)
├── stat                # статус (для парсинга)
├── io                  # статистика ввода-вывода
├── maps                # карта памяти
├── mem                 # память процесса (нужны права)
├── fd/                 # файловые дескрипторы
│   ├── 0 → /dev/pts/0  # stdin
│   ├── 1 → ...         # stdout
│   └── 2 → ...         # stderr
├── mounts              # что примонтировано (для процесса)
├── net/                # сетевое пространство (namespaces)
├── ns/                 # namespace'ы процесса
└── cgroup              # в каких cgroup состоит
```

```bash
# Примеры
cat /proc/$$/cmdline | tr '\0' ' '         # команда текущего shell
cat /proc/1/status | head                  # init/systemd
cat /proc/$(pgrep nginx | head -1)/environ | tr '\0' '\n'   # env nginx

ls -la /proc/1234/fd/                      # открытые файлы процесса
readlink /proc/1234/exe                    # путь к бинарнику
readlink /proc/1234/cwd                    # текущий каталог

# Кто держит файл открытым
ls -l /proc/*/fd/* 2>/dev/null | grep filename

# Все процессы и их команды
ps -e -o pid,cmd        # = читает /proc
```

### Системная информация

```bash
cat /proc/cpuinfo                         # процессоры
cat /proc/meminfo                         # память
cat /proc/loadavg                         # load average
cat /proc/uptime                          # время работы (сек)
cat /proc/version                         # версия ядра
cat /proc/cmdline                         # параметры загрузки ядра

cat /proc/filesystems                     # поддерживаемые ФС
cat /proc/mounts                          # примонтированные ФС

# Сеть
cat /proc/net/tcp                         # TCP-соединения
cat /proc/net/udp
cat /proc/net/dev                         # статистика интерфейсов
cat /proc/net/route                       # таблица маршрутов

# Железо
cat /proc/interrupts                      # прерывания
cat /proc/dma
cat /proc/ioports
cat /proc/iomem
```

### Динамическая настройка ядра

```bash
# /proc/sys — настраиваемые параметры (sysctl)
cat /proc/sys/net/ipv4/ip_forward         # статус IP-форвардинга
echo 1 > /proc/sys/net/ipv4/ip_forward    # включить (временно!)

# Безопаснее через sysctl
sudo sysctl -w net.ipv4.ip_forward=1
# Постоянно — в /etc/sysctl.d/*.conf
```

---

## 🎛️ /sys — sysfs (устройства и драйверы)

Информация о **устройствах, драйверах, ядре** (введено в 2.6).

```
/sys/
├── block/               # блочные устройства (sda, nvme0n1)
│   └── sda/
│       ├── size         # размер в блоках
│       ├── device/model # модель
│       └── stat         # статистика I/O
├── bus/                 # шины (pci, usb, ...)
├── class/               # классы устройств
│   ├── net/             # сетевые интерфейсы
│   │   └── eth0/
│   │       ├── address  # MAC
│   │       ├── mtu
│   │       └── statistics/
│   ├── block/           # блочные
│   ├── tty/             # терминалы
│   └── hwmon/           # датчики (temp, fan)
├── dev/                 # устройства по типу (char, block)
├── devices/             # дерево устройств (по шинам)
├── firmware/            # прошивки (ACPI, EFI)
├── fs/                  # файловые системы
├── kernel/              # ядро
│   ├── hostname
│   ├── ostype
│   └── mm/              # memory management
├── module/              # загруженные модули
└── power/               # управление питанием
```

```bash
# Примеры
cat /sys/class/net/enp4s0/address        # MAC-адрес
cat /sys/class/hwmon/hwmon2/temp1_input  # температура (÷1000 = °C)
cat /sys/block/sda/size                  # размер в 512-байт блоках
cat /sys/block/nvme0n1/device/model      # модель SSD

# Сетевые интерфейсы
ls /sys/class/net/

# Загруженные модули
ls /sys/module/

# Bluetooth, USB и т.п.
ls /sys/bus/usb/devices/
```

### Управление через sysfs
```bash
# Включить/выключить светодиод
echo 1 > /sys/class/leds/input0::capslock/brightness

# Изменить яркость экрана
echo 500 > /sys/class/backlight/intel_backlight/brightness

# Перезагрузить PCI-устройство
echo 1 > /sys/bus/pci/devices/0000:00:00.0/reset

# Отмонтировать USB
echo 1 > /sys/bus/usb/devices/1-2/remove
```

---

## 📊 cgroups (Control Groups)

**Контроль ресурсов** процессов: CPU, RAM, I/O, сеть.
Используется systemd, Docker, Kubernetes, LXC.

### Версии
- **cgroup v1** — старая, по контроллеру на иерархию.
- **cgroup v2** — унифицированная (рекомендуется, дефолт в новых ядрах).

```bash
# Какая версия
stat -fc %T /sys/fs/cgroup/
# cgroup2fs — v2
# tmpfs — v1

# Mount
mount | grep cgroup
```

### Иерархия cgroup v2
```
/sys/fs/cgroup/
├── cpu.weight             # вес CPU
├── memory.max             # лимит памяти (всех детей)
├── io.max                 # I/O лимиты
├── user.slice/            # пользовательские процессы
├── system.slice/          # системные сервисы
│   ├── docker.service/
│   │   ├── cpu.max
│   │   ├── memory.max
│   │   └── cgroup.procs   # PID'ы
└── ...
```

### Управление cgroup v2 вручную
```bash
# Создать группу
sudo mkdir /sys/fs/cgroup/myapp

# Лимит памяти (50MB)
echo 52428800 | sudo tee /sys/fs/cgroup/myapp/memory.max

# CPU weight (1-10000)
echo 100 | sudo tee /sys/fs/cgroup/myapp/cpu.weight

# CPU max (полное ядро = 100000/100000)
echo "100000 100000" | sudo tee /sys/fs/cgroup/myapp/cpu.max

# Добавить процесс
echo $$ | sudo tee /sys/fs/cgroup/myapp/cgroup.procs

# Посмотреть использование
cat /sys/fs/cgroup/myapp/memory.current
cat /sys/fs/cgroup/myapp/cpu.stat
```

### Контроллеры cgroup v2
| Контроллер | Что |
|---|---|
| `cpu` | CPU time, weight, max |
| `cpuset` | На каких ядрах |
| `memory` | RAM, swap |
| `io` | I/O (BPS, IOPS) |
| `pids` | Макс. число процессов |
| `rdma` | RDMA ресурсы |
| `hugetlb` | Huge pages |
| `devices` | Доступ к устройствам (только v1) |
| `freezer` | Заморозка процессов (в v2 встроено) |
| `net_cls` / `net_prio` | Сетевые теги (только v1) |

### cgroup через systemd
systemd управляет cgroups автоматически:
```bash
# Запустить сервис с лимитами
sudo systemd-run --uid=1000 --gid=1000 \
    --property=MemoryMax=500M \
    --property=CPUQuota=50% \
    --property=IOWeight=10 \
    --unit=myapp --slice=user-1000.slice \
    /usr/bin/myapp

# Статус
systemctl status myapp
systemd-cgls                       # дерево cgroups
systemd-cgtop                      # top по cgroups

# Лимиты через .service
# /etc/systemd/system/myapp.service
[Service]
ExecStart=/usr/bin/myapp
MemoryMax=500M
CPUQuota=50%
TasksMax=100
IOWeight=10
```

### Docker и cgroups
```bash
docker run --memory=512m --cpus=1.5 myapp
# = создаёт cgroup в /sys/fs/cgroup/system.slice/docker-<id>/
```

---

## 🌍 Namespaces (изоляция)

**Изоляция ресурсов** — основа контейнеров (Docker, Podman, LXC).
Каждый namespace — отдельное "представление" ресурса.

### Типы namespaces
| Namespace | Что изолирует | С версии |
|---|---|---|
| **mnt** | Точки монтирования (ФС) | 2.4.19 |
| **pid** | PID (номера процессов) | 2.6.24 |
| **net** | Сетевые интерфейсы, порты, маршруты | 2.6.29 |
| **ipc** | IPC (очереди сообщений, semaphores) | 2.6.19 |
| **uts** | Hostname, domainname | 2.6.19 |
| **user** | UID/GID (map) | 3.8 |
| **cgroup** | Cgroup view | 4.6 |
| **time** | Часы (boottime, monotonic) | 5.6 |

### Просмотр namespaces процесса
```bash
ls -la /proc/<pid>/ns/
# lrwxrwxrwx ... ipc -> ipc:[4026531839]
# lrwxrwxrwx ... mnt -> mnt:[4026531840]
# lrwxrwxrwx ... net -> net:[4026531992]
# lrwxrwxrwx ... pid -> pid:[4026531836]
# lrwxrwxrwx ... user -> user:[4026531837]
# lrwxrwxrwx ... uts -> uts:[4026531838]

# Число в скобках — inode; одинаковое = один namespace
```

### Утилиты для namespaces

```bash
# nsenter — выполнить в namespace другого процесса
sudo nsenter -t <pid> -m -u -i -n -p -- bash   # войти в namespaces контейнера
sudo nsenter -t $(pgrep nginx) -n -- ip a      # сеть nginx

# unshare — создать новый namespace и выполнить команду
sudo unshare --fork --pid --mount-proc bash    # новый PID namespace
unshare --user --map-root-user bash            # стать root в новом user ns
sudo unshare --net bash                        # изолированная сеть

# lsns — список всех namespace'ов
lsns                                           # все
lsns -t net                                    # только network
lsns -t pid

# ip netns — управление network namespaces
sudo ip netns add mynet
sudo ip netns list
sudo ip netns exec mynet ip a
sudo ip netns del mynet
```

### Пример: ручной контейнер
```bash
# 1. Создать namespaces
sudo unshare --fork --pid --mount --net --uts --ipc \
    --mount-proc bash

# Внутри:
hostname mycontainer
mount -t proc proc /proc
ip link set lo up

# 2. Это и есть контейнер!
ps aux        # PID 1 — bash
ip a          # своя сеть
mount         # свои точки монтирования
```

### Docker и namespaces
```bash
docker run --pid=host ...        # использовать host PID ns
docker run --network=host ...    # host network ns
docker run --userns=host ...
docker run --uts=host ...

# Все ns процесса-контейнера:
ls -la /proc/$(docker inspect -f '{{.State.Pid}}' container)/ns/
```

---

## 🧩 Связь cgroups + namespaces = контейнеры

| Технология | cgroups | namespaces | Что даёт |
|---|---|---|---|
| Docker | ✅ | ✅ | Контейнеры |
| Podman | ✅ | ✅ | Rootless контейнеры |
| LXC / LXD | ✅ | ✅ | Полноценные Linux-контейнеры |
| Kubernetes pods | ✅ | ✅ (разделяют net) | Оркестрация |
| systemd-nspawn | ✅ | ✅ | Лёгкие контейнеры |
| Firejail | — | ✅ | Песочница для приложений |

---

## 📡 Другие виртуальные ФС

### /dev — устройства
```bash
ls /dev/
# /dev/null —黑洞
# /dev/zero — бесконечные нули
# /dev/random, /dev/urandom — случайные
# /dev/pts/* — псевдотерминалы
# /dev/sda, /dev/nvme0n1 — диски
# /dev/stdin, /dev/stdout, /dev/stderr
# /dev/tcp, /dev/udp — сетевые (только bash)

echo "hello" > /dev/null           # выкинуть вывод
dd if=/dev/zero of=file bs=1M count=10
head -c 16 /dev/urandom | xxd
```

### /tmp — временные файлы
- Часто tmpfs (в RAM) — быстро, но теряется при ребуте.
- Очищается при загрузке (systemd-tmpfiles).

### /run — runtime данные
- PID-файлы, сокеты, lock-файлы.
- tmpfs, очищается при загрузке.
```bash
ls /run/
# /run/user/<uid>/ — пользовательские (XDG_RUNTIME_DIR)
```

### debugfs
```bash
# /sys/kernel/debug — отладочная информация (root)
sudo mount -t debugfs none /sys/kernel/debug
ls /sys/kernel/debug/
```

### tracefs
```bash
# /sys/kernel/tracing — ftrace
sudo cat /sys/kernel/tracing/available_tracers
echo function > /sys/kernel/tracing/current_tracer
echo 1 > /sys/kernel/tracing/tracing_on
cat /sys/kernel/tracing/trace | head
```

---

## 🛠️ Утилиты для интроспекции

### Процессы
```bash
ps aux / ps -ef                # процессы
pstree -p                     # дерево процессов
top / htop / btop             # мониторинг
pgrep -af nginx               # найти процессы
pidof nginx                   # PID по имени

# lsof — открытые файлы
lsof                          # все
lsof -p 1234                  # процесс
lsof -i :80                   # кто слушает порт
lsof /var/log/syslog          # кто открыл файл

# fuser — кто использует
fuser -v 80/tcp
fuser -k /var/log/app.log     # убить процессы, использующие файл
```

### Сеть
```bash
ss -tlnp                      # TCP-порты с процессами
ss -tuln                      # TCP+UDP
ss -t state established       # активные
ip a / ip route
netstat (старый)
```

### Память
```bash
free -h                       # общая
cat /proc/meminfo             # подробно
vmstat 1                      # статистика каждую секунду
slabtop                       # slab cache (kernel)
pmap 1234                     # карта памяти процесса
cat /proc/1234/maps           # то же в /proc
```

### I/O
```bash
iostat -x 1                   # статистика дисков
iotop                         # топ по I/O
pidstat -d 1                  # по процессам
```

### Системные вызовы
```bash
strace -p 1234                # трассировка системных вызовов
strace -e trace=openat,read,write -p 1234
strace -c ls                  # статистика syscalls
ltrace ls                     # библиотечные вызовы
perf stat -a sleep 1          # perf-счётчики
perf top                      # top по функциям в kernel
```

### eBPF (современная интроспекция)
```bash
# bpftrace — мощный трассировщик
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { @[comm] = count(); }'

# BCC tools
sudo execsnoop                # новые процессы
sudo opensnoop                # открытия файлов
sudo biosnoop                 # I/O
sudo tcpconnect               # TCP-соединения
sudo runqlat                  # задержки планировщика
```

---

## 🎛️ Параметры ядра (sysctl)

```bash
# Текущие
sysctl -a | grep ipv4

# Изменить временно
sudo sysctl -w net.ipv4.ip_forward=1

# Постоянно — /etc/sysctl.d/99-my.conf
net.ipv4.ip_forward = 1
vm.swappiness = 10
fs.file-max = 1000000
net.core.somaxconn = 65535

# Применить
sudo sysctl -p /etc/sysctl.d/99-my.conf
```

### Полезные параметры
| Параметр | Что |
|---|---|
| `net.ipv4.ip_forward` | IP-форвардинг (для роутеров/Docker) |
| `vm.swappiness` | Склонность к swap (0-100) |
| `vm.overcommit_memory` | Выделение памяти |
| `fs.file-max` | Лимит открытых файлов |
| `net.core.somaxconn` | Размер очереди listen |
| `net.ipv4.tcp_max_syn_backlog` | SYN backlog |
| `kernel.pid_max` | Максимум PID |
| `net.ipv4.tcp_tw_reuse` | Переиспользование TIME_WAIT |

### ulimit vs sysctl
- `ulimit` (per-process) — `ulimit -n 65535` (open files).
- `sysctl` (system-wide) — `fs.file-max`.
- `/etc/security/limits.conf` — persisting ulimits.

---

## 🐛 Практическое применение

### 1. Кто держит порт?
```bash
sudo ss -tlnp | grep :8080
sudo lsof -i :8080
sudo fuser -v 8080/tcp
```

### 2. Кто пишет в файл?
```bash
sudo lsof /var/log/syslog
# или inotify
sudo inotifywait -m /path
# или через eBPF
sudo opensnoop -n nginx
```

### 3. Почему процесс тормозит?
```bash
# Что делает
sudo strace -p 1234 -c         # статистика syscalls
sudo strace -p 1234 -e trace=futex,read,write

# CPU profile
sudo perf top -p 1234

# I/O profile
sudo iotop -p 1234
pidstat -d -p 1234 1
```

### 4. Контейнер без docker
```bash
# systemd-nspawn — лёгкий контейнер
sudo debootstrap stable /var/lib/container/debian http://deb.debian.org/debian
sudo systemd-nspawn -D /var/lib/container/debian
```

### 5. Ограничить память процесса
```bash
# Через systemd
sudo systemd-run --scope -p MemoryMax=100M stress --vm 1 --vm-bytes 200M

# Напрямую в cgroup v2
sudo mkdir /sys/fs/cgroup/stress
echo 104857600 | sudo tee /sys/fs/cgroup/stress/memory.max
echo $$ | sudo tee /sys/fs/cgroup/stress/cgroup.procs
stress --vm 1 --vm-bytes 200M    # будет OOM-killed
```

### 6. Найти утечку памяти в процессе
```bash
cat /proc/<pid>/status | grep -E 'VmRSS|VmSize|VmPeak'
watch -n 1 'cat /proc/<pid>/status | grep VmRSS'
# Растёт → утечка
```

### 7. Сделать образ контейнера минимальным
```bash
# Свои namespace'ы через unshare
unshare --pid --fork --mount-proc --net --uts --ipc \
    bash -c "hostname test; mount -t proc proc /proc; ip link set lo up; ps aux"
```

---

## 🪤 Частые ошибки

1. **Не root не видит /proc/<чужой_pid>** — нужны права или `ptrace_scope=0`.
2. **Ручная правка /proc/sys** — временно, используйте sysctl.
3. **`echo 1 > /proc/sys/...`** без sudo — permission denied.
4. **Смешивание cgroup v1/v2** — переход болезненный.
5. **Лимит cgroup без swappiness** — OOM на ровном месте.
6. **`docker run --network=host`** — нет изоляции сети.
7. **Не размонтированный namespace** — утечка ресурсов.
8. **`ulimit` не наследуется** через systemd без `LimitNOFILE=`.
9. **`ftrace` требует root** — или `CAP_SYS_ADMIN`.
10. **`/proc/<pid>/mem`** читается только с `ptrace` или root.

---

## 🔗 Полезные ссылки

- man: `man proc`, `man sysfs`, `man cgroups`, `man namespaces`
- kernel.org: https://www.kernel.org/doc/html/latest/admin-guide
- cgroup v2 docs: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- namespaces overview: https://man7.org/linux/man-pages/man7/namespaces.7.html
- LWN cgroups: https://lwn.net/Articles/604609
- BPF Performance Tools (книга, Brendan Gregg)
- bpftrace: https://github.com/iovisor/bpftrace
- BCC tools: https://github.com/iovisor/bcc
- systemd.resource-control: `man systemd.resource-control`

---

## 💡 Полезные советы

1. **`/proc` — ваш друг** — там почти всё о процессах и ядре.
2. **`lsns` / `nsenter`** — для дебага контейнеров.
3. **`systemd-cgls` / `systemd-cgtop`** — топ процессов по cgroups.
4. **`strace`** — когда процесс «завис» или ведёт себя странно.
5. **`lsof` / `ss -p`** — кто держит порт/файл.
6. **cgroup v2** — будущее, переходите.
7. **`sysctl -p`** — после правки `/etc/sysctl.d/*.conf`.
8. **eBPF/bpftrace** — современная, безопасная интроспекция.
9. **`perf`** — для профилирования ядра/процессов.
10. **`/sys/class/hwmon`** — датчики температуры/вентиляторов.
11. **Docker = cgroups + namespaces** — понимание баз = понимание контейнеров.
12. **`unshare`** — для ручного создания namespace'ов.
13. **Limits**: ulimit (per-process) vs sysctl (system) vs limits.conf.
14. **`/proc/<pid>/maps`** — карта памяти, для отладки memory leaks.
15. **OOM killer** — смотрит на oom_score в `/proc/<pid>/oom_score`.

---

*Сгенерировано как шпаргалка. Linux internals — глубокая тема —
углубляйтесь через man pages и https://www.kernel.org/doc/html/latest/*

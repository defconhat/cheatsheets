# 🔐 SSH — шпаргалка по командам и конфигурации

> **SSH (Secure Shell)** — сетевой протокол для безопасного удалённого доступа,
> передачи файлов, проброса портов и туннелей.
> Документация: https://www.openssh.com · `man ssh` · `man ssh_config`

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **SSH client** | Программа `ssh` на вашей машине |
| **SSH server** | `sshd` (демон) на удалённой машине |
| **keypair** | Пара ключей: приватный (`id_ed25519`) + публичный (`id_ed25519.pub`) |
| **known_hosts** | Список известных серверов (с их отпечатками) |
| **authorized_keys** | Список публичных ключей, которым разрешён вход на сервер |
| **config** | `~/.ssh/config` — настройки подключения |
| **agent** | `ssh-agent` — держит расшифрованные ключи в памяти |
| **ControlMaster** | Мультиплексирование: одно соединение для нескольких сессий |

---

## 🚀 Базовое подключение

```bash
# Простейшее
ssh user@host                    # hostname или IP
ssh user@192.168.1.10
ssh user@example.com

# Короткие формы
ssh example.com                  # если в ~/.ssh/config задан user
ssh host                         # alias из ~/.ssh/config

# С явным пользователем/портом
ssh -l user host                 # = ssh user@host
ssh -p 2222 user@host            # нестандартный порт

# С конкретным ключом
ssh -i ~/.ssh/id_ed25519 user@host

# Запуск команды (без интерактивной оболочки)
ssh user@host "uname -a"
ssh user@host "df -h"
ssh user@host uptime

# Несколько команд
ssh user@host "cd /tmp && ls -la"

# Here-doc через SSH
ssh user@host << 'EOF'
echo "Hello"
uname -a
EOF

# Принять новый ключ сервера автоматически (НЕ для продакшена!)
ssh -o StrictHostKeyChecking=accept-new user@host

# Подробный вывод (для отладки)
ssh -v user@host
ssh -vv user@host                # ещё подробнее
ssh -vvv user@host               # максимальный дебаг

# Форсировать выделение TTY (для интерактивных программ)
ssh -t user@host "top"
```

### Опции командной строки
| Опция | Действие |
|---|---|
| `-p PORT` | Порт сервера |
| `-i KEYFILE` | Файл приватного ключа |
| `-l USER` | Имя пользователя |
| `-v` / `-vv` / `-vvv` | Подробность логирования |
| `-C` | Сжатие (медленные сети) |
| `-4` / `-6` | Только IPv4 / IPv6 |
| `-t` | Принудительный TTY |
| `-T` | Без TTY |
| `-N` | Без выполнения команды (для туннелей) |
| `-f` | Уйти в фон после аутентификации |
| `-F FILE` | Альтернативный конфиг |
| `-o OPTION=value` | Любая опция из ssh_config |
| `-J jumpuser@jumphost` | Jump host (бастион) |
| `-A` | Включить agent forwarding |
| `-a` | Отключить agent forwarding |
| `-X` / `-Y` | X11 forwarding (графика) |
| `-q` | Тихий режим |
| `-b IP` | С какого локального IP подключаться |
| `-L` / `-R` / `-D` | Проброс портов |
| `-w local:remote` | TUN/TAP устройство (VPN) |

---

## 🔑 Ключи SSH

### Создание пары ключей
```bash
# Современный (РЕКОМЕНДУЕТСЯ) — Ed25519
ssh-keygen -t ed25519 -C "your_email@example.com"

# С большим размером (более старый стандарт, RSA 4096)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# ECDSA
ssh-keygen -t ecdsa -b 521 -C "email"

# С указанием файла и паролем (passphrase)
ssh-keygen -t ed25519 -f ~/.ssh/my_key -C "work key" -N "secret passphrase"

# Без passphrase (для автоматизации, менее безопасно)
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N ""

# Список публичных ключей
ls ~/.ssh/*.pub
```

> ⚠️ **Ed25519** предпочтительнее: короче, быстрее, безопаснее RSA.

### Смена passphrase (без смены ключа)
```bash
ssh-keygen -p -f ~/.ssh/id_ed25519
```

### Узнать отпечаток (fingerprint)
```bash
ssh-keygen -l -f ~/.ssh/id_ed25519.pub
# 256 SHA256:abc123... your_email@example.com (ED25519)
ssh-keygen -l -E md5 -f ~/.ssh/id_ed25519.pub    # в формате MD5
```

### Конвертация форматов
```bash
# PEM (для некоторых старых клиентов)
ssh-keygen -p -m PEM -f ~/.ssh/id_rsa

# В формат PuTTY (нужен puttygen)
puttygen ~/.ssh/id_ed25519 -o key.ppk
# Из PPK в OpenSSH
puttygen key.ppk -O private-openssh -o id_ed25519
```

---

## 📤 Копирование ключа на сервер

### ssh-copy-id (проще всего)
```bash
# По умолчанию копирует ~/.ssh/id_rsa.pub или id_ed25519.pub
ssh-copy-id user@host

# С конкретным ключом
ssh-copy-id -i ~/.ssh/my_key.pub user@host

# На нестандартный порт
ssh-copy-id -p 2222 user@host

# Если ещё несколько ключей
ssh-copy-id -i ~/.ssh/work.pub -o IdentitiesOnly=yes user@host
```

### Вручную
```bash
# Без ssh-copy-id (например, в Windows)
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

---

## ⚙️ Конфиг `~/.ssh/config`

Самый мощный инструмент — один раз настроил, потом `ssh myserver`.

```ssh-config
# ~/.ssh/config

# ── Глобальные дефолты ─────────────────────────────
Host *
    AddKeysToAgent yes
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
    HashKnownHosts no
    UserKnownHostsFile ~/.ssh/known_hosts

# ── Конкретные хосты ───────────────────────────────

Host myserver
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes

Host prod
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/work_ed25519
    # Jump через бастион
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User ops

# Группы (wildcards)
Host *.internal
    User worker
    ProxyJump bastion
    IdentityFile ~/.ssh/internal_key

Host github.com
    User git
    IdentityFile ~/.ssh/github_ed25519

Host gitlab.com
    User git
    IdentityFile ~/.ssh/gitlab_ed25519

# Алиасы с разными ключами для одного хоста
Host personal-github
    HostName github.com
    User git
    IdentityFile ~/.ssh/personal_ed25519

Host work-github
    HostName github.com
    User git
    IdentityFile ~/.ssh/work_ed25519
```

После этого:
```bash
ssh myserver                  # вместо ssh admin@192.168.1.100
ssh prod                      # автоматически через bastion
ssh web01.internal            # через bastion
```

### Директивы config
| Директива | Что |
|---|---|
| `Host NAME` | Имя алиаса (можно с `*` и `?`) |
| `HostName` | Реальный адрес |
| `User` | Пользователь по умолчанию |
| `Port` | Порт |
| `IdentityFile` | Путь к приватному ключу |
| `IdentitiesOnly yes` | Использовать только указанный ключ (не все в агенте) |
| `ProxyJump HOST` | Jump host (бастион) |
| `ProxyCommand CMD` | Произвольная команда как прокси |
| `ForwardAgent yes` | Проброс ssh-agent |
| `LocalForward` / `RemoteForward` | Проброс портов |
| `ServerAliveInterval` | Keepalive (секунды) |
| `ServerAliveCountMax` | Сколько раз пробовать |
| `Compression yes` | Сжатие трафика |
| `RequestTTY` | Запрос TTY |
| `RemoteCommand CMD` | Выполнить команду при входе |
| `ControlMaster` / `ControlPath` | Мультиплексирование |

### Мультиплексирование (ускорение)
```ssh-config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 10m
```
Первое соединение устанавливается медленно, все последующие к тому же
хосту — мгновенно (через существующий сокет).

---

## 🔐 ssh-agent — хранение расшифрованных ключей

```bash
# Запустить агента
eval "$(ssh-agent -s)"

# Добавить ключи
ssh-add ~/.ssh/id_ed25519              # спросит passphrase
ssh-add                                # все ключи по умолчанию
ssh-add -l                             # список загруженных (с отпечатками)
ssh-add -L                             # список публичных частей
ssh-add -d ~/.ssh/id_ed25519           # удалить ключ
ssh-add -D                             # удалить все ключи
ssh-add -t 3600 ~/.ssh/id_ed25519      # на 1 час

# macOS: добавить в связку ключей (Keychain)
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### Автозапуск агента
В `~/.bashrc` / `~/.zshrc`:
```bash
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" >/dev/null
fi
```

Или через systemd user-юнит:
```bash
# /etc/systemd/user/ssh-agent.service
systemctl --user enable --now ssh-agent.service
```

### ForwardAgent (проброс агента)
```bash
ssh -A user@host             # ваш агент доступен на сервере
# В config: ForwardAgent yes
```
> ⚠️ **Осторожно**: на скомпрометированном сервере root может использовать
> ваш агент. Не включайте на ненадёжных хостах.

---

## 📁 Передача файлов

### scp — простое копирование
```bash
# С компьютера на сервер
scp file.txt user@host:/path/to/destination/
scp file.txt user@host:~/              # в домашний каталог

# С сервера на компьютер
scp user@host:/var/log/app.log ./
scp user@host:/etc/nginx/nginx.conf ./

# С нестандартным портом (ЗАМЕТИТЬ позицию -P!)
scp -P 2222 file.txt user@host:~/

# Каталог рекурсивно
scp -r mydir/ user@host:~/

# Несколько файлов
scp file1.txt file2.txt user@host:~/

# Между двумя серверами (медленно — через ваш комп)
scp user1@host1:/file user2@host2:/dest/

# С конкретным ключом
scp -i ~/.ssh/key file user@host:~/

# Сжатие
scp -C bigfile.bin user@host:~/
```

> ⚠️ scp объявлен deprecated в OpenSSH 9+. Используйте **rsync** или **sftp**.

### rsync — синхронизация (РЕКОМЕНДУЕТСЯ)
```bash
# Базовый синтаксис
rsync [опции] источник назначение

# Локально → удалённо
rsync -avz ./localdir/ user@host:/remote/path/

# Удалённо → локально
rsync -avz user@host:/remote/dir/ ./local/

# Ключ -a = archive (рекурсивно + права + владельцы + симлинки + ...)
# Ключ -v = verbose
# Ключ -z = сжатие
# Ключ -P = --partial --progress (докачка + прогресс)
# Ключ --delete = удалять в приёмнике то, чего нет в источнике

# Полезные опции
rsync -avz --progress src/ user@host:dst/
rsync -avz --partial --progress src/ user@host:dst/   # докачка
rsync -avz --delete --exclude '.git' --exclude 'node_modules' src/ user@host:dst/
rsync -avz -e "ssh -p 2222" src/ user@host:dst/        # порт
rsync -avz -e "ssh -i ~/.ssh/key" src/ user@host:dst/  # ключ
rsync -avz --dry-run src/ user@host:dst/               # только показать
rsync -avz --backup --backup-dir=/backup src/ dst/      # с бэкапом

# Копирование с информацией о диске (большими файлами)
rsync -avz --info=progress2 bigfile user@host:~/
```

> ⚠️ **Слэш в конце пути важен!**
> - `rsync a/ b/` — содержимое `a` в `b`
> - `rsync a b/` — каталог `a` внутри `b`

### sftp — интерактивный FTP поверх SSH
```bash
sftp user@host
sftp -P 2222 user@host

# Команды внутри sftp:
sftp> ls
sftp> cd remote/dir
sftp> lcd local/dir
sftp> pwd                    # удалённый путь
sftp> lpwd                   # локальный путь
sftp> get remote.txt         # скачать
sftp> get -r remotedir/      # рекурсивно
sftp> put local.txt          # загрузить
sftp> put -r localdir/
sftp> mget *.log             # несколько
sftp> mput *.py
sftp> mkdir / rm / rmdir
sftp> chmod 644 file
sftp> exit
```

### tar + ssh — для больших объёмов
```bash
# Архив на лету через SSH (быстро для многих мелких файлов)
tar czf - ./project | ssh user@host "tar xzf - -C ~/projects/"

# С pv для прогресса
tar cf - ./bigdir | pv | ssh user@host "tar xf - -C ~/"

# Обратное (скачать с сервера)
ssh user@host "tar czf - /var/log/" | tar xzf - -C ./
```

---

## 🌉 Проброс портов (tunnels)

### Локальный проброс (`-L`) — самый частый
Делает удалённый сервис доступным на вашей машине.

```bash
# Локальный порт 8080 → удалённый localhost:80
ssh -L 8080:localhost:80 user@host
# Теперь на вашей машине: http://localhost:8080 → на сервере localhost:80

# Доступ к БД на сервере
ssh -L 5432:localhost:5432 user@host
# psql -h localhost -p 5432 (но это на сервере!)

# Цепочка: localhost:8080 → host → другой сервер
ssh -L 8080:internal-server:80 user@bastion
# http://localhost:8080 → bastion → internal-server:80

# Бинд на все интерфейсы (доступ с других машин)
ssh -L 0.0.0.0:8080:localhost:80 user@host
ssh -g -L 8080:localhost:80 user@host      # -g = allow remote

# Несколько пробросов сразу
ssh -L 8080:localhost:80 -L 5432:localhost:5432 user@host

# В фоне (без командной оболочки)
ssh -fNL 8080:localhost:80 user@host
```

### Удалённый проброс (`-R`)
Делает ваш локальный сервис доступным с удалённой машины.

```bash
# Удалённый порт 8080 → ваш localhost:80
ssh -R 8080:localhost:80 user@host
# На сервере: http://localhost:8080 → ваш локальный сервис

# Пробросить сервис с сервера наружу (например, расшарить dev-сервер)
ssh -R 8080:localhost:3000 user@public-server
# Теперь public-server:8080 → ваш localhost:3000

# Туннель в обратную сторону для доступа к домашнему ПК
# (на домашнем ПК, с пробросом наружу):
ssh -R 2222:localhost:22 user@vps.example.com
# На VPS: ssh -p 2222 user@localhost → попадёт на домашний ПК
```

> На сервере в sshd_config нужно `GatewayPorts yes` для бинда на 0.0.0.0.

### Динамический проброс (`-D`) — SOCKS-прокси
```bash
# SOCKS5-прокси на localhost:1080
ssh -D 1080 user@host
ssh -D 1080 -fNC user@host            # в фоне

# Использовать как прокси в браузере:
# Firefox → Settings → Network → SOCKS Host: localhost, Port: 1080, SOCKS v5
# Или в curl:
curl --socks5-hostname localhost:1080 https://ifconfig.me

# Сpecific DNS через прокси (не утекает)
curl --proxy socks5h://localhost:1080 https://example.com
```

### Reverse-туннель (постоянный, для NAT traversal)
Полезно, когда нужно подключаться к машине за NAT.

На машине за NAT (например, домашний ПК):
```bash
# autossh для поддержания соединения
autossh -M 0 -fN -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" \
    -R 2222:localhost:22 user@vps.example.com
```

На VPS:
```bash
ssh -p 2222 user@localhost        # попадёт на домашний ПК
```

### Jump host (бастион)
```bash
# Через один jump
ssh -J user@bastion user@internal-server

# Несколько jump'ов
ssh -J user@bastion1,user@bastion2 user@target

# В config:
Host internal
    HostName 10.0.0.5
    ProxyJump bastion
```

---

## 🌐 VPN через SSH (TUN/TAP)

```bash
# Создать TUN-туннель (нужны права root с обеих сторон)
ssh -w 0:0 user@host
# Локальный tun0 ↔ удалённый tun0

# На клиенте:
sudo ip addr add 10.0.0.1/24 dev tun0
sudo ip link set tun0 up

# На сервере:
sudo ip addr add 10.0.0.2/24 dev tun1
sudo ip link set tun1 up
```

> Простые случаи проброса портов обычно лучше, чем полноценный VPN через SSH.

---

## 🔐 Настройка sshd (сервер)

Файл: `/etc/ssh/sshd_config`

```sshd-config
# ── Базовое ──────────────────────────────
Port 22                            # лучше сменить на нестандартный
AddressFamily any                  # any / inet (IPv4) / inet6 (IPv6)
ListenAddress 0.0.0.0              # на каком IP слушать

# ── Аутентификация ──────────────────────
PermitRootLogin no                 # prohibit-password / yes / no
# ❗ Никогда не разрешайте root с паролем!
PasswordAuthentication no          # только ключи
PubkeyAuthentication yes
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# ── Ключи хоста ─────────────────────────
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# ── Лимиты и таймауты ───────────────────
LoginGraceTime 30                  # секунд на вход
MaxAuthTries 3                     # попыток
MaxSessions 10
ClientAliveInterval 300            # проверка активности каждые 5 мин
ClientAliveCountMax 2              # сколько раз
AllowUsers alice bob ops           # белый список
AllowGroups ssh-users
DenyUsers root guest

# ── Проброс портов ──────────────────────
AllowTcpForwarding yes             # local/remote/yes/no
AllowAgentForwarding no
X11Forwarding no
PermitTunnel no
GatewayPorts no                    # разрешить -R на 0.0.0.0

# ── Безопасность ────────────────────────
Protocol 2                         # только v2 (v1 устарел)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com
KexAlgorithms curve25519-sha256
AllowStreamLocalForwarding no
PermitUserEnvironment no
Compression no                     # (последние версии - атака CRIME)

# ── Логи ────────────────────────────────
SyslogFacility AUTH
LogLevel VERBOSE                   # QUIET/FATAL/ERROR/INFO/VERBOSE
# VERBOSE логирует отпечатки ключей (полезно для аудита)

# ── SFTP ────────────────────────────────
Subsystem sftp /usr/lib/ssh/sftp-server
# Для chroot:
# Subsystem sftp internal-sftp
# Match Group sftp-only
#     ChrootDirectory /home/%u
#     ForceCommand internal-sftp
#     AllowTcpForwarding no
#     X11Forwarding no

# ── Banner (приветствие) ────────────────
Banner /etc/ssh/banner
```

### Условные блоки `Match`
```sshd-config
# Для конкретного пользователя
Match User alice
    PasswordAuthentication yes
    ForceCommand internal-sftp

# Для группы
Match Group admins
    PermitRootLogin yes
    AllowTcpForwarding yes

# Для адреса
Match Address 192.168.1.0/24
    PasswordAuthentication yes     # в локалке можно пароль
Match Address *,!192.168.1.0/24
    PasswordAuthentication no      # снаружи только ключи
```

### Применение изменений
```bash
# Проверить синтаксис (ОЧЕНЬ важно перед перезапуском!)
sudo sshd -t                       # если ничего не выводит — ОК

# Перезапуск
sudo systemctl reload sshd         # мягко (без разрыва соединений)
sudo systemctl restart sshd        # жёстко

# Debian/Ubuntu: ssh.service вместо sshd.service
sudo systemctl reload ssh
```

> 💡 **Лайфхак**: при настройке sshd держите активную SSH-сессию и
> проверяйте новую в отдельном окне. Так не заблокируете себя.

### Сгенерировать host-ключи (новый сервер)
```bash
sudo rm /etc/ssh/ssh_host_*
sudo ssh-keygen -A                 # сгенерировать все нужные
sudo systemctl restart sshd
```

---

## 🚪 authorized_keys на сервере

```bash
# Куда добавлять публичные ключи
~/.ssh/authorized_keys             # построчно

# Права — КРИТИЧНО!
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown -R $USER:$USER ~/.ssh
```

### Ограничения в authorized_keys
```authorized_keys
# Запретить проброс портов, разрешить только с IP
from="192.168.1.0/24" ssh-ed25519 AAAA... user@host

# Принудительная команда (только backup)
command="/usr/local/bin/backup.sh",no-pty ssh-ed25519 AAAA... backup@host

# Полные ограничения для автоматизации
command="rsync-only",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 AAAA...
```

---

## 🔒 Безопасность

### Харденинг (best practices)
1. **Запретить root**: `PermitRootLogin no` (или `prohibit-password`).
2. **Только ключи**: `PasswordAuthentication no`.
3. **Сменить порт** (не спасёт от целенаправленной атаки, но уберёт 99% ботов).
4. **Fail2ban** или **sshguard** для блокировки brute-force.
5. **Белый список** пользователей: `AllowUsers`, `AllowGroups`.
6. **Минимум cipher/MAC/kex** (только современные).
7. **Отдельные ключи** для разных целей (не один на всё).
8. **Passphrase** на приватный ключ.
9. **ssh-agent** с таймаутом.
10. **Не использовать ForwardAgent** на ненадёжных серверах.

### Установка fail2ban
```bash
sudo pacman -S fail2ban           # Arch
sudo apt install fail2ban         # Debian/Ubuntu

# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 1h
findtime = 10m

sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

### Аудит
```bash
# Кто пытался войти (Debian)
sudo journalctl -u ssh -u sshd | grep "Failed"
sudo grep "Failed password" /var/log/auth.log

# Успешные входы
last                              # история входов
lastlog                           # последний вход каждого пользователя

# Активные сессии
who
w
```

---

## 🔄 Хранение паролей/секретов

### Менеджер ключей (рекомендуется)
- **1Password**, **Bitwarden** — имеют SSH-agent интеграцию.
- **KeePassXC** — локальный, имеет SSH-agent.

### Для автоматизации (CI/CD)
```bash
# Ключи без passphrase, в секретах CI/CD
# .gitlab-ci.yml / .github/workflows/:
- echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
- chmod 600 ~/.ssh/id_ed25519
- ssh -o StrictHostKeyChecking=no user@host "deploy.sh"
```

### SSH CA (центр сертификации)
Вместо десятков ключей — один CA подписывает сертификаты:
```bash
# На сервере CA
ssh-keygen -t ed25519 -f ~/.ssh/ca -N ""

# Подписать публичный ключ пользователя
ssh-keygen -s ~/.ssh/ca -I "alice-laptop" -n alice -V +1d ~/.ssh/alice.pub

# Сервер доверяет CA (в /etc/ssh/sshd_config):
TrustedUserCAKeys /etc/ssh/ca.pub

# Преимущества: срок действия, revocation, no authorized_keys
```

---

## 🛠️ Полезные трюки

### Запуск приложения через SSH (nohup-аналог)
```bash
# Запустить и сразу отключиться
ssh -f user@host "nohup long-running-task.sh &"
# или
ssh user@host "nohup task.sh > /dev/null 2>&1 < /dev/null &"

# В tmux/screen на сервере
ssh user@host -t "tmux new -s work"
ssh user@host -t "tmux attach -t work"
```

### Передать файл без scp (когда закрыт)
```bash
# Через SSH напрямую
cat local.txt | ssh user@host "cat > remote.txt"
ssh user@host "cat remote.txt" > local.txt

# base64 (для бинарных)
base64 image.png | ssh user@host "base64 -d > image.png"
```

### Проброс агента с ограничением (ProxyJump + ключ)
```bash
ssh -J bastion -A internal
```

### Удалить хост из known_hosts (сменился ключ сервера)
```bash
ssh-keygen -R hostname                    # удалить
ssh-keygen -R 192.168.1.10
ssh-keygen -R "[host]:2222"               # нестандартный порт

# Подключиться заново, принять новый ключ
ssh user@host
```

### Узнать публичный ключ сервера
```bash
ssh-keyscan hostname                      # все ключи
ssh-keyscan -t ed25519 hostname           # конкретный тип
ssh-keygen -l -f <(ssh-keyscan -t ed25519 hostname 2>/dev/null)  # отпечаток
```

### Сравнить отпечаток с реальным
```bash
# На сервере:
ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub

# При первом подключении сверяйте с этим!
```

### Автоматизация с паролем (НЕБЕЗОПАСНО, но иногда нужно)
```bash
# Установить sshpass
sudo pacman -S sshpass

# Использовать (пароль в командной строке — небезопасно!)
sshpass -p "password" ssh user@host
sshpass -p "password" scp file user@host:~/
sshpass -f passwordfile ssh user@host       # из файла (лучше)
sshpass -e ssh user@host                    # из SSHPASS env var (лучше всего)
```

> ❗ **Лучше используйте ключи**. sshpass оставляет пароль в истории.

---

## 🖥️ SSH на Windows

### Встроенный OpenSSH (Windows 10/11)
```powershell
# Установить через Optional Features (если нет)
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*'
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Использование как в Linux
ssh user@host
ssh-keygen -t ed25519
# Конфиг: C:\Users\you\.ssh\config
```

### PuTTY (классика)
- `putty.exe` — клиент
- `puttygen.exe` — генератор ключей (свой формат .ppk)
- `pageant.exe` — агент ключей
- `pscp.exe`, `psftp.exe` — копирование файлов

### WSL (Windows Subsystem for Linux)
В WSL работает полноценный Linux-SSH — лучший вариант.

---

## 🐛 Отладка

### Подключение не работает
```bash
# 1. Подробный вывод
ssh -vvv user@host

# 2. Проверить доступность
ping host
nc -zv host 22                  # порт открыт?
telnet host 22                  # альтернатива

# 3. Проверить ключ
ssh -i ~/.ssh/key -v user@host
ls -la ~/.ssh/                  # права 700 на каталог, 600 на ключи!

# 4. На сервере посмотреть логи
sudo journalctl -u sshd -f      # или ssh на Debian/Ubuntu
sudo tail -f /var/log/auth.log  # Debian/Ubuntu

# 5. Проверить конфиг сервера
sudo sshd -t                    # синтаксис
sudo sshd -T                    # действующие настройки

# 6. Запустить sshd в debug-режиме (на другом порту)
sudo /usr/sbin/sshd -d -p 2222  # затем подключаться к 2222
```

### Частые причины
- **Неверные права на `~/.ssh`** — должны быть 700, файлы 600.
- **`authorized_keys`** — должен быть 600, владелец — пользователь.
- **`PasswordAuthentication no`** но ключ не добавлен.
- **Файрвол** блокирует порт 22.
- **`AllowUsers`/`AllowGroups`** не содержат пользователя.
- **Сервер использует ssh.service** (Debian), а вы перезапускаете sshd.

---

## 📊 Полезные однострочники

```bash
# Конфиг для известного хоста
ssh -G myhost | grep -E "^(hostname|user|port|identityfile)"

# Список ваших публичных ключей
for f in ~/.ssh/*.pub; do ssh-keygen -l -f "$f"; done

# Закачать публичный ключ на новый сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@newserver

# Мгновенный HTTP-сервер на порту 8080 (расшарить файлы)
ssh -R 8080:localhost:8080 user@vps
python -m http.server 8080

# Бэкап через SSH + tar
tar czf - /data | ssh user@host "cat > backup-$(date +%F).tar.gz"

# Восстановить
ssh user@host "cat backup-2024-01-15.tar.gz" | tar xzf - -C /

# Синхронизировать сайт в продакшн
rsync -avz --delete --exclude '.git' --exclude 'node_modules' \
    ./dist/ deploy@prod:/var/www/site/

# Запустить GUI-приложение с сервера (нужен X11 forwarding)
ssh -X user@host "firefox"

# Пробросить локальный порт к БД (для DBeaver, например)
ssh -L 5432:db.internal:5432 user@bastion -fN
psql -h localhost -p 5432

# SOCKS-прокси через VPS
ssh -D 1080 -fNC user@vps
curl --socks5-hostname localhost:1080 https://ifconfig.me
```

---

## 🆚 Сравнение scp / rsync / sftp

| | scp | rsync | sftp |
|---|---|---|---|
| Простота | ★★★★★ | ★★★ | ★★★ |
| Докачка | ❌ | ✅ | ✅ |
| Синхронизация | ❌ | ✅ | ❌ |
| Удаление лишнего | ❌ | ✅ (--delete) | ❌ |
| Скорость (мелкие файлы) | медленно | быстро | средне |
| Прогресс | базовый | детальный | нет |
| Интерактивно | нет | нет | ✅ |
| Статус | **deprecated** | рекомендуется | рекомендуется |

---

## 🪤 Частые ошибки и грабли

1. **Права на `~/.ssh`** — должны быть 700, иначе ssh откажется читать ключи.
2. **`authorized_keys` 644** — должно быть 600, иначе сервер игнорирует.
3. **Забыли `IdentitiesOnly yes`** — ssh пробует все ключи в агенте, попадает в лимит.
4. **root с паролем** — `PermitRootLogin yes` + `PasswordAuthentication yes` = катастрофа.
5. **`ssh-keygen -R`** после смены ключа сервера — иначе `Host key verification failed`.
6. **`-p` vs `-P`** — ssh: `-p`, scp: `-P`. rsync: `-e "ssh -p"`.
7. **Слэш в rsync** — `a/ b/` копирует *содержимое*, `a b/` копирует *каталог*.
8. **ForwardAgent на чужом сервере** — root может использовать ваш агент.
9. **`Port` в config** — `ssh myhost` использует его, но `scp` тоже читает config.
10. **Перезапуск sshd без проверки** — `sshd -t` перед `systemctl restart`!
11. **Host key changed** — норма после переустановки сервера; проверьте отпечаток.
12. **`PermitRootLogin prohibit-password`** — root может только по ключу (это норма).

---

## 🔗 Полезные ссылки

- OpenSSH: https://www.openssh.com
- Документация: https://man.openbsd.org/ssh
- Arch Wiki SSH: https://wiki.archlinux.org/title/Secure_Shell
- ssh_config: https://man.openbsd.org/ssh_config
- sshd_config: https://man.openbsd.org/sshd_config
- Mozilla SSH guidelines: https://infosec.mozilla.org/guidelines/openssh
- SSH Security: https://sshaudit.com (аудит конфигурации сервера)
- Explained Visually: https://www.ssh.com/academy/ssh

---

## 💡 Полезные советы

1. **`~/.ssh/config`** — настройте алиасы один раз, жизнь станет проще.
2. **Ed25519** — современный стандарт ключей, используйте его.
3. **`ssh-copy-id`** — проще, чем ручное добавление в authorized_keys.
4. **rsync вместо scp** — мощнее, быстрее, с докачкой.
5. **ControlMaster** — мультиплексирование, мгновенные новые сессии.
6. **`-fNL`** — проброс порта в фоне без интерактива.
7. **`ProxyJump`** — современная замена ProxyCommand для бастионов.
8. **Проверяйте `sshd -t`** перед перезапуском сервера.
9. **Fail2ban** — защита от brute-force (особенно если пароли включены).
10. **Не используете пароли** — только ключи, всё остальное уязвимо.
11. **Passphrase на ключе** + ssh-agent — баланс удобства и безопасности.
12. **`GatewayPorts`** в sshd_config — для доступа к reverse-tunnels снаружи.
13. **autossh** — для постоянных туннелей (пере подключается при обрыве).
14. **Менеджер паролей с SSH-agent** (1Password/Bitwarden) — удобно и безопасно.
15. **Храните бэкап ключей** в зашифрованном виде (не в открытом git!).

---

*Сгенерировано как шпаргалка. SSH мощен и опасен —
углубляйтесь через `man ssh`, `man ssh_config`, `man sshd_config`*

# ⏰ cron — шпаргалка по планировщику задач

> **cron** — классический планировщик задач в Unix/Linux.
> Запускает команды по расписанию (каждую минуту, час, день и т.д.).
> Документация: `man cron` · `man crontab` · `man 5 crontab`

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **cron** | Демон (служба), выполняющий задачи по расписанию |
| **crontab** | Файл с расписанием задач пользователя |
| **cron job / task** | Одна запись в crontab |
| **cron expression** | Формат времени (5 полей) |
| **anacron** | Для задач, которые можно пропустить (выполняет при загрузке) |
| **crond** | Процесс демона (системный) |

> **Альтернатива**: systemd timers (мощнее, с зависимостями и логами в journal).

---

## 🚀 Команды crontab

```bash
crontab -e                    # редактировать свой crontab
crontab -l                    # показать свой crontab
crontab -r                    # удалить весь crontab
crontab -ri                   # с подтверждением
crontab FILE                  # установить из файла
crontab -u user -e            # редактировать чужой (нужен root)
crontab -u user -l            # показать чужой
crontab -u alice -e
```

### Файлы
| Расположение | Назначение |
|---|---|
| `/etc/crontab` | Системный (с полем USER) |
| `/etc/cron.d/` | Системные drop-in (как отдельные crontab'ы) |
| `/etc/cron.hourly/` | Скрипты, выполняемые раз в час |
| `/etc/cron.daily/` | Раз в день |
| `/etc/cron.weekly/` | Раз в неделю |
| `/etc/cron.monthly/ | Раз в месяц |
| `/var/spool/cron/` | Пользовательские crontab'ы |
| `/var/log/cron` | Логи (или journalctl на systemd) |

### Запуск скриптов из /etc/cron.{hourly,daily,...}
Просто положите исполняемый скрипт:
```bash
sudo install -m 755 backup.sh /etc/cron.daily/backup
```
Время выполнения настраивается в `/etc/crontab` (по умолчанию 6:25 для daily).

---

## 📋 Формат cron expression

```
┌───── минуты (0-59)
│ ┌───── часы (0-23)
│ │ ┌───── день месяца (1-31)
│ │ │ ┌───── месяц (1-12 или JAN-DEC)
│ │ │ │ ┌───── день недели (0-7, 0 и 7 = Sunday, или SUN-SAT)
│ │ │ │ │
* * * * * команда
```

### Примеры
```cron
# Каждую минуту
* * * * * /script.sh

# Каждые 5 минут
*/5 * * * * /script.sh

# В 0 минуту каждого часа (раз в час)
0 * * * * /script.sh

# Каждый день в 3:00 ночи
0 3 * * * /script.sh

# Каждый понедельник в 9:00
0 9 * * 1 /script.sh

# Каждый понедельник и пятницу в 18:00
0 18 * * 1,5 /script.sh

# 1-го числа каждого месяца в полночь
0 0 1 * * /script.sh

# Каждые 15 минут в рабочее время (9-18) по будням
*/15 9-18 * * 1-5 /script.sh

# Каждый день 1 января в 00:00
0 0 1 1 * /script.sh

# Дважды в день (3:00 и 15:00)
0 3,15 * * * /script.sh

# Каждые 6 часов
0 */6 * * * /script.sh

# В 30 минут 3-го часа, каждые 2 дня
30 3 */2 * * /script.sh

# Каждую среду в полночь
0 0 * * 3 /script.sh

# В последний день месяца (через test)
0 0 28-31 * * [ "$(date +\%d -d tomorrow)" = "01" ] && /script.sh
```

### Спец-строки (расширения Vixie cron)
```cron
@reboot         # при загрузке системы
@yearly/@annually  # раз в год (0 0 1 1 *)
@monthly        # раз в месяц (0 0 1 * *)
@weekly         # раз в неделю (0 0 * * 0)
@daily/@midnight  # раз в день (0 0 * * *)
@hourly         # раз в час (0 * * * *)
```

```cron
@reboot /script.sh
@daily /backup.sh
```

### Списки, диапазоны, шаги
| Синтаксис | Пример | Значение |
|---|---|---|
| `*` | `*` | Любое значение |
| Конкретное | `5` | Ровно 5 |
| `,` список | `1,5,10` | 1, 5 или 10 |
| `-` диапазон | `1-5` | от 1 до 5 |
| `/` шаг | `*/5` | каждые 5 (0, 5, 10, ...) |
| `2-10/2` | `2-10/2` | 2, 4, 6, 8, 10 |

### Дни недели
| Число | День |
|---|---|
| 0 / 7 | Воскресенье (SUN) |
| 1 | Понедельник (MON) |
| 2 | Вторник (TUE) |
| 3 | Среда (WED) |
| 4 | Четверг (THU) |
| 5 | Пятница (FRI) |
| 6 | Суббота (SAT) |

---

## 📝 Структура crontab

### Пользовательский crontab
```cron
# ── Переменные окружения ──────────────────────
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=alice@example.com      # отправлять вывод на почту
# MAILTO=""                   # отключить почту
HOME=/home/alice

# ── Задачи ────────────────────────────────────
# m  h  dom mon dow  command
*/15 * *  *  *   /home/alice/scripts/sync.sh >> /tmp/sync.log 2>&1
0   3  *  *  *   /usr/local/bin/backup.sh
0   0  *  *  1   rsync -avz /data/ backup:/backup/
@reboot           /home/alice/scripts/startup.sh
```

### Системный crontab (/etc/crontab) — с полем USER
```cron
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# m  h  dom mon dow  user  command
0   3  *  *  *   root   /usr/local/bin/backup.sh
*/30 *  *  *  *   alice  /home/alice/scripts/sync.sh
```

---

## 🌍 Практические примеры

### 1. Регулярный backup
```cron
# Бэкап базы каждый день в 2:00
0 2 * * * pg_dump mydb | gzip > /backup/db-$(date +\%Y\%m\%d).sql.gz

# Бэкап в S3 еженедельно
0 4 * * 0 aws s3 sync /data/ s3://mybucket/backup/
```

### 2. Очистка временных файлов
```cron
# Удалить файлы старше 7 дней в /tmp
0 3 * * * find /tmp -type f -mtime +7 -delete

# Удалить логи старше 30 дней
0 5 * * * find /var/log/app -name "*.log" -mtime +30 -exec gzip {} \;
```

### 3. Мониторинг сайта
```cron
# Каждую минуту проверять сайт
* * * * * curl -sf https://example.com/health > /dev/null || echo "DOWN" | mail -s "Site down" admin@example.com

# Каждые 5 минут проверять SSL
*/5 * * * * /scripts/check_ssl.sh
```

### 4. Обновление сертификатов Let's Encrypt
```cron
# Дважды в день проверять/обновлять
0 0,12 * * * certbot renew --quiet
```

### 5. Запуск Docker-контейнеров
```cron
# Бэкап всех Docker volumes еженедельно
0 2 * * 0 docker run --rm -v /var/lib/docker/volumes:/data alpine tar czf - /data | gzip > /backup/volumes.tar.gz
```

### 6. Запуск Python скрипта в venv
```cron
# Ежечасно в venv
0 * * * * cd /app && .venv/bin/python script.py

# Альтернатива с активацией
0 * * * * /bin/bash -c 'source /app/.venv/bin/activate && cd /app && python script.py'
```

### 7. Синхронизация времени
```cron
# Синхронизировать время каждый час
0 * * * * /usr/sbin/ntpdate pool.ntp.org
```

### 8. Логирование с timestamp
```cron
* * * * * echo "$(date): task ran" >> /var/log/mytask.log
```

---

## ⚠️ Частые грабли (важно!)

### 1. Минимальная среда окружения
cron запускает задачи в **минимальной среде** — не ваши `.bashrc`/`.zshrc`!

```cron
# ❌ Не сработает — PATH короткий
* * * * * curl https://example.com/

# ✅ Указать полный путь
* * * * * /usr/local/bin/curl https://example.com/

# ✅ Или расширить PATH в начале crontab
PATH=/usr/local/bin:/usr/bin:/bin
* * * * * curl https://example.com/
```

### 2. `%` — спецсимвол в cron (newline)
```cron
# ❌ % нужно экранировать!
* * * * * date +%Y-%m-%d

# ✅ Экранировать
* * * * * date +\%Y-\%m-\%d

# Или использовать одинарные кавычки (но % всё равно спецсимвол)
* * * * * bash -c 'date +%Y-%m-%d'
```

### 3. Относительные пути не работают
```cron
# ❌ cron запускается из HOME (или /)
* * * * * cd project && ./script.sh

# ✅ Абсолютные пути
* * * * * /home/alice/project/script.sh

# ✅ cd с абсолютным путём
* * * * * cd /home/alice/project && /home/alice/project/script.sh
```

### 4. Перенаправление вывода
```cron
# ❌ По умолчанию cron отправит stdout по почте (MAILTO)
* * * * * /script.sh

# ✅ Логировать
* * * * * /script.sh >> /var/log/script.log 2>&1

# ✅ Выкинуть вывод
* * * * * /script.sh > /dev/null 2>&1

# ✅ Только ошибки
* * * * * /script.sh > /dev/null
```

### 5. Не работает скрипт — проверьте права и shebang
```bash
chmod +x script.sh
head -1 script.sh              # должна быть строка #!/bin/bash
```

### 6. Дублирование при перезагрузке
```cron
# @reboot + обычное расписание могут запуститься дважды при загрузке в момент расписания
```

### 7. Часовой пояс
cron использует **системный** timezone.
```bash
timedatectl                  # проверить
sudo timedatectl set-timezone Europe/Moscow
sudo systemctl restart cron  # перезапустить, чтобы подхватил
```

---

## 🐛 Отладка cron

### Проверить синтаксис
```bash
# crontab -e и сохранить → cron проверяет и сообщает об ошибках
# Или использовать онлайн-валидатор: https://crontab.guru
```

### Проверить, что cron вообще работает
```bash
systemctl status cron        # или crond
sudo systemctl restart cron
pgrep cron                   # процесс запущен?
```

### Посмотреть логи
```bash
# systemd
sudo journalctl -u cron -f
sudo journalctl -u cron --since "1 hour ago"
sudo journalctl -t cron

# Старый стиль (Debian/Ubuntu)
sudo tail -f /var/log/cron.log
sudo grep CRON /var/log/syslog

# RHEL/CentOS
sudo tail -f /var/log/cron
```

### Тест: простая задача
```cron
* * * * * echo "$(date) cron works" >> /tmp/crontest.log
```
Через минуту проверьте:
```bash
cat /tmp/crontest.log
```

### cron не запускает — чеклист
1. ✅ Сервис активен? `systemctl status cron`
2. ✅ crontab сохранён? `crontab -l`
3. ✅ Права на скрипт? `chmod +x`
4. ✅ Shebang в скрипте? `#!/bin/bash`
5. ✅ Абсолютные пути? `/usr/bin/python`, не `python`
6. ✅ Вывод логируется? `>> /log 2>&1`
7. ✅ `%` экранированы? `\%`
8. ✅ Cron user имеет права? (для root-задач)
9. ✅ Часовой пояс правильный?
10. ✅ Машина не спала/не выключалась в это время?

### Инструменты
- **crontab.guru** — онлайн тестер cron-выражений: https://crontab.guru
- **cronitor** — мониторинг cron jobs: https://cronitor.io
- **cron-utils** (Java) — парсинг и описание

---

## 🌐 anacron — для настольных ПК

cron не запускает пропущенные задачи (если ПК был выключен).
**anacron** запускает пропущенное при включении.

### /etc/anacrontab
```cron
# period  delay  job-identifier  command
1         5      cron.daily      run-parts /etc/cron.daily
7         25     cron.weekly     run-parts /etc/cron.weekly
@monthly  45     cron.monthly    run-parts /etc/cron.monthly
```

- `period` — как часто (в днях)
- `delay` — задержка после загрузки (минуты)
- `job-identifier` — имя (для /var/spool/anacron)

### Когда использовать anacron
- Настольные ПК / ноутбуки (могут быть выключены ночью).
- Задачи, которые нужно выполнить обязательно (backup, обновления).

---

## 🆚 cron vs systemd timers

| | cron | systemd timers |
|---|---|---|
| Простота | ★★★★★ | ★★★ |
| Логи | в файле/MAILTO | в journal |
| Зависимости | нет | есть (After=) |
| Условия (Condition) | нет | есть |
| Пропущенные задачи | только anacron | `Persistent=true` |
| Точность | минута | миллисекунды |
| Передача параметров | строка команды | environment, args |
| Мониторинг | вручную | `systemctl list-timers` |
| Дебаг | сложно | легко (journal) |

**Когда что**:
- **cron**: простые задачи, совместимость, очень простая настройка.
- **systemd timers**: современные Linux, нужны зависимости/условия/логи.

### Пример: та же задача двумя способами
```cron
# cron
0 3 * * * /usr/local/bin/backup.sh
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```
```bash
sudo systemctl enable --now backup.timer
```

---

## 🌍 cron в Docker

```dockerfile
# Dockerfile
FROM alpine
RUN apk add --no-cache bash
COPY script.sh /script.sh
COPY crontab /etc/crontabs/root
RUN chmod +x /script.sh
CMD ["crond", "-f", "-l", "2"]
```

```cron
# crontab
* * * * * /script.sh >> /var/log/script.log 2>&1
```

### Альтернативы для Docker
- **supercronic** — cron для контейнеров (с логами в stdout).
- **ofelia** — Docker-native scheduler.
- **systemd timers** в Docker (через specific base image).

---

## 🪤 Частые ошибки

1. **Короткий PATH** — используйте абсолютные пути или расширьте PATH.
2. **`%` без экранирования** — `date +%Y` → `date +\%Y`.
3. **Без логирования** — `> /dev/null 2>&1` или в файл.
4. **MAILTO спам** — по умолчанию cron шлёт вывод на почту. Отключите `MAILTO=""`.
5. **Забыли `chmod +x`** — скрипт не запустится.
6. **Shebang отсутствует** — cron не знает, чем выполнять.
7. **Не обновляется часовой пояс** — `systemctl restart cron`.
8. **Вложенный crontab** — не делайте `crontab -e` из cron job.
9. **Минута=0 vs `*`** — `0 * * * *` (раз в час) ≠ `* * * * *` (раз в минуту).
10. **0 и 7 — оба воскресенье** — путаница в дне недели.

---

## 🔗 Полезные ссылки

- man: `man 5 crontab`, `man cron`
- crontab.guru (тестер): https://crontab.guru
- Wikipedia: https://ru.wikipedia.org/wiki/Cron
- cron scheduler online: https://www.freeformatter.com/cron-expression-generator-quartz.html
- systemd timers comparison: https://wiki.archlinux.org/title/Cron
- Awesome Cron: https://github.com/while-loop/cron-cheatsheet

---

## 💡 Полезные советы

1. **crontab.guru** — всегда проверяйте выражение онлайн.
2. **Абсолютные пути** — для всего (команды, скрипты, файлы).
3. **Логируйте** — `>> /log 2>&1`, иначе не узнаете об ошибках.
4. **`MAILTO=""`** — отключите спам почтой.
5. **`@reboot`** — для запуска при старте системы.
6. **`anacron`** — для настольных ПК (запустит пропущенное).
7. **systemd timers** — для новых задач на современных Linux.
8. **Test в CLI** — `* * * * * echo test >> /tmp/test` для проверки.
9. **Часовой пояс** — `timedatectl` + `systemctl restart cron`.
10. **Минимальная среда** — cron не загружает `.bashrc`.
11. **`*/5`** — каждые 5 минут, а не «в 5 минуту».
12. **Lock-файлы** — для задач, которые не должны перекрываться (`flock`).
13. **`flock -n /tmp/lock.lock -c 'command'`** — защита от параллельного запуска.
14. **Не ставьте `cron` в Docker** — используйте supercronic или внешний оркестратор.
15. **Мониторинг** — используйте healthchecks.io или dead-mans-snitch для критичных задач.

---

*Сгенерировано как шпаргалка. cron прост, но капризен —
углубляйтесь через `man 5 crontab` и crontab.guru*

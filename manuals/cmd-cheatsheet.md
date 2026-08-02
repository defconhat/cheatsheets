# 🪟 CMD (cmd.exe) — шпаргалка по командам

> **cmd.exe** — классическая командная строка Windows (Command Prompt).
> Наследник `command.com` из MS-DOS. До сих пор встроен в Windows 10/11.
>
> Для современного использования Microsoft рекомендует **PowerShell**, но CMD
> остаётся быстрым и незаменимым для: `.bat`/`.cmd` скриптов, системных задач,
> совместимости со старым софтом, низкоуровневых команд.

---

## 🚀 Запуск

| Способ | Описание |
|---|---|
| `Win+R` → `cmd` → Enter | Быстрый запуск |
| Пуск → «Командная строка» | Через меню |
| В адресной строке проводника: `cmd` | В текущей папке |
| `cmd` в терминале Windows | Вкладка CMD |
| **От администратора:** Пуск → cmd → `Ctrl+Shift+Enter` | С правами admin |
| `cmd /c "команда"` | Выполнить и закрыть |
| `cmd /k "команда"` | Выполнить и остаться |
| `cmd /?` | Справка по ключам запуска |
| `exit` | Выйти |

### Ключи запуска
| Ключ | Действие |
|---|---|
| `/c command` | Выполнить команду и завершиться |
| `/k command` | Выполнить и остаться открытым |
| `/s /c "complex"` | Корректно обработать кавычки |
| `/q` | Отключить echo |
| `/e:on` | Включить расширения команд |
| `/v:on` | Отложенное расширение переменных (`!var!`) |

---

## 🧭 Навигация по каталогам

| Команда | Действие |
|---|---|
| `cd` | Показать текущий каталог |
| `cd ..` | На уровень вверх |
| `cd \` | В корень диска |
| `cd Users\Admin` | Перейти в подкаталог |
| `cd "C:\Program Files"` | С пробелами — в кавычках |
| `chdir` | То же что `cd` |
| `D:` | Перейти на диск D: |
| `pushd \\server\share` | Перейти + запомнить (вкл. сетевой путь) |
| `popd` | Вернуться к запомненному |
| `dir` | Список файлов |
| `dir /a` | Со скрытыми |
| `dir /a:d` | Только каталоги |
| `dir /a:-d` | Только файлы |
| `dir /b` | Только имена (без шапки) |
| `dir /s` | Рекурсивно (по подкаталогам) |
| `dir /o:n` | Отсортировать по имени |
| `dir /o:-n` | По имени в обратном порядке |
| `dir /o:s` | По размеру |
| `dir /o:d` | По дате |
| `dir /p` | Постранично |
| `dir /w` | В несколько колонок |
| `dir *.txt` | По шаблону |
| `tree` | Дерево каталогов |
| `tree /f` | Дерево + файлы |
| `tree /a` | ASCII-символами |
| `cls` | Очистить экран |

> Шаблоны (wildcards): `*` — любое число символов, `?` — один символ.
> `dir *.txt` — все .txt, `dir file?.txt` — file1.txt, fileA.txt.

---

## 📄 Работа с файлами и каталогами

| Команда | Действие |
|---|---|
| `mkdir folder` / `md folder` | Создать каталог |
| `mkdir a\b\c` | Создать вложенные (сразу) |
| `rmdir folder` / `rd folder` | Удалить пустой каталог |
| `rmdir /s folder` | Удалить со всем содержимым |
| `rmdir /s /q folder` | Тихо, без подтверждения |
| `del file.txt` | Удалить файл |
| `del *.tmp` | По шаблону |
| `del /s *.log` | Рекурсивно |
| `del /q *.tmp` | Без подтверждения |
| `erase` | То же что `del` |
| `copy src dst` | Копировать файл |
| `copy a.txt + b.txt c.txt` | Склеить файлы |
| `copy /y src dst` | Без подтверждения перезаписи |
| `xcopy src dst /s /e` | Копировать дерево каталогов |
| `xcopy src dst /s /e /h /y` | + скрытые, без вопросов |
| `robocopy src dst /mir` | Надёжное копирование + синхронизация (рекомендуется!) |
| `move file.txt ..\` | Переместить |
| `move old.txt new.txt` | Переименовать |
| `ren file.txt file.bak` | Переименовать |
| `rename` | То же что `ren` |
| `type file.txt` | Вывести содержимое (как `cat`) |
| `type file.txt \| more` | Постранично |
| `more file.txt` | Постраничный просмотр |
| `find "text" file.txt` | Поиск текста (без регулярок) |
| `find /i "text" file.txt` | Без учёта регистра |
| `find /n "text" file.txt` | С номерами строк |
| `find /c "text" *.txt` | Подсчёт совпадений |
| `findstr "pattern" *.txt` | Поиск с regex |
| `findstr /i /s /n "TODO" *.py` | Рекурсивно, с номерами |
| `findstr /r "^Error" log.txt` | Регулярка |
| `fc file1 file2` | Сравнить файлы |
| `comp a.txt b.txt` | Посимвольное сравнение |
| `attrib +h file.txt` | Установить атрибут «скрытый» |
| `attrib +r file.txt` | «Только чтение» |
| `attrib -h -r file.txt` | Снять атрибуты |
| `attrib` | Показать атрибуты |
| `assoc .txt` | Узнать ассоциацию расширения |
| `ftype txtfile` | Узнать программу для типа |
| `where notepad` | Найти путь к программе (как `which`) |
| `touch` | ❌ Нет в CMD; используйте `type nul > file` |

### robocopy — мощный инструмент копирования
```cmd
:: Базовое копирование
robocopy C:\src D:\backup /e

:: Зеркало (источник → приёмник, удалять лишнее в приёмнике)
robocopy C:\src D:\backup /mir

:: С重启овое копирование, многопоточное, с логом
robocopy C:\src D:\backup /e /z /mt:16 /log:copy.log /tee

:: Только файлы изменённые за последние 7 дней
robocopy C:\src D:\backup /maxage:7

:: Исключить папки/файлы
robocopy C:\src D:\backup /e /xd node_modules .git /xf *.tmp
```

---

## 🔊 Сеть

| Команда | Действие |
|---|---|
| `ipconfig` | IP-конфигурация |
| `ipconfig /all` | Подробно |
| `ipconfig /release` | Освободить IP (DHCP) |
| `ipconfig /renew` | Получить новый IP |
| `ipconfig /flushdns` | Очистить кэш DNS |
| `ipconfig /displaydns` | Показать кэш DNS |
| `ping google.com` | Проверка связи |
| `ping -t google.com` | Бесконечно (до Ctrl-C) |
| `ping -n 10 google.com` | 10 пакетов |
| `tracert google.com` | Маршрут (traceroute) |
| `tracert -d google.com` | Без разрешения имён |
| `pathping google.com` | tracert + статистика потерь |
| `netstat` | Активные соединения |
| `netstat -ano` | + PID процессов |
| `netstat -ano \| findstr :80` | Кто слушает 80-й порт |
| `netstat -r` | Таблица маршрутизации |
| `route print` | Таблица маршрутов |
| `route add 0.0.0.0 mask 0.0.0.0 192.168.1.1` | Добавить маршрут |
| `arp -a` | Таблица ARP (MAC-адреса) |
| `nslookup example.com` | DNS-запрос |
| `ftp server.com` | FTP-клиент |
| `curl http://example.com` | HTTP-запрос (Win10+) |
| `curl -O https://site.com/file.zip` | Скачать файл |
| `wget` | ❌ Нет; используйте `curl` или PowerShell `iwr` |

### netsh — настройка сети
```cmd
netsh interface ip show config
netsh interface ip set address "Ethernet" static 192.168.1.100 255.255.255.0 192.168.1.1
netsh wlan show profiles
netsh wlan show profile name="WiFiName" key=clear    :: показать пароль WiFi
netsh advfirewall set allprofiles state off           :: отключить файрвол
```

---

## ⚙️ Система и процессы

| Команда | Действие |
|---|---|
| `systeminfo` | Информация о системе |
| `systeminfo \| findstr /B /C:"OS"` | Только ОС |
| `ver` | Версия Windows |
| `hostname` | Имя компьютера |
| `whoami` | Текущий пользователь |
| `whoami /groups` | Группы пользователя |
| `set` | Все переменные окружения |
| `set USER` | Переменные на USER |
| `echo %USERNAME%` | Имя пользователя |
| `echo %COMPUTERNAME%` | Имя ПК |
| `echo %USERPROFILE%` | Домашний каталог |
| `echo %DATE%` / `%TIME%` | Текущие дата/время |
| `tasklist` | Список процессов |
| `tasklist \| findstr chrome` | Фильтр |
| `tasklist /svc` | Процессы + службы |
| `tasklist /m` | Загруженные DLL |
| `taskkill /im chrome.exe` | Убить по имени |
| `taskkill /im chrome.exe /f` | Принудительно |
| `taskkill /pid 1234 /f` | По PID |
| `taskkill /f /im node.exe /t` | + дочерние |
| `start notepad` | Запустить в новом окне |
| `start "" "https://google.com"` | Открыть URL в браузере |
| `start file.txt` | Открыть приложением по умолчанию |
| `wmic product get name,version` | Установленные программы |
| `wmic cpu get name` | Процессор |
| `wmic bios get serialnumber` | Серийный номер |
| `shutdown /s /t 0` | Выключить сейчас |
| `shutdown /r /t 0` | Перезагрузить |
| `shutdown /l` | Выйти из системы |
| `shutdown /a` | Отменить запланированное |
| `shutdown /s /t 3600` | Через час |
| `powercfg /batteryreport` | Отчёт о батарее |
| `chkdsk C: /f` | Проверка и修复 диска |
| `sfc /scannow` | Проверка целостности системных файлов |
| `DISM /Online /Cleanup-Image /RestoreHealth` | Восстановление образа |
| `diskpart` | Управление дисками (интерактивно) |
| `driverquery` | Список драйверов |

---

## 🧰 Службы и реестр

### Службы
```cmd
sc query                        :: все службы
sc query type=service state=all
sc start "Spooler"              :: запустить
sc stop "Spooler"               :: остановить
sc config "Spooler" start=auto  :: тип запуска (auto/demand/disabled)
sc qc "Spooler"                 :: конфигурация службы
sc delete "MyService"           :: удалить

:: Альтернатива через net
net start                       :: список запущенных
net start "Spooler"             :: запустить
net stop "Spooler"              :: остановить
```

### Реестр (reg)
```cmd
:: Чтение
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion" /v ProgramFilesDir

:: Чтение всего раздела
reg query "HKCU\Software\MyApp"

:: Запись
reg add "HKCU\Software\MyApp" /v Version /t REG_SZ /d "1.0" /f

:: Удаление значения
reg delete "HKCU\Software\MyApp" /v Version /f

:: Удаление раздела
reg delete "HKCU\Software\MyApp" /f

:: Экспорт/импорт
reg export "HKCU\Software\MyApp" backup.reg
reg import backup.reg
```

Сокращения корневых ключей:
- `HKCR` = HKEY_CLASSES_ROOT
- `HKCU` = HKEY_CURRENT_USER
- `HKLM` = HKEY_LOCAL_MACHINE
- `HKU`  = HKEY_USERS
- `HKCC` = HKEY_CURRENT_CONFIG

---

## 👤 Пользователи

```cmd
net user                        :: список пользователей
net user username               :: инфо о пользователе
net user newuser password /add  :: создать
net user username /delete       :: удалить
net localgroup                  :: список групп
net localgroup administrators newuser /add   :: добавить в админы
runas /user:Administrator "cmd"  :: запустить от имени
whoami /priv                    :: привилегии
whoami /groups                  :: группы
```

---

## 📦 Управление пакетами

### winget (Windows 10/11, встроен)
```cmd
winget install Microsoft.VisualStudioCode
winget install --id Git.Git -e
winget uninstall Mozilla.Firefox
winget upgrade --all
winget list
winget search python
winget show Microsoft.VisualStudioCode
winget export packages.json
```

### chocolatey (нужно установить отдельно)
```cmd
choco install firefox googlechrome -y
choco upgrade all -y
choco uninstall nodejs -y
choco list --local-only
```

### scoop (альтернатива, для dev-инструментов)
```cmd
scoop install git curl ripgrep fd fzf bat neovim
scoop update *
scoop list
```

---

## 🔤 Переменные окружения

```cmd
:: Просмотр
set                          :: все переменные
echo %PATH%                  :: конкретная
echo %USERPROFILE%           :: домашний каталог

:: Установка (только в текущей сессии)
set MYVAR=hello
set /A NUM=5+3               :: арифметика → NUM=8
set "MYVAR=hello world"      :: безопасно (с пробелами)

:: Удаление
set MYVAR=

:: Ввод от пользователя
set /p NAME=Enter your name:

:: Постоянные переменные (для системы)
setx MYVAR "hello"           :: пользовательская (только будущие сессии)
setx MYVAR "hello" /M        :: системная (нужен admin)

:: Вставить переменную в команду
echo %PATH%;C:\new\path
```

### Часто используемые переменные
| Переменная | Что содержит |
|---|---|
| `%CD%` | Текущий каталог |
| `%DATE%` / `%TIME%` | Дата / время |
| `%RANDOM%` | Случайное число 0–32767 |
| `%ERRORLEVEL%` | Код возврата последней команды |
| `%USERNAME%` | Имя пользователя |
| `%USERPROFILE%` | `C:\Users\имя` |
| `%APPDATA%` | `C:\Users\имя\AppData\Roaming` |
| `%LOCALAPPDATA%` | `C:\Users\имя\AppData\Local` |
| `%TEMP%` / `%TMP%` | Временная папка |
| `%PROGRAMFILES%` | `C:\Program Files` |
| `%PROGRAMFILES(X86)%` | `C:\Program Files (x86)` |
| `%WINDIR%` | `C:\Windows` |
| `%COMPUTERNAME%` | Имя ПК |
| `%NUMBER_OF_PROCESSORS%` | Число ядер |
| `%OS%` | `Windows_NT` |
| `%PATH%` | Пути поиска программ |
| `%CMDCMDLINE%` | Строка запуска CMD |
| `%0` `%1` … `%9` | Аргументы батника |

---

## 🔄 Перенаправления и конвейеры

| Оператор | Действие |
|---|---|
| `command > file` | stdout в файл (перезапись) |
| `command >> file` | stdout дописать |
| `command 2> file` | stderr в файл |
| `command 2>&1` | stderr туда же, куда stdout |
| `command > nul` | Выкинуть stdout (как `/dev/null`) |
| `command 2> nul` | Выкинуть stderr |
| `command > file 2>&1` | stdout + stderr в файл |
| `command < file` | Читать stdin из файла |
| `command1 \| command2` | Конвейер (pipe) |
| `command1 & command2` | Выполнить вторую после первой (всегда) |
| `command1 && command2` | Вторую ТОЛЬКО если первая успешна |
| `command1 \|\| command2` | Вторую ТОЛЬКО если первая упала |
| `command1 \|\| command2 && command3` | Цепочки |

Примеры:
```cmd
:: Сохранить вывод в файл
ipconfig /all > network.txt

:: Дописать
echo done >> log.txt

:: Только ошибки в файл
build.exe 2> errors.log

:: И stdout и stderr в файл
build.exe > all.log 2>&1

:: Конвейер с фильтром
dir | findstr ".txt"
tasklist | find "chrome"

:: Условные операторы
mkdir newfolder && cd newfolder
copy file.txt backup.txt || echo "Ошибка копирования"
```

---

## ⏰ Планировщик задач (schtasks)

```cmd
:: Создать задачу — запускать каждый день в 9:00
schtasks /create /tn "MyBackup" /tr "C:\scripts\backup.bat" /sc daily /st 09:00

:: Запускать при входе в систему
schtasks /create /tn "Startup" /tr "prog.exe" /sc onlogon

:: Запускать каждые 30 минут
schtasks /create /tn "Sync" /tr "sync.bat" /sc minute /mo 30

:: С правами админа
schtasks /create /tn "Task" /tr "prog.exe" /sc onstart /ru "SYSTEM" /rl HIGHEST

:: Просмотр
schtasks /query /fo LIST
schtasks /query /tn "MyBackup"

:: Запустить немедленно
schtasks /run /tn "MyBackup"

:: Удалить
schtasks /delete /tn "MyBackup" /f
```

---

## 📝 Пакетные файлы (`.bat` / `.cmd`)

### Структура
```bat
@echo off
REM Это комментарий
:: Тоже комментарий (но не в некоторых местах)
echo Hello, %1

setlocal enabledelayedexpansion
set /a counter=0

:loop
set /a counter+=1
echo Counter: !counter!
if !counter! lss 5 goto loop

endlocal
pause
```

### Команды для скриптов

| Команда | Действие |
|---|---|
| `@echo off` | Не выводить сами команды (вверху скрипта) |
| `echo Текст` | Вывести текст |
| `echo.` | Пустая строка |
| `rem комментарий` | Комментарий |
| `:: комментарий` | Комментарий (короче) |
| `pause` | Ждать нажатия клавиши |
| `title Заголовок` | Заголовок окна |
| `color 0A` | Цвет фона и текста (0=чёрный, A=зелёный) |
| `prompt $P$G` | Вид приглашения |
| `cls` | Очистить экран |
| `goto label` | Переход к метке `:label` |
| `:label` | Объявление метки |
| `call script.bat` | Вызвать другой батник |
| `call :function arg1` | Вызвать функцию в этом же файле |
| `exit /b 0` | Выйти из скрипта с кодом |
| `exit 0` | Закрыть cmd с кодом |
| `setlocal` | Начало локальной области переменных |
| `endlocal` | Конец |
| `shift` | Сдвинуть аргументы (%1→%0, %2→%1) |
| `start "" prog.exe` | Запустить в новом окне |
| `timeout /t 5` | Пауза 5 секунд |
| `timeout /t 5 /nobreak` | Без возможности прервать |
| `choice /c YN /m "Да или нет"` | Выбор пользователя |

### Коды возврата (`%errorlevel%`)
```bat
@echo off
ping google.com >nul

if %errorlevel% equ 0 (
    echo Интернет работает
) else (
    echo Нет связи
)

:: Альтернативный синтаксис
ping google.com >nul && echo OK || echo FAIL
```

---

## 🔀 Управляющие конструкции

### if
```bat
:: Сравнение строк
if "%var%"=="hello" echo Совпадает
if not "%var%"=="hello" echo Не совпадает
if /i "%var%"=="HELLO" echo Без учёта регистра

:: Сравнение чисел
if %num% equ 5 echo Равно
if %num% neq 5 echo Не равно
if %num% gtr 5 echo Больше
if %num% geq 5 echo Больше или равно
if %num% lss 5 echo Меньше
if %num% leq 5 echo Меньше или равно

:: Существование файла
if exist file.txt echo Есть
if not exist file.txt echo Нет

:: Существование переменной
if defined MYVAR echo Задана

:: Блочный if (со скобками)
if %num% gtr 10 (
    echo Большое
    set result=high
) else (
    echo Малое
    set result=low
)
```

### for — циклы

Цикл `for` в CMD **очень** отличается от bash и имеет много вариантов:

```bat
:: Простой перебор списка
for %%i in (1 2 3) do echo %%i
for %%f in (*.txt) do echo %%f
for %%f in (*.txt) do copy "%%f" "backup\%%f"

:: Цикл по числам (range /L)
for /l %%i in (0,1,9) do echo %%i          :: 0..9, шаг 1
for /l %%i in (10,-2,0) do echo %%i         :: 10,8,6,4,2,0

:: Перебор файлов рекурсивно (/r)
for /r %%f in (*.log) do del "%%f"

:: Перебор строк файла (/f)
for /f "tokens=1,2" %%a in (data.txt) do echo %%a - %%b

:: Парсинг вывода команды
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do echo IP:%%a

:: Модификаторы переменной цикла
for %%f in (file.txt) do (
    echo Полный путь: %%~ff      :: полный путь
    echo Имя:        %%~nf       :: только имя
    echo Расширение: %%~xf       :: только расширение
    echo Диск:       %%~df       :: диск
    echo Путь:       %%~pf       :: путь без имени
)
```

> ⚠️ В командной строке используйте `%i`, в `.bat` — `%%i` (двойной процент).

### Модификаторы for /f
| Опция | Действие |
|---|---|
| `eol=#` | Символ комментария (до конца строки) |
| `skip=n` | Пропустить n строк в начале |
| `delims=xyz` | Разделители (по умолчанию пробел и таб) |
| `tokens=1,2,3` | Какие столбцы брать (в `%%a`, `%%b`, `%%c`) |
| `tokens=2*` | 2-й столбец + весь остаток |
| `usebackq` | Использовать обратные кавычки для команд |

---

## 🎨 Цвета и форматирование

### Команда color
```cmd
color 0A    :: чёрный фон (0), зелёный текст (A)
color 07    :: стандартные цвета
color       :: сброс к значению по умолчанию
```

Коды цветов:
| Код | Цвет | Код | Цвет |
|---|---|---|---|
| 0 | Чёрный | 8 | Серый |
| 1 | Синий | 9 | Светло-синий |
| 2 | Зелёный | A | Светло-зелёный |
| 3 | Голубой | B | Светло-голубой |
| 4 | Красный | C | Светло-красный |
| 5 | Лиловый | D | Светло-лиловый |
| 6 | Жёлтый | E | Светло-жёлтый |
| 7 | Белый | F | Ярко-белый |

> Первая цифра — фон, вторая — текст. `color FC` — красный фон, белый текст.

### ANSI-цвета (Windows 10+)
В батниках можно использовать ANSI-коды через escape-символ:
```bat
:: Создание ESC-символа (ASCII 27)
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

echo %ESC%[32mЗелёный текст%ESC%[0m
echo %ESC%[31m%ESC%[47mКрасный на белом%ESC%[0m
echo %ESC%[1mЖирный%ESC%[22m %ESC%[4mПодчёркнутый%ESC%[24m
```

---

## 🧰 Полезные команды

| Команда | Действие |
|---|---|
| `help` | Список всех команд |
| `help command` / `command /?` | Справка по команде |
| `doskey /history` | История команд |
| `doskey alias=full command $*` | Создать алиас (макрос) |
| `clip` | Копировать вывод в буфер обмена (`dir \| clip`) |
| `clip < file.txt` | Скопировать файл в буфер |
| `powershell -c "Get-Clipboard"` | Вставить из буфера |
| `sort file.txt` | Отсортировать строки |
| `sort file.txt /r` | В обратном порядке |
| `sort file.txt /unique` | Уникальные строки |
| `find /c /v "" file.txt` | Подсчёт строк |
| `mode con cols=120 lines=40` | Размер окна |
| `title My Script` | Заголовок окна |
| `subst Z: C:\path` | Назначить букву диска |
| `subst Z: /d` | Отменить |
| `powershell -c "command"` | Вызвать PowerShell из CMD |
| `start wt` | Открыть Windows Terminal |

### doskey — макросы (алиасы)
```cmd
:: Создать макрос
doskey ls=dir /b $*
doskey ll=dir $*
doskey cat=type $*
doskey grep=findstr $*
doskey ..=cd ..
doskey h=doskey /history

:: Сохранить макросы
doskey /macros > %USERPROFILE%\cmd_macros.txt

:: Применить при старте (через ярлык cmd /k doskey /macrofile=...)
```

> Макросы doskey действуют только в текущей сессии. Чтобы сохранить —
> настройте автозагрузку через ярлык `cmd /k doskey /macrofile=path`.

---

## ⌨️ Горячие клавиши CMD

| Клавиша | Действие |
|---|---|
| `Ctrl+C` | Прервать текущую команду |
| `Ctrl+Break` | Принудительно прервать |
| `Ctrl+Home` / `Ctrl+End` | Удалить до начала/конца строки |
| `Home` / `End` | В начало / конец строки |
| `↑` / `↓` | История команд |
| `F1` | Вставить символ из последней команды |
| `F2` | Вставить до указанного символа |
| `F3` | Повторить последнюю команду |
| `F4` | Удалить до указанного символа |
| `F5` | Предыдущая команда (как ↑) |
| `F7` | Список истории (выбор цифрой) |
| `F8` | История по префиксу |
| `F9` | Команда по номеру из истории |
| `Esc` | Очистить строку |
| `Tab` | Автодополнение файла/каталога |
| `Shift+←/→` | Выделение текста |
| `Ctrl+Shift+C/V` | Копировать/вставить (Win10+) |
| `Enter` | Копировать выделение (в режиме QuickEdit) |
| `Right-click` | Вставить (в режиме QuickEdit) |

### Полезные настройки окна
- **QuickEdit mode** — позволяет выделять и копировать мышью
  (Свойства → Experimental → Enable Ctrl+Shift+C/V).
- **Insert mode** — вставка вместо замены.

---

## 🐛 Дебаг и диагностика

```cmd
:: Эхо команд для отладки (временно)
@echo on

:: Вывести значение переменной
echo var=[%MYVAR%]

:: Показать код ошибки
command
echo Error level: %errorlevel%

:: Проверить синтаксис без выполнения (просто читая)
type script.bat

:: Где лежит команда?
where python
where /r C:\ python.exe

:: Проверить ассоциации файлов
assoc .py
ftype Python.File
```

---

## 🌐 Примеры скриптов

### 1. Backup с датой
```bat
@echo off
set BACKUP_DIR=D:\backups
set SRC=%USERPROFILE%\Documents
set STAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%
set STAMP=%STAMP: =0%
set STAMP=%STAMP::=%

robocopy "%SRC%" "%BACKUP_DIR%\docs_%STAMP%" /mir /xd temp
echo Backup completed: %BACKUP_DIR%\docs_%STAMP%
pause
```

### 2. Меню выбора
```bat
@echo off
:menu
cls
echo 1. Запустить сервис
echo 2. Остановить сервис
echo 3. Статус
echo 4. Выход
set /p choice=Выбор:

if "%choice%"=="1" net start "MyService"
if "%choice%"=="2" net stop "MyService"
if "%choice%"=="3" sc query "MyService"
if "%choice%"=="4" exit
goto menu
```

### 3. Массовое переименование
```bat
@echo off
setlocal enabledelayedexpansion
for %%f in (*.jpg) do (
    set name=%%~nf
    ren "%%f" "vacation_!name:~0,4!%%~xf"
)
```

### 4. Пинг нескольких хостов
```bat
@echo off
for %%h in (google.com github.com stackoverflow.com) do (
    ping -n 1 %%h >nul && echo %%h: OK || echo %%h: FAIL
)
```

### 5. Установка программ через winget
```bat
@echo off
echo Установка софта...
winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
winget install --id Microsoft.VisualStudioCode -e --accept-source-agreements --accept-package-agreements
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
echo Готово!
pause
```

---

## 🪤 Частые ошибки и грабли

1. **Пробелы в путях** — `cd C:\Program Files` упадёт; используйте кавычки:
   `cd "C:\Program Files"`.
2. **`%var%` в блоках `if`/`for`** — раскрывается **один раз** при парсинге блока.
   Для обновления внутри блока включайте `setlocal enabledelayedexpansion`
   и используйте `!var!`.
3. **`&` vs `&&`** — `&` выполняет обе команды, `&&` только если первая успешна.
4. **`>` в строке** — `echo a > b` запишет в файл; экранируйте `^>`: `echo a ^> b`.
5. **`%` в батнике** — удваивайте: `echo 50%%` выведет `50%`.
6. **Цикл `for`** — `%i` в командной строке, `%%i` в батнике.
7. **Чувствительность к регистру** — команды нечувствительны, но переменные
   и пути в CMD тоже (по умолчанию).
8. **`del` без подтверждения** — добавляйте `/q` для пакетов.
9. **`set VAR = value`** — создаст переменную с пробелом в имени и значении!
   Делайте `set "VAR=value"` (кавычки защищают).
10. **`rmdir /s`** без проверки пути — может удалить всё. Всегда проверяйте.
11. **Кодировка** — `chcp 65001` для UTF-8 (по умолчанию cp866/cp1251).
12. **`::` внутри скобок** — может ломать блоки; используйте `rem` внутри `()`.

---

## 🔗 Полезные ссылки

- Справочник команд SS64: https://ss64.com/nt
- Microsoft Learn CMD: https://learn.microsoft.com/windows-server/administration/windows-commands/windows-commands
- Robocopy reference: https://learn.microsoft.com/windows-server/administration/windows-commands/robocopy
- Bat-файлы учебник: https://www.tutorialspoint.com/batch_script
- Doskey reference: https://ss64.com/nt/doskey.html
- CMD на Wikipedia: https://ru.wikipedia.org/wiki/Cmd.exe

---

## 💡 Полезные советы

1. **Используйте `robocopy`** вместо `copy`/`xcopy` для резервного копирования —
   он надёжнее, умеет докачку, многопоточность, логи.
2. **`tab`** автодополняет имена файлов/каталогов (как в bash).
3. **`F7`** открывает список истории с выбором.
4. **`where`** — это аналог `which` в Linux.
5. **`findstr`** — это `grep` (с ограниченной поддержкой regex).
6. **`winget`** (Win10/11) — современный пакетный менеджер от Microsoft.
7. **`start`** — открывает файлы приложением по умолчанию, URLs в браузере.
8. **Для сложных задач — переходите на PowerShell.** CMD хорош для простого,
   но PS мощнее (объекты, функции, модули).
9. **`chcp 65001`** в начале батника — для корректного UTF-8.
10. **`setlocal enabledelayedexpansion`** — обязательно для счётчиков в циклах.
11. **`@echo off`** в начале — стандарт, чтобы не выводить команды.
12. **`2>nul`** — скрыть ошибки (но осторожно — упускаете важное).
13. **Windows Terminal** (`wt`) — современная обёртка с вкладками, намного
    удобнее классического `cmd.exe`.
14. **`timeout /t N`** лучше старого `ping -n N 127.0.0.1 > nul`.
15. **Тестируйте `rmdir /s /q` и `del /s`** на тестовых данных — они опасны.

---

*Сгенерировано как шпаргалка. CMD стар, но живуч —
углубляйтесь через `command /?` и https://ss64.com/nt*

# 💻 PowerShell — шпаргалка по командам и скриптингу

> **PowerShell** — кроссплатформенная оболочка и язык сценариев от Microsoft
> (Windows PowerShell 5.1 на .NET Framework; PowerShell 7+ на .NET — кроссплатформенный).
> Документация: https://learn.microsoft.com/powershell
>
> Ключевая особенность: cmdlet'ы работают с **объектами** (не с текстом),
> вывод можно передавать по конвейеру и фильтровать как данные.

---

## 🚀 Запуск и версия

| Команда | Действие |
|---|---|
| `pwsh` | Запустить PowerShell 7+ (кроссплатформенный) |
| `powershell` | Запустить Windows PowerShell 5.1 |
| `$PSVersionTable` | Версия и сведения о среде |
| `Get-Host` | Информация о хосте |
| `Exit` / `exit` | Выйти |

Установка PowerShell 7 на Linux:
```bash
# Arch / CachyOS (AUR)
yay -S powershell-bin
# или через snap
sudo snap install powershell --classic
```

---

## 🧭 Навигация

| Команда | Эквивалент bash | Действие |
|---|---|---|
| `Get-Location` / `gl` / `pwd` | `pwd` | Текущий путь |
| `Set-Location <dir>` / `cd` / `sl` | `cd` | Сменить каталог |
| `Set-Location ..` | `cd ..` | На уровень вверх |
| `Set-Location ~` | `cd ~` | Домашний каталог |
| `Set-Location -` | `cd -` | Предыдущий каталог |
| `Push-Location <dir>` / `pushd` | `pushd` | Перейти с запоминанием |
| `Pop-Location` / `popd` | `popd` | Вернуться |
| `Get-ChildItem` / `gci` / `ls` / `dir` | `ls` | Список файлов |
| `Get-ChildItem -Force` | `ls -a` | Со скрытыми |
| `Get-ChildItem -Recurse` | `ls -R` | Рекурсивно |
| `Get-ChildItem *.py` | `ls *.py` | По шаблону |
| `Tree` | `tree` | Дерево каталогов |
| `Clear-Host` / `cls` / `clear` | `clear` | Очистить экран |

> ⚠️ `ls`, `cd`, `cp`, `mv`, `rm`, `cat` — это **алиасы**, под капотом работают
> настоящие cmdlet'ы. У них **другие** параметры: `ls -la` в PowerShell НЕ сработает,
> надо `Get-ChildItem -Force`.

---

## 🔤 Алиасы и глаголы

PowerShell использует правило **Глагол-Существительное** (`Verb-Noun`).

| Алиас | Полная команда | Эквивалент bash |
|---|---|---|
| `ls` / `dir` / `gci` | `Get-ChildItem` | `ls` |
| `cd` / `sl` | `Set-Location` | `cd` |
| `pwd` / `gl` | `Get-Location` | `pwd` |
| `cp` / `copy` / `cpi` | `Copy-Item` | `cp` |
| `mv` / `move` / `mi` | `Move-Item` | `mv` |
| `rm` / `del` / `ri` | `Remove-Item` | `rm` |
| `cat` / `type` / `gc` | `Get-Content` | `cat` |
| `echo` / `write` | `Write-Output` | `echo` |
| `clear` / `cls` | `Clear-Host` | `clear` |
| `curl` / `iwr` | `Invoke-WebRequest` | `curl` |
| `wget` / `irm` | `Invoke-RestMethod` | — |
| `select` | `Select-Object` | — |
| `where` / `?` | `Where-Object` | `grep` (фильтр) |
| `foreach` / `%` | `ForEach-Object` | `xargs`/`for` |
| `sort` | `Sort-Object` | `sort` |
| `group` / `group` | `Group-Object` | `uniq -c` |
| `measure` | `Measure-Object` | `wc` |
| `compare` | `Compare-Object` | `diff` |
| `test` | `Test-Path` | `test -e` |
| `ni` | `New-Item` | `touch`/`mkdir` |
| `hp` | `Get-Help` | `man` |
| `gcm` | `Get-Command` | `which`/`type` |
| `gm` | `Get-Member` | (интроспекция) |

### Глаголы (approved verbs)
| Глагол | Назначение |
|---|---|
| `Get-` | Получить |
| `Set-` | Установить |
| `New-` | Создать |
| `Remove-` | Удалить |
| `Add-` | Добавить |
| `Copy-` / `Move-` | Копировать / переместить |
| `Invoke-` | Вызвать действие (запрос, команда) |
| `Test-` | Проверить условие |
| `ConvertTo-` / `ConvertFrom-` | Преобразовать |
| `Select-` / `Where-` | Выбрать поля / отфильтровать |
| `Write-` | Вывести |
| `Out-` | Направить вывод |

### Полезные команды интроспекции
```powershell
Get-Command                  # все доступные команды
Get-Command *-Service        # все cmdlet'ы про Service
Get-Command git              # где лежит команда (аналог which)
Get-Alias                    # список всех алиасов
Get-Alias ls                 # раскрыть алиас
Get-Member                   # свойства/методы объекта (по конвейеру!)
Get-Process | Get-Member     # типы объектов процесса
Get-Help Get-Process -Full   # полный мануал
Get-Help Get-Process -Examples   # только примеры
Update-Help                  # скачать свежую документацию
```

---

## 📄 Работа с файлами

| Команда | Действие |
|---|---|
| `New-Item file.txt` | Создать файл |
| `New-Item -ItemType Directory dir1` | Создать каталог |
| `ni folder -ItemType Directory` | Коротко |
| `Copy-Item src dst -Recurse` | Копировать |
| `Move-Item src dst` | Переместить / переименовать |
| `Rename-Item old.txt new.txt` | Переименовать |
| `Remove-Item file` | Удалить |
| `Remove-Item folder -Recurse -Force` | Удалить каталог рекурсивно |
| `Test-Path file.txt` | Существует? (`True`/`False`) |
| `Get-Item file` | Информация о файле |
| `Get-Item file | Select-Object Length, LastWriteTime` | Размер и дата |
| `Get-Content file.txt` | Вывести файл |
| `Get-Content file -Tail 20` | Последние 20 строк |
| `Get-Content file -Wait` | Следить (как `tail -f`) |
| `Set-Content file "text"` | Записать (перезаписать) |
| `Add-Content file "text"` | Дописать |
| `Clear-Content file` | Очистить содержимое |

### Чтение/запись через .NET-классы
```powershell
# Прочитать весь файл как одну строку
[IO.File]::ReadAllText("file.txt")

# Записать без BOM (UTF-8)
[IO.File]::WriteAllText("out.txt", $content)

# Прочитать как массив строк
Get-Content file.txt | ForEach-Object { $_.ToUpper() }
```

---

## 🔍 Поиск и фильтрация

```powershell
# Поиск файлов
Get-ChildItem -Filter "*.py" -Recurse
Get-ChildItem -Path . -Recurse -Include *.log
Get-ChildItem | Where-Object Name -like "*.txt"
Get-ChildItem | Where Length -gt 10MB       # больше 10 МБ
Get-ChildItem | Where LastWriteTime -gt (Get-Date).AddDays(-7)

# Поиск текста в файлах (аналог grep)
Select-String -Path *.py -Pattern "def "        # аналог grep
Select-String -Pattern "TODO" -Recurse
sls "error" log.txt -SimpleMatch               # без регулярок
sls "\d{4}-\d{2}" log.txt                       # с регулярками
Select-String "TODO" *.py | Select LineNumber, Line

# Сравнение с bash
# bash:   grep -r "TODO" .
# pwsh:   Get-ChildItem -Recurse -File | Select-String "TODO"
```

---

## 🧠 Объекты и конвейер (pipeline)

Главное отличие от bash: **по конвейеру идут объекты**, а не текст.

```powershell
# Каждый процесс — это объект со свойствами
Get-Process | Select-Object Name, CPU, WorkingSet
Get-Process | Where-Object CPU -gt 10 | Sort-Object CPU -Descending
Get-Process | Sort-Object WS -Descending | Select-Object -First 5

# Группировка и подсчёт
Get-Process | Group-Object Company | Sort-Object Count -Descending
Get-ChildItem | Group-Object Extension | Select Name, Count

# Мера (счёт, сумма, среднее)
Get-ChildItem *.log | Measure-Object Length -Sum
(Get-ChildItem -Recurse -File | Measure-Object Length -Sum).Sum / 1MB

# Форматирование вывода
Get-Process | Format-Table Name, CPU -AutoSize      # таблица
Get-Process | Format-List Name, CPU, Path           # список
Get-Process | Format-Wide Name -Column 4            # в несколько колонок

# Ограничение и уникальность
Get-Process | Select-Object -First 5
Get-Process | Select-Object -Last 3
Get-Process | Select-Object Company -Unique
```

### Where-Object — синтаксис фильтра
```powershell
# Полная форма (script block)
Get-Process | Where-Object { $_.CPU -gt 10 -and $_.Name -like "*chrome*" }

# Сокращённая (comparison statement) — для простых условий
Get-Service | Where-Object Status -eq "Running"
Get-ChildItem | Where-Object Length -gt 1MB
Get-ChildItem | Where-Object Name -match "\.log$"     # regex

# $_ — текущий объект в конвейере
1..10 | Where-Object { $_ % 2 -eq 0 }                  # чётные
```

### Операторы сравнения
| Оператор | Описание |
|---|---|
| `-eq` / `-ne` | равно / не равно |
| `-gt` / `-ge` | больше / больше или равно |
| `-lt` / `-le` | меньше / меньше или равно |
| `-like` / `-notlike` | шаблон (с `*` и `?`) |
| `-match` / `-notmatch` | регулярное выражение |
| `-contains` / `-notcontains` | есть ли в массиве |
| `-in` / `-notin` | элемент в наборе |
| `-and` / `-or` / `-not` / `!` | логические |
| `-replace` | замена по регулярке |
| `-split` / `-join` | разрезать / склеить |
| `+` `-` `*` `/` `%` | арифметические |

> ⚠️ В PowerShell операторы **не** символы (`>`, `<`), а слова (`-gt`, `-lt`).
> `>` используется для перенаправления вывода в файл.

---

## 🔢 Переменные

```powershell
$name = "Alice"               # все переменные начинаются с $
$age = 30
$pi = 3.14
$arr = 1, 2, 3, 4             # массив
$arr = @(1, 2, 3)             # явный массив
$hash = @{ Name="Alice"; Age=30 }   # хеш-таблица
$true / $false / $null        # встроенные

# Сильная типизация (опционально)
[int]$count = 10
[string]$name = "Bob"
[datetime]$date = "2024-01-01"

# Вывод
$name                          # просто написать — выведет
Write-Output $name             # явный вывод
Write-Host "Hi" -F Green       # цветной вывод (как echo -e)

# Область видимости
$global:counter = 0            # глобальная
$script:config = @{}           # на уровне скрипта
$local:tmp = 1                 # локальная

# Специальные
$_        # текущий объект в конвейере
$PSItem   # то же, что $_
$?        # успех последней команды (True/False)
$LASTEXITCODE  # код выхода внешней программы
$args     # аргументы скрипта/функции
$PID      # PID текущего процесса
$Host     # информация о хосте
$error[0] # последняя ошибка
$Matches  # результаты последнего -match (хеш регулярок)
```

---

## 📊 Строки

```powershell
# Одинарные кавычки — литерал (без подстановки)
$name = "World"
'Hello $name'         # → Hello $name (буквально)
"Hello $name"         # → Hello World (с подстановкой)

# Подстановка выражений ($(...))
"2 + 2 = $(2 + 2)"
"Files: $(Get-ChildItem).Count"
"Date: $((Get-Date).ToString('yyyy-MM-dd'))"

# Here-string (многострочный)
$text = @"
Первая строка
Подставка: $name
Дата: $(Get-Date)
"@

# Here-string литерал (без подстановки)
$text = @'
Буквально $name
'@

# Длина и индекс
"hello".Length               # 5
"hello"[0]                   # 'h'
"hello".ToUpper()            # HELLO
"Hello".ToLower()            # hello
"  hi  ".Trim()              # hi
"hello".Replace("l", "L")    # heLLo
"hello".Substring(1, 3)      # ell
"a,b,c".Split(",")           # массив ['a','b','c']
("a","b","c") -join "|"      # a|b|c
"hello world" -replace "o","0"   # hell0 w0rld
"hello" -match "l+"          # True (regex), результат в $Matches
```

---

## 🔁 Управляющие конструкции

### if / elseif / else
```powershell
if ($age -lt 18) {
    "Несовершеннолетний"
} elseif ($age -eq 18) {
    "Ровно 18"
} else {
    "Взрослый"
}
```

### switch
```powershell
switch ($day) {
    "Monday"    { "Понедельник"; break }
    "Tuesday"   { "Вторник"; break }
    default     { "Другой день" }
}

# switch по условиям (мощно!)
switch ($score) {
    { $_ -ge 90 } { "A"; break }
    { $_ -ge 80 } { "B"; break }
    { $_ -ge 70 } { "C"; break }
    default       { "F" }
}

# switch по regex
switch -Regex ($line) {
    "^ERROR"  { Write-Host $_ -F Red }
    "^WARN"   { Write-Host $_ -F Yellow }
    default   { Write-Host $_ }
}
```

### for / foreach / while / do
```powershell
# for (как C)
for ($i = 0; $i -lt 5; $i++) { $i }

# foreach по коллекции
foreach ($f in Get-ChildItem *.txt) { $f.Name }

# foreach по конвейеру (|% или ForEach-Object)
1..5 | ForEach-Object { $_ * 2 }     # 2 4 6 8 10
Get-Process | ForEach-Object { $_.Name }

# while
$i = 0
while ($i -lt 5) { $i; $i++ }

# do-while / do-until
do { $i++ } while ($i -lt 10)
do { $i++ } until ($i -ge 10)

# break / continue
foreach ($n in 1..10) {
    if ($n -eq 5) { break }
    if ($n % 2 -eq 0) { continue }
    $n
}
```

---

## 🧮 Функции

```powershell
# Простая функция
function Greet {
    param($name)
    "Hello, $name!"
}
Greet -name "Alice"

# С типами, значениями по умолчанию и описанием
function Add {
    param(
        [int]$a,
        [int]$b = 10,
        [string]$label = "Sum"
    )
    $sum = $a + $b
    "$label: $sum"
    return $sum        # return опционален, всё выводимое вернётся
}
Add -a 5 -b 3           # → "Sum: 8"

# Advanced function (с [CmdletBinding])
function Get-Greeting {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,
        [int]$Times = 1
    )
    1..$Times | ForEach-Object { "Hi, $Name!" }
}
Get-Greeting -Name "Bob" -Times 3
```

> ⚠️ Особенность: функция возвращает **всё, что выводится** в потоке output,
> а не только значение после `return`. `return` лишь прерывает выполнение.

---

## 📤 Ввод/вывод и перенаправления

```powershell
# Перенаправление в файл
Get-Process > procs.txt              # перезаписать
Get-Process >> procs.txt             # дописать
Get-Process | Out-File procs.txt     # явно (с кодировкой)
Get-Process | Out-File -Encoding utf8 procs.txt

# Импорт/экспорт CSV
Get-Process | Export-Csv procs.csv -NoTypeInformation
Import-Csv procs.csv | Select Name, CPU

# Экспорт в HTML
Get-Process | ConvertTo-Html | Out-File procs.html

# Конвертация в JSON/XML
Get-Process | Select -First 3 | ConvertTo-Json -Depth 3
"key","val" | ConvertTo-Xml -As Text

# Вывод в Grid View (Windows) — таблица с фильтрами
Get-Process | Out-GridView

# Null-устройство
$output = $null
Get-Process | Out-Null               # выкинуть вывод

# Чтение ввода
$name = Read-Host "Введите имя"
$pass = Read-Host "Пароль" -AsSecureString

# Write-Host с цветом
Write-Host "Error" -ForegroundColor Red -BackgroundColor Black
Write-Host "OK" -ForegroundColor Green
```

### Потоки (streams)
| Номер | Поток | Перенаправление |
|---|---|---|
| 1 | Success output | `>` `>>` `1>` |
| 2 | Error | `2>` `2>&1` |
| 3 | Warning | `3>` |
| 4 | Verbose | `4>` |
| 5 | Debug | `5>` |
| 6 | Information | `6>` |
| * | All streams | `*>` |

```powershell
# Слить stdout + stderr
Get-Process 2>&1 | Out-File all.txt
# Слить всё
cmd *> out.txt
```

---

## 🌐 Сеть и Web

```powershell
# HTTP-запрос (аналог curl)
Invoke-WebRequest "https://api.github.com"           # iwr / curl
$response = Invoke-RestMethod "https://api.github.com/repos/microsoft"  # irm, возвращает объект
$response.name                                       # свойство объекта!

# Скачать файл
Invoke-WebRequest "https://site.com/file.zip" -OutFile file.zip
iwr "https://site.com/file.zip" -OutFile file.zip

# POST с JSON
$body = @{ name = "test"; value = 42 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri $url -Body $body -ContentType "application/json"

# Тест сети
Test-Connection google.com            # аналог ping
Test-NetConnection -ComputerName google.com -Port 443   # порт + traceroute

# DNS
Resolve-DnsName google.com

# IP-конфигурация
Get-NetIPConfiguration
Get-NetIPAddress
ipconfig                              # алиас на Windows

# HTTP-заголовки
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-RestMethod -Uri $url -Headers $headers
```

---

## ⚙️ Процессы и службы

```powershell
# Процессы
Get-Process                           # все процессы
Get-Process chrome                    # по имени
Get-Process | Sort CPU -Desc | Select -First 5
Start-Process notepad                 # запустить программу
Start-Process "code" -ArgumentList "."
Stop-Process -Name chrome -Force      # убить
Stop-Process -Id 1234                 # по PID
Wait-Process -Name chrome             # дождаться завершения

# Службы (Windows)
Get-Service                           # все службы
Get-Service | Where Status -eq "Running"
Get-Service -Name "Spooler"
Start-Service Spooler
Stop-Service Spooler
Restart-Service Spooler
Set-Service -Name "Spooler" -StartupType Automatic

# События (Windows Event Log)
Get-EventLog -LogName System -Newest 20
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2} -MaxEvents 10
```

---

## 🔐 Безопасность и Execution Policy

```powershell
# Execution Policy — какие скрипты можно запускать
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Политики:
#   Restricted   — ничего (по умолчанию на клиенте)
#   RemoteSigned — локальные можно, скачанные должны быть подписаны
#   AllSigned    — все должны быть подписаны
#   Unrestricted — можно все (предупреждает)
#   Bypass       — без предупреждений

# Обойти политику для одного запуска
powershell -ExecutionPolicy Bypass -File script.ps1
pwsh -ExecutionPolicy Bypass -File script.ps1

# Запуск скрипта из интернета без сохранения
iex ((New-Object Net.WebClient).DownloadString('https://.../install.ps1'))
iex (irm "https://get.scoop.sh")
```

### Профиль (profile)
```powershell
# Где лежит профиль
$PROFILE
$PROFILE.CurrentUserCurrentHost       # для текущего пользователя
$PROFILE.AllUsersCurrentHost          # для всех

# Создать/открыть
if (!(Test-Path $PROFILE)) { New-Item $PROFILE -Force }
notepad $PROFILE                       # отредактировать

# Применить без перезапуска
. $PROFILE
```

---

## 📦 Пакетные менеджеры

### PowerShell Gallery (модули)
```powershell
Get-PSRepository
Find-Module *sql*                     # поиск
Install-Module PSReadLine -Scope CurrentUser
Install-Module Terminal-Icons -Scope CurrentUser
Update-Module PSReadLine
Uninstall-Module PSReadLine
Import-Module PSReadLine
```

### Scoop (Windows, рекомендуется)
```powershell
# Установка Scoop
iwr -useb get.scoop.sh | iex

# Использование
scoop install git curl ripgrep fd fzf bat
scoop search neovim
scoop update *
scoop list
```

### Winget (Windows)
```powershell
winget install Microsoft.VisualStudioCode
winget upgrade --all
winget list
winget search git
```

### Chocolatey (Windows)
```powershell
choco install firefox -y
choco upgrade all -y
choco list --local-only
```

### На Linux — нативный pacman/apt
```powershell
# В pwsh на Arch можно вызывать нативно
pacman -S ripgrep
```

---

## 📝 Скрипты

### Структура скрипта (`.ps1`)
```powershell
<#
.SYNOPSIS
    Краткое описание.
.DESCRIPTION
    Подробное описание.
.PARAMETER Name
    Описание параметра.
.EXAMPLE
    .\script.ps1 -Name "Alice"
.NOTES
    Author: you
#>
param(
    [string]$Name = "World",
    [switch]$Verbose
)

# Strict mode (рекомендуется)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Starting..." -F Cyan
Write-Host "Hello, $Name"
```

### Дебаг
```powershell
# Встроенный отладчик
Set-PSBreakpoint -Script script.ps1 -Line 15
Set-PSBreakpoint -Variable name -Mode Write

# Trace
Set-PSDebug -Trace 1                  # выводить каждую строку
Set-PSDebug -Off

# Подробный вывод
cmd /c dir -Verbose

# Проверка синтаксиса без выполнения
$null = [System.Management.Automation.PSParser]::Tokenize((Get-Content script.ps1 -Raw), [ref]$null)
```

### Обработка ошибок
```powershell
# try/catch/finally
try {
    Get-Content "missing.txt" -ErrorAction Stop
} catch {
    Write-Host "Ошибка: $($_.Exception.Message)" -F Red
} finally {
    Write-Host "Завершено"
}

# $ErrorActionPreference
$ErrorActionPreference = "Stop"      # останавливать при ошибке
#               = "Continue"        # продолжать (по умолчанию)
#               = "SilentlyContinue" # молча
#               = "Inquire"         # спросить

# Throw
if (!$path) { throw "Path is required" }

# Проверка последней ошибки
$error[0] | Format-List -Force
```

---

## 🛠️ Практические примеры

### 1. Массовое переименование файлов
```powershell
Get-ChildItem *.jpg | ForEach-Object {
    $newName = "img_" + $_.LastWriteTime.ToString("yyyyMMdd") + "_" + $_.Name
    Rename-Item $_.FullName $newName
}
```

### 2. Найти топ-10 самых больших файлов
```powershell
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
    Sort-Object Length -Descending |
    Select-Object -First 10 Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}}
```

### 3. Backup с проверкой
```powershell
$src = "C:\Users\me\Documents"
$dst = "D:\Backup\docs_$(Get-Date -f yyyyMMdd).zip"
if (!(Test-Path $src)) { throw "Источник не найден" }
Compress-Archive -Path $src -DestinationPath $dst -Force
Write-Host "Готово: $dst ($([math]::Round((Get-Item $dst).Length/1MB,2)) MB)" -F Green
```

### 4. Массовая обработка CSV
```powershell
Import-Csv users.csv | ForEach-Object {
    [PSCustomObject]@{
        FullName = "$($_.FirstName) $($_.LastName)"
        Email    = $_.Email.ToLower()
    }
} | Export-Csv processed.csv -NoTypeInformation
```

### /bash эквиваленты
```powershell
# bash: ps aux | grep nginx
Get-Process | Where-Object Name -like "*nginx*"

# bash: find . -name "*.py" -size +1M
Get-ChildItem -Recurse -Filter *.py | Where Length -gt 1MB

# bash: grep -rl "TODO" .
Get-ChildItem -Recurse -File | Select-String "TODO" | Select -Expand Path -Unique

# bash: cat file | wc -l
(Get-Content file).Count

# bash: kill -9 1234
Stop-Process -Id 1234 -Force

# bash: df -h
Get-Volume        # Windows
Get-PSDrive       # PowerShell drives (вкл. HKLM:, HKCU:)

# bash: curl http://example.com
(Invoke-WebRequest http://example.com).Content
```

### 6. Запрос JSON-API и обработка
```powershell
$repo = Invoke-RestMethod "https://api.github.com/repos/PowerShell/PowerShell"
"⭐ $($repo.stargazers_count) stars"
"🍴 $($repo.forks_count) forks"
"Last update: $([datetime]$repo.updated_at)"
```

---

## ⌨️ Горячие клавиши консоли (PSReadLine)

| Клавиша | Действие |
|---|---|
| `Ctrl-a` / `Ctrl-e` | В начало / конец строки |
| `Ctrl-b` / `Ctrl-f` | Влево / вправо |
| `Alt-b` / `Alt-f` | На слово назад / вперёд |
| `Ctrl-d` | Удалить символ справа |
| `Backspace` / `Ctrl-h` | Удалить символ слева |
| `Ctrl-w` | Удалить слово слева |
| `Ctrl-Delete` | Удалить слово справа |
| `Ctrl-u` | Удалить до начала |
| `Ctrl-k` | Удалить до конца |
| `Ctrl-y` / `Ctrl-v` | Вставить |
| `Ctrl-_` | Undo |
| `Ctrl-r` | Обратный поиск по истории |
| `Ctrl-s` | Прямой поиск |
| `Ctrl-l` | Очистить экран |
| `Ctrl-c` | Прервать |
| `Ctrl-Home` / `Ctrl-End` | Удалить до начала/конца буфера |
| `Tab` / `Shift-Tab` | Автодополнение (вперёд / назад) |
| `↑` / `↓` | История |
| `F7` | Список истории (встроенный) |
| `F8` | История по префиксу |
| `F9` | Команда по номеру |
| `PgUp` / `PgDn` | История в начало / конец |
| `Home` / `End` | В начало / конец строки |

### PSReadLine — улучшение истории и подсветка
В `$PROFILE`:
```powershell
# Подсветка синтаксиса в командной строке
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
Set-PSReadLineOption -EditMode Emacs            # или Windows, Vi
Set-PSReadLineOption -HistoryNoDuplicates
Set-PSReadLineOption -BellStyle None

# Подсветка цветами (PowerShell 7+)
Set-PSReadLineOption -Colors @{
    Command   = "`e[36m"
    Parameter = "`e[33m"
    String    = "`e[32m"
    Comment   = "`e[90m"
}

# Привязки клавиш
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Key Ctrl+d -Function DeleteCharOrExit
Set-PSReadLineKeyHandler -Key Ctrl+f -Function ForwardWord
```

---

## 🎨 Кастомизация промпта

```powershell
# В $PROFILE
function prompt {
    $loc = Split-Path -Leaf (Get-Location)
    $time = Get-Date -f "HH:mm"
    "$([char]27)[36m[$time]$([char]27)[33m PS $loc> $([char]27)[0m"
}

# С модулем oh-my-posh
Install-Module oh-my-posh -Scope CurrentUser
# В $PROFILE:
oh-my-posh --init --shell pwsh --config ~/.mytheme.omp.json | Invoke-Expression

# Терминальные иконки
Install-Module Terminal-Icons -Scope CurrentUser
Import-Module Terminal-Icons
```

---

## 🧩 Полезные модули

| Модуль | Что делает |
|---|---|
| `PSReadLine` | Улучшенная readline, подсветка, история |
| `Terminal-Icons` | Иконки файлов/папок в `ls` |
| `oh-my-posh` | Красивые промпты (темя dracula, agnoster, ...) |
| `posh-git` | Git-статус в промпте |
| `z` | Переход по частоте (как zoxide) |
| `PSFzf` | FZF-интерфейс в PowerShell |
| `ExchangeOnlineManagement` | Microsoft 365 |
| `Az` | Azure (Get-AzVM, ...) |
| `DbgC...

---

## 🐛 Частые ошибки и грабли

1. **`-` vs `:`** — параметры: `-Name` или `-Name value`, не `-Name=value`.
2. **Операторы сравнения** — `>`, `<` в PS это перенаправления, не сравнения!
   Используйте `-gt`, `-lt`.
3. **`&` для вызова** — `& "C:\path with space\prog.exe"`, иначе путь-строка не запустится.
4. **`return` выводит всё** — функция возвращает любой output, не только после `return`.
5. **Алиасы != bash** — `ls -la` не сработает, нужны параметры PS (`-Force`).
6. **Регистр** — команды case-insensitive, но переменные и строки обычно тоже
   (если без `-cmatch`, `-ceq`).
7. **`$()` vs `()`** — `$()` для подстановки в строках, `()` для группировки.
8. **Case-sensitive варианты** — `-ceq`, `-cmatch`, `-clike` (точное совпадение регистра).
9. **`Out-File` vs `Set-Content`** — `Out-File` форматирует как на экране (по умолчанию),
   `Set-Content` пишет как есть.
10. **ExecutionPolicy** — не мера безопасности, а защита от случайного запуска;
    обходится `-ExecutionPolicy Bypass`.
11. **BOM в файлах** — `Out-File` пишет UTF-16LE с BOM по умолчанию (Windows PS 5.1);
    используйте `-Encoding utf8` или `Set-Content -Encoding UTF8`.
12. **`$_` в pipeline** — это текущий объект, не строка. Обращайтесь к свойствам: `$_.Name`.

---

## 🔗 Ссылки

- Официальная документация: https://learn.microsoft.com/powershell
- PowerShell Gallery: https://www.powershellgallery.com
- PowerShell на GitHub: https://github.com/PowerShell/PowerShell
- Awesome PowerShell: https://github.com/janikvonrotz/awesome-powershell
- SS64 (краткие справки): https://ss64.com/ps
- Книга: *Learn Windows PowerShell in a Month of Lunches*
- DevOps: https://learn.microsoft.com/training/paths/powershell/

---

## 💡 Полезные советы

1. **Всё — объекты**: забудьте про `grep/awk/sed`-парсинг текста.
   `Get-X | Select-Object` — фильтруйте по свойствам.
2. **`Get-Member`** — ваш лучший друг, показывает свойства/методы объекта:
   `Get-Process | Get-Member`.
3. **`Select-String`** — это `grep`, ищите по файлам и содержимому.
4. **`Get-Help X -Examples`** — всегда показывает примеры, часто понятнее мануала.
5. **`Show-Command X`** — GUI-форма с параметрами команды (Windows).
6. **Тайные пути (PSDrives)** — `HKLM:`, `HKCU:`, `Env:`, `Cert:`, `Variable:`, `WSMan:`.
   `cd Env:; ls` — увидеть все переменные окружения.
7. **`Invoke-WebRequest`** — замена `curl`, но возвращает **объект** (с `.Content`,
   `.Headers`, `.StatusCode`).
8. **Pipeline с объектами** — `Get-X | Export-Csv`, `ConvertTo-Json`, `Format-Table`.
9. **Aliases** — `gal` показывает все, но в скриптах используйте полные имена для читаемости.
10. **`$PSStyle`** (PS 7.2+) — настройки ANSI-цветов и форматирования.
11. **Профиль** — настройте `$PROFILE`: промпт, алиасы, импорт модулей.
12. **PSReadLine + oh-my-posh + Terminal-Icons** — делают PowerShell почти как zsh.
13. **Кроссплатформенность** — PowerShell 7+ работает на Linux/macOS; используйте
    `pwsh` вместо `powershell`.
14. **Не делайте `Remove-Item -Recurse -Force`** без проверки пути!
15. **`#Requires -Version 7`** в начале скрипта — зафиксировать минимальную версию.

---

*Сгенерировано как шпаргалка. PowerShell огромен —
углубляйтесь через `Get-Help <cmd> -Full`, `Get-Command *-X*` и
https://learn.microsoft.com/powershell*

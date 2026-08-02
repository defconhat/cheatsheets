# 🐚 Bash — шпаргалка по скриптингу и использованию

> **bash** — стандартная оболочка Linux (Bourne-Again Shell).
> Мануал: `man bash` · Справочник: https://www.gnu.org/software/bash/manual
>
> Применимо к большинству POSIX-shell'ов (с оговорками для zsh/fish).

---

## 🚀 Базовый синтаксис

### Shebang
```bash
#!/usr/bin/env bash
# Всегда ставьте в первой строке скрипта.
# Использование env — портативно (находит bash в PATH).
```

### Строгий режим (рекомендуется всегда)
```bash
set -euo pipefail
# -e          выйти при ошибке любой команды
# -u          ошибка при использовании несуществующей переменной
# -o pipefail_pipeline] код ошибки последней упавшей команды в пайпе
IFS=$'\n\t'   # безопасный разделитель полей
```

### Запуск скрипта
```bash
chmod +x script.sh
./script.sh                 # как исполняемый

bash script.sh              # явно через bash
bash -x script.sh           # с трассировкой (debug)
bash -n script.sh           # только проверка синтаксиса
source script.sh  /  . script.sh   # выполнить в текущем shell
```

---

## 💬 Комментарии и вывод

```bash
# Это комментарий
echo "Hello"               # простейший вывод
echo -n "без перевода"      # без \n
echo -e "строка\tс\tтабами" # интерпретация escape
printf "Имя: %-10s Возраст: %d\n" "$name" "$age"   # форматированный
```

---

## 🔤 Переменные

```bash
name="Alice"               # БЕЗ пробелов вокруг =
age=30
readonly PI=3.14           # константа
unset name                 # удалить переменную

# Использование
echo "$name"               # всегда берите в кавычки!
echo "${name}"             # явный синтаксис
echo "$name_$suffix"       # неоднозначно
echo "${name}_$suffix"     # правильно
greeting="Hi, $name!"      # подстановка внутри строки
```

### ⚠️ Важно про кавычки
```bash
file="my file.txt"
ls $file          # ОШИБКА: разобьётся на "my" и "file.txt"
ls "$file"        # ПРАВИЛЬНО: один аргумент
ls "$file".bak    # с дополнительным текстом

# Разница одинарных и двойных:
echo "$name"      # значение переменной
echo '$name'      # буквально $name
echo "`date`"     # вывод команды (старый синтаксис)
echo "$(date)"    # вывод команды (современный, предпочтительный)
```

---

## 📥 Чтение ввода

```bash
read -p "Введите имя: " name        # с приглашением
read -s -p "Пароль: " password      # молча (как пароль)
read -a nums                        # в массив (через пробел)
read line                           # вся строка в $line
read -r line                        # -r не интерпретировать \
IFS=: read user passwd uid < /etc/passwd   # с разделителем
```

---

## 🎯 Параметры и аргументы

```bash
./script.sh foo bar baz
# $0 = ./script.sh (имя скрипта)
# $1 = foo          (1-й аргумент)
# $2 = bar
# $3 = baz
# $# = 3            (число аргументов)
# $@ = foo bar baz  (все аргументы, по одному)
# "$@"              ← так правильно (сохраняет пробелы в аргументах)
# $* = foo bar baz  (одна строка)
```

### Разбор аргументов (getopts)
```bash
while getopts ":a:b:cv" opt; do
  case $opt in
    a) arg_a="$OPTARG" ;;
    b) arg_b="$OPTARG" ;;
    c) flag_c=1 ;;
    v) verbose=1 ;;
    \?) echo "Неизвестный: -$OPTARG" >&2; exit 1 ;;
    :)  echo "Требуется аргумент: -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND -1))   # отбросить разобранные опции
echo "Остальные: $@"
```

---

## 🔢 Арифметика

```bash
# Только целые числа!
x=5
y=3
echo $((x + y))          # 8 — сложение
echo $((x - y))          # 2
echo $((x * y))          # 15
echo $((x / y))          # 1 (целочисленное!)
echo $((x % y))          # 2 (остаток)
echo $((2 ** 10))        # 1024 (степень)
((x++))                  # инкремент
((x += 5))               # сокращённые операторы
((x > 4)) && echo yes    # сравнение

# Сравнения возвращают 0 (true) / 1 (false) для if
if (( x >= 18 )); then echo "взрослый"; fi
```

### Дробные числа — нужен bc/awk
```bash
echo "scale=2; 10/3" | bc        # 3.33
echo "3.14 * 2" | bc             # 6.28
awk 'BEGIN { print 10/3 }'        # 3.33333
```

---

## 📊 Строки

```bash
s="Hello, World"
echo "${#s}"              # 12 — длина строки
echo "${s:0:5}"           # "Hello" — срез с 0, 5 символов
echo "${s:7}"             # "World" — с 7-го символа до конца
echo "${s,}"              # "hello, World" — первый символ в нижний регистр
echo "${s^^}"             # "HELLO, WORLD" — весь в верхний
echo "${s,,}"             # весь в нижний
echo "${s//o/0}"          # "Hell0, W0rld" — замена всех вхождений
echo "${s/o/0}"           # "Hell0, World" — только первое
echo "${s/#Hello/Hi}"     # "Hi, World" — в начале
echo "${s/%World/Earth}"  # "Hello, Earth" — в конце
echo "${s#H}"             # "ello, World" — удалить префикс (короткий)
echo "${s##He}"           # "llo, World" — удалить префикс (жадный)
echo "${s%d}"             # "Hello, Worl" — удалить суффикс
echo "${s%,*}"            # "Hello"      — до первой запятой
echo "${s#*, }"           # "World"      — после запятой
```

### Мнемоника для `#` и `%`
- **`#`** — на клавиатуре слева от `$` → удаляет **слева** (префикс)
- **`%`** — справа от `$` → удаляет **справа** (суффикс)

---

## 📋 Массивы

```bash
# Обычные массивы (индексные)
fruits=("apple" "banana" "cherry")
fruits+=("date")              # добавить элемент
echo "${fruits[0]}"           # apple
echo "${fruits[@]}"           # все элементы
echo "${#fruits[@]}"          # 4 — число элементов
echo "${!fruits[@]}"          # индексы: 0 1 2 3
fruits[1]="blueberry"        # изменить
unset 'fruits[0]'             # удалить элемент

# Перебор
for f in "${fruits[@]}"; do echo "$f"; done

# Ассоциативные (как dict/map)
declare -A person
person[name]="Alice"
person[age]=30
echo "${person[name]}"
for key in "${!person[@]}"; do echo "$key = ${person[$key]}"; done
```

---

## 🔀 Условия

### if / elif / else
```bash
if [[ -z "$var" ]]; then
    echo "пустая"
elif [[ "$var" == "yes" ]]; then
    echo "да"
else
    echo "другое"
fi
```

### `[[ ]]` vs `[ ]` vs `test`
- **`[[ ]]`** — расширенный синтаксис bash, безопасный, используйте его.
- **`[ ]`** — POSIX-вариант, медленнее, для совместимости.
- `test` — то же, что `[ ]`.

```bash
[[ $a == $b ]]      # строки равны
[[ $a != $b ]]      # не равны
[[ $a < $b ]]       # лексикографическое (в алфавите)
[[ $a =~ ^[0-9]+$ ]]# регулярное выражение!
[[ -n $a ]]         # не пустая
[[ -z $a ]]         # пустая
```

### Файловые проверки
```bash
[[ -e file ]]       # существует
[[ -f file ]]       # обычный файл
[[ -d dir  ]]       # каталог
[[ -L link ]]       # символическая ссылка
[[ -r file ]]       # читаемый
[[ -w file ]]       # writable
[[ -x file ]]       # исполняемый
[[ -s file ]]       # непустой (size > 0)
[[ file1 -nt file2 ]]  # новее
[[ file1 -ot file2 ]]  # старше
```

### Числовые сравнения (в `[ ]`)
```bash
[ $a -eq $b ]    # равно
[ $a -ne $b ]    # не равно
[ $a -lt $b ]    # меньше
[ $a -le $b ]    # меньше или равно
[ $a -gt $b ]    # больше
[ $a -ge $b ]    # больше или равно
# В (( )) можно обычными < > <= >= == !=
```

### case (switch)
```bash
case "$1" in
    start)   echo "Запуск";;
    stop)    echo "Остановка";;
    restart) echo "Перезапуск";;
    status)  echo "Статус";;
    -h|--help) echo "Использование: $0 {start|stop|restart}";;
    *)       echo "Неизвестная команда: $1" >&2; exit 1;;
esac
```

### Тернарный оператор
```bash
[[ -f config ]] && source config || echo "нет конфига"
result=$(( x > 5 ? 1 : 0 ))
```

---

## 🔁 Циклы

### for
```bash
for i in 1 2 3 4 5; do echo "$i"; done
for i in {1..5};        do echo "$i"; done    # range
for i in {1..10..2};    do echo "$i"; done    # шаг 2
for i in {a..z};        do echo "$i"; done    # буквы
for f in *.txt;         do echo "$f"; done    # glob
for f in "$@";          do echo "арг: $f"; done
for ((i=0; i<10; i++)); do echo "$i"; done    # C-style

# C-style над массивом
arr=(a b c)
for ((i=0; i<${#arr[@]}; i++)); do echo "${arr[i]}"; done
```

### while / until
```bash
n=0
while (( n < 5 )); do echo "$n"; ((n++)); done

while read -r line; do     # читать файл построчно
    echo "$line"
done < file.txt

# while с пайпом (subshell — переменные не выйдут наружу!)
some_cmd | while read -r line; do
    count=$((count+1))
done
# Чтобы переменные сохранились — используйте lastpipe или process substitution:
while read -r line; do
    count=$((count+1))
done < <(some_cmd)
```

### break / continue
```bash
for i in {1..10}; do
    [[ $i -eq 5 ]] && break        # выход из цикла
    [[ $((i%2)) -eq 0 ]] && continue  # пропуск чётных
    echo "$i"
done
```

---

## 🧮 Функции

```bash
# Два синтаксиса
greet() {
    local name="$1"           # local — важная штука!
    echo "Hello, $name"
    return 0                  # код возврата (0-255), не значение!
}

function greet2 {              # устаревший синтаксис
    echo "Hi"
}

# Вызов
greet "Alice"
greet "Alice" "Bob"           # лишние аргументы игнорируются
# Внутри функции: $1, $2, $@, $# — аргументы функции (не скрипта)

# "Возврат значения" — через echo + подстановку
get_pid() { pgrep -x nginx; }
pid=$(get_pid)
```

---

## 📤 Ввод/вывод и перенаправления

```bash
cmd > file          # stdout в файл (перезапись)
cmd >> file         # stdout дописать
cmd 2> file         # stderr в файл
cmd > file 2>&1     # stdout + stderr в файл
cmd &> file         # то же (короткая форма в bash)
cmd > /dev/null 2>&1  # выкинуть весь вывод
cmd < file          # stdin из файла
cmd << 'EOF'        # heredoc (буквальный, без подстановки)
строка1
$name               # так НЕ подставится
EOF

cmd << EOF          # heredoc с подстановкой переменных
привет, $USER
EOF

cmd <<< "строка"    # here-string (одна строка в stdin)

# Process substitution
diff <(ls dir1) <(ls dir2)        # выводы команд как файлы
while read x; do ...; done < <(find . -name '*.py')
```

### Дескрипторы
| FD | Что |
|---|---|
| 0 | stdin (ввод) |
| 1 | stdout (вывод) |
| 2 | stderr (ошибки) |

---

## 🚦 Коды возврата и проверка команд

```bash
cmd && echo "успех (код 0)"
cmd || echo "провал (код ≠ 0)"
cmd1 && cmd2 && cmd3       # цепочка успехов
cmd1 || cmd2 || cmd3       # цепочка фолбэков

if cmd; then ...; fi       # выполняется, если код 0
echo $?                    # код возврата последней команды
true; echo $?              # 0
false; echo $?             # 1
! cmd                      # инверсия кода
```

---

## 🧰 Подстановка команд и процессов

```bash
today=$(date +%Y-%m-%d)        # подстановка вывода
files=$(ls *.txt)
count=$(ls | wc -l)

# Глоббинг (раскрытие имён файлов)
ls *.txt          # все .txt
ls *.{txt,md}     # txt и md
ls file?.txt      # один любой символ
ls file[0-9].txt  # цифра
ls file[!a-c].txt # НЕ a,b,c

# Включить расширенный глоббинг
shopt -s extglob
ls !(test).txt    # всё, кроме test.txt
ls @(foo|bar)*    # foo или bar в начале
```

---

## 🛠️ trap — обработка сигналов и завершения

```bash
cleanup() {
    echo "Удаляю временные файлы..."
    rm -f "$TMPFILE"
}
trap cleanup EXIT INT TERM   # вызов при выходе/Ctrl-C/kill

TMPFILE=$(mktemp)
# ...работа...
# cleanup вызовется автоматически
```

Полезные сигналы:
| Сигнал | Событие |
|---|---|
| `EXIT` | Завершение скрипта (любое) |
| `INT` | Ctrl-C |
| `TERM` | `kill` (по умолчанию) |
| `HUP` | Закрытие терминала |
| `ERR` | Ошибка команды (с `set -e`) |

---

## 🌍 Переменные окружения

```bash
export VAR="value"        # сделать переменную env-переменной
env                       # показать все env-переменные
printenv PATH             # конкретная переменная
echo "$PATH"              # текущий PATH
PATH="$PATH:/new/dir"     # добавить в PATH

# Дочерний процесс наследует env-переменные (export-нутые),
# но не обычные локальные переменные.
NAME=Alice bash -c 'echo $NAME'   # одноразовая env для команды
```

### Специальные переменные
| Переменная | Что |
|---|---|
| `$?` | Код возврата последней команды |
| `$!` | PID последнего фонового процесса |
| `$$` | PID текущего shell |
| `$0` | Имя скрипта/shell |
| `$-` | Текущие опции (как у `set`) |
| `$_` | Последний аргумент предыдущей команды |
| `$RANDOM` | Случайное число 0..32767 |
| `$LINENO` | Номер строки в скрипте |
| `$BASH_SOURCE` | Путь к скрипту |
| `$SECONDS` | Секунд с запуска shell |
| `$UID` | Текущий UID |

---

## 🐛 Дебаг

```bash
bash -x script.sh          # трассировка выполнения (+ каждая команда)
bash -v script.sh          # вывод строк перед выполнением
bash -n script.sh          # только проверка синтаксиса

# В скрипте точечно:
set -x                     # включить трассировку
# ...код для дебага...
set +x                     # выключить

# Вывод в stderr с префиксом
echo "DEBUG: var=$var" >&2

PS4='+ ${BASH_SOURCE}:${LINENO}: '   # улучшить вид трассировки
set -x
```

### Проверка синтаксиса онлайн/офлайн
- `shellcheck script.sh` — лучший линтер для shell (ставится через pacman)
- https://www.shellcheck.net

---

## 📝 Практические примеры

### 1. Безопасный backup с проверкой
```bash
#!/usr/bin/env bash
set -euo pipefail

SRC="${1:?Укажите источник}"
DST="${2:?Укажите назначение}"

if [[ ! -d "$SRC" ]]; then
    echo "Ошибка: $SRC не существует" >&2
    exit 1
fi

backup_name="$(basename "$SRC")_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$DST/$backup_name" -C "$(dirname "$SRC")" "$(basename "$SRC")"
echo "Готово: $DST/$backup_name ($(du -h "$DST/$backup_name" | cut -f1))"
```

### 2. Пакетная обработка файлов
```bash
for f in *.jpg; do
    [[ -f "$f" ]] || continue       # защита, если нет файлов
    convert "$f" "thumb_${f%.jpg}_small.jpg"
done
```

### 3. Меню выбора
```bash
PS3="Выберите действие: "
select opt in "Создать" "Удалить" "Выйти"; do
    case $opt in
        "Создать")  echo "Создание..."; break ;;
        "Удалить")  echo "Удаление..."; break ;;
        "Выйти")    exit 0 ;;
        *)          echo "Неверный выбор" ;;
    esac
done
```

### 4. Параллельный запуск с xargs
```bash
echo -e "file1\nfile2\nfile3" | xargs -P 4 -I {} process_file {}
# -P 4  — 4 параллельных процесса
# -I {} — placeholder для аргумента
```

### 5. Подтверждение действия
```bash
read -p "Удалить $FILE? [y/N] " ans
[[ "$ans" =~ ^[Yy]$ ]] || { echo "Отменено"; exit 0; }
rm -rf "$FILE"
```

### 6. Запрос с таймаутом
```bash
if read -t 5 -p "Имя (5с на ответ): " name; then
    echo "Привет, $name"
else
    echo "Время вышло"
fi
```

---

## 🎨 Цветной вывод

```bash
# ANSI-коды
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'        # No Color

echo -e "${RED}Ошибка${NC}: что-то не так"
echo -e "${GREEN}Успех${NC}: всё хорошо"

# Логирование
log()  { echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"; }
err()  { echo -e "${RED}[ERROR]${NC} $*" >&2; }
ok()   { echo -e "${GREEN}[OK]${NC} $*"; }

log "Старт"; ok "Готово"; err "Что-то сломалось"
```

---

## 📚 Конфиг `~/.bashrc` — полезные настройки

```bash
# История
HISTSIZE=10000
HISTFILESIZE=20000
HISTCONTROL=ignoreboth:erasedups   # без дублей и пробелов
shopt -s histappend                # дополнять, а не перезаписывать

# Алиасы
alias ll='ls -lah'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias diff='diff --color=auto'
alias rm='rm -i'                   # подтверждение удаления
alias cp='cp -i'
alias mv='mv -i'

# Функции
mkcd() { mkdir -p "$1" && cd "$1"; }
extract() {
    case "$1" in
        *.tar.gz|*.tgz) tar xzf "$1" ;;
        *.tar.bz2)      tar xjf "$1" ;;
        *.zip)          unzip "$1" ;;
        *.rar)          unrar x "$1" ;;
        *) echo "Не знаю формат $1" ;;
    esac
}

# Промпт (PS1)
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
```

---

## ⌨️ Readline: горячие клавиши bash

| Клавиша | Действие |
|---|---|
| `Ctrl-a` / `Ctrl-e` | В начало / конец строки |
| `Ctrl-b` / `Ctrl-f` | Влево / вправо |
| `Alt-b` / `Alt-f` | На слово назад / вперёд |
| `Ctrl-w` | Удалить слово слева |
| `Ctrl-u` | Удалить до начала |
| `Ctrl-k` | Удалить до конца |
| `Ctrl-y` | Вставить (yank) |
| `Ctrl-_` | Undo |
| `Ctrl-r` | Обратный поиск по истории |
| `Ctrl-s` | Прямой поиск |
| `Ctrl-l` | Очистить экран |
| `Ctrl-c` | Прервать |
| `Ctrl-d` | EOF / выход |
| `Ctrl-z` | Приостановить |
| `Tab` | Автодополнение |
| `Alt-.` | Вставить последний аргумент |
| `!!` | Повторить последнюю команду |
| `!$` | Последний аргумент |
| `!*` | Все аргументы последней |
| `!n` | Команду №n из истории |

---

## 🪤 Частые ошибки и грабли

1. **Пробелы вокруг `=`** — `x = 5` ошибка, надо `x=5`.
2. **Без кавычек** — `[[ $x == "a b" ]]` ломается; используйте `"$x"`.
3. **`[ ]` без пробелов** — `[ 1==2 ]` ошибка, надо `[ 1 == 2 ]` или `(( ))`.
4. **`$(cmd)` vs `` `cmd` ``** — `$()` вкладывается, `` ` ` `` нет.
5. **Подстановка в heredoc** — `<< 'EOF'` не подставляет, `<< EOF` подставляет.
6. **`local var=$(cmd)`** — маскирует код возврата `cmd`. Проверяйте отдельно.
7. **Подshell в пайпе** — `cmd | while read` меняет переменные в subshell'е.
8. **`rm $files`** — если в имени пробел, удалит не то. Кавычки!
9. **`set -e` и функции** — `func || true` нужен, чтобы не падать.
10. **Имена файлов с `-`** — `rm -file` будет воспринято как флаг; `rm -- -file`.
11. **`eval`** — почти всегда зло, опасен инъекциями.
12. **`bash -c` с одинарными кавычками** — переменные не подставляются.

---

## 🔗 Ссылки

- `man bash` (полный, очень подробный)
- ShellCheck: https://www.shellcheck.net
- Shell Style Guide (Google): https://google.github.io/styleguide/shellguide.html
- Pure Bash Bible: https://github.com/dylanaraps/pure-bash-bible
- Bash Hackers Wiki: https://wiki.bash-hackers.org
- Learn Bash: https://learnbash.org / https://linuxcommand.org
- Сайт с примерами: https://shellsnippets.com

---

## 💡 Полезные советы

1. **Всегда** `set -euo pipefail` в начале нетривиальных скриптов.
2. **Всегда** кавычки: `"$var"` почти всегда безопаснее, чем `$var`.
3. **Используйте `[[ ]]`** вместо `[ ]` — мощнее и безопаснее.
4. **ShellCheck** — прогоняйте каждый скрипт, ловит 90% багов.
5. **`local`** в функциях — иначе глобальная переменная!
6. **`printf`** вместо `echo` для сложного/портативного вывода.
7. **`read -r`** — всегда с `-r`, чтобы `\` не интерпретировался.
8. **`trap`** для очистки временных файлов при выходе/ошибке.
9. **`mktemp`** для временных файлов, не придумывайте имена сами.
10. **Если задача сложная** — возможно, лучше Python/Go; bash хорош для
    склеивания команд, не для сложной логики.

---

*Сгенерировано как шпаргалка. Подробности — `man bash`,
он огромный, но очень полезный.*

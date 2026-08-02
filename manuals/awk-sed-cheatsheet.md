# ✂️ awk / sed — шпаргалка по обработке текста

> **sed** (Stream Editor) — потоковый редактор (поиск/замена/удаление).
> **awk** — язык для обработки структурированного текста (полей/колонок).
> Документация: `man sed` · `man awk` · GNU awk: https://www.gnu.org/software/gawk/manual

---

# ✂️ ЧАСТЬ 1. sed

## 🚀 Базовый синтаксис

```bash
sed [опции] 'команды' [файл...]
echo "hello" | sed 's/hello/bye/'     # bye
```

### Опции
| Опция | Назначение |
|---|---|
| `-n` | Тихий режим (не выводить по умолчанию) |
| `-e` | Несколько команд |
| `-f file` | Читать команды из файла |
| `-i` | In-place (изменить файл) |
| `-i.bak` | In-place + резервная копия |
| `-E` / `-r` | Extended regex (как `egrep`) |
| `-u` | Unbuffered (для tail -f) |
| `-s` | Каждый файл отдельно |

### Команды sed
| Команда | Что делает |
|---|---|
| `s/old/new/` | Заменить |
| `s/old/new/g` | Заменить все в строке |
| `s/old/new/2` | Заменить 2-е вхождение |
| `s/old/new/gi` | Все + без учёта регистра |
| `s/old/new/I` | Без учёта регистра |
| `p` | Вывести (с `-n`) |
| `d` | Удалить строку |
| `y/abc/ABC/` | Трансляция символов (как `tr`) |
| `=` | Номер строки |
| `q` | Выйти |
| `a\ text` | Добавить строку после |
| `i\ text` | Вставить строку перед |
| `c\ text` | Заменить строку |
| `r file` | Читать из файла |
| `w file` | Записать в файл |
| `n` | Следующая строка |
| `N` | Добавить следующую к текущей |
| `{...}` | Блок команд |

---

## 🔤 Замена (s)

```bash
# Базовая замена
echo "hello world" | sed 's/world/earth/'      # hello earth
sed 's/foo/bar/' file                          # первое вхождение в строке
sed 's/foo/bar/g' file                         # все вхождения
sed 's/foo/bar/2' file                         # 2-е вхождение
sed 's/foo/bar/gI' file                        # все + case-insensitive

# С группами (extended regex -E)
echo "John Doe" | sed -E 's/(\w+) (\w+)/\2, \1/'   # Doe, John
sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3.\2.\1/'   # 2024-01-15 → 15.01.2024

# Только в строках с паттерном
sed '/error/s/foo/bar/' file                   # заменить foo на bar только в строках с "error"

# По номеру строки
sed '5s/foo/bar/' file                         # только в 5-й строке
sed '5,10s/foo/bar/g' file                     # в строках 5-10
sed '$s/foo/bar/' file                         # в последней строке

# Несколько замен
sed 's/a/A/g; s/b/B/g' file                    # через ;
sed -e 's/a/A/g' -e 's/b/B/g' file             # через -e

# In-place
sed -i 's/foo/bar/g' file                      # изменить файл (БЕЗ бэкапа!)
sed -i.bak 's/foo/bar/g' file                  # + резервная копия file.bak

# С переменными (нужны двойные кавычки)
sed "s/$VAR/replacement/g" file
sed "s/${USER}/admin/g" /etc/passwd
```

### Спецсимволы в замене
| Символ | Значение |
|---|---|
| `&` | Найденное совпадение (весь match) |
| `\1`, `\2`, ... | Группы из шаблона |
| `\n` | Перевод строки (GNU sed) |
| `\t` | Таб (GNU sed, не везде) |

```bash
echo "hello" | sed 's/hello/[&]/'             # [hello]
echo "John" | sed -E 's/(John)/Mr. \1/'        # Mr. John
```

### Разделители (когда есть `/` в тексте)
```bash
sed 's/\/usr\/local\/bin/PATH/' file          # экранирование (некрасиво)
sed 's|/usr/local/bin|PATH|' file              # другой разделитель
sed 's#/path#newpath#' file                    # любой символ-разделитель
sed 's_,/path_,newpath_' file                  # даже запятая
```

---

## ✂️ Удаление (d)

```bash
sed '/pattern/d' file                          # удалить строки с паттерном
sed '/^$/d' file                               # удалить пустые строки
sed '/^[[:space:]]*$/d' file                   # пустые + только пробелы
sed '5d' file                                  # удалить 5-ю строку
sed '5,10d' file                               # строки 5-10
sed '5,$d' file                                # с 5-й до конца
sed '1d;3d;5d' file                            # 1, 3, 5
sed '/start/,/end/d' file                      # от start до end (включительно)
sed '/regex/!d' file                           # удалить всё КРОМЕ строк с regex
```

---

## 📝 Вставка/добавление

```bash
# Добавить строку после совпадения
sed '/pattern/a\New line' file
sed '/pattern/a\\tNew line' file               # с табом

# Вставить строку перед
sed '/pattern/i\Before line' file

# Заменить строку целиком
sed '/pattern/c\Replaced line' file

# Вставить в начало файла
sed '1i\Header line' file

# В конец файла
sed '$a\Footer line' file

# GNU (однострочный синтаксис)
sed '/pattern/a New line' file                 # без \
```

---

## 🔢 Адреса (на каких строках работать)

```bash
sed '5 command' file                           # 5-я строка
sed '5,10 command' file                        # диапазон 5-10
sed '5,$ command' file                         # с 5-й до конца
sed '/start/,/end/ command' file               # от regex до regex
sed '/regex/ command' file                     # строки с regex
sed '1~2 command' file                         # каждая 2-я (1, 3, 5, ...)
sed '0~3 command' file                         # каждая 3-я
sed '$ command' file                           # последняя
```

---

## 🌍 Практические примеры sed

```bash
# Заменить во всех файлах
sed -i 's/old/new/g' *.txt

# Удалить комментарии и пустые строки из конфига
sed -e 's/#.*//' -e '/^[[:space:]]*$/d' nginx.conf

# Извлечь значение (как grep -o)
echo "key=value" | sed -n 's/.*=\(.*\)/\1/p'   # value

# Перевернуть 2 поля
echo "John Doe" | sed -E 's/(\S+) (\S+)/\2 \1/'   # Doe John

# Удалить ANSI-цвета из вывода
sed 's/\x1b\[[0-9;]*m//g'

# Удалить trailing whitespace
sed 's/[[:space:]]*$//' file
sed 's/^[[:space:]]*//' file                   # leading

# Конвертировать разделители CSV
sed 's/,/;/g' data.csv

# Преобразовать Markdown-заголовок в HTML
sed 's/^# \(.*\)/<h1>\1<\/h1>/' file.md

# Показать строки 10-20
sed -n '10,20p' file                           # = sed '10,20!d'

# Вставить строку в указанную позицию
sed '3a\inserted line' file

# Заменить строку целиком (если содержит X)
sed '/pattern/c\new content' file
```

---

# 📊 ЧАСТЬ 2. awk

## 🚀 Базовый синтаксис

```bash
awk [опции] 'program' [file...]
awk 'pattern { action }' file
echo "a b c" | awk '{print $1}'                # a
```

### Структура программы awk
```awk
BEGIN { ... }              # до обработки (инициализация)
/pattern/ { ... }          # для строк с совпадением
/pattern1/,/pattern2/ { }  # диапазон
condition { action }       # по условию
END { ... }                # после обработки (итоги)
```

### Поля и переменные
| Переменная | Что |
|---|---|
| `$0` | Вся строка |
| `$1`, `$2`, ... | Поля (колонки) |
| `$NF` | Последнее поле |
| `$(NF-1)` | Предпоследнее |
| `NF` | Число полей |
| `NR` | Номер строки (всех файлов) |
| `FNR` | Номер строки в текущем файле |
| `FILENAME` | Имя файла |
| `FS` | Разделитель полей (по умолчанию пробел/таб) |
| `OFS` | Output field separator |
| `RS` | Разделитель записей (по умолчанию \n) |
| `ORS` | Output record separator |
| `SUBSEP` | Разделитель в многомерных массивах |

### Опции
| Опция | Назначение |
|---|---|
| `-F:` | Разделитель полей `:` |
| `-v var=val` | Присвоить переменную |
| `-f file.awk` | Программа из файла |
| `-v OFS=","` | Установить output separator |

---

## 🎯 Поля и вывод

```bash
# Печать
echo "a b c" | awk '{print}'                   # вся строка
echo "a b c" | awk '{print $1}'                # a (1-е поле)
echo "a b c" | awk '{print $2, $1}'            # b a
echo "a b c" | awk '{print $1 $2}'             # ab (без пробела!)
echo "a b c" | awk '{print $NF}'               # c (последнее)
echo "a b c" | awk '{print $(NF-1)}'           # b
echo "a b c" | awk '{print NR, $0}'            # с номером строки

# /etc/passwd (разделитель :)
awk -F: '{print $1}' /etc/passwd               # имена пользователей
awk -F: '{print $1, $7}' /etc/passwd           # имя + shell
awk -F: '{print $1":"$7}' /etc/passwd          # без пробела

# Несколько разделителей
awk -F'[: ]' '{print $1}' file                 # двоеточие ИЛИ пробел
awk -F'[,\t]' '{print $1}' file                # запятая ИЛИ таб
```

### Изменение полей
```bash
echo "a b c" | awk '{$2="X"; print}'           # a X c
echo "a b c" | awk '{$4="d"; print}'           # a b c d
echo "a b c" | awk 'OFS="," {print $1,$2,$3}'  # a,b,c (с разделителем)
```

---

## 🔢 Арифметика и переменные

```bash
# Подсчёт
echo "5" | awk '{print $1 * 2}'                # 10
echo "5 3" | awk '{print $1 + $2}'             # 8
echo "5 3" | awk '{print $1 / $2}'             # 1.66667
echo "10" | awk '{print $1 % 3}'               # 1
echo "5" | awk '{print $1 ^ 2}'                # 25 (или **)

# Сумма колонки
awk '{sum += $1} END {print sum}' nums.txt
# Среднее
awk '{sum += $1} END {print sum/NR}' nums.txt
# Максимум
awk 'NR==1 || $1>max {max=$1} END {print max}' nums.txt

# Переменные
awk -v name="Alice" '{print name, $1}' file
awk -v OFS="|" '{print $1, $2}' file
```

### Встроенные функции
```awk
length           # длина строки
length($0)
length(arr)      # число элементов
substr(s, m, n)  # подстрока (1-indexed)
index(s, sub)    # позиция подстроки
split(s, arr, sep)  # разделить
tolower(s), toupper(s)
sprintf(fmt, ...)    # как printf
sin(x), cos(x), exp(x), log(x), sqrt(x)
int(x)               # целая часть
srand(), rand()      # случайные
```

---

## 🔀 Условия и паттерны

```bash
# По условию
awk '$1 > 100 {print}' file                    # 1-я колонка > 100
awk '$3 == "NYC" {print $1}' file              # 3-я колонка = NYC
awk 'NR > 1 {print}' file                      # пропустить заголовок
awk 'NR == 1' file                             # только 1-ю строку
awk 'NR % 2 == 0' file                         # чётные строки
awk 'NF == 0' file                             # пустые строки
awk 'NF > 5' file                              # больше 5 полей

# По regex
awk '/error/ {print}' log                      # строки с "error"
awk '/^[0-9]/ {print}' file                    # начинающиеся с цифры
awk '!/debug/ {print}' log                     # НЕ содержащие debug

# Комбинирование
awk '$1 > 100 && $2 < 50' file
awk '$1 > 100 || $3 == "VIP"' file
awk '/error/ && /database/' log
```

### Диапазоны
```bash
awk '/start/,/end/' file                       # от start до end
awk 'NR>=10 && NR<=20' file                    # строки 10-20
```

---

## 🔄 Циклы

```awk
# for
awk '{for(i=1; i<=NF; i++) print $i}' file     # каждое поле отдельно
awk 'BEGIN {for(i=1; i<=10; i++) print i}'

# for-in (по массиву)
awk '{count[$1]++} END {for(k in count) print k, count[k]}' file

# while
awk '{i=1; while(i<=NF) {print $i; i++}}' file

# do-while
awk 'BEGIN {i=1; do {print i; i++} while(i<5)}'

# break / continue
awk '{for(i=1;i<=NF;i++) {if($i=="X") break; print $i}}' file
```

---

## 📦 Массивы и группировка

awk поддерживает ассоциативные массивы — основа для агрегаций.

```bash
# Подсчёт по ключу (как group by)
awk '{count[$1]++} END {for(k in count) print k, count[k]}' file
# uniq -c, но для любой колонки

# Сумма по группе
awk '{sum[$1] += $2} END {for(k in sum) print k, sum[k]}' file

# Группировка с условием
awk '{total[$1] += $2; cnt[$1]++} END {
    for(k in total) printf "%s\t%.2f\n", k, total[k]/cnt[k]
}' file
# среднее по группе
```

### Многомерные массивы
```awk
awk '{matrix[$1, $2] = $3} END {
    for(k in matrix) {
        split(k, idx, SUBSEP)
        print idx[1], idx[2], matrix[k]
    }
}' file
```

---

## 🌍 Практические примеры awk

```bash
# Топ-5 процессов по памяти
ps aux | sort -k6 -rn | awk 'NR<=5 {print $1, $2, $6/1024 " MB", $11}'

# Сумма размеров файлов
ls -l | awk '{sum += $5} END {print sum/1024 " KB"}'

# Найти самый большой файл
ls -lS | awk 'NR==2 {print $5, $9}'   # второй после total

# Подсчёт HTTP-статусов в логе
awk '{count[$9]++} END {for(k in count) print k, count[k]}' access.log | sort

# uniq -c по колонке
awk '{print $1}' file | sort | uniq -c | sort -rn

# CSV: сумма по колонке
awk -F, '{sum += $3} END {print sum}' data.csv

# Конвертировать CSV в TSV
awk -F, 'BEGIN{OFS="\t"} {$1=$1; print}' data.csv

# Пропустить 1-ю строку (заголовок)
awk 'NR>1' file.csv

# Уникальные строки с сохранением порядка
awk '!seen[$0]++' file

# Присоединить файлы (как join)
awk 'NR==FNR {a[$1]=$2; next} {print $0, a[$1]}' map.txt data.txt

# Вычислить проценты
awk '{sum += $1} END {print sum "%"}' values.txt

# Хвост файла как tail
awk 'END {print}' file

# Подсчёт строк/слов/символов (как wc)
awk 'END {print NR}' file                       # строки
awk '{total += NF} END {print total}' file      # слова

# Найти пустые строки
awk 'NF==0' file
awk 'length == 0' file

# Топ длинных строк
awk '{print length, $0}' file | sort -rn | head
```

---

## 🆚 awk vs sed vs cut vs grep

| Задача | Лучший инструмент |
|---|---|
| Поиск строк | `grep` |
| Замена текста | `sed` |
| Извлечение колонки | `awk` или `cut` |
| Сложные вычисления | `awk` |
| Простое разделение по символу | `cut` |
| Группировка/агрегация | `awk` |
| Удаление строк по условию | `sed` или `awk` |
| Модификация строки | `sed` |

```bash
# То же самое разными инструментами:
echo "a:b:c" | cut -d: -f2          # b
echo "a:b:c" | awk -F: '{print $2}' # b
echo "a:b:c" | sed 's/[^:]*:\([^:]*\).*/\1/'   # b (намного сложнее)
```

---

## 🪤 Частые ошибки

### sed
1. **Не использовать `-i.bak`** — изменяет без возможности отката.
2. **`/` в pattern без экранирования** — `s/path//` ломается, юзайте `s|path||`.
3. **Забыть `g`** — заменяет только первое вхождение.
4. **`-i` на macOS** — требует `-i ''` (пустой аргумент).
5. **Спецсимволы в replacement** — `&`, `\1` нужно экранировать.

### awk
1. **`print $1 $2`** — склеивает без пробела! Нужно `print $1, $2`.
2. **Разделитель по умолчанию** — пробел И таб, не только пробел.
3. **`$0` vs `$1`** — `$0` вся строка, `$1` первое поле.
4. **Числа vs строки** — awk сам конвертирует, но `"10"+0` надёжнее.
5. **Порядок BEGIN/main/END** — BEGIN до чтения, END после.
6. **`next`** — пропустить остальные правила для этой строки.
7. **`printf` без `\n`** — не добавляет перевод строки автоматически.

---

## 🔗 Полезные ссылки

### sed
- GNU sed manual: https://www.gnu.org/software/sed/manual/sed.html
- Awesome sed: https://github.com/mbucc/sed-scripts
- sed tutorial: https://www.grymoire.com/Unix/Sed.html
- sed one-liners: http://sed.sourceforge.net/sed1line.txt

### awk
- GNU awk manual: https://www.gnu.org/software/gawk/manual
- Awesome awk: https://github.com/mlohse/awk-tips
- awk tutorial: https://www.grymoire.com/Unix/Awk.html
- awk one-liners: http://www.catonmat.net/blog/awk-one-liners-explained-part-one/

---

## 💡 Полезные советы

### sed
1. **`-i.bak`** — всегда делайте резервную копию при in-place.
2. **`-E`** — extended regex (как в grep -E), намного удобнее.
3. **`&`** — найденный текст в замене.
4. **Меняйте разделитель** — `s|/path|new|` вместо `s/\/path/.../`.
5. **`/pattern/d`** — удалить строки с паттерном.
6. **`-n '...p'`** — вывести только совпадения (как grep).

### awk
1. **`-F:`** — задать разделитель (как `cut -d:`).
2. **`$NF`** — последнее поле.
3. **`NR>1`** — пропустить заголовок.
4. **`{sum+=$1} END {print sum}`** — сумма колонки.
5. **`count[$1]++`** — группировка/подсчёт (мощь awk!).
6. **`!seen[$0]++`** — уникальные строки с сохранением порядка.
7. **`length`** — длина строки; `awk 'length > 80'` — длинные строки.
8. **`printf`** — форматированный вывод (как в C).
9. **Многоколоночные данные** — awk мощнее cut.
10. **`awk -v OFS=,`** — выходной разделитель для CSV.

---

*Сгенерировано как шпаргалка. sed/awk — классика Unix —
углубляйтесь через grymoire.com и `man sed`/`man awk`*

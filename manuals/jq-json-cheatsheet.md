# 🔧 jq + JSON — шпаргалка

> **jq** — командный процессор JSON (как `sed`/`awk`/`grep` для JSON).
> **JSON** — JavaScript Object Notation, формат обмена данными.
> Документация: https://jqlang.github.io/jq/manual

---

## 🔑 Главные понятия JSON

| Тип | Пример | Описание |
|---|---|---|
| **Object** | `{"key": "val"}` | Объект/словарь |
| **Array** | `[1, 2, 3]` | Массив/список |
| **String** | `"hello"` | Строка (всегда в двойных кавычках!) |
| **Number** | `42`, `3.14` | Число (int или float) |
| **Boolean** | `true` / `false` | Логическое (с маленькой буквы!) |
| **Null** | `null` | Пустое значение |
| Whitespace | пробелы/таб/перевод | Не значимы (кроме внутри строк) |

### Синтаксис
```json
{
  "name": "Alice",
  "age": 30,
  "active": true,
  "email": null,
  "tags": ["admin", "user"],
  "address": {
    "city": "NYC",
    "zip": "10001"
  }
}
```

### Правила
- Ключи объектов — **всегда в двойных кавычках**.
- Строки — двойные кавычки (одинарные запрещены!).
- Нет trailing comma (запятой после последнего элемента).
- Комментарии **запрещены** (в строгом JSON).
- Числа: `1.5e10` допускается.

---

## 🚀 jq — установка и базовое использование

```bash
# Установка
sudo pacman -S jq                  # Arch / CachyOS
sudo apt install jq                # Debian/Ubuntu
brew install jq                    # macOS

# Простейший запуск
echo '{"name":"Alice"}' | jq
# {
#   "name": "Alice"
# }

# Файл
jq . file.json                    # pretty-print всего файла
jq '.' file.json                  # то же
cat file.json | jq                # через пайп
```

### Полезные флаги
| Флаг | Назначение |
|---|---|
| `.` | Вывести всё (identity) |
| `-c` | Компактный вывод (одна строка) |
| `-r` | Raw output (без кавычек у строк) |
| `-R` | Читать input как raw строки |
| `-s` | Slurp: весь input как один массив |
| `-e` | Exit code 1 если последний output null/false |
| `-n` | Не читать input (использовать с `null` или данными) |
| `-a` | ASCII output (не UTF-8) |
| `-f file.jq` | Читать фильтр из файла |
| `--arg name val` | Передать строковую переменную |
| `--argjson name 'json'` | Передать JSON-переменную |
| `--slurpfile name f` | Прочитать файл в переменную |
| `-S` | Отсортировать ключи объектов |

---

## 🎯 Базовые фильтры

### Идентичность и доступ
```bash
echo '{"name":"Alice","age":30}' | jq '.'
# { "name": "Alice", "age": 30 }

echo '{"name":"Alice"}' | jq '.name'
# "Alice"

echo '{"name":"Alice"}' | jq '.["name"]'    # альтернатива
# "Alice"

# Глубокий путь (dot notation)
echo '{"user":{"name":"Alice"}}' | jq '.user.name'
# "Alice"

# Bracket для ключей со спецсимволами
echo '{"my-key":"val"}' | jq '.["my-key"]'
# "val"

# Несуществующий ключ → null
echo '{"name":"Alice"}' | jq '.email'
# null

# Optional chaining (?— не падать если null)
jq '.user.name?'                      # не упадёт если user === null
```

### Массивы
```bash
echo '[1,2,3]' | jq '.[0]'            # 1 (первый)
echo '[1,2,3]' | jq '.[-1]'           # 3 (последний)
echo '[1,2,3]' | jq '.[1:3]'          # [2,3] (срез 1..2)
echo '[1,2,3]' | jq '.[:2]'           # [1,2]
echo '[1,2,3]' | jq '.[1:]'           # [2,3]
echo '[1,2,3]' | jq '.[-2:]'          # [2,3]
echo '[1,2,3]' | jq 'length'          # 3
echo '[1,2,3]' | jq 'first'           # 1
echo '[1,2,3]' | jq 'last'            # 3
```

### Итерация по массиву
```bash
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '.[].name'
# "Alice"
# "Bob"

# Map (применить к каждому элементу)
echo '[1,2,3]' | jq 'map(. * 2)'      # [2,4,6]
echo '[{"age":30},{"age":25}]' | jq 'map(.age)'   # [30,25]

# Select (фильтр)
echo '[1,2,3,4]' | jq 'map(select(. > 2))'   # [3,4]
echo '[1,2,3,4]' | jq '.[] | select(. > 2)'  # 3 \n 4

# Итерация по объекту
echo '{"a":1,"b":2}' | jq 'to_entries'
# [{"key":"a","value":1},{"key":"b","value":2}]
echo '[{"key":"a","value":1}]' | jq 'from_entries'   # {"a":1}
echo '{"a":1,"b":2}' | jq 'keys'        # ["a","b"]
echo '{"a":1,"b":2}' | jq 'values'      # [1,2]
```

---

## 🔧 Встроенные функции

### Строковые
```bash
echo '"hello"' | jq 'length'           # 5
echo '"hello"' | jq 'ascii'            # [104,101,...]
echo '"Hello"' | jq 'ascii_downcase'   # "hello"
echo '"hello"' | jq 'ascii_upcase'     # "HELLO"
echo '"  hi  "' | jq 'ltrimstr(" ")'   # обрезать префикс
echo '"hello"' | jq 'split("l")'       # ["he","","o"]
echo '["a","b"]' | jq 'join(",")'      # "a,b"
echo '"hello world"' | jq 'ascii_downcase | split(" ") | .[0]'
echo '"abc"' | jq '@base64'            # "YWJj"
echo '"YWJj"' | jq '@base64d'          # "abc"
echo '"a&b"' | jq '@uri'               # "a%26b"
echo '"2024-01-15"' | jq 'explode'     # [50,48,...]
```

### Математические
```bash
echo '5' | jq '. + 3'                  # 8
echo '5' | jq '. * 2'                  # 10
echo '10' | jq '. / 3'                 # 3.333...
echo '10' | jq 'floor'                 # 10
echo '10' | jq 'ceil'
echo '5' | jq 'sqrt'                   # 2.236...
echo '5' | jq 'pow(2; 2)'              # 25  (5^2 — осторожно, синтаксис)
echo '[1,2,3]' | jq 'add'              # 6
echo '[1,2,3]' | jq 'min'              # 1
echo '[1,2,3]' | jq 'max'              # 3
echo '[1,2,3]' | jq 'length'           # 3
echo '5' | jq 'tonumber'               # 5
echo '"42"' | jq 'tonumber'            # 42
echo '42' | jq 'tostring'              # "42"
```

### Типы
```bash
echo '"hi"' | jq 'type'                # "string"
echo '42' | jq 'type'                  # "number"
echo '[1,2]' | jq 'type'               # "array"
echo '{"a":1}' | jq 'type'             # "object"
echo 'null' | jq 'type'                # "null"
echo 'true' | jq 'type'                # "boolean"

echo '"42"' | jq 'tonumber'
echo '42' | jq 'tojson'                # сериализовать обратно в строку-JSON
echo '"{\"a\":1}"' | jq 'fromjson'     # распарсить строку-JSON в объект
```

### Условия
```bash
echo '5' | jq 'if . > 3 then "big" else "small" end'
echo '5' | jq '. > 3'                  # true
echo '5' | jq '. > 3 and . < 10'       # true
echo '5' | jq '. > 3 or . > 100'       # true
echo '5' | jq 'not'                    # false
echo 'null' | jq 'has("key")'          # false
echo '{"a":1}' | jq 'has("a")'         # true
echo '{"a":1}' | jq 'in({"a":1})'      # true
echo '"str"' | jq '. == "str"'         # true
```

### Альтернативы (`//`)
```bash
# Оператор // — значение по умолчанию
echo '{"name":"Alice"}' | jq '.email // "no email"'
# "no email"

echo 'null' | jq '. // "default"'
# "default"

# Цепочка альтернатив
jq '.user.email // .user.phone // "no contact"'
```

---

## 📦 Создание объектов (construction)

```bash
# Копировать и добавить поле
echo '{"name":"Alice"}' | jq '. + {"age":30}'
# {"name":"Alice","age":30}

# Удалить поле
echo '{"a":1,"b":2}' | jq 'del(.b)'
# {"a":1}

# Создать новый объект
echo '{"name":"Alice","age":30}' | jq '{name, age}'
# {"name":"Alice","age":30}

# С переименованием
echo '{"name":"Alice"}' | jq '{username: .name}'
# {"username":"Alice"}

# С вычислением
echo '{"a":1,"b":2}' | jq '{sum: (.a + .b)}'
# {"sum":3}

# Сокращённый синтаксис {a, b} = {a: .a, b: .b}
echo '{"a":1,"b":2}' | jq '{a, b}'
```

---

## 🔁 Pipe и продвинутые фильтры

### Pipe `|`
```bash
echo '{"users":[{"name":"Alice"}]}' | jq '.users | .[0] | .name'
# = .users[0].name
# "Alice"

# С map
echo '[{"name":"Alice","age":30},{"name":"Bob","age":25}]' | \
    jq '. | map(.name)'
# ["Alice","Bob"]
```

### select (фильтрация)
```bash
echo '[1,2,3,4,5]' | jq '.[] | select(. > 3)'
# 4
# 5

echo '[{"name":"Alice","age":30},{"name":"Bob","age":25}]' | \
    jq '.[] | select(.age > 28)'
# {"name":"Alice","age":30}

# Несколько условий
jq '.[] | select(.age > 25 and .city == "NYC")'

# Сравнение строк
jq '.[] | select(.status == "active")'
```

### map / select / recurse
```bash
echo '[1,2,3]' | jq 'map(. * 2)'               # [2,4,6]
echo '[1,2,3]' | jq 'map(select(. > 1))'       # [2,3]

# recurse — рекурсивный обход (для вложенных структур)
echo '{"a":{"b":{"c":1}}}' | jq 'recurse'
echo '{"a":{"b":{"c":1}}}' | jq 'recurse | objects'
echo '{"a":{"b":1}}' | jq '.. | .b? // empty'  # найти все .b где есть

# .. (рекурсивный спуск)
echo '{"a":{"b":1},"c":2}' | jq '..'
echo '{"a":{"b":1}}' | jq '.. | numbers'       # все числа (1)
echo '{"a":{"b":1}}' | jq '.. | scalars'       # все скаляры
```

### group_by / sort / unique
```bash
echo '[{"c":"NYC","n":1},{"c":"NYC","n":2},{"c":"LA","n":3}]' | \
    jq 'group_by(.c)'
# [
#   [{"c":"LA","n":3}],
#   [{"c":"NYC","n":1},{"c":"NYC","n":2}]
# ]

echo '[3,1,2]' | jq 'sort'                     # [1,2,3]
echo '[3,1,2]' | jq 'sort | reverse'           # [3,2,1]
echo '[{"a":3},{"a":1}]' | jq 'sort_by(.a)'
echo '[1,2,2,3,3,3]' | jq 'unique'             # [1,2,3]
echo '[{"id":1},{"id":1}]' | jq 'unique_by(.id)'
```

### any / all
```bash
echo '[true,false,true]' | jq 'any'            # true
echo '[true,false,true]' | jq 'all'            # false
echo '[1,2,3]' | jq 'any(. > 2)'               # true
echo '[1,2,3]' | jq 'all(. > 0)'               # true
echo '[{"age":30},{"age":25}]' | jq 'any(.age > 28)'   # true
```

### limit / first / last / nth
```bash
echo '[1,2,3,4,5]' | jq 'limit(2; .[])'        # 1 \n 2
echo '[1,2,3]' | jq 'first'                    # 1
echo '[1,2,3]' | jq 'last'                     # 3
echo '[1,2,3]' | jq 'nth(1)'                   # 2 (индекс 1)
```

---

## 🌍 Переменные и функции

### Переменные (через --arg/--argjson)
```bash
jq --arg name "Alice" '.name = $name' <<< '{}'
# {"name":"Alice"}

jq --argjson age 30 '.age = $age' <<< '{}'
# {"age":30}

# Из shell-переменной
USER_NAME="Bob"
jq --arg u "$USER_NAME" '.user = $u' <<< '{}'

# Сравнение
jq --arg q "alice" '.[] | select(.name == $q)' users.json
```

### Внутренние переменные (with foreach/reduce)
```bash
# reduce
echo '[1,2,3,4]' | jq 'reduce .[] as $x (0; . + $x)'
# 10  (сумма)

echo '[1,2,3,4]' | jq 'reduce .[] as $x (0; . + $x) / length'
# среднее

# foreach (с сохранением состояния)
echo '[1,2,3]' | jq 'foreach .[] as $x (0; . + $x; {item: $x, sum: .})'
```

### Пользовательские функции
```bash
# Определить функцию
jq 'def double: . * 2; double' <<< 5
# 10

# С аргументами
jq 'def addn(n): . + n; addn(10)' <<< 5
# 15

# В файле
# ~/.jq или -f filters.jq
echo 'def greet: "Hello " + .;' > /tmp/filters.jq
jq -f /tmp/filters.jq <<< '"Alice"'
# "Hello Alice"
```

---

## 📊 Практические примеры

### 1. Извлечь поле из массива объектов
```bash
# users.json: [{"name":"Alice","age":30},...]
jq '.[].name' users.json                 # имена (каждый с новой строки)
jq '[.[].name]' users.json               # массив имён
jq -r '.[].name' users.json              # без кавычек
jq 'map(.name)' users.json               # массив имён
```

### 2. Фильтрация + извлечение
```bash
# Все активные пользователи, только имя и email
jq '.[] | select(.active == true) | {name, email}' users.json

# С группировкой
jq -r '.[] | "\(.name)\t\(.age)"' users.json   # TSV

# Сортировка по возрасту, топ-5
jq '[.[] | {name, age}] | sort_by(-.age) | .[0:5]' users.json
```

### 3. Группировка и агрегация
```bash
# Сумма по городу
jq 'group_by(.city) | map({city: .[0].city, total: map(.amount) | add})' sales.json

# Среднее по категории
jq 'group_by(.category) | map({cat: .[0].category, avg: (map(.price) | add / length)})' products.json
```

### 4. Обработка API-ответа
```bash
# GitHub API: получить звёзды топовых репозиториев
curl -s https://api.github.com/search/repositories?q=stars:>100000 | \
    jq '.items[] | {name, stars: .stargazers_count}' | head

# Только имена
curl -s https://api.github.com/users/torvalds/repos | \
    jq -r '.[].full_name'

# Топ-5 по звёздам
curl -s https://api.github.com/users/torvalds/repos | \
    jq -r 'sort_by(-.stargazers_count) | .[0:5] | .[].full_name'
```

### 5. docker inspect
```bash
# IP-адрес контейнера
docker inspect <container> | jq '.[0].NetworkSettings.IPAddress'

# Все порты
docker inspect <container> | jq '.[0].NetworkSettings.Ports'

# Список всех контейнеров: имя + статус
docker ps -a --format '{{json .}}' | jq -r '.Names + " | " + .Status'
```

### 6. kubectl
```bash
# Все pod'ы: имя + статус
kubectl get pods -o json | jq -r '.items[] | .metadata.name + " " + .status.phase'

# Внешние IP всех сервисов
kubectl get svc -o json | jq -r '.items[] | .metadata.name + ": " + (.status.loadBalancer.ingress[0].ip // "pending")'
```

### 7. Логи в JSON (частый случай в микросервисах)
```bash
# log line: {"level":"error","msg":"...","time":"..."}
cat app.log | jq 'select(.level == "error") | .msg'
cat app.log | jq -c 'select(.level == "error")'
cat app.log | jq 'select(.status >= 500) | {time, msg, status}'
```

### 8. Конвертация CSV → JSON
```bash
# С rq (rust q) или mlr
mlr --c2j cat data.csv > data.json

# Python
python -c "import csv,json; print(json.dumps(list(csv.DictReader(open('data.csv')))))"
```

### 9. Объединение JSON-файлов
```bash
# slurp: считать все объекты в массив
jq -s '.' *.json > merged.json

# Объединить массивы
jq -s 'add' file1.json file2.json
jq -s 'map(.users) | add' *.json

# Map-reduce-style
jq -s 'map(.count) | add' *.json   # сумма всех count
```

### 10. Найти все совпадения во вложенной структуре
```bash
# Все значения поля "id" на любой глубине
jq '[.. | objects | .id? // empty]' data.json

# Все email'ы
jq '[.. | objects | .email? // empty] | unique' users.json
```

---

## 🐍 Python + JSON

```python
import json

# Чтение
data = json.loads(json_string)
with open("file.json", encoding="utf-8") as f:
    data = json.load(f)

# Запись
json_str = json.dumps(data, indent=2, ensure_ascii=False)
with open("out.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Из CLI
data = json.loads(subprocess.run(["jc", "ls"], capture_output=True).stdout)
```

### Modern Python: pydantic / msgspec
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User.model_validate_json('{"name":"Alice","age":30}')
user.name   # 'Alice'

# Быстрее: msgspec
import msgspec
user = msgspec.json.decode('{"name":"Alice","age":30}', type=User)
```

---

## 🌐 JavaScript + JSON

```javascript
// Парсинг
const data = JSON.parse('{"name":"Alice"}');
data.name;                            // "Alice"

// Сериализация
JSON.stringify({name: "Alice"});      // '{"name":"Alice"}'
JSON.stringify({name: "Alice"}, null, 2);  // pretty-print

// JSON с regex-подобной фильтрацией
const active = data.filter(u => u.active);
```

---

## 🛠️ Альтернативы jq

| Инструмент | Особенность |
|---|---|
| **jq** | Классика, де-факто стандарт |
| **yq** | Как jq, но для YAML/XML/TOML |
| **dasel** | Универсальный: JSON/YAML/TOML/XML |
| **jaq** | Быстрее jq (на Rust) |
| **gq** | Go-версия |
| **rq** | Rust, поддерживает выражения |
| **jc** | Конвертер вывода команд в JSON |
| **jid** | Интерактивный jq (с автодополнением) |
| **fx** | Интерактивный TUI-просмотрщик JSON |

### jc — вывод команд в JSON
```bash
jc ls -la                            # список файлов как JSON
jc ifconfig                          # сетевые интерфейсы JSON
jc ps aux                            # процессы JSON
jc df -h                             # диски JSON
```

### fx — TUI для JSON
```bash
fx data.json                         # интерактивный просмотр
echo '{"a":1}' | fx                  # через пайп
echo '{"a":1}' | fx '.a'             # фильтр
```

---

## 🪤 Частые ошибки

1. **Одинарные кавычки** — `jq '.name'` (внешние), внутри JSON — двойные.
2. **Pipe порядок** — `.users[].name` ≠ `.name` после `.users[]` (хотя результат тот же).
3. **`map(select(...))`** — для фильтрации массива; `select` без `map` выводит каждый отдельно.
4. **`// "default"`** — оператор альтернативы, не деление.
5. **Доступ к полю с дефисом** — `.["my-key"]`, не `.my-key` (вычитание!).
6. **Типизация** — `length` для строки/массива/объекта считает разное.
7. **`--arg` vs `--argjson`** — первое строка, второе — JSON-значение.
8. **`-r` для сырого вывода** — иначе строки в кавычках.
9. **Файл vs пайп** — `jq . file.json` или `cat file | jq .`, оба работают.
10. **JSON trailing comma** — запрещена, упадёт парсинг.

---

## 🔗 Полезные ссылки

- jq manual: https://jqlang.github.io/jq/manual
- jq playground: https://jqplay.org
- jq tutorial: https://jqplay.org/s/byjY3oZEmbj
- awesome-jq: https://github.com/fiatjaf/awesome-jq
- dasel: https://github.com/TomWright/dasel
- fx: https://github.com/antonmedv/fx
- jc: https://github.com/kellyjonbrazil/jc
- JSON specification: https://www.json.org
- JSON Formatter (Chrome): https://chrome.google.com/webstore/detail/json-formatter

---

## 💡 Полезные советы

1. **`jq '.'`** — самое простое: pretty-print (форматирование).
2. **`-r`** — для вывода строк без кавычек (использовать в скриптах).
3. **`.[].field`** — достать поле из каждого элемента массива.
4. **`map(select(...))`** — фильтрация массива.
5. **`-s` (slurp)** — объединить несколько JSON-документов в массив.
6. **`--arg`/`--argjson`** — для передачи переменных из shell.
7. **`//` (альтернатива)** — значения по умолчанию.
8. **`to_entries` / `from_entries`** — для работы с объектами как с массивами.
9. **`..`** — рекурсивный поиск по всем уровням.
10. **`@base64`, `@uri`** — кодирование внутри jq.
11. **`jq -r '.[] | "@\(.name)"'`** — генерация строк.
12. **fx** — интерактивный просмотр JSON (намного удобнее для исследования).
13. **jc** — превращает вывод команд в JSON.
14. **`jq -e`** — exit code 1 если null/false (для скриптов).
15. **yq** — для YAML, тот же синтаксис.

---

*Сгенерировано как шпаргалка. jq мощный и неочевидный —
углубляйтесь через https://jqplay.org и https://jqlang.github.io/jq/manual*

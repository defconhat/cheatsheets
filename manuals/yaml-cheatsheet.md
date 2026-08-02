# 📄 YAML — шпаргалка по синтаксису

> **YAML** (YAML Ain't Markup Language) — человекочитаемый формат сериализации данных.
> Используется в K8s, Docker Compose, Ansible, GitHub Actions, CI/CD.
> Документация: https://yaml.org · https://yaml.org/spec/1.2.2

---

## 🔑 Главные правила

1. **Отступы — пробелами** (не табами!). Обычно по 2 пробела.
2. **Регистрозависимость** (`Name` ≠ `name`).
3. **`:` после ключа** + пробел: `key: value`.
4. **`#` — комментарий** (до конца строки).
5. **`---` — разделитель документов** (несколько YAML в одном файле).
6. **`...` — конец документа** (опционально).

---

## 🚀 Базовые типы

### Скаляры
```yaml
string: hello
string_quoted: "hello"
string_single: 'hello'
integer: 42
float: 3.14
boolean: true       # или yes / on (не рекомендуется)
boolean2: false     # или no / off
null_value: null    # или ~
null_implicit:      # пустое = null
date: 2024-01-15
datetime: 2024-01-15T10:30:00Z
```

### Строки
```yaml
# Простая
plain: hello world

# С кавычками (для спецсимволов)
quoted: "hello: world"
single: 'it''s a test'

# Multiline (несколько строк)
folded: >            # > = folded (переносы → пробелы)
    This is
    a long paragraph
    on one line.

literal: |           # | = literal (сохраняет переносы)
    Line 1
    Line 2
    Line 3

# С сохранением trailing newline
literal_keep: |+
    text
    text

# Без trailing newline
literal_strip: |-
    text
    text
```

> Multiline-операторы:
> - `|` — literal (как есть, с `\n`)
> - `>` — folded (переносы → пробелы)
> - `+` — keep trailing newline
> - `-` — strip trailing newline

---

## 📋 Коллекции

### Последовательности (списки/массивы)
```yaml
# Block style
fruits:
  - apple
  - banana
  - cherry

# Inline (flow style)
fruits: [apple, banana, cherry]

# Список словарей
users:
  - name: Alice
    age: 30
  - name: Bob
    age: 25

# Список списков
matrix:
  - [1, 2, 3]
  - [4, 5, 6]
```

### Отображения (словари/объекты)
```yaml
# Block style
person:
  name: Alice
  age: 30
  address:
    city: NYC
    zip: "10001"

# Flow style
person: {name: Alice, age: 30}

# Вложенные
config:
  database:
    host: localhost
    port: 5432
```

### Комбинирование
```yaml
servers:
  - name: web1
    ip: 10.0.0.1
    roles:
      - web
      - cache
  - name: db1
    ip: 10.0.0.2
    roles:
      - primary
```

---

## 🔄 Якоря и алиасы (DRY)

Повторное использование значений (как переменные).

```yaml
# Определение якоря (&name)
defaults: &defaults
  adapter: postgres
  host: localhost
  port: 5432

# Использование (*name) — ссылка
development:
  <<: *defaults      # merge keys
  database: dev_db

production:
  <<: *defaults
  host: prod.example.com
  database: prod_db

# Переопределение после merge
test:
  <<: *defaults
  database: test_db   # переопределит
```

### Альтернативный синтаксис (YAML 1.2)
```yaml
x-common: &common
  restart: unless-stopped
  networks: [appnet]

services:
  web:
    <<: *common
    image: nginx
  db:
    <<: *common
    image: postgres
```

---

## 🛠️ Спецсимволы

| Символ | Назначение |
|---|---|
| `#` | Комментарий |
| `---` | Начало документа |
| `...` | Конец документа |
| `-` | Элемент списка |
| `:` | Разделитель key: value |
| `&` | Определить якорь |
| `*` | Ссылка на якорь |
| `<<` | Merge keys |
| `?` | Complex key |
| `!` | Тег типа |
| `|` / `>` | Multiline literal/folded |
| `{}` | Flow mapping |
| `[]` | Flow sequence |
| `,` | Разделитель в flow |
| `~` | null |

---

## 🏷️ Типы и теги

YAML автоматически определяет тип, но можно явно:

```yaml
# Явные теги
string: !!str 42
integer: !!int "42"
float: !!float 3
bool: !!bool yes
null: !!null ~
binary: !!binary "SGVsbG8="
timestamp: !!timestamp 2024-01-15T10:30:00Z

# Пользовательские теги (в K8s, Ansible)
custom: !my_tag value
```

### Специальные значения
```yaml
# yes/no/on/off → boolean (ОПАСНО!)
version: 1.0      # float
version: "1.0"    # string
enabled: yes      # true (boolean)
enabled: "yes"    # "yes" (string)

# Sexagesimal (углы/время)
time: 12:30:00    # интерпретируется как 4500
ip: 192.168.1.1   # обычно строка, но следите
```

> ⚠️ Всегда кавычьте строки, которые выглядят как числа/даты/булевы!

---

## 🌍 Мультидокументы

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: app1
---
apiVersion: v1
kind: Service
metadata:
  name: app1-svc
```

Используется в K8s для нескольких ресурсов в одном файле.

---

## 🐍 Python + YAML

### PyYAML (классика)
```python
import yaml

# Чтение
with open("config.yaml", encoding="utf-8") as f:
    data = yaml.safe_load(f)        # безопасно (без произвольных объектов!)

# Не использовать yaml.load() без Loader — уязвимость!
# data = yaml.load(f, Loader=yaml.FullLoader)  # если нужны теги

# Запись
with open("out.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

# Несколько документов
for doc in yaml.safe_load_all(f):
    print(doc)

yaml.dump_all([doc1, doc2], f)
```

### ruamel.yaml (сохраняет форматирование/комментарии)
```python
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

with open("config.yaml", encoding="utf-8") as f:
    data = yaml.load(f)

data["key"] = "new value"

with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f)              # сохранит комментарии и порядок!
```

---

## 🐚 CLI-инструменты

### yq (как jq для YAML)
```bash
# Установка
sudo pacman -S yq                  # Arch (могут быть разные yq)
# mikefarah/yq (Go, рекомендуется): https://github.com/mikefarah/yq

# Чтение значения
yq '.database.host' config.yaml
yq '.services.web.image' docker-compose.yaml

# Изменение (in-place)
yq '.database.host = "newhost"' config.yaml -i

# Конвертация в JSON
yq -o=json config.yaml

# Конвертация JSON → YAML
echo '{"a":1}' | yq -P

# Несколько документов
yq 'select(.kind == "Pod")' k8s.yaml
```

### Альтернативы
- **dasel** — универсальный (JSON/YAML/TOML/XML)
- **yaml-cli** — простой
- **jq + yq** — конвертировать в JSON, обработать, вернуть

---

## 📋 Где встречается YAML

### 1. Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
```

### 2. Docker Compose
```yaml
version: "3.9"
services:
  web:
    image: nginx:alpine
    ports:
      - "127.0.0.1:8080:80"
    environment:
      DEBUG: "true"
    depends_on:
      - db
  db:
    image: postgres:16
```

### 3. GitHub Actions
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
```

### 4. Ansible
```yaml
---
- name: Configure web server
  hosts: webservers
  become: yes
  vars:
    http_port: 80
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

### 5. GitLab CI
```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
```

### 6. Pre-commit
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
      - id: ruff-format
```

---

## 🪤 Частые ошибки и грабли

1. **Табы вместо пробелов** — YAML НЕ принимает табы для отступов.
2. **Несогласованные отступы** — все элементы списка должны быть на одном уровне.
3. **`key:value`** без пробела после двоеточия — `key:value` ошибка, нужно `key: value`.
4. **Boolean конфузы** — `yes/no/on/off` конвертируются в `true/false`.
5. **`version: 1.0`** — парсится как float. Кавычьте: `version: "1.0"`.
6. **`:` в строке** — `message: hello: world` сломается. Кавычьте.
7. **Trailing пробелы** — невидимы, но могут ломать.
8. **Anchor без merge** — `*ref` заменит целиком, `<<: *ref` мерджит.
9. **Спецсимволы в начале** — `*`, `&`, `!`, `|`, `>`, `%`, `@`, `\`` — кавычьте.
10. **`null` vs пустое** — `key:` (без значения) = null.
11. **YAML 1.1 vs 1.2** — разные правила (например, `yes` → bool в 1.1).
12. **Комментарии** — не могут быть на той же строке после `|` или `>`.

---

## 🔧 Линтинг и валидация

### yamllint
```bash
sudo pacman -S yamllint
yamllint config.yaml
yamllint -d relaxed config.yaml
yamllint .                          # все .yaml в каталоге

# .yamllint.yaml — конфиг
extends: default
rules:
  line-length: disable
  indentation:
    spaces: 2
    indent-sequences: consistent
  comments:
    require-starting-space: false
```

### pre-commit
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/adrienverge/yamllint.git
    rev: v1.35.1
    hooks:
      - id: yamllint
```

### Схема (Schema) валидация
```bash
# K8s: kubeval
kubeval deployment.yaml

# JSON Schema + YAML
check-jsonschema --schema schema.yaml config.yaml

# В VS Code: YAML расширение Red Hat (с схемами)
```

---

## 🔗 Полезные ссылки

- Спецификация: https://yaml.org/spec/1.2.2
- YAML tutorial: https://circleci.com/blog/what-is-yaml-a-beginner-s-guide
- Online validator: https://yamlchecker.com
- Online parser: https://yaml-online-parser.appspot.com
- yq (mikefarah): https://github.com/mikefarah/yq
- yamllint: https://github.com/adrienverge/yamllint
- Awesome YAML: https://github.com/Maxel03/YAML-files
- JSON Schema Store: https://www.schemastore.org/json/

---

## 💡 Полезные советы

1. **2 пробела** для отступов (стандарт).
2. **Никогда табы** — только пробелы.
3. **Кавычьте строки** с цифрами/датами/`yes`/`no`.
4. **`yamllint`** — для единообразия в команде.
5. **Якоря `&`/`*`** — для DRY (не повторяйтесь).
6. **`<<: *ref`** — для merge keys (Docker Compose).
7. **`|` для скриптов**, `>` для текста.
8. **`safe_load`** в Python (безопасное чтение).
9. **`ruamel.yaml`** — для правки YAML с сохранением комментариев.
10. **yq** — как jq для YAML, мощно.
11. **Схемы (Schema Store)** — автокомплит в VS Code.
12. **Multi-document (`---`)** — для K8s манифестов.
13. ** Комментарии `#`** — для документации.
14. **Не клади секреты** в YAML — используйте vars/secrets.
15. **Пробел после `:`** — обязательное правило.

---

*Сгенерировано как шпаргалка. YAML прост, но капризен —
углубляйтесь через https://yaml.org/spec/1.2.2 и yamllint*

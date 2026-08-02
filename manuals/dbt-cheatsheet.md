# 🔧 dbt (data build tool) — шпаргалка

> **dbt** — инструмент для трансформации данных в хранилище (ELT «T» часть).
> SQL + Jinja-шаблоны, версии, тесты, документация.
> Документация: https://docs.getdbt.com

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Model** | SQL-файл → таблица/view в DWH |
| **Source** | Исходные таблицы (внешние) |
| **Seed** | CSV-файлы, загружаемые в DWH |
| **Snapshot** | Type 2 SCD (история изменений) |
| **Test** | Проверка качества данных |
| **Macro** | Переиспользуемый Jinja-код |
| **Materialization** | Как сохраняется: view/table/incremental |
| **Ref** | Ссылка на другую модель |
| **Staging / Intermediate / Mart** | Слои трансформации |
| **Schema.yml** | Конфигурация моделей/тестов/источников |
| **dbt Cloud / Core** | Хостинг / CLI |

---

## 🚀 Установка и проект

### Установка dbt Core
```bash
# Через pip (с адаптером)
pip install dbt-core dbt-postgres
pip install dbt-core dbt-bigquery
pip install dbt-core dbt-snowflake
pip install dbt-core dbt-spark

# Через uv (быстрее)
uv pip install dbt-core dbt-postgres

# Через Homebrew
brew install dbt-postgres
```

### Создание проекта
```bash
dbt init my_project
# Спросит: тип DWH, хост, порт, юзер, пароль, БД, схему, потоки

# Структура проекта
my_project/
├── dbt_project.yml        # главный конфиг
├── profiles.yml           # подключение к DWH (обычно в ~/.dbt/)
├── models/                # SQL-модели
│   ├── staging/           # stg_ — сырые → нормализованные
│   ├── intermediate/      # int_ — промежуточные
│   └── marts/             # fct_/dim_ — финальные таблицы
├── seeds/                 # CSV-файлы
├── snapshots/             # SCD Type 2
├── macros/                # Jinja-макросы
├── tests/                 # кастомные тесты
├── analyses/              # аналитические запросы (не материализуются)
├── docs/                  # Markdown-документация
└── target/                # (генерируется) compiled SQL, manifest
```

### profiles.yml (`~/.dbt/profiles.yml`)
```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: dbt_user
      password: "{{ env_var('DBT_PASSWORD') }}"
      port: 5432
      dbname: analytics
      schema: dev
      threads: 4
    prod:
      type: postgres
      host: dwh.prod.example.com
      user: dbt_prod
      password: "{{ env_var('DBT_PASSWORD') }}"
      port: 5432
      dbname: analytics
      schema: analytics_prod
      threads: 8
```

---

## 🎯 Команды dbt

```bash
dbt --version                  # версия
dbt debug                      # проверить подключение
dbt run                        # выполнить все модели
dbt run --select my_model      # конкретная модель
dbt run --select my_model+     # + downstream (зависимые)
dbt run --select +my_model     # + upstream (зависимости)
dbt run --select tag:nightly   # по тегу
dbt run --select path:models/staging/   # по пути
dbb run --select my_model --full-refresh   # incremental полностью

dbt test                       # запустить все тесты
dbt test --select my_model
dbt test --select test_type:singular

dbt build                      # run + test (всё сразу)
dbt build --select my_model+

dbt seed                       # загрузить CSV
dbt snapshot                   # обновить snapshots
dbt compile                    # только сгенерировать SQL (без выполнения)
dbt docs generate              # сгенерировать документацию
dbt docs serve --port 8080     # открыть в браузере
dbt run-operation              # вызвать макрос
dbt clean                      # удалить target/, dbt_packages/
dbt deps                       # установить пакеты (dbt_packages.yml)
dbt list                       # список ресурсов
dbt parse                      # проверить синтаксис
dbt source freshness           # проверить свежесть источников
```

### Селекторы (selection syntax)
```bash
dbt run --select my_model              # одна модель
dbt run --select my_model+             # + downstream
dbt run --select +my_model             # + upstream
dbt run --select +my_model+            # обе стороны
dbt run --select 2+my_model            # + 2 уровня upstream
dbt run --select my_model my_other     # несколько
dbt run --select tag:nightly           # по тегу
dbt run --select path:models/staging/  # по пути
dbt run --select package:dbt_utils     # из пакета
dbt run --select resource_type:model   # только модели
dbt run --exclude my_old_model         # исключить
dbt run --select my_model --selector prod   # с YML-селектором
```

---

## 📝 Модель (Model)

`models/staging/stg_customers.sql`:
```sql
{{ config(
    materialized='view',
    tags=['staging']
) }}

WITH source AS (
    SELECT * FROM {{ source('raw', 'customers') }}
),
renamed AS (
    SELECT
        id AS customer_id,
        first_name,
        last_name,
        email,
        created_at
    FROM source
)
SELECT * FROM renamed
```

### Материализации
```sql
{{ config(materialized='view') }}          -- VIEW (по умолчанию)
{{ config(materialized='table') }}         -- TABLE (полная пересборка)
{{ config(materialized='incremental') }}   -- добавлять новые
{{ config(materialized='ephemeral') }}     -- CTE (не сохраняется)
```

### Incremental
```sql
{{ config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='merge'   -- merge / append / delete+insert
) }}

WITH events AS (
    SELECT * FROM {{ ref('stg_events') }}
    {% if is_incremental() %}
    WHERE event_date > (SELECT MAX(event_date) FROM {{ this }})
    {% endif %}
)
SELECT * FROM events
```

### Ref (ссылки на другие модели)
```sql
SELECT
    o.order_id,
    c.customer_name
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id
```

### Source (исходные таблицы)
```sql
SELECT * FROM {{ source('raw', 'orders') }}
```

---

## 📋 schema.yml — конфигурация и тесты

```yaml
version: 2

models:
  - name: stg_customers
    description: "Customers with cleaned names"
    columns:
      - name: customer_id
        description: "Unique customer ID"
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - not_null

  - name: dim_customers
    description: "Customer dimension with metrics"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id

sources:
  - name: raw
    database: analytics
    schema: raw_data
    tables:
      - name: customers
        columns:
          - name: id
            tests:
              - not_null
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

### Встроенные тесты
| Тест | Что проверяет |
|---|---|
| `unique` | Уникальность значений |
| `not_null` | Нет NULL |
| `accepted_values` | Только из списка |
| `relationships` | Foreign-key целостность |

### Свой тест (singular)
`tests/assert_total_revenue_positive.sql`:
```sql
SELECT *
FROM {{ ref('fct_orders') }}
WHERE total_revenue < 0
```

### Generic тест
`tests/generic/no_future_dates.sql`:
```sql
{% test no_future_dates(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} > CURRENT_DATE
{% endtest %}
```

---

## 🔧 Macros (Jinja)

`macros/cents_to_dollars.sql`:
```sql
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)
{% endmacro %}
```

Использование:
```sql
SELECT {{ cents_to_dollars('price_cents') }} AS price_dollars
FROM {{ ref('orders') }}
```

### Полезные макросы dbt-utils
```sql
{{ dbt_utils.get_column_values(ref('stg_customers'), 'country') }}
{{ dbt_utils.pivot('category', dbt_utils.get_column_values(...)) }}
{{ dbt_utils.date_spine("day", "'2024-01-01'", "'2024-12-31'") }}
{{ dbt_utils.safe_add([col1, col2]) }}
```

---

## 📸 Snapshots (история изменений)

`snapshots/orders_snapshot.sql`:
```sql
{% snapshot orders_snapshot %}
{{
    config(
      target_schema='snapshots',
      unique_key='order_id',
      strategy='timestamp',
      updated_at='updated_at',
    )
}}
SELECT * FROM {{ source('raw', 'orders') }}
{% endsnapshot %}
```

После: `dbt snapshot`

Результат — таблица с `dbt_valid_from`, `dbt_valid_to`, `dbt_scd_id`.

---

## 🌱 Seeds (CSV → таблицы)

`seeds/countries.csv`:
```csv
country_id,country_name,iso_code
1,Russia,RU
2,USA,US
3,Germany,DE
```

```bash
dbt seed                       # загрузить все
dbt seed --select countries    # один
```

Использование:
```sql
SELECT * FROM {{ ref('countries') }}
```

---

## 🔌 packages (dbt-utils и др.)

`packages.yml`:
```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: dbt-labs/codegen
    version: 0.12.1
  - git: https://github.com/dbt-labs/dbt-codegen.git
    revision: 1.0.0
  - local: /path/to/local/package
```

```bash
dbt deps                       # установить
dbt clean                      # очистить
```

---

## 📊 Документация

```bash
dbt docs generate
dbt docs serve --port 8080
```

- DAG-визуализация моделей
- Описания колонок
- Линии (lineage)
- SQL-код (compiled)

В `.yml` файле:
```yaml
models:
  - name: stg_customers
    description: "Customers from raw layer"
    columns:
      - name: customer_id
        description: "UUID of the customer"
```

В SQL — Markdown через `{{ doc(...) }}`:
```sql
{{ doc("orders_table") }}
```

`docs/orders_table.md`:
```markdown
{% docs orders_table %}
Заказы из CRM-системы.
{% enddocs %}
```

---

## 🌍 dbt + Airflow (Cosmos)

```python
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.constants import LoadMode

dbt = DbtTaskGroup(
    project_config=ProjectConfig("/path/to/dbt-project"),
    profile_config=ProfileConfig(profile_name="my_project", target_name="dev"),
    render_config={"load_method": LoadMode.DBT_LS},
    default_args={"retries": 2},
)
```

---

## 🪤 Частые ошибки

1. **`profiles.yml` не найден** — проверьте `~/.dbt/profiles.yml` или `DBT_PROFILES_DIR`.
2. **Schema в DWH** — `dev` для разработки, не пишите в продакшен-схему.
3. **Incremental без `unique_key`** — дубликаты.
4. **`ref()` вместо имён таблиц** — иначе dbt не узнает зависимости.
5. **Macro без Jinja** — `{{ ... }}` обязательно.
6. **Слишком большие test-выборки** — тесты на всю таблицу медленные.
7. **`full-refresh`** в продакшене — дорого для больших incremental.
8. **`{{ this }}`** — текущая модель; использовать в WHERE incremental.
9. **Cache miss** — `threads: 4+` для параллелизма.
10. **Не использовать `tags`** — трудно запускать подмножества.

---

## 🔗 Полезные ссылки

- Документация: https://docs.getdbt.com
- dbt Learn: https://courses.getdbt.com
- dbt Hub (packages): https://hub.getdbt.com
- Awesome dbt: https://github.com/dbt-labs/dbt-core
- dbt-utils: https://github.com/dbt-labs/dbt-utils
- dbt-codegen: https://github.com/dbt-labs/dbt-codegen
- TheAnalyticsEngineers (blog): https://www.getdbt.com/blog

---

## 💡 Полезные советы

1. **Слои (модульность)**: staging → intermediate → marts.
2. **Именование**: `stg_`, `int_`, `fct_`, `dim_`.
3. **Тесты на ключах** — `unique` + `not_null` обязательны.
4. **`schema.yml`** — для описаний и тестов.
5. **`ref()`** — всегда, не хардкодьте имена.
6. **Macros** — для DRY (повторяющихся вычислений).
7. **`dbt docs`** — отличная автодокументация.
8. **Incremental** — для больших таблиц (только новые записи).
9. **`source` с `freshness`** — мониторинг свежести источников.
10. **dbt-utils** — почти обязательный пакет.
11. **`dbt build`** — `run` + `test` одним заходом.
12. **dev/prod targets** — изолируйте dev-схемы.
13. **`{% if is_incremental() %}`** — для фильтра новых данных.
14. **Кастомные тесты (singular)** — для сложных бизнес-правил.
15. **Cosmos / dbt-cloud-run** — интеграция с Airflow.

---

*Сгенерировано как шпаргалка. dbt меняет подход к DWH —
углубляйтесь через https://docs.getdbt.com и курс dbt fundamentals*

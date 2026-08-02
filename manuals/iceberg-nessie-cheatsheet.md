# 🧊 Apache Iceberg + Nessie — шпаргалка

> **Apache Iceberg** — открытый формат таблиц для огромных аналитических датасетов.
> **Nessie** — Git-подобный каталог таблиц (с.branches, commits, merges).
> Документация: https://iceberg.apache.org · https://projectnessie.org

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Table format** | Формат хранения табличных данных в файловой системе |
| **Catalog** | Где хранятся метаданные таблиц (Hive, Glue, REST, Nessie) |
| **Snapshot** | Версия таблицы (иммутабельный набор файлов) |
| **Manifest** | Список файлов данных (для snapshot) |
| **Manifest list** | Список manifest'ов |
| **Partition spec** | Правила партиционирования |
| **Time travel** | Чтение данных на прошлый момент времени |
| **Schema evolution** | Изменение схемы без переписывания данных |
| **Hidden partitioning** | Автоматическое партиционирование |
| **Merge-on-read / Copy-on-write** | Стратегии UPDATE/DELETE |

### Зачем Iceberg?
- Замена форматов Hive/Parquet с метаданными.
- ACID-транзакции на файловом хранилище (S3, HDFS).
- Schema evolution без переписывания данных.
- Time travel (читать данные на момент времени).
- Hidden partitioning (автопартиции).
- Совместимость: Spark, Flink, Trino, Impala, Presto, Athena.

---

## 🚀 Архитектура Iceberg

```
┌────────────────────────────────────────────┐
│   SQL Engine (Spark/Flink/Trino/Impala)    │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│                Catalog                     │
│  (Hive Metastore, AWS Glue, REST, Nessie)  │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│              Metadata Layer                │
│   metadata.json → manifest list → manifest │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│     Data Layer (S3, HDFS, ADLS, GCS)       │
│           Parquet / ORC / Avro             │
└────────────────────────────────────────────┘
```

### Слои
1. **Catalog** — где найти `metadata.json` таблицы.
2. **Metadata** — `metadata.json` → указывает на manifest list.
3. **Manifest list** — список manifest'ов (snapshot).
4. **Manifest** — список data-файлов + статистика.
5. **Data files** — Parquet/ORC/Avro.

---

## 🐍 PySpark + Iceberg

### Установка
```bash
pip install pyspark
# Нужен jar: iceberg-spark-runtime-<version>.jar
```

### Spark Session с Iceberg
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("iceberg") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "/tmp/warehouse") \
    .config("spark.sql.catalog.local.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
    .getOrCreate()
```

### Создание таблицы
```sql
CREATE TABLE local.db.events (
    id BIGINT,
    event_time TIMESTAMP,
    user_id STRING,
    event_type STRING,
    properties MAP<STRING, STRING>
)
USING iceberg
PARTITIONED BY (days(event_time))
TBLPROPERTIES (
    'format-version' = '2',
    'write.format.default' = 'parquet'
);
```

### Запись
```python
df = spark.createDataFrame([(1, "click"), (2, "view")], ["id", "event_type"])
df.writeTo("local.db.events").create()
df.writeTo("local.db.events").append()
df.writeTo("local.db.events").overwritePartitions()
```

### Чтение
```sql
SELECT * FROM local.db.events;
SELECT * FROM local.db.events WHERE event_time >= '2024-01-01';

-- Time travel
SELECT * FROM local.db.events VERSION AS OF 12345;
SELECT * FROM local.db.events TIMESTAMP AS OF '2024-01-15 10:00:00';
SELECT * FROM local.db.events FOR SYSTEM_VERSION AS OF '2024-01-15';
```

### Iceberg table procedures
```sql
-- История snapshot'ов
CALL local.system.snapshot_history('db.events');

-- Метаданные файлов
CALL local.system.files('db.events');

-- Сжатие мелких файлов
CALL local.system.rewrite_data_files('db.events');

-- Удаление старых snapshot'ов
CALL local.system.expire_snapshots('db.events', TIMESTAMP '2024-01-01');

-- Удаление orphan-файлов
CALL local.system.remove_orphan_files('db.events');
```

---

## 🌳 Nessie — каталог с ветвями

Nessie — отдельный сервис (Docker). Предоставляет REST API.

### Запуск Nessie
```yaml
# docker-compose.yml
services:
  nessie:
    image: ghcr.io/projectnessie/nessie:latest
    ports:
      - "127.0.0.1:19120:19120"
    environment:
      - QUARKUS_PROFILE=prod
```

### Подключение из Spark
```python
spark = SparkSession.builder \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.nessie", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.nessie.catalog-impl", "org.apache.iceberg.nessie.NessieCatalog") \
    .config("spark.sql.catalog.nessie.uri", "http://nessie:19120/api/v1") \
    .config("spark.sql.catalog.nessie.ref", "main") \
    .config("spark.sql.catalog.nessie.warehouse", "s3://my-bucket/warehouse") \
    .getOrCreate()
```

### Создание таблицы в Nessie
```sql
-- Создать namespace
CREATE NAMESPACE IF NOT EXISTS nessie.db;

-- Создать таблицу
CREATE TABLE nessie.db.events (id BIGINT, ...);

-- Switch на ветку
USE REF dev IN nessie;

-- Снова создать (в dev-ветке)
CREATE TABLE nessie.db.events (id BIGINT, ...);
```

### Управление ветками через SQL
```sql
-- Создать ветку от main
CREATE BRANCH dev IN nessie FROM main;

-- Переключиться
USE REF dev IN nessie;

-- Список веток
SHOW REFERENCES IN nessie;

-- Merge dev в main
MERGE BRANCH dev INTO main IN nessie;
```

### CLI: nessie-cli
```bash
# Установить через pip
pip install pynessie

# Команды (как git!)
nessie branch list
nessie branch create dev
nessie branch delete dev
nessie branch list

nessie log                          # история коммитов
nessie merge dev -b main            # слить dev в main
nessie contents list
nessie contents show db.events
```

---

## ⚙️ Ключевые особенности Iceberg

### Hidden partitioning
```sql
CREATE TABLE events (
    event_time TIMESTAMP,
    ...
) PARTITIONED BY (days(event_time));   -- по дням, без колонки-партиции

-- Автопартиционирование: WHERE event_time > '2024-01-15' использует partition pruning
```

### Schema evolution
```sql
ALTER TABLE db.events ADD COLUMNS (
    new_col STRING,
    cost DECIMAL(10, 2)
);
ALTER TABLE db.events DROP COLUMN old_col;
ALTER TABLE db.events RENAME COLUMN old TO new;
ALTER TABLE db.events ALTER COLUMN id TYPE BIGINT;
```
> Не требует переписывания данных!

### Partition evolution
```sql
ALTER TABLE db.events ADD PARTITION FIELD weeks(event_time);
ALTER TABLE db.events DROP PARTITION FIELD days(event_time);
```

### Time travel
```sql
-- Через snapshot ID
SELECT * FROM db.events VERSION AS OF 123456789;

-- Через timestamp
SELECT * FROM db.events TIMESTAMP AS OF TIMESTAMP '2024-01-01 00:00:00';

-- Через "5 дней назад"
SELECT * FROM db.events TIMESTAMP AS OF current_timestamp() - INTERVAL 5 DAYS;
```

### Maintenance
```sql
-- Compaction (объединить мелкие файлы)
CALL system.rewrite_data_files('db.events', map('min_input_files', 5));

-- Expire old snapshots
CALL system.expire_snapshots('db.events', TIMESTAMP '2024-01-01');

-- Remove orphan files
CALL system.remove_orphan_files('db.events');

-- Rewrite manifests
CALL system.rewrite_manifests('db.events');
```

---

## 📊 Catalogs — выбор

| Catalog | Описание | Когда |
|---|---|---|
| **Hive Metastore** | Классика | Существующий Hive |
| **AWS Glue** | Менеджер AWS | В AWS |
| **REST Catalog** | HTTP API | Свой/облачный (Nessie) |
| **Nessie** | Git-подобный, ветки | Multi-branch dev |
| **Hadoop / Filesystem** | Файл `metadata.json` | Локально/тесты |
| **JDBC** | В SQL-БД | Простая интеграция |
| **Polaris / Unity / Snowflake** | Managed | Cloud-нативно |

---

## 🆚 Iceberg vs Delta Lake vs Hudi

| | Iceberg | Delta Lake | Hudi |
|---|---|---|---|
| Создатель | Netflix → Apache | Databricks | Uber → Apache |
| Catalog | Любой | _delta_log в S3 | .hoodie в S3 |
| Branches | ✅ (через Nessie) | ✅ (Unity) | ✅ |
| Time travel | ✅ | ✅ | ✅ |
| Schema evolution | ✅ | ✅ | ✅ |
| Engines | Spark/Flink/Trino/Impala | Spark/Databricks | Spark/Flink |
| UPDATE/DELETE | Merge-on-read, CoW | CoW | MoR/CoW |

---

## 🪤 Частые ошибки

1. **Мелкие файлы** — много маленьких Parquet → медленно. Регулярный compaction.
2. **Слишком много партиций** — overhead.
3. **Snapshot expire забыт** — данные растут бесконечно.
4. **Orphan files** — файлы без ссылки. `remove_orphan_files`.
5. **Не настроен compaction** — `rewrite_data_files` нужен регулярно.
6. **Branches без merge** — в Nessie копятся расходящиеся ветки.
7. **S3 eventual consistency** — Iceberg обходит, но осторожно.
8. **Catalog down** — таблица недоступна (data есть, metadata нет).
9. **Разные engines, разные snapshot'ы** — конкурентная запись.
10. **Partition evolution без rewrite** — старые данные в старых партициях.

---

## 🔗 Полезные ссылки

- Iceberg: https://iceberg.apache.org
- Iceberg docs: https://iceberg.apache.org/docs/latest
- Nessie: https://projectnessie.org
- Nessie docs: https://projectnessie.org/docs
- PyIceberg: https://py.iceberg.apache.org
- Iceberg Spark: https://iceberg.apache.org/docs/latest/spark-getting-started
- Таблицы форматов: https://www.dremio.com/blog/introduction-to-apache-iceberg

---

## 💡 Полезные советы

1. **Iceberg + Parquet** — де-факто стандарт для lakehouse.
2. **Hidden partitioning** — не дублируйте колонку партиции.
3. **Nessie** — для dev-веток (как git для данных).
4. **`rewrite_data_files`** — регулярно для compaction.
5. **`expire_snapshots`** — для очистки старых версий.
6. **Time travel** — для отладки и аудита.
7. **Schema evolution** — безболезненно меняйте структуру.
8. **REST Catalog / Nessie** — для multi-engine.
9. **Format v2** — для row-level deletes (UPDATE/DELETE).
10. **`CALL system.*`** — встроенные maintenance-процедуры.
11. **Merge-on-read** — для частых UPDATE, медленнее чтение.
12. **Copy-on-write** — быстрое чтение, медленная запись.
13. **Statistical metadata** — в manifest'ах, для file pruning.
14. **Trino + Iceberg** — для ad-hoc SQL.
15. **Flink + Iceberg** — для streaming ingest.

---

*Сгенерировано как шпаргалка. Iceberg/Nessie — современный lakehouse —
углубляйтесь через https://iceberg.apache.org/docs и https://projectnessie.org*

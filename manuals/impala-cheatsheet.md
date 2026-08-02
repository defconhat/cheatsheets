# 🐬 Apache Impala — шпаргалка по SQL-движку

> **Apache Impala** — MPP SQL-движок для интерактивной аналитики на HDFS/S3/Kudu.
> Низкая задержка (миллисекунды), высокое параллелизм.
> Документация: https://impala.apache.org

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **impalad** | Демон на узле (Coordinator + Executor) |
| **statestored** | Распространение метаданных |
| **catalogd** | Метаданные каталога (HMS) |
| **Coordinator** | Узел, принимающий запрос |
| **Executor** | Узел, выполняющий фрагменты запроса |
| **HMS** | Hive Metastore (метаданные таблиц) |
| **HDFS / S3 / Kudu** | Хранилища |
| **Parquet** | Рекомендуемый формат |
| **Compute Stats** | Сбор статистики для оптимизатора |

### Когда Impala, а когда Spark/Hive?
- **Impala**: интерактивные BI-запросы,.dashboard, низкая задержка (<сек).
- **Hive**: тяжёлые batch-задачи, трансформации.
- **Spark**: ETL, ML, batch + streaming.
- **Presto/Trino**:联邦查询, как Impala, но больше коннекторов.

---

## 🚀 Запуск (Docker / кластер)

```yaml
# docker-compose.yml (упрощённо)
services:
  impala-coord:
    image: apache/impala:latest
    command: impalad
    ports:
      - "127.0.0.1:21050:21050"   # HiveServer2 (JDBC/ODBC)
      - "127.0.0.1:25000:25000"   # Web UI
      - "127.0.0.1:28000:28000"   # debug
    depends_on: [statestored, catalogd]

  statestored:
    image: apache/impala:latest
    command: statestored
    ports: ["127.0.0.1:25010:25010"]

  catalogd:
    image: apache/impala:latest
    command: catalogd
    ports: ["127.0.0.1:25020:25020"]
    depends_on: [statestored]
```

### Подключение
```bash
# impala-shell
impala-shell -i localhost -p 21050 -d default

# С аутентификацией (Kerberos/LDAP)
impala-shell -i host -u user --ldap --ldap_password_cmd="..."

# Через JDBC (DBeaver, Tableau)
jdbc:hive2://localhost:21050/default
```

---

## 📝 Базовые операции (Hive-совместимый SQL)

### DDL
```sql
-- Создать БД
CREATE DATABASE IF NOT EXISTS mydb
LOCATION '/user/hive/warehouse/mydb.db';

-- Создать таблицу (Parquet)
CREATE TABLE mydb.events (
    id BIGINT,
    event_time TIMESTAMP,
    user_id STRING,
    event_type STRING,
    amount DECIMAL(10,2)
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET;

-- Внешняя таблица (на существующих файлах)
CREATE EXTERNAL TABLE mydb.logs (
    line STRING
)
STORED AS TEXTFILE
LOCATION '/data/logs/';

-- Kudu таблица
CREATE TABLE mydb.users (
    id BIGINT PRIMARY KEY,
    name STRING,
    email STRING
)
STORED AS KUDU
TBLPROPERTIES (
    'kudu.num_tablet_replicas' = '3'
);

-- Iceberg таблица
CREATE TABLE mydb.events_iceberg (id BIGINT, ...)
STORED AS ICEBERG;
```

### DML
```sql
-- Вставка
INSERT INTO mydb.events VALUES (1, '2024-01-01', 'u1', 'click', 10.5);
INSERT INTO mydb.events SELECT * FROM staging.events;

-- Перезапись (как INSERT OVERWRITE)
INSERT OVERWRITE TABLE mydb.events SELECT * FROM staging;

-- UPDATE / DELETE (только Kudu/Iceberg)
UPDATE mydb.users SET email='new@x.com' WHERE id=1;
DELETE FROM mydb.users WHERE id=1;

-- Truncate
TRUNCATE TABLE mydb.events;

-- Drop
DROP TABLE mydb.events;
ALTER TABLE mydb.events RENAME TO events_archive;
```

---

## 📊 Партиции

### Hive-style partitioning
```sql
-- Статическая партиция
INSERT INTO events PARTITION (dt='2024-01-15')
SELECT id, event_time, user_id FROM staging WHERE dt='2024-01-15';

-- Динамическая (Impala сама распределит)
INSERT INTO events PARTITION (dt)
SELECT id, event_time, user_id, dt FROM staging;

-- Обновить список партиций
REFRESH events;
REFRESH events PARTITION (dt='2024-01-15');

INVALIDATE METADATA events;          -- полностью перечитать
INVALIDATE METADATA;                 -- все таблицы
```

### Управление партициями
```sql
-- Добавить партицию
ALTER TABLE events ADD PARTITION (dt='2024-02-01');
ALTER TABLE events ADD IF NOT EXISTS PARTITION (dt='2024-02-01');

-- Удалить
ALTER TABLE events DROP PARTITION (dt='2024-01-15');

-- Изменить LOCATION
ALTER TABLE events PARTITION (dt='2024-01-15') SET LOCATION '/new/path';
```

---

## ⚡ Производительность

### Сбор статистики (КРИТИЧНО!)
```sql
-- Полная статистика
COMPUTE STATS events;
COMPUTE INCREMENTAL STATS events;     -- для партиционированных

-- Столбцовая
COMPUTE STATS events (event_type, user_id);

-- Удалить статистику
DROP STATS events;
DROP INCREMENTAL STATS events;

-- Посмотреть
SHOW STATS events;
SHOW TABLE STATS events;
SHOW PARTITION STATS events PARTITION (dt='2024-01-15');
```

> ⚠️ БЕЗ `COMPUTE STATS` оптимизатор Impala работает вслепую → плохие планы.

### ANALYZE (альтернатива)
```sql
ANALYZE TABLE events COMPUTE STATISTICS;
ANALYZE TABLE events COMPUTE STATISTICS FOR COLUMNS event_type, user_id;
```

### Форматы и сжатие
```sql
-- Parquet + Snappy (рекомендуется)
CREATE TABLE events (...)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Другие форматы
STORED AS TEXTFILE
STORED AS AVRO
STORED AS RCFILE
STORED AS SEQUENCEFILE
STORED AS KUDU
STORED AS ICEBERG
```

### Параллелизм / память
```sql
-- Установить параллелизм для запроса
SET EXPLAIN_LEVEL=2;
SET MEM_LIMIT=10g;          -- лимит памяти на узел
SET NUM_SCANNER_THREADS=8;
SET MT_DOP=4;               -- многопоточный query

-- Время ожидания
SET QUERY_TIMEOUT_S=300;
```

---

## 🔍 EXPLAIN (план выполнения)

```sql
EXPLAIN SELECT COUNT(*) FROM events WHERE dt='2024-01-15';
EXPLAIN LEVEL=2 SELECT ...;          -- подробнее
EXPLAIN LEVEL=3 SELECT ...;          -- максимально

-- Профилирование (после выполнения)
SUMMARY SELECT COUNT(*) FROM events;
PROFILE;                              -- полный профиль
```

### Что смотреть в PROFILE
- `NumPartitions` — сколько партиций просканировано.
- `RowsRead` — сколько строк прочитано.
- `BytesRead` — объём данных.
- `PerHostPeakMemoryUsage` — пиковая память.
- `Fragment` timings — что долго.

---

## 📋 Функции SQL (Impala)

### Агрегаты
```sql
SELECT
    COUNT(*),
    COUNT(DISTINCT user_id),
    SUM(amount),
    AVG(amount),
    MIN(event_time), MAX(event_time),
    STDDEV(amount), VARIANCE(amount),
    NDV(user_id)                    -- approximate distinct (HyperLogLog)
FROM events;
```

### Окна
```sql
SELECT
    user_id,
    event_time,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time) AS rn,
    LAG(event_type) OVER (PARTITION BY user_id ORDER BY event_time) AS prev,
    LEAD(event_type) OVER (...) AS next,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY event_time) AS cumulative,
    FIRST_VALUE(event_type) OVER (...) AS first,
    NTILE(4) OVER (...) AS quartile
FROM events;
```

### Дата/время
```sql
YEAR(date_col), MONTH(date_col), DAY(date_col), HOUR(ts)
DATE_ADD(date_col, INTERVAL 7 DAYS)
DATE_SUB(date_col, INTERVAL 1 MONTH)
DATEDIFF(end, start)
UNIX_TIMESTAMP(ts), FROM_UNIXTIME(unixts)
DATE_TRUNC('MONTH', ts)
TO_DATE(ts), NOW(), CURRENT_TIMESTAMP()
```

### Строковые
```sql
SUBSTR(s, 1, 5), LENGTH(s)
UPPER(s), LOWER(s), INITCAP(s)
TRIM(s), LTRIM(s), RTRIM(s)
SPLIT_PART(s, ',', 2)
REGEXP_EXTRACT(s, 'pattern', 1)
REGEXP_REPLACE(s, 'pattern', 'repl')
CONCAT(a, b, c), CONCAT_WS('-', a, b, c)
```

### Условные
```sql
CASE WHEN x > 0 THEN 'pos' WHEN x < 0 THEN 'neg' ELSE 'zero' END
COALESCE(a, b, c)         -- первое не-null
NVL(a, b)                 -- как COALESCE(a, b)
NULLIF(a, b)
DECODE(col, val1, res1, val2, res2, default)
```

---

## 🛠️ Полезные команды

```sql
SHOW DATABASES;
SHOW TABLES IN mydb;
SHOW TABLES IN mydb LIKE 'events*';
SHOW CREATE TABLE mydb.events;
DESCRIBE mydb.events;
DESCRIBE FORMATTED mydb.events;
DESCRIBE mydb.events.event_type;

SHOW FUNCTIONS;
SHOW AGGREGATE FUNCTIONS;
SHOW PARTITIONS events;

-- Метаданные
SHOW TABLE STATS events;
SHOW COLUMN STATS events;

-- Загрузить/выгрузить
LOAD DATA INPATH '/path/file.csv' INTO TABLE events;
INSERT OVERWRITE DIRECTORY '/output' SELECT * FROM events;

-- Файлы таблицы
SHOW FILES IN events;
SHOW FILES IN events PARTITION (dt='2024-01-15');
```

---

## 🐍 Python (Impyla / PyHive)

```python
from impala.dbapi import connect

conn = connect(host='localhost', port=21050, user='impala')
cursor = conn.cursor()

cursor.execute('USE mydb')
cursor.execute('SELECT * FROM events LIMIT 10')
for row in cursor.fetchall():
    print(row)

# Через pandas
import pandas as pd
from impala.dbapi import connect

conn = connect(host='localhost', port=21050)
df = pd.read_sql('SELECT * FROM mydb.events LIMIT 1000', conn)
```

### SQLAlchemy
```python
from sqlalchemy import create_engine
engine = create_engine('impala://localhost:21050/mydb')
df = pd.read_sql('SELECT * FROM events', engine)
```

---

## 🌐 Web UI

- **Coordinator UI**: `http://host:25000/`
  - Active queries
  - Completed queries
  - Memory
  - Sessions
- **Statestored**: `http://host:25010/`
- **Catalogd**: `http://host:25020/`

В UI можно:
- Смотреть выполняющиеся запросы.
- Профиль завершённого.
- Cancel долгого запроса.
- Лимиты/квоты.

---

## 🪤 Частые ошибки

1. **Не собраны STATS** — `COMPUTE STATS` обязателен после INSERT/LOAD.
2. **`REFRESH` vs `INVALIDATE`** — REFRESH одной таблицы/партиции, INVALIDATE — всё.
3. **Маленькие файлы** — Parquet любит большие файлы (128MB+).
4. **Много мелких партиций** — overhead.
5. **Нет partition pruning** — фильтруйте по partition-колонке.
6. **SELECT * на больших таблицах** — миллиарды строк переносятся.
7. **Курсоры в Python** — `fetchall()` на больших данных → OOM.
8. **`SELECT DISTINCT`** — медленнее, чем `GROUP BY`.
9. **Не настроен MEM_LIMIT** — OOM на сложных JOIN.
10. **Kudu без primary key** — медленные UPDATE.

---

## 🆚 Impala vs Presto/Trino vs Spark SQL

| | Impala | Presto/Trino | Spark SQL |
|---|---|---|---|
| Latency | ⚡⚡⚡ (мс) | ⚡⚡ | ⚡ |
| Throughput | Высокий | Средний | Высокий |
| Формат | Parquet/Avro/Text/Kudu | Любой | Parquet/Avro |
| HMS | Нативно | Опционально | Опционально |
| Memory | Native C++ | JVM | JVM |
| Кластер | HDFS-нативный | Universal | Universal |
| Best for | BI на Hadoop | Federated | ETL + BI |

---

## 🔗 Полезные ссылки

- Документация: https://impala.apache.org/docs.html
- SQL Reference: https://impala.apache.org/docs/impala/latest/langref
- Impyla (Python): https://github.com/cloudera/impyla
- Tuning: https://impala.apache.org/docs/impala/latest/topics/impala_performance.html
- Awesome Impala: https://github.com/mulia/awesome-impala

---

## 💡 Полезные советы

1. **`COMPUTE STATS`** — после каждой загрузки данных.
2. **Parquet + Snappy** — лучший формат для Impala.
3. **Partition pruning** — фильтруйте по partition-колонке.
4. **`REFRESH`** после INSERT из других систем (Hive/Spark).
5. **`INVALIDATE METADATA`** — если менялась структура.
6. **Memory limits** — `SET MEM_LIMIT=10g;` для тяжёлых.
7. **`NDV()` вместо `COUNT(DISTINCT)`** — быстрее (approx).
8. **`LIMIT`** — для exploration.
9. **`EXPLAIN`** — смотрите partition pruning.
10. **`PROFILE`** — для тормозных запросов.
11. **Кэш metadata** — Coordinator кэширует, не паникуйте при «медленном старте».
12. **Kudu** — для часто обновляемых таблиц.
13. **Iceberg** — для time travel и эволюции схемы.
14. **JDBC-пул** — в BI-инструментах (Tableau, DBeaver).
15. **`impala-shell -f script.sql`** — для запуска SQL-файлов.

---

*Сгенерировано как шпаргалка. Impala — для low-latency SQL на Hadoop —
углубляйтесь через https://impala.apache.org/docs.html*

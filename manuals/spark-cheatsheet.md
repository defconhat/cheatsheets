# ⚡ Apache Spark / PySpark — шпаргалка

> **Apache Spark** — движок распределённой обработки больших данных.
> **PySpark** — Python API для Spark. В 100× быстрее Hadoop MapReduce (in-memory).
> Документация: https://spark.apache.org/docs/latest

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Driver** | Процесс, выполняющий main(), создаёт SparkContext/SparkSession |
| **Executor** | Процесс на worker-узле, выполняет задачи |
| **RDD** | Resilient Distributed Dataset — базовая абстракция (низкий уровень) |
| **DataFrame** | Распределённая таблица (как pandas, но распределённая) |
| **Dataset** | Типизированный DataFrame (Java/Scala) |
| **Partition** | Часть данных, обрабатываемая одной задачей |
| **Transformation** | Ленивая операция (map, filter) — не выполняется сразу |
| **Action** | Запускает вычисления (collect, count, write) |
| **Shuffle** | Перераспределение данных между партициями (дорого!) |
| **Narrow vs Wide dependency** | Без shuffle / с shuffle |
| **Catalyst** | Оптимизатор запросов |
| **Tungsten** | Движок выполнения (off-heap memory) |

---

## 🚀 Запуск

### Локально (для разработки)
```bash
pip install pyspark[sql]              # pip
uv pip install pyspark[sql]           # uv (быстрее)
```

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "10") \
    .getOrCreate()
```

### Подключение к кластеру
```python
spark = SparkSession.builder \
    .appName("ProductionApp") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.cores.max", "10") \
    .getOrCreate()
```

### Через spark-submit
```bash
spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --executor-memory 4G \
    --executor-cores 2 \
    --num-executors 5 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    my_script.py
```

### Web UI
- **Spark Master UI**: `http://spark-master:8080`
- **Spark Application UI**: `http://<driver>:4040` (во время работы приложения)
- **History Server**: `http://<host>:18080`

---

## 📊 DataFrame — создание

```python
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from pyspark.sql import types as T

spark = SparkSession.builder.appName("demo").master("local[*]").getOrCreate()

# 1. Из списка/Python-объектов
df = spark.createDataFrame([
    ("Alice", 30, "NYC"),
    ("Bob", 25, "LA"),
    ("Charlie", 35, "NYC"),
], ["name", "age", "city"])

# 2. Из RDD
rdd = spark.sparkContext.parallelize([("Alice", 30), ("Bob", 25)])
df = rdd.toDF(["name", "age"])

# 3. Из pandas
import pandas as pd
pdf = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
df = spark.createDataFrame(pdf)

# 4. Чтение файлов (см. ниже)
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.parquet("data.parquet")
df = spark.read.json("data.json")
```

### Схема (Schema)
```python
# Явная схема (рекомендуется для производительности)
schema = T.StructType([
    T.StructField("name", T.StringType(), False),
    T.StructField("age", T.IntegerType(), True),
    T.StructField("salary", T.DoubleType(), True),
    T.StructField("tags", T.ArrayType(T.StringType())),
    T.StructField("address", T.StructType([
        T.StructField("city", T.StringType()),
        T.StructField("zip", T.StringType()),
    ])),
])

df = spark.read.schema(schema).csv("data.csv")
```

### Типы данных
| Тип | Описание |
|---|---|
| `ByteType`, `ShortType`, `IntegerType`, `LongType` | Целые |
| `FloatType`, `DoubleType` | С плавающей точкой |
| `DecimalType(precision, scale)` | Десятичное (для денег) |
| `StringType` | Строка |
| `BinaryType` | Байты |
| `BooleanType` | Логическое |
| `DateType`, `TimestampType` | Дата/время |
| `ArrayType(elementType)` | Массив |
| `MapType(keyType, valueType)` | Словарь |
| `StructType([StructField(...)])` | Структура (вложенная) |

---

## 🔍 Просмотр и исследование

```python
df.show()                             # вывести (по умолчанию 20 строк)
df.show(5, truncate=False)            # 5 строк, без обрезки
df.printSchema()                      # схема дерева
df.columns                            # список колонок
df.dtypes                             # [(name, type), ...]
df.count()                            # число строк (action!)
df.describe().show()                  # статистика (min, max, mean, stddev)
df.summary().show()                   # расширенная статистика (с квартилями)
df.first()                            # первая строка (Row)
df.head(5)                            # первые 5 строк (list)
df.take(5)                            # = head
df.collect()                          # ВСЕ строки в список (ОСТОРОЖНО!)
df.toPandas()                         # в pandas DataFrame (собирает на driver!)
df.limit(100).toPandas()              # безопасно — ограничить
```

### Row — доступ к полям
```python
row = df.first()
row["name"]                           # по имени
row.name                              # атрибутом
row[0]                                # по индексу
row.asDict()                          # в словарь
```

---

## ⚙️ Transformations (ленивые)

### Выбор и фильтрация
```python
df.select("name", "age")              # выбрать колонки
df.select(df.name, df.age + 1)        # с выражением
df.selectExpr("name", "age * 2 as double_age")   # SQL-выражение
df.filter("age > 25")                 # SQL-фильтр
df.filter(df.age > 25)                # column-фильтр
df.where(df.age > 25)                 # = filter
df.where((df.age > 25) & (df.city == "NYC"))  # AND/OR
df.where("age > 25 AND city = 'NYC'")
df.distinct()                         # уникальные строки
df.dropDuplicates(["name"])           # по конкретным колонкам
df.drop("col1", "col2")               # удалить колонки
df.withColumn("age2", df.age * 2)     # добавить/заменить колонку
df.withColumnRenamed("age", "years")  # переименовать
df.withColumn("const", F.lit(1))      # константа
```

### Сортировка
```python
df.orderBy("age")                     # по возрастанию
df.orderBy(df.age.desc())             # по убыванию
df.orderBy(df.age.desc(), df.name.asc())  # несколько
df.sort(df.age.desc())                # = orderBy
```

### Агрегации
```python
df.count()
df.agg(F.sum("salary"), F.avg("age"), F.max("age"))

# Group By
df.groupBy("city").count()
df.groupBy("city").avg("age")
df.groupBy("city").agg(
    F.sum("salary").alias("total"),
    F.avg("age").alias("avg_age"),
    F.count("*").alias("n"),
    F.max("age"),
    F.collect_set("name"),
)
df.groupBy("city").pivot("gender").avg("age")   # pivot
df.cube("city", "gender").count()               # multi-dim
df.rollup("city", "gender").count()
```

### Общие агрегатные функции
```python
F.count("*"), F.countDistinct("col"), F.approx_count_distinct("col")
F.sum("col"), F.avg("col"), F.mean("col")
F.min("col"), F.max("col")
F.stddev("col"), F.variance("col"), F.kurtosis("col"), F.skewness("col")
F.first("col"), F.last("col")
F.collect_list("col"), F.collect_set("col")
F.sumDistinct("col")
F.correlation("col1", "col2"), F.covar_pop("col1", "col2")
```

### Window functions
```python
from pyspark.sql.window import Window

w = Window.partitionBy("city").orderBy(df.age.desc())
df.withColumn("rank", F.rank().over(w))
df.withColumn("denserank", F.dense_rank().over(w))
df.withColumn("rownum", F.row_number().over(w))
df.withColumn("lag", F.lag("age", 1).over(w))
df.withColumn("lead", F.lead("age", 1).over(w))
df.withColumn("prev_total", F.sum("salary").over(w))

# Скользящее окно
w_range = Window.partitionBy("city").orderBy("age").rowsBetween(-1, 1)
df.withColumn("moving_avg", F.avg("age").over(w_range))

# Накопительный итог
w_cum = Window.orderBy("date").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df.withColumn("cumsum", F.sum("amount").over(w_cum))
```

### Joins
```python
joined = df1.join(df2, "id")                  # по одной колонке
joined = df1.join(df2, ["id", "code"])        # несколько
joined = df1.join(df2, df1.id == df2.user_id) # разные имена
joined = df1.join(df2, cond, "inner")         # тип
joined = df1.join(df2, cond, "left")
joined = df1.join(df2, cond, "right")
joined = df1.join(df2, cond, "outer")         # full outer
joined = df1.join(df2, cond, "left_semi")     # только совпавшие из df1
joined = df1.join(df2, cond, "left_anti")     # только НЕ совпавшие из df1

# Без дублей колонок
joined = df1.join(df2, ["id"])                # id не дублируется
```

### Union / Set operations
```python
df1.union(df2)                        # union all (с дублями)
df1.unionByName(df2)                  # по имени колонок
df1.intersect(df2)                    # пересечение
df1.exceptAll(df2)                    # разность
```

---

## 📝 SQL-функции (pyspark.sql.functions)

### Строковые
```python
F.upper("col"), F.lower("col"), F.initcap("col")
F.length("col")
F.concat("a", "b"), F.concat_ws("-", "a", "b", "c")
F.substring("col", 1, 3)             # pos 1-indexed, length
F.split("col", ",")                  # в массив
F.regexp_extract("col", r"(\d+)", 1) # regex-группа
F.regexp_replace("col", r"\d+", "#")
F.trim("col"), F.ltrim(), F.rtrim()
F.lpad("col", 5, "0"), F.rpad("col", 5, "0")
F.instr("col", "sub")                # позиция подстроки
F.translate("col", "abc", "123")     # замена символов
F.format_string("%s-%d", "col1", "col2")
F.format_number("col", 2)
```

### Математические
```python
F.abs("col"), F.sqrt("col"), F.exp("col"), F.log("col")
F.sin("col"), F.cos("col"), F.tan("col")
F.ceil("col"), F.floor("col"), F.round("col", 2)
F.pow("col", 2), F.greatest("a", "b"), F.least("a", "b")
F.rand(), F.randn()
```

### Даты и время
```python
F.current_date(), F.current_timestamp(), F.now()
F.year("date"), F.month("date"), F.dayofmonth("date"), F.dayofweek("date")
F.hour("ts"), F.minute("ts"), F.second("ts")
F.date_format("date", "yyyy-MM-dd")
F.date_add("date", 7), F.date_sub("date", 7)
F.datediff("end", "start")
F.months_between("end", "start")
F.to_date("col", "yyyy-MM-dd")
F.to_timestamp("col", "yyyy-MM-dd HH:mm:ss")
F.trunc("date", "month")             # начало месяца
F.date_trunc("hour", "ts")           # округление до часа
F.window("ts", "1 hour")             # оконная агрегация по времени
```

### Условные
```python
F.when(df.age < 18, "minor").otherwise("adult")
F.when(df.age < 18, "minor") \
  .when(df.age < 65, "adult") \
  .otherwise("senior")

# Условие
F.expr("age > 18 AND city = 'NYC'")
```

### NULL-обработка
```python
F.isnull("col"), F.isnan("col")
F.col("x").isNull()
df.na.drop()                          # удалить строки с NULL
df.na.drop(how="all")                 # только если все NULL
df.na.drop(subset=["name"])           # по конкретным колонкам
df.na.fill(0)                         # заполнить NULL
df.na.fill({"name": "unknown", "age": 0})
df.na.replace([""], ["unknown"], "name")
```

### Массивы
```python
F.array("a", "b", "c")                # создать массив
F.array_size("arr"), F.size("arr")
F.explode("arr")                      # каждый элемент → отдельную строку
F.posexplode("arr")                   # + позиция
F.array_contains("arr", "x")
F.array_distinct("arr")
F.array_sort("arr")
F.flatten("arr_of_arr")
F.concat("arr1", "arr2")
F.slice("arr", 1, 3)
F.array_join("arr", ",")              # массив в строку
```

### JSON
```python
F.get_json_object("col", "$.key")
F.from_json("col", schema)
F.to_json("col")
F.json_tuple("col", "a", "b", "c")
```

---

## 📥 Чтение и запись

### Чтение
```python
# CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.option("header", True).option("inferSchema", True).csv("data.csv")
df = spark.read.option("delimiter", ";").csv("data.csv")
df = spark.read.option("mode", "DROPMALFORMED").csv("bad.csv")

# Партиционированные данные
df = spark.read.parquet("s3://bucket/data")
df = spark.read.parquet("data/year=2024/month=01")

# Несколько файлов
df = spark.read.csv("data/*.csv")
df = spark.read.csv(["file1.csv", "fileCSV2.csv"])

# JSON (по строке)
df = spark.read.json("data.json")
df = spark.read.option("multiLine", True).json("data.json")

# Parquet / ORC / Avro
df = spark.read.parquet("data.parquet")   # рекомендуется
df = spark.read.orc("data.orc")
df = spark.read.avro("data.avro")         # нужно: --packages ...avro...

# JDBC (БД)
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://host/db") \
    .option("dbtable", "schema.table") \
    .option("user", "user").option("password", "secret") \
    .load()

# Партиционированное чтение из БД
df = spark.read.jdbc(url, table, column="id", lowerBound=1, upperBound=100000, numPartitions=10, properties={})
```

### Запись
```python
# Базовые форматы
df.write.csv("output.csv")
df.write.json("output.json")
df.write.parquet("output.parquet")        # рекомендуется
df.write.orc("output.orc")

# Опции записи
df.write.mode("overwrite").parquet("data")    # перезаписать
df.write.mode("append").parquet("data")       # дописать
df.write.mode("ignore").parquet("data")       # если есть — ничего
df.write.mode("errorifexists").parquet("data") # по умолчанию (ошибка)

# Партиционирование
df.write.partitionBy("year", "month").parquet("data")
df.write.bucketBy(100, "id").sortBy("id").saveAsTable("bucketed")

# Один файл (coalesce)
df.coalesce(1).write.csv("one_file")

# JDBC
df.write.jdbc(url, "table_name", properties=props)

# Streaming
df.writeStream.format("console").start()
```

### Кэширование
```python
df.cache()                            # в память (MEMORY_AND_DISK)
df.persist(StorageLevel.MEMORY_ONLY)
df.unpersist()                        # освободить
df.is_cached
```

### Storage Levels
| Уровень | Описание |
|---|---|
| `MEMORY_ONLY` | Только RAM (может не поместиться) |
| `MEMORY_AND_DISK` | RAM + диск (по умолчанию) |
| `MEMORY_ONLY_SER` | Сериализованный (меньше RAM) |
| `DISK_ONLY` | Только диск |
| `MEMORY_AND_DISK_SER` | Сериализованный RAM+disk |

---

## 📜 SQL в Spark

```python
# Зарегистрировать DataFrame как временную таблицу
df.createOrReplaceTempView("people")

# SQL-запрос
result = spark.sql("""
    SELECT city, COUNT(*) as n, AVG(age) as avg_age
    FROM people
    WHERE age > 20
    GROUP BY city
    ORDER BY n DESC
""")

# Глобальная временная таблица (доступна во всех сессиях)
df.createOrReplaceGlobalTempView("people_global")
spark.sql("SELECT * FROM global_temp.people_global")
```

---

## 🔧 UDF (User Defined Functions)

```python
# Python UDF (медленно — сериализация)
@F.udf(T.StringType())
def upper_case(s):
    return s.upper() if s else None

df.withColumn("name_upper", upper_case(df.name))

# С декоратором и схемой
@F.udf(returnType=T.IntegerType())
def square(x):
    return x * x

# Регистрация для SQL
spark.udf.register("upper_case", upper_case)
spark.sql("SELECT upper_case(name) FROM people")

# Pandas UDF (быстро — векторизованно, рекомендуется!)
import pandas as pd

@F.pandas_udf(T.DoubleType())
def multiply_by_two(s: pd.Series) -> pd.Series:
    return s * 2

df.withColumn("doubled", multiply_by_two(df.col))

# Iterator of pandas DataFrames (для ML)
@F.pandas_udf(T.DoubleType())
def predict_batch(iterator):
    for pdf in iterator:
        yield model.predict(pdf)
```

---

## 🌊 Structured Streaming

Обработка потоковых данных (Kafka, файлы, сокеты).

```python
# Источник
stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "topic1") \
    .load()

# Или из каталога (новые файлы)
stream = spark.readStream.format("csv").option("header", True).schema(schema).load("data/")

# Трансформации (как у обычного DataFrame!)
result = stream.selectExpr("CAST(value AS STRING)") \
    .groupBy(window("timestamp", "1 minute"), "category") \
    .count()

# Sink
query = result \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
```

### Output modes
| Mode | Описание |
|---||
| `append` | Только новые строки (default) |
| `complete` | Вся таблица каждый раз |
| `update` | Только изменившиеся |
| Sinks | `console`, `memory`, `file`, `kafka`, `foreach`, `foreachBatch` |

---

## ⚙️ Конфигурация и производительность

### Важные настройки
```python
spark = SparkSession.builder \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.executor.instances", "10") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.adaptive.enabled", "true")   # AQE (рекомендуется!) \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.files.maxPartitionBytes", "128MB") \
    .getOrCreate()
```

### Adaptive Query Execution (AQE) — рекомендуется в Spark 3+
- Меняет план выполнения на лету
- Coalesce partitions (уменьшает shuffle)
- Switch join strategy
- Skew join optimization

### Ключевые принципы производительности
1. **Используйте DataFrame API, не RDD** — Catalyst оптимизирует.
2. **Parquet/ORC вместо CSV/JSON** — колоночное хранение + сжатие.
3. **Кэшируйте** часто используемые DataFrame'ы.
4. **Избегайте shuffle** — narrow transformations быстрее.
5. **broadcast join** для маленьких таблиц (< 10MB по умолчанию):
   ```python
   df1.join(broadcast(df2), "id")
   ```
6. **Partitioning** — число партиций = число ядер × 2-4.
7. **`spark.sql.adaptive.enabled=true`** — почти всегда плюс.
8. **Avoid `collect()`** — собирает всё на driver, может OOM.
9. **Repartition/Coalesce**:
   ```python
   df.repartition(100)                # увеличить (вызывает shuffle)
   df.coalesce(10)                    # уменьшить (без shuffle)
   df.repartition("key")              # по колонке
   df.repartitionByRange(100, "key")
   ```

### Partitioning (партиционирование)
```python
# Число партиций по умолчанию
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Влияет на:
df.rdd.getNumPartitions()
df.repartition(200)
df.coalesce(10)
```

---

## 🐛 Дебаг и мониторинг

### Логи
```python
# Уровень логирования
spark.sparkContext.setLogLevel("WARN")   # OFF/FATAL/ERROR/WARN/INFO/DEBUG

# В web UI видно:
# - Stages и задачи
# - Shuffle read/write
# - Storage (кэш)
# - Executors (память, CPU)
# - SQL план выполнения
```

### Explain (план выполнения)
```python
df.explain()                          # физический план
df.explain(True)                      # полный (parsed, analyzed, optimized, physical)
df.explain("formatted")               # красивый
df.explain("cost")                    # со стоимостью
```

### Память
```python
# Исполнение memory
print(spark.sparkContext._jsc.getJavaSparkContext().defaultParallelism())
```

### Частые ошибки
- **OOM on driver** — `collect()` собрал слишком много. Используйте `.take()`/`.limit()`.
- **OOM on executor** — мало `spark.executor.memory` или слишком большие partition'ы.
- **Shuffle слишком большой** — настройте `spark.sql.shuffle.partitions`.
- **Skew (перекос)** — одна партиция в 10× больше. Используйте AQE.
- **Small files problem** — много мелких файлов. `coalesce` перед записью.

---

## 🆚 pandas vs PySpark

| | pandas | PySpark |
|---|---|---|
| Объём данных | ГБ (в RAM) | ТБ (распределённо) |
| API | Похожи | Похожи (намеренно!) |
| Ленивость | нет | да (transformations) |
| Выполнение | immediate | action запускает |
| Типы | numpy dtype | Spark types |
| Индекс | есть | нет (нет .loc[]) |
| `collect()/toPandas()` | — | собрать на driver |

```python
# Конвертация
df.toPandas()                         # Spark → pandas (собирает!)
spark.createDataFrame(pdf)            # pandas → Spark
```

---

## 🪤 Частые ошибки и грабли

1. **`collect()` на больших данных** — OOM. Используйте `.show()`/`.take()`.
2. **`toPandas()` на больших данных** — собирает на driver. Только для агрегатов.
3. **Забыли `.cache()`** — DataFrame пересчитывается при каждом action.
4. **Python UDF** — медленно (serialization). Используйте built-in functions или pandas_udf.
5. **Wide transformations** (join, groupBy) — вызывают shuffle (дорого).
6. **CSV inferSchema** — может ошибиться. Задавайте схему явно.
7. **`count()` после каждого шага** — каждый раз пересчитывает весь граф.
8. **Не настроен `spark.sql.shuffle.partitions`** — по умолчанию 200 (часто много).
9. **`union` vs `unionByName`** — первый по позиции, второй по имени (безопаснее).
10. **`coalesce(1)` для записи одного файла** — но без параллелизма.
11. **Слева направо порядок join'ов** — оптимизатор может не справиться.
12. **Spark не для OLTP** — он для batch + аналитики, не для транзакций.

---

## 🔗 Полезные ссылки

- Официальная документация: https://spark.apache.org/docs/latest
- PySpark API: https://spark.apache.org/docs/latest/api/python
- Spark SQL functions: https://spark.apache.org/docs/latest/api/sql/index.html
- Книга: *Spark Definitive Guide* (Zaharia, Karau)
- Excellent tuning guide: https://www.bmc.com/blogs/spark-tips-performance
- Databricks blog: https://www.databricks.com/blog/category/engineering/spark
- Awesome Spark: https://github.com/awesome-spark/awesome-spark

---

## 💡 Полезные советы

1. **DataFrame API** — основной, не RDD (если не нужно низкоуровневое).
2. **Parquet** — лучший формат (колоночный, со сжатием, со схемой).
3. **`cache()`** — если DataFrame используется несколько раз.
4. **`broadcast join`** — для маленькой таблицы (избегает shuffle).
5. **AQE (`spark.sql.adaptive.enabled=true`)** — включите в Spark 3+.
6. **Указывайте схему явно** — быстрее и надёжнее `inferSchema`.
7. **Partition pruning** — фильтруйте по партициям (`where year=2024`).
8. **Predicate pushdown** — фильтры доходят до источника (JDBC, Parquet).
9. **`explain()`** — смотрите план выполнения, ищите shuffle/exchange.
10. **Избегайте UDF** — используйте встроенные функции Spark.
11. **`spark.sql.shuffle.partitions`** — настройте под объём данных.
12. **KryoSerializer** — быстрее стандартной Java-сериализации.
11. **`.coalesce(1)` перед write** — чтобы получить один файл.
14. **`.toPandas()` только после агрегации** — не на raw big data.
15. **Structured Streaming** — для real-time (Kafka → Spark → sink).

---

*Сгенерировано как шпаргалка. Spark огромен —
углубляйтесь через https://spark.apache.org/docs/latest/ и Spark Definitive Guide*

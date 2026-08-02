# 🐘 Apache Kafka — шпаргалка

> **Apache Kafka** — распределённая платформа потоковой обработки.
> Pub/Sub-очереди, персистентное хранение, replay, потоковая аналитика.
> Документация: https://kafka.apache.org/documentation

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Broker** | Узел Kafka (сервер) |
| **Cluster** | Кластер брокеров |
| **Topic** | Канал/тема (куда пишут и читают) |
| **Partition** | Партиция внутри topic (для параллелизма) |
| **Offset** | Позиция сообщения в партиции |
| **Producer** | Тот, кто пишет в topic |
| **Consumer** | Тот, кто читает из topic |
| **Consumer Group** | Группа потребителей (делит partitions) |
| **Replication** | Репликация partition'ов для отказоустойчивости |
| **Leader / Follower** | Главный/запасной брокер для partition |
| **ZooKeeper / KRaft** | Координатор кластера (KRaft — новый, без ZK) |
| **Retention** | Сколько хранить сообщения |

---

## 🚀 Установка и запуск

### Через Docker (быстрее всего)
```bash
# С Compose
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  kafka:
    image: confluentinc/cp-kafka:7.6.0
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: 'broker,controller'
      KAFKA_LISTENERS: 'PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://localhost:9092'
      KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:9093'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'
    ports:
      - "127.0.0.1:9092:9092"
EOF
docker compose up -d
```

### Локально (тяжелее)
```bash
# Скачать с https://kafka.apache.org/downloads
tar -xzf kafka_2.13-3.7.0.tgz
cd kafka_2.13-3.7.0

# KRaft (без ZooKeeper, современный способ)
bin/kafka-storage.sh format --config config/kraft/server.properties --cluster-id $(bin/kafka-storage.sh random-uuid)
bin/kafka-server-start.sh config/kraft/server.properties
```

---

## 🛠️ CLI-утилиты (kafka-tools)

### Топики
```bash
# Создать
bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic my-topic \
    --partitions 3 \
    --replication-factor 1

# Без указания partitions (по умолчанию)
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic my-topic

# С конфигом
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 \
    --topic logs --partitions 6 --replication-factor 1 \
    --config retention.ms=604800000 \
    --config cleanup.policy=delete

# Список
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Описание
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-topic

# Удалить
bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic my-topic

# Увеличить partitions (нельзя уменьшить!)
bin/kafka-topics.sh --alter --bootstrap-server localhost:9092 \
    --topic my-topic --partitions 6
```

### Producer (CLI)
```bash
# Интерактивный ввод с клавиатуры
bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --topic my-topic

# С key
bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --topic my-topic \
    --property "parse.key=true" \
    --property "key.separator=:"

# Ввести: key1:value1

# Из файла
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 \
    --topic my-topic < messages.txt

# С acks (гарантия записи)
--producer-property acks=all
```

### Consumer (CLI)
```bash
# Чтение
bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --topic my-topic \
    --from-beginning

# С key
bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --topic my-topic \
    --property print.key=true \
    --property key.separator=" - "

# В группе
bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --topic my-topic \
    --group my-group
```

### Consumer Groups
```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --describe --group my-group

# Сбросить offset
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --group my-group --reset-offsets --to-earliest \
    --topic my-topic --execute

# На конкретный offset
--reset-offsets --to-offset 42
--reset-offsets --to-datetime 2024-01-01T00:00:00.000
--reset-offsets --shift-by -10
```

### Группы и конфиги
```bash
bin/kafka-configs.sh --bootstrap-server localhost:9092 \
    --alter --entity-type topics --entity-name my-topic \
    --add-config retention.ms=86400000

bin/kafka-acls.sh ...        # управление доступом
bin/kafka-log-dirs.sh ...    # размеры partition'ов
```

---

## 🐍 Python-клиенты

### kafka-python (простой)
```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None,
    acks='all',
    retries=3,
)

producer.send('my-topic', key='user1', value={'name': 'Alice', 'age': 30})
producer.send('my-topic', value={'event': 'login'})

# Дождаться доставки
producer.flush()
producer.close()

# Consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['localhost:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',     # earliest/latest/none
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

for message in consumer:
    print(f"{message.topic}:{message.partition}:{message.offset}: {message.value}")
```

### aiokafka (асинхронный)
```python
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio

async def produce():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait('my-topic', b'hello')
    finally:
        await producer.stop()

asyncio.run(produce())
```

### confluent-kafka (быстрый, C-биндинг)
```python
from confluent_kafka import Producer, Consumer

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err: print(f"Error: {err}")
    else: print(f"Sent to {msg.topic()} [{msg.partition()}]")

producer.produce('my-topic', key='key', value='value', callback=delivery_report)
producer.flush()
```

### Faust (потоковая обработка, как Spark Streaming)
```python
import faust

app = faust.App('my-app', broker='kafka://localhost:9092')

class Order(faust.Record):
    id: int
    amount: float

orders_topic = app.topic('orders', value_type=Order)

@app.agent(orders_topic)
async def process_order(orders):
    async for order in orders:
        print(f"Processing order {order.id}: {order.amount}")

@app.timer(interval=10.0)
async def produce_test():
    await orders_topic.send(value=Order(id=1, amount=99.99))
```

---

## 🎓 Архитектура и паттерны

### Топологии
```
Producer → Topic → Consumer

         ┌─ Partition 0 ─ [msg1, msg2, msg3]
Topic ───┼─ Partition 1 ─ [msg4, msg5]
         └─ Partition 2 ─ [msg6, msg7, msg8]
```

### Consumer Group
- Группа разделяет partition'ы между своими consumer'ами.
- В группе N consumers → до N partition'ов (по 1 на consumer).
- Если consumers > partition'ов → лишние простаивают.

```
Topic с 3 partitions, 2 consumers в группе:
  Consumer A → partition 0, 1
  Consumer B → partition 2
```

### Partitioning по ключу
```python
# Сообщения с одним key идут в одну партицию (порядок гарантирован)
producer.send('orders', key='user_123', value=order)
```

### Репликация
- Каждый partition имеет N реплик.
- **Leader** обрабатывает все записи/чтения.
- **Followers** синхронизируются (ISR — In-Sync Replicas).
- `replication.factor=3` для продакшена.
- `min.insync.replicas=2` + `acks=all` — гарантия durable.

### Semantics
| Semantics | Что |
|---|---|
| At-most-once | Может потеряться (acks=0) |
| At-least-once | Может дублироваться (по умолчанию) |
| Exactly-once | Идемпотентность (транзакции) |

---

## ⚙️ Важные параметры

### Producer
| Параметр | Что |
|---|---|
| `acks` | 0/1/all — гарантия записи |
| `retries` | Кол-во повторов |
| `batch.size` | Размер батча (байт) |
| `linger.ms` | Ждать N мс для батча |
| `compression.type` | none/gzip/snappy/lz4/zstd |
| `max.in.flight.requests.per.connection` | для ordered delivery = 1 |
| `enable.idempotence` | Идемпотентность (dedup) |

### Consumer
| Параметр | Что |
|---|---|
| `group.id` | ID группы |
| `auto.offset.reset` | earliest/latest/none (новая группа) |
| `enable.auto.commit` | Авто-коммит offset'ов |
| `auto.commit.interval.ms` | Частота авто-коммита |
| `max.poll.records` | Сколько за раз |
| `session.timeout.ms` | Считать мёртвым через N мс |
| `heartbeat.interval.ms` | Частота heartbeat'а |
| `fetch.min.bytes` | Минимум данных для возврата |

### Topic/Broker
| Параметр | Что |
|---|---|
| `retention.ms` | Сколько хранить сообщения |
| `retention.bytes` | Лимит по размеру |
| `cleanup.policy` | delete/compact |
| `compression.type` | Сжатие на уровне topic'а |
| `min.insync.replicas` | Минимум ISR для записи |
| `unclean.leader.election.enable` | Избрать не-ISR лидером (опасно) |
| `num.partitions` | Кол-во partition'ов по умолчанию |

### Log Compaction
```bash
# Хранить только последнее значение по key
cleanup.policy=compact

# Гуд для состояний (state): user_id → settings
```

---

## 🌍 Экосистема

| Компонент | Назначение |
|---|---|
| **Kafka Connect** | Коннекторы (источники/стоки) — без кода |
| **Kafka Streams** | Потоковая обработка (Java/Scala) |
| **Schema Registry** | Avro/Protobuf/JSON-схемы |
| **ksqlDB** | SQL поверх Kafka |
| **REST Proxy** | REST API для Kafka |
| **MirrorMaker 2** | Репликация между кластерами |

### Kafka Connect
```bash
# Пример: источник из БД → Kafka
curl -X PUT http://localhost:8083/connectors/postgres-source/config \
    -H "Content-Type: application/json" \
    -d '{
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "connection.url": "jdbc:postgresql://localhost:5432/db",
        "connection.user": "user",
        "connection.password": "pass",
        "table.whitelist": "users",
        "mode": "incrementing",
        "incrementing.column.name": "id",
        "topic.prefix": "postgres_"
    }'
```

### ksqlDB
```sql
CREATE STREAM clicks (user_id BIGINT, url VARCHAR)
    WITH (KAFKA_TOPIC='clicks', VALUE_FORMAT='JSON');

CREATE TABLE user_clicks AS
    SELECT user_id, COUNT(*) as clicks
    FROM clicks WINDOW TUMBLING (SIZE 5 MINUTES)
    GROUP BY user_id;
```

---

## 🐛 Дебаг и мониторинг

```bash
# Утилита для просмотра сообщений с фильтром
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic my-topic --from-beginning | grep "error"

# Получить последний offset
bin/kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list localhost:9092 --topic my-topic

# Лаг consumer group
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --describe --group my-group

# Dump segment
bin/kafka-dump-log.sh --files /var/lib/kafka/data/my-topic-0/00000000000000000000.log --print-data-log
```

### Метрики
- **JMX** через Prometheus JMX Exporter.
- **Burrow** — мониторинг consumer lag.
- **Kafka UI** (AKHQ, Kafka Drop, Conduktor) — веб-интерфейсы.
- **CMAK** (Cluster Manager for Kafka).

### Полезные вопросы для дебага
1. **Consumer lag растёт** — consumer не успевает, добавьте partition'ы / consumers.
2. **Сообщения пропадают** — `retention.ms` истёк или `cleanup.policy`.
3. **Дубли** — at-least-once, используйте идемпотентность.
4. **Порядок нарушен** — разные partition'ы (порядок только в одном).
5. **Producer не пишет** — проверьте `acks` и `bootstrap.servers`.

---

## 🌟 Kafka + Spark Streaming

```python
# PySpark Structured Streaming из Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .load()

# Парсинг
parsed = df.selectExpr("CAST(value AS STRING)")

query = parsed \
    .writeStream \
    .format("console") \
    .start()

query.awaitTermination()
```

---

## 🆚 Kafka vs RabbitMQ vs Redis Streams

| | Kafka | RabbitMQ | Redis Streams |
|---|---|---|---|
| Модель | Лог (offset) | Очередь (delete after read) | Лог |
| Хранение | Диск, долго | До подтверждения | RAM/диск |
| Replay | ✅ | ❌ | ✅ |
| Партиции | ✅ | exchanges/queues | ✅ |
| Пропускная | Миллионы/сек | Тысячи/сек | Высокая |
| Сложность | Высокая | Средняя | Низкая |
| Use case | Event streaming, log | Task queue, RPC | Простые стримы |

---

## 🪤 Частые ошибки

1. **1 partition, много consumers** — лишние простаивают.
2. **Нет ключа** — round-robin, порядок не гарантирован.
3. **`acks=0`** — данные могут потеряться.
4. **`auto.offset.reset=latest`** — новая группа пропустит старые.
5. **`enable.auto.commit=true`** — at-least-once может дублировать.
6. **Слишком много partition'ов** — overhead на broker.
7. **Слишком мало partition'ов** — узкое место для параллелизма.
8. **`replication.factor=1`** — нет отказоустойчивости.
9. **Long-running consumer** — `session.timeout.ms` прервёт.
10. **Schema Registry игнор** — нет совместимости схем.

---

## 🔗 Полезные ссылки

- Документация: https://kafka.apache.org/documentation
- Quickstart: https://kafka.apache.org/quickstart
- kafka-python: https://kafka-python.readthedocs.io
- confluent-kafka-python: https://github.com/confluentinc/confluent-kafka-python
- aiokafka: https://aiokafka.readthedocs.io
- Faust: https://faust.readthedocs.io
- Kafka UI (AKHQ): https://github.com/tchiotludo/akhq
- awesome-kafka: https://github.com/infoslack/awesome-kafka
- Kafka: The Definitive Guide (книга, O'Reilly)

---

## 💡 Полезные советы

1. **Partitioning по ключу** — для упорядоченности и локальности.
2. **`acks=all` + `min.insync.replicas=2`** — гарантия durable.
3. **Compression (lz4/zstd)** — экономит место и сеть.
4. **Batching** — `linger.ms=10` для пропускной способности.
5. **Consumer Group** — для параллельного чтения.
6. **Schema Registry** — для эволюционирующих схем.
7. **Idempotent producer** — `enable.idempotence=true`.
8. **Транзакции** — exactly-once (Kafka Streams).
9. **Kafka Connect** — без кода для интеграций.
10. **ksqlDB** — SQL для стриминга.
11. **MirrorMaker 2** — DR между кластерами.
12. **Burrow** — мониторинг consumer lag.
13. **AKHQ** — лучший UI (плюс admin/consume/produce).
14. **Логи хранятся долго** — `retention.ms`, не думайте как об очереди.
15. **Тесты** — через `kafka-console-consumer` с `--from-beginning`.

---

*Сгенерировано как шпаргалка. Kafka сложна —
углубляйтесь через https://kafka.apache.org/documentation и "Kafka: The Definitive Guide"*

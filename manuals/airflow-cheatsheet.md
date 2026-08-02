# 🌪️ Apache Airflow — шпаргалка

> **Apache Airflow** — платформа для оркестрации ETL/ELT пайплайнов.
> DAG'и (направленные графы) на Python, расписание, мониторинг.
> Документация: https://airflow.apache.org/docs

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **DAG** | Directed Acyclic Graph — пайплайн (граф задач без циклов) |
| **Task** | Задача в DAG (узел графа) |
| **Operator** | Шаблон для создания Task (BashOperator, PythonOperator) |
| **Task Instance** | Конкретный запуск Task в определённый run |
| **DAG Run** | Запуск всего DAG в конкретный момент |
| **Scheduler** | Демон, планирующий запуск DAG'ов |
| **Executor** | Как выполняются задачи (Local, Celery, Kubernetes) |
| **Worker** | Процесс, выполняющий задачи |
| **Webserver** | Веб-интерфейс |
| **Metadata DB** | PostgreSQL/MySQL — состояние |
| **XCom** | Cross-communication — обмен данными между задачами |
| **Connection** | Учётные данные для внешнего сервиса |
| **Variable** | Глобальная переменная в БД |

---

## 🚀 Запуск

### Через PyPI (локально)
```bash
# Установка
pip install "apache-airflow[celery,postgres]==2.9.0"
# или с constraints (рекомендуется)
pip install "apache-airflow==2.9.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.8.txt"

# Инициализация БД (SQLite для разработки)
airflow db migrate
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email admin@example.com \
    --password admin

# Запуск компонентов
airflow webserver --port 8080
airflow scheduler
# Web UI: http://localhost:8080
```

### Через Docker (официальный compose)
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up -d
# UI: http://localhost:8080 (airflow/airflow)
```

### Структура проекта
```
project/
├── dags/                    # ← DAG'и (Python-файлы)
│   ├── my_dag.py
│   └── ...
├── plugins/                 # кастомные операторы/хуки
├── logs/                    # логи задач
├── config/                  # конфиги
├── tests/                   # тесты DAG'ов
├── requirements.txt         # доп. Python-пакеты
└── docker-compose.yaml
```

---

## 📝 Структура DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

# Определение DAG
with DAG(
    dag_id="my_pipeline",
    description="My first pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",                    # расписание
    catchup=False,                        # не запускать пропущенные
    default_args={
        "owner": "data_team",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": False,
        "depends_on_past": False,
    },
    tags=["etl", "production"],
    max_active_runs=1,
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_function,
        op_kwargs={"source": "api"},
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="echo 'transforming' && python transform.py",
    )

    # Зависимости (направление графа)
    start >> extract >> transform >> end
    # или
    start >> [extract, parallel_task] >> end   # fan-out / fan-in
```

### Расписание (schedule)
```python
schedule="@daily"            # ежедневно
schedule="@hourly"
schedule="@weekly"
schedule="@monthly"
schedule="@yearly"
schedule=None                # только вручную
schedule="0 2 * * *"         # cron-выражение (каждый день в 2:00)
schedule="*/15 * * * *"      # каждые 15 минут
schedule=timedelta(days=1)   # timedelta
schedule="0 0 * * MON"       # cron с днём недели (quartz-like)
```

### cron vs timetable
- **Cron**: классические cron-выражения (`0 2 * * *`).
- **Timetable**: более гибкие, со временной зоной.

```python
from airflow.timetables.interval import CronDataIntervalTimetable

schedule=CronDataIntervalTimetable(
    "0 2 * * *",
    timezone="Europe/Moscow",
)
```

---

## 🎓 Операторы (Operators)

### BashOperator
```python
from airflow.operators.bash import BashOperator

task = BashOperator(
    task_id="run_script",
    bash_command="/opt/scripts/run.sh {{ params.date }}",
    params={"date": "2024-01-15"},
    cwd="/opt/scripts",
    env={"MY_VAR": "value"},     # доп. переменные окружения
)
```

### PythonOperator
```python
from airflow.operators.python import PythonOperator

def process_data(**context):
    ds = context["ds"]               # дата как YYYY-MM-DD
    ti = context["ti"]               # task instance
    # логика...

task = PythonOperator(
    task_id="process",
    python_callable=process_data,
    op_kwargs={"source": "api"},     # позиционные/именованные аргументы
    op_args=["positional"],
)
```

### EmptyOperator (бывший DummyOperator)
```python
from airflow.operators.empty import EmptyOperator

start = EmptyOperator(task_id="start")
end = EmptyOperator(task_id="end")
```

### EmailOperator
```python
from airflow.operators.email import EmailOperator

task = EmailOperator(
    task_id="send_email",
    to="admin@example.com",
    subject="Pipeline {{ ds }} done",
    html_content="Data processed successfully.",
    files=["/tmp/report.csv"],
)
```

### BranchPythonOperator (условное ветвление)
```python
from airflow.operators.python import BranchPythonOperator

def decide_branch(**context):
    if context["execution_date"].day == 1:
        return "monthly_task"
    return "daily_task"

branch = BranchPythonOperator(
    task_id="decide",
    python_callable=decide_branch,
)
```

### ShortCircuitOperator (полная остановка)
```python
from airflow.operators.python import ShortCircuitOperator

def is_weekend(**context):
    return context["execution_date"].weekday() >= 5   # False → DAG останавливается

skip_weekend = ShortCircuitOperator(
    task_id="skip_weekend",
    python_callable=is_weekend,
)
```

### SparkSubmitOperator
```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

spark_task = SparkSubmitOperator(
    task_id="spark_job",
    application="/opt/spark/jobs/my_job.py",
    conn_id="spark_default",
    conf={"spark.master": "spark://spark-master:7077"},
    application_args=["{{ ds }}"],
)
```

### Provider Operators
```python
# PostgreSQL
from airflow.providers.postgres.operators.postgres import PostgresOperator

sql_task = PostgresOperator(
    task_id="run_sql",
    postgres_conn_id="postgres_default",
    sql="SELECT * FROM users WHERE created_at >= '{{ ds }}'",
)

# S3
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator

# Docker
from airflow.providers.docker.operators.docker import DockerOperator

docker_task = DockerOperator(
    task_id="docker_pipeline",
    image="my-app:latest",
    api_version="auto",
    auto_remove=True,
    command="run.sh",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
)
```

### @dag и @task (TaskFlow API — современный стиль)
```python
from airflow.decorators import dag, task

@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["modern"],
)
def my_pipeline():

    @task
    def extract():
        return {"data": [1, 2, 3]}

    @task
    def transform(data):
        return [x * 2 for x in data["data"]]

    @task
    def load(data):
        print(f"Loaded: {data}")

    data = extract()
    transformed = transform(data)
    load(transformed)

my_pipeline()
```

> TaskFlow автоматически передаёт результаты между задачами через XCom!

---

## 🔗 Зависимости задач

```python
# Линейная
task1 >> task2 >> task3

# Fan-out
start >> [task1, task2, task3] >> end

# Сложные
[extract1, extract2] >> transform >> [load1, load2]

# Chain
task1 >> task2 >> task3
# эквивалентно
task1.set_downstream(task2)
task2.set_downstream(task3)

# Chain (несколько)
chain(task1, task2, task3)
chain([t1, t2], [t3, t4])    # cross-dependencies

# cross_downstream
from airflow.models.baseoperator import chain, cross_downstream
cross_downstream([start1, start2], [end1, end2])
```

---

## 📨 XCom (обмен данными)

XCom (Cross-Communication) — обмен маленькими данными между задачами.

```python
# Push (явный)
from airflow.operators.python import PythonOperator

def push_data(**context):
    context["ti"].xcom_push(key="my_key", value={"a": 1})

def pull_data(**context):
    val = context["ti"].xcom_pull(key="my_key", task_ids="push_task")
    print(val)     # {'a': 1}

# Push (неявный через return в TaskFlow / PythonOperator)
def push_implicit():
    return {"data": 1}     # автоматически пушится в XCom под key="return_value"

# Pull
val = ti.xcom_pull(task_ids="task1", key="return_value")

# Из другой DAG (внешний)
val = ti.xcom_pull(task_ids="external_dag.task1", dag_id="other_dag")
```

### Custom XCom backend
```python
# В airflow.cfg:
[core]
xcom_backend = my_package.CustomXComBackend
# По умолчанию XCom хранит в metadata DB.
# Для больших данных: S3, GCS, Custom backend.
```

> ⚠️ XCom не для больших данных! Используйте внешнее хранилище (S3, БД).

---

## 🔧 Hooks (подключения)

Hooks — обёртки над внешними API/сервисами.

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Использование в PythonOperator
def query_db(**context):
    hook = PostgresHook(postgres_conn_id="my_db")
    df = hook.get_pandas_df("SELECT * FROM users LIMIT 10")
    records = hook.get_records("SELECT count(*) FROM users")

# Напрямую соединение
hook = PostgresHook(postgres_conn_id="my_db")
conn = hook.get_conn()
cursor = conn.cursor()
cursor.execute("SELECT 1")
```

### Провайдеры (Providers)
```bash
pip install apache-airflow-providers-postgres
pip install apache-airflow-providers-amazon
pip install apache-airflow-providers-google
pip install apache-airflow-providers-apache-spark
pip install apache-airflow-providers-docker
```

---

## 🔌 Connections и Variables

### Connections (учётки для сервисов)
```bash
# Через CLI
airflow connections add my_postgres \
    --conn-uri "postgresql://user:pass@host:5432/db"

airflow connections add my_aws \
    --conn-type aws \
    --conn-login AKIA... \
    --conn-password secret

# Через UI: Admin → Connections
```

### Variables (глобальные переменные)
```bash
# CLI
airflow variables set my_var '{"key":"value"}'
airflow variables get my_var
airflow variables delete my_var
airflow variables list

# UI: Admin → Variables
```

```python
from airflow.models import Variable

# Чтение (кэшируется)
value = Variable.get("my_var")
value = Variable.get("my_var", default_var="fallback")

# Как JSON
config = Variable.get("config", deserialize_json=True)

# Запись
Variable.set("my_var", "new_value")
```

### Templates (Jinja2)
```python
# Доступные переменные в шаблонах
{{ ds }}                          # YYYY-MM-DD
{{ ds_nodash }}                   # YYYYMMDD
{{ ts }}                          # 2024-01-15T00:00:00+00:00
{{ ts_nodash }}
{{ dag_run.id }}
{{ run_id }}
{{ execution_date }}
{{ data_interval_start }}
{{ data_interval_end }}
{{ params.my_param }}
{{ var.value.my_variable }}       # Variable
{{ var.json.my_json_variable }}   # Variable as JSON
{{ conn.my_conn_id.host }}        # Connection

# В bash_command
bash_command="echo {{ ds }}"

# В SQL
sql="SELECT * FROM sales WHERE date = '{{ ds }}'"
```

---

## ⏰ Trigger Rules

Когда выполнять задачу (по умолчанию `all_success`).

```python
from airflow.utils.trigger_rule import TriggerRule

task = PythonOperator(
    task_id="cleanup",
    python_callable=cleanup,
    trigger_rule=TriggerRule.ALL_DONE,    # независимо от успеха/провала
)

# Варианты:
# ALL_SUCCESS         — все родители успешны (по умолчанию)
# ALL_FAILED          — все провалились
# ALL_DONE            — все завершены (успех или провал)
# ONE_SUCCESS         — хотя бы один успешен
# ONE_FAILED          — хотя бы один провалился
# NONE_FAILED         — ни один не провалился
# NONE_SKIPPED        — ни один не пропущен
```

---

## 📊 UI и мониторинг

Web UI: `http://localhost:8080`

### Главные разделы
- **DAGs** — список всех DAG'ов
- **Browse** → Task Instances, Job, Audit Logs
- **Admin** → Connections, Variables, Pools, Configuration
- **Browse** → XComs (просмотр XCom)

### Вкладки DAG'а
- **Tree View** — дерево запусков
- **Graph** — граф выполнения (визуально)
- **Calendar** — календарь запусков
- **Gantt** — диаграмма Ганта
- **Code** — исходный код DAG
- **Details** — детали DAG

### Статусы задач
- 🟩 success
- 🟥 failed
- 🟨 running
- ⬜ no status (planned)
- 🟪 upstream_failed
- 🔳 skipped (branch)

---

## 🛠️ CLI команды

```bash
# DAG'и
airflow dags list
airflow dags list-runs -d my_dag
airflow dags trigger my_dag                   # ручной запуск
airflow dags trigger my_dag -c '{"key":"val"}'   # с конфигом
airflow dags pause my_dag
airflow dags unpause my_dag
airflow dags delete my_dag
airflow dags show my_dag                      # граф в Graphviz
airflow dags test my_dag 2024-01-15           # тестовый прогон
airflow dags state my_dag 2024-01-15          # статус
airflow dags report

# Tasks
airflow tasks list my_dag
airflow tasks test my_dag extract 2024-01-15  # тест одной задачи
airflow tasks clear my_dag -s 2024-01-01 -e 2024-01-15   # очистить
airflow tasks run my_dag extract 2024-01-15
airflow tasks failed my_dag

# БД и миграции
airflow db migrate
airflow db reset
airflow db check
airflow db shell

# Пользователи
airflow users create
airflow users list
airflow users delete -e user@example.com
airflow users reset-password -u admin

# Connections / Variables
airflow connections list
airflow variables list

# Scheduler
airflow scheduler
airflow celery worker
airflow celery flower

# Info
airflow info
airflow version
airflow config list
airflow kerberos
```

---

## 🐛 Тестирование DAG'ов

### Тест в CLI
```bash
# Тестовый запуск DAG (без состояния)
airflow dags test my_dag 2024-01-15

# Тест одной задачи
airflow tasks test my_dag extract 2024-01-15

# С режимом (data interval)
airflow dags test my_dag 2024-01-01 2024-01-15
```

### Unit-тесты pytest
```python
import pytest
from airflow.models import DagBag

@pytest.fixture(scope="module")
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)

def test_dag_loaded(dagbag):
    assert "my_dag" in dagbag.dags
    assert dagbag.import_errors == {}

def test_dag_structure(dagbag):
    dag = dagbag.get_dag("my_dag")
    assert len(dag.tasks) == 4
    assert dag.schedule_interval == "@daily"

def test_task_dependencies(dagbag):
    dag = dagbag.get_dag("my_dag")
    extract = dag.get_task("extract")
    assert extract.downstream_task_ids == {"transform"}
```

---

## 📋 Best practices

### Структура DAG
1. **Идиоматичные ID**: `extract_users`, `transform_sales` (что делает, не что это).
2. **Атомарные задачи**: одна задача = одно логическое действие.
3. **Идемпотентность**: повторный запуск с теми же параметрами даёт тот же результат.
4. **Чистый граф**: не делайте слишком много задач в одном DAG (>50 — повод разделить).
5. **Top-level код**: код на верхнем уровне должен только определять DAG (без тяжёлых вычислений).

### Производительность
1. **Не делайте тяжёлые операции в top-level коде** — он выполняется при каждом heartbeat scheduler'а.
2. **Параллелизм**: настраивайте `parallelism`, `max_active_runs_per_dag`.
3. **Pools** — ограничивайте параллельные задачи ресурсоёмких типов.
4. **XCom** — не для больших данных (используйте S3/БД).
5. **Retries** — настраивайте разумно (1-3).
6. **timeout** — для каждой задачи.

### Безопасность
1. **Connections/Variables** — для секретов, не в коде.
2. **Secrets backend** — HashiCorp Vault, AWS Secrets Manager.
3. **Mask sensitive** — Airflow маскирует значения типа `password` в логах.
4. **RBAC** — роли и права пользователей.

---

## 🪤 Частые ошибки

1. **Тяжёлый top-level код** — Python-импорт должен быть лёгким.
2. **Динамические DAG'и** — генерация DAG'ов в цикле может создать тысячи файлов.
3. **XCom для больших данных** — забивает БД. Используйте S3/БД.
4. **`catchup=True`** — для старого `start_date` запустит тысячи пропущенных.
5. **`schedule` без timezone** — может запускаться в непредсказуемое время.
6. **`depends_on_past=True`** — заблокирует DAG при падении.
7. **Нет `retries`** — падение одной задачи = падение всего DAG.
8. **Hardcoded credentials** — используйте Connections.
9. **Сложные шаблоны Jinja** — тестируйте через `airflow tasks test`.
10. **`schedule_interval` устарел** — в 2.4+ просто `schedule`.

---

## 🔗 Полезные ссылки

- Официальная документация: https://airflow.apache.org/docs
- Tutorial: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html
- Best Practices: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
- Awesome Airflow: https://github.com/apache/airflow
- Astronomer (managed): https://www.astronomer.io
- Provider packages: https://airflow.apache.org/docs/apache-airflow-providers/index.html
- Executors: https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html
- DAG examples: https://github.com/apache/airflow/tree/main/tests/system

---

## 💡 Полезные советы

1. **TaskFlow API (`@dag`/`@task`)** — современный и лаконичный стиль.
2. **`catchup=False`** — для новых DAG'ов, чтобы не запускать прошлое.
3. **Connections/Variables** — для конфигов и секретов.
4. **`{{ ds }}`** — дата выполнения для параметризации.
5. **Pools** — ограничивают параллелизм ресурсоёмких задач.
6. **Sensors** — ждут внешнего условия (файл, S3-объект).
7. **`airflow dags test`** — для отладки локально без scheduler.
8. **DAG-factory** — для генерации DAG'ов из YAML.
9. **astronomer-cosmos** — для dbt + Airflow.
10. **`max_active_runs=1`** — для последовательных пайплайнов.
11. **Retries + retry_delay** — обязательно для прод-задач.
12. **Templates (Jinja2)** — мощная параметризация.
13. **CeleryExecutor + Redis/RabbitMQ** — для прод (распределённые workers).
14. **KubernetesExecutor** — для масштабируемости (dynamic workers).
15. **Мониторинг** — экспортер метрик в Prometheus/Grafana.

---

*Сгенерировано как шпаргалка. Airflow огромен —
углубляйтесь через https://airflow.apache.org/docs/ и tutorial*

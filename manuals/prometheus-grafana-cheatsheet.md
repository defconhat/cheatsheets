# 📊 Prometheus / Grafana — шпаргалка

> **Prometheus** — база данных временных рядов (time-series DB) + сбор метрик.
> **Grafana** — визуализация метрик из множества источников (dashboards).
> Документация: https://prometheus.io/docs · https://grafana.com/docs

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Metric** | Метрика (число во времени) |
| **Time series** | Ряд значений (timestamp + value + labels) |
| **Label** | Метка метрики (`method="GET"`, `status="200"`) |
| **Target** | Источник метрик (host:port) |
| **Exporter** | Программа, отдающая метрики (node_exporter, mysql_exporter) |
| **Scrape** | Опрос таргетов Prometheus'ом (pull-модель) |
| **Alertmanager** | Компонент для алертов (email, Slack,PagerDuty) |
| **Recording Rule** | Предвычисленная метрика |
| **Alerting Rule** | Правило для срабатывания алерта |
| **Pushgateway** | Для push-метрик (cron jobs) |
| **PromQL** | Язык запросов Prometheus |

### Типы метрик
| Тип | Что | Пример |
|---|---|---|
| **Counter** | Только растёт | `http_requests_total` |
| **Gauge** | Любое значение (вверх/вниз) | `temperature`, `memory_usage` |
| **Histogram** | Распределение (бакеты) | `request_duration_seconds` |
| **Summary** | Квантили | `request_duration_seconds{quantile="0.95"}` |

---

## 🚀 Запуск (Docker Compose)

```yaml
version: "3.9"
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "127.0.0.1:9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'    # для reload через API

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "127.0.0.1:9100:9100"

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "127.0.0.1:9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro

volumes:
  prometheus_data:
  grafana_data:
```

### Минимальный `prometheus.yml`
```yaml
global:
  scrape_interval: 15s          # как часто опрашивать
  evaluation_interval: 15s      # как часто выполнять rules

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'docker'
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
```

---

## 🎯 Targets и Service Discovery

### Static (статические)
```yaml
scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['app1:8080', 'app2:8080']
        labels:
          env: 'prod'
          region: 'us-east'
```

### File-based
```yaml
scrape_configs:
  - job_name: 'myapp'
    file_sd_configs:
      - files: ['/etc/prometheus/targets/*.yml']
        refresh_interval: 30s
```
`targets/app.yml`:
```yaml
- targets: ['app1:8080']
  labels:
    env: prod
- targets: ['app2:8080']
```

### Service Discovery (динамические)
```yaml
scrape_configs:
  # Consul
  - job_name: 'consul'
    consul_sd_configs:
      - server: 'consul:8500'

  # Kubernetes
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod

  # Docker
  - job_name: 'docker'
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: [__meta_docker_container_name]
        regex: '/(.*)'
        target_label: container

  # AWS EC2
  - job_name: 'ec2'
    ec2_sd_configs:
      - region: us-east-1
        access_key: XXX
        secret_key: YYY
```

### Аннотации K8s (для автообнаружения)
```yaml
# Pod с метриками
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

---

## 📜 PromQL — язык запросов

### Базовые
```promql
# Текущее значение метрики
http_requests_total

# С лейблом
http_requests_total{method="GET"}
http_requests_total{method="GET", status="200"}
http_requests_total{status=~"5.."}        # regex: 500-599
http_requests_total{status!~"4..|5.."}    # НЕ 4xx/5xx

# Несколько значений
up                                      # 1 если таргет жив
up == 0                                 # упавшие таргеты
```

### Фильтры и агрегации
```promql
# Filter
node_cpu_seconds_total{mode="idle"}

# Aggregation
sum(http_requests_total)               # сумма всех лейблов
sum by (method) (http_requests_total)  # группировка
sum by (method, status) (http_requests_total)
avg by (instance) (rate(http_requests_total[5m]))
count by (job) (up)
topk(5, http_requests_total)           # топ-5
bottomk(5, ...)
quantile(0.95, ...)                    # 95-й перцентиль
```

### Rate / Increase (для Counter)
```promql
# Скорость (запросов в секунду за последние 5 минут)
rate(http_requests_total[5m])

# Увеличение за час
increase(http_requests_total[1h])

# Средняя скорость за 10 минут
avg_over_time(memory_usage[10m])
min_over_time(...)
max_over_time(...)

# Instant rate (последние 2 семпла)
irate(http_requests_total[1m])
```

### Арифметика
```promql
# CPU utilization (%)
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# Сложение/вычитание метрик
sum(metric_a) + sum(metric_b)

# Bytes → MB / GB
memory_bytes / 1024 / 1024
```

### Histogram (перцентили)
```promql
# 95-й перцентиль длительности запроса за 5 минут
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# По лейблу
histogram_quantile(0.99, sum by (le, method) (rate(...[5m])))
```

### Временные окна
```promql
[5m]      # 5 минут
[1h]      # 1 час
[7d]      # 7 дней
rate(metric[5m])
avg_over_time(metric[1h])
```

### offset (сдвиг по времени)
```promql
# То же, но неделю назад
metric offset 7d

# Сравнение с прошлой неделей
rate(http_requests_total[1h]) / rate(http_requests_total[1h] offset 7d)
```

### Подзапросы
```promql
# Максимум из 5-минутных rate за последний час
max_over_time(rate(http_requests_total[5m])[1h:1m])
```

---

## 🛠️ Частые запросы

```promql
# Все упавшие таргеты
up == 0

# CPU busy % (по инстансам)
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance))

# Memory used %
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

# Disk usage %
100 * (1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})

# Network RX bytes
rate(node_network_receive_bytes_total[5m])

# HTTP error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Top instances by request rate
topk(5, sum by (instance) (rate(http_requests_total[5m])))

# p99 latency
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

---

## 📋 Rules (recording & alerting)

### Recording rules (кэш сложных запросов)
```yaml
# rules/recording.yml
groups:
  - name: example
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job)(rate(http_requests_total[5m]))

      - record: job:http_request_duration_seconds:p99
        expr: histogram_quantile(0.99, sum by (le, job)(rate(http_request_duration_seconds_bucket[5m])))
```

### Alerting rules
```yaml
# rules/alerts.yml
groups:
  - name: alerts
    rules:
      - alert: HighRequestLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 10m                       # ждать 10 минут
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.instance }}"
          description: "p99 latency is {{ $value }}s"

      - alert: ServiceDown
        expr: up == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} down"

      - alert: HighCPU
        expr: 100 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100 > 80
        for: 5m
        labels:
          severity: warning

      - alert: DiskFull
        expr: 100 - 100 * node_filesystem_avail_bytes / node_filesystem_size_bytes > 90
        for: 10m
        labels:
          severity: critical
```

---

## 🔔 Alertmanager

### `alertmanager.yml`
```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/...'

route:
  receiver: 'default'
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers:
        - severity="critical"
      receiver: 'pagerduty'
    - matchers:
        - severity="warning"
      receiver: 'slack'

receivers:
  - name: 'default'
    email_configs:
      - to: 'ops@example.com'
        from: 'alertmanager@example.com'
        smarthost: 'smtp.example.com:587'

  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true
        title: '[{{ .Status }}] {{ .CommonLabels.alertname }}'
        text: '{{ .CommonAnnotations.summary }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_KEY'

inhibit_rules:
  - source_matchers: [severity="critical"]
    target_matchers: [severity="warning"]
    equal: ['instance']
```

---

## 📈 Grafana

### Подключение Prometheus
1. **Configuration → Data Sources → Add data source**
2. Выбрать **Prometheus**
3. URL: `http://prometheus:9090`
4. Save & Test

### Полезные datasource'ы
| Источник | Назначение |
|---|---|
| Prometheus | Метрики |
| Loki | Логи |
| Tempo / Jaeger | Tracing |
| InfluxDB | Time-series |
| PostgreSQL / MySQL | SQL |
| Elasticsearch | Логи/документы |
| CloudWatch | AWS |
| Zabbix | Мониторинг |

### Создание dashboard
- **New Dashboard → Add panel**
- Запрос: PromQL
- Визуализация: Time series, Stat, Gauge, Bar gauge, Table, Heatmap, Geomap.
- Variables: `${variable}` для интерактивных фильтров.

### Variables (для фильтрации)
```promql
# Query variable
label_values(up, job)

# Использование в панелях
rate(http_requests_total{job="$job"}[5m])
```

### Templates: переменные
```
$server                # выбранное значение
$server:regex          # для regex
[[server]]             # в тексте/title
$__interval            # текущий интервал (для rate)
$__rate_interval       # оптимальный интервал для rate
```

### Dashboard JSON
- Export/Import через JSON (share dashboards).
-社区: https://grafana.com/grafana/dashboards.

### ID популярных dashboards
| ID | Что |
|---|---|
| **1860** | Node Exporter Full |
| **193** | Docker monitor |
| **3662** | Prometheus 2.0 |
| **9628** | cAdvisor |
| **1516** | Redis |
| **7362** | PostgreSQL |
| **11074** | Nginx |

---

## 🐍 Экспорт метрик из Python

### prometheus_client (простой)
```python
from prometheus_client import Counter, Gauge, Histogram, start_server

# Определить метрики
REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'status'])
IN_PROGRESS = Gauge('http_requests_in_progress', 'Requests in progress')
LATENCY = Histogram('http_request_duration_seconds', 'Request latency', buckets=(0.1, 0.5, 1, 5))

# Использовать
REQUESTS.labels(method='GET', status='200').inc()
IN_PROGRESS.inc()
with LATENCY.time():
    do_work()
IN_PROGRESS.dec()

# Запустить сервер метрик на :8000
start_server(addr='0.0.0.0', port=8000)
```

### FastAPI + Prometheus
```python
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

### Flask + Prometheus
```python
from prometheus_client import generate_latest
from flask import Flask, Response

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

---

## 🛠️ CLI и API

### Promtool
```bash
promtool check config prometheus.yml      # проверить конфиг
promtool check rules rules.yml            # проверить rules
promtool query instant http://prom:9090 'up'   # запрос
promtool tsdb create block ...            # управление TSDB
```

### HTTP API
```bash
# Запрос
curl -s 'http://localhost:9090/api/v1/query?query=up' | jq

# Range запрос
curl -G 'http://localhost:9090/api/v1/query_range' \
    --data-urlencode 'query=rate(http_requests_total[5m])' \
    --data-urlencode 'start=2024-01-01T00:00:00Z' \
    --data-urlencode 'end=2024-01-01T01:00:00Z' \
    --data-urlencode 'step=15s' | jq

# Targets
curl -s http://localhost:9090/api/v1/targets | jq

# Alerts
curl -s http://localhost:9090/api/v1/alerts | jq

# Reload конфигурации
curl -X POST http://localhost:9090/-/reload
```

### Management API
```bash
curl -X POST http://localhost:9090/-/reload      # reload
curl -X POST http://localhost:9090/-/quit        # выйти
curl http://localhost:9090/-/healthy             # healthcheck
curl http://localhost:9090/-/ready               # readiness
```

---

## 📦 Экспортёры (полезные)

| Exporter | Что собирает |
|---|---|
| **node_exporter** | CPU, RAM, disk, network (Linux) |
| **windows_exporter** | Для Windows |
| **mysqld_exporter** | MySQL |
| **postgres_exporter** | PostgreSQL |
| **redis_exporter** | Redis |
| **nginx_exporter** | nginx |
| **blackbox_exporter** | HTTP/TCP/ICMP пробы |
| **cadvisor** | Docker-контейнеры |
| **kafka_exporter** | Kafka |
| **mongodb_exporter** | MongoDB |
| **elasticsearch_exporter** | ES |
| **jmx_exporter** | Java/JMX |
| **snmp_exporter** | Сетевое оборудование |
| **pushgateway** | Push-метрики (для cron) |

### Pushgateway (для коротких задач)
```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g = Gauge('job_last_success_seconds', 'Last job success', registry=registry)
g.set_to_current_time()
push_to_gateway('pushgateway:9091', job='my_batch', registry=registry)
```

---

## 🪤 Частые ошибки

1. **Counter без `rate`** — значение всегда растёт, смотрят скорость.
2. **`rate()` на gauge** — для gauge используйте `avg_over_time` и т.п.
3. **Слишком короткие `[5s]` окна** — шумно.
4. **Слишком длинные `[7d]`** — дорого вычислять.
5. **Большой cardinality** — много уникальных label'ов убивает производительность.
6. **Не настроен retention** — диск забьётся.
7. **Alerts без `for`** — срабатывают на «мгновенные» скачки.
8. **Нет inhibit_rules** — спам дублирующих алертов.
9. **Pushgateway для долгоживущих** — только для batch jobs.
10. **Сбор в `0.0.0.0`** — Prometheus стучится к таргету, не наоборот.

---

## 🔗 Полезные ссылки

- Prometheus: https://prometheus.io/docs
- PromQL: https://prometheus.io/docs/prometheus/latest/querying/basics
- Grafana: https://grafana.com/docs
- Dashboards: https://grafana.com/grafana/dashboards
- Awesome Prometheus: https://github.com/roaldnefs/awesome-prometheus
- prometheus-client (Python): https://github.com/prometheus/client_python
- Robust Perception blog: https://www.robustperception.io/blog

---

## 💡 Полезные советы

1. **Counter + `rate()`** — основной паттерн для событий.
2. **Histogram + `histogram_quantile`** — для перцентилей.
3. **Recording rules** — для сложных запросов, что часто используются.
4. **Service Discovery** — для динамических сред (K8s, EC2).
5. **Variables в Grafana** — для интерактивных дашбордов.
6. **Alerts с `for:`** — ждать, чтобы не ловить короткие скачки.
7. **`up == 0`** — главный health-check таргета.
8. **Loki + Grafana** — логи рядом с метриками.
9. **Alert routing** — критичное в PagerDuty, остальное в Slack.
10. **Retention** — настраивайте `--storage.tsdb.retention.time`.
11. **Federation** — для масштабирования (один P читает из других).
12. **Thanos / Cortex / Mimir** — для долгого хранения и HA.
13. **`$__rate_interval`** в Grafana — автоматический выбор окна.
14. **Dashboard JSON** — храните в Git.
15. **Базовые дашборды** — Node Exporter (1860), cAdvisor (193).

---

*Сгенерировано как шпаргалка. Prometheus + Grafana — стандарт мониторинга —
углубляйтесь через https://prometheus.io/docs и https://grafana.com/docs*

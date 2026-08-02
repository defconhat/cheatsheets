# 🦊 GitLab CI / GitHub Actions — шпаргалка по CI/CD

> **GitLab CI/CD** — встроенный CI/CD в GitLab (файл `.gitlab-ci.yml`).
> **GitHub Actions** — CI/CD для GitHub (`.github/workflows/*.yml`).
> Документация: https://docs.gitlab.com/ee/ci · https://docs.github.com/actions

---

# 🦊 ЧАСТЬ 1. GitLab CI/CD

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Pipeline** | Конвейер (набор jobs) |
| **Stage** | Этап (build → test → deploy) |
| **Job** | Одна задача (внутри stage) |
| **Runner** | Машина, выполняющая job'ы |
| **Executor** | Тип runner'а (docker, shell, k8s) |
| **Artifact** | Файлы между jobs (передаются) |
| **Cache** | Кэш между pipeline'ами |
| **Variable** | Переменная окружения |
| **Environment** | Среда развертывания (dev/prod) |
| **Manual** | Ручной запуск job'а |

---

## 📝 Структура `.gitlab-ci.yml`

```yaml
# Глобальные настройки
image: python:3.12-slim

stages:
  - build
  - test
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

# ── Job: сборка ────────────────────────────────────
build:
  stage: build
  script:
    - python setup.py build
  artifacts:
    paths:
      - build/
    expire_in: 1 week

# ── Job: тесты ─────────────────────────────────────
test:unit:
  stage: test
  script:
    - pytest tests/unit -v --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

test:lint:
  stage: test
  script:
    - ruff check .
    - mypy src/

# ── Job: деплой (только main) ──────────────────────
deploy:prod:
  stage: deploy
  image: alpine:latest
  before_script: []      # переопределить глобальный
  script:
    - echo "Deploying..."
  only:
    - main
  environment:
    name: production
    url: https://app.example.com
```

---

## ⚙️ Ключевые слова GitLab CI

### Структура pipeline
| Ключевое слово | Что |
|---|---|
| `stages` | Список этапов (по порядку) |
| `stage` | К какому этапу относится job |
| `default` | Настройки для всех jobs |
| `include` | Включить другой YAML |
| `workflow` | Правила запуска pipeline |

### Job
| Ключевое слово | Что |
|---|---|
| `script` | Команды для выполнения |
| `before_script` | Перед script |
| `after_script` | После script |
| `image` | Docker-образ |
| `services` | Доп. контейнеры (БД и т.д.) |
| `variables` | Переменные |
| `cache` | Кэш |
| `artifacts` | Артефакты |
| `needs` | Запускать не дожидаясь stage |
| `dependencies` | Какие артефакты забрать |
| `only` / `except` | Когда запускать |
| `rules` | Современная замена only/except |
| `tags` | Выбор runner'а |
| `when` | on_success/on_failure/manual/always/delayed |
| `allow_failure` | true = не падает pipeline |
| `environment` | Среда (deploy) |
| `coverage` | Регэксп для извлечения покрытия |
| `retry` | Кол-во повторов |
| `timeout` | Таймаут |
| `parallel` | N параллельных копий |
| `extends` | Наследовать шаблон |
| `trigger` | Запустить другой pipeline |
| `resource_group` | Сериализация |
| `inherit` | Что наследовать от глобального |

---

## 🌍 Условия запуска (rules)

```yaml
# Современный способ
deploy:
  stage: deploy
  script: ./deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: on_success
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: manual
    - if: '$CI_COMMIT_TAG'
      variables:
        ENV: "release"
    - when: never

# Старый синтаксис (only/except)
deploy:
  only:
    - main
    - tags
  except:
    - branches
```

### Переменные условий
| Переменная | Что |
|---|---|
| `$CI_COMMIT_BRANCH` | Имя ветки |
| `$CI_COMMIT_TAG` | Тег |
| `$CI_PIPELINE_SOURCE` | Источник (push, merge_request, schedule) |
| `$CI_MERGE_REQUEST_ID` | ID MR |
| `$CI_PROJECT_PATH` | group/project |
| `$CI_COMMIT_SHA` | Хэш коммита |

---

## 📦 Artifacts и Cache

### Artifacts (между jobs)
```yaml
build:
  script: make build
  artifacts:
    paths:
      - build/
      - dist/
    exclude:
      - binaries/**/*.tmp
    expire_in: 1 week            # удалить через неделю
    reports:
      junit: test-results.xml    # тест-репорты в UI
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    name: "$CI_COMMIT_REF_NAME"  # имя архива
    untracked: false
    when: on_failure             # сохранить даже при провале
```

### Cache (между pipeline'ами)
```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}     # разный кэш для каждой ветки
  paths:
    - .cache/pip
    - node_modules/
  policy: pull-push              # pull/push/pull-push

# Несколько кэшей
cache:
  - key: files-v1
    paths: [node_modules/]
  - key: files-v2
    paths: [.cache/]
```

---

## 🔌 Сервисы (БД и др.)

```yaml
test:integration:
  services:
    - name: postgres:16
      alias: db
      variables:
        POSTGRES_DB: testdb
        POSTGRES_USER: test
        POSTGRES_PASSWORD: secret
    - name: redis:7-alpine
      alias: cache
  variables:
    DATABASE_URL: postgres://test:secret@db:5432/testdb
  script:
    - pytest tests/integration
```

---

## 📜 includes и шаблоны

```yaml
# Включить из другого файла
include:
  - local: /templates/build.yml
  - project: 'mygroup/myproject'
    ref: main
    file: /templates/.gitlab-ci.yml
  - template: Jobs/Build.gitlab-ci.yml
  - remote: https://example.com/ci.yml

# Шаблон (hidden job)
.build_template:
  image: node:20
  before_script:
    - npm ci
  script:
    - npm run build

build:web:
  extends: .build_template
  variables:
    TARGET: web
```

---

## 🛠️ Runner

### Регистрация своего runner'а
```bash
sudo gitlab-runner register
# URL: https://gitlab.com/
# Token: из Settings → CI/CD → Runners
# Tags: linux, docker
# Executor: docker
```

### Управление
```bash
gitlab-runner status
gitlab-runner start
gitlab-runner stop
gitlab-runner restart
gitlab-runner verify
gitlab-runner list
gitlab-runner run
```

---

# 🐙 ЧАСТЬ 2. GitHub Actions

## 📝 Структура workflow

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:           # ручной запуск
  schedule:
    - cron: "0 2 * * *"        # каждый день в 2:00

permissions:
  contents: read

env:
  PYTHON_VERSION: "3.12"

jobs:
  test:
    runs-on: ubuntu-latest      # ubuntu-latest/windows/macos
    timeout-minutes: 30
    strategy:
      matrix:
        python: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: Install
        run: pip install -r requirements.txt

      - name: Test
        run: pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        if: always()
        with:
          file: ./coverage.xml

  build:
    needs: test                 # дождаться test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker
        run: docker build -t myapp .
      - name: Login to registry
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_TOKEN }}
      - name: Push
        run: docker push myapp:latest

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

---

## 🔑 Ключевые слова GitHub Actions

### Workflow
| Ключ | Что |
|---|---|
| `name` | Имя workflow |
| `on` | Триггеры |
| `env` | Глобальные переменные |
| `jobs` | Задачи |
| `permissions` | Права GITHUB_TOKEN |
| `concurrency` | Сериализация (отменять старые) |

### Job
| Ключ | Что |
|---|---|
| `runs-on` | Машина (ubuntu-latest и т.д.) |
| `steps` | Шаги |
| `needs` | Зависимости |
| `if` | Условие запуска |
| `env` | Переменные job |
| `strategy` | Матрица / параллелизм |
| `timeout-minutes` | Таймаут |
| `environment` | Среда |
| `continue-on-error` | Не падать с ошибкой |
| `services` | Контейнеры (БД) |
| `defaults` | Настройки для всех steps |

### Step
| Ключ | Что |
|---|---|
| `uses` | Использовать action |
| `with` | Параметры для action |
| `run` | Выполнить команды shell |
| `name` | Имя шага |
| `if` | Условие |
| `env` | Переменные |
| `working-directory` | Каталог |

---

## 🚀 Триггеры (on)

```yaml
on:
  push:
    branches: [main]
    paths: ['src/**', 'tests/**']     # только при изменениях в src/tests
    tags: ['v*']
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:                  # ручной
    inputs:
      env:
        description: 'Environment'
        default: 'staging'
  schedule:
    - cron: "0 2 * * *"
  release:
    types: [published]
  workflow_run:
    workflows: ["Build"]
    types: [completed]
```

---

## 📦 Secrets и Variables

### Secrets (зашифрованные)
```yaml
steps:
  - name: Login
    run: docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_TOKEN }}
```

### Variables (открытые)
```yaml
env:
  IMAGE_NAME: myapp
```

Через UI: Settings → Secrets and variables → Actions.

### Передача между jobs
```yaml
jobs:
  job1:
    outputs:
      version: ${{ steps.set.outputs.version }}
    steps:
      - id: set
        run: echo "version=1.0" >> $GITHUB_OUTPUT

  job2:
    needs: job1
    steps:
      - run: echo ${{ needs.job1.outputs.version }}
```

---

## 🎨 Контекстные выражения

```yaml
${{ github.event_name }}
${{ github.ref }}                    # refs/heads/main
${{ github.sha }}                    # commit SHA
${{ github.actor }}                  # кто запустил
${{ env.VAR }}
${{ secrets.SECRET }}
${{ vars.VARIABLE }}                 # из Variables (не секрет)
${{ job.status }}                    # success/failure
${{ steps.step1.outputs.value }}
${{ runner.os }}                     # Linux/macOS/Windows

# Условия
if: github.ref == 'refs/heads/main'
if: github.event_name == 'pull_request'
if: success()                        # все предыдущие успешны
if: always()                         # всегда (даже при провале)
if: failure()                        # хотя бы один провалился
if: cancelled()
```

---

## 🔌 Полезные Actions

| Action | Что |
|---|---|
| `actions/checkout@v4` | Клонировать репозиторий |
| `actions/setup-python@v5` | Установить Python |
| `actions/setup-node@v4` | Установить Node |
| `actions/cache@v4` | Кэшировать файлы |
| `actions/upload-artifact@v4` | Загрузить артефакт |
| `actions/download-artifact@v4` | Скачать артефакт |
| `actions/create-release@v1` | Создать GitHub Release |
| `docker/build-push-action@v5` | Собрать и запушить образ |
| `docker/login-action@v3` | Логин в registry |
| `codecov/codecov-action@v4` | Загрузить покрытие |
| `softprops/action-gh-release@v2` | Releases с файлами |

---

## 🌍 Self-hosted runners

```bash
# Settings → Actions → Runners → New self-hosted runner
# Следуйте инструкции:
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L https://...
tar xzf actions-runner-linux-x64.tar.gz
./config.sh --url https://github.com/owner/repo --token TOKEN
./run.sh
sudo ./svc.sh install
sudo ./svc.sh start
```

В workflow:
```yaml
runs-on: self-hosted
# или с лейблами
runs-on: [self-hosted, linux, x64]
```

---

## 🆚 GitLab CI vs GitHub Actions

| | GitLab CI | GitHub Actions |
|---|---|---|
| Файл | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| Конвейер | Pipeline | Workflow |
| Задача | Job | Job |
| Шаги | `script` (многострочный) | `steps` (массив) |
| Условие | `rules` / `only` | `if` |
| Runner | Свой / shared | GitHub-hosted / self-hosted |
| Маркетплейс | Templates | Actions Marketplace |
| Docker | `image:` | `container:` |
| Secrets | Settings → CI/CD | Settings → Secrets |
| Built-in | Docker-in-Docker | docker уже работает |

### Пример: тот же pipeline

**GitLab CI:**
```yaml
build:
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths: [dist/]
```

**GitHub Actions:**
```yaml
build:
  runs-on: ubuntu-latest
  container: node:20
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run build
    - uses: actions/upload-artifact@v4
      with:
        path: dist/
```

---

## 🪤 Частые ошибки

1. **Secrets в логах** — случайно вывели. GitLab/GitHub маскируют, но осторожно.
2. **Долгий pipeline** — параллельте через `needs` и матрицы.
3. **Кэш не работает** — ключи (key) неправильные.
4. **Артефакты удаляются** — `expire_in` / retention policy.
5. **Тесты flaky** — `retry` или изоляция.
6. **Runner offline** — self-hosted упал, проверьте сервис.
7. **`only/except` устарели** — используйте `rules` (GitLab).
8. **`needs` без зависимостей** — могут идти в любом порядке.
9. **`if: always()` без нужды** — выполняется даже при отмене.
10. **`permissions: write-all`** — слишком широкие права токена.

---

## 🔗 Полезные ссылки

### GitLab CI
- Документация: https://docs.gitlab.com/ee/ci
- YAML reference: https://docs.gitlab.com/ee/ci/yaml
- Pipeline editor: в GitLab UI
- Predefined variables: https://docs.gitlab.com/ee/ci/variables/predefined_variables.html

### GitHub Actions
- Документация: https://docs.github.com/actions
- Marketplace: https://github.com/marketplace/actions
- Workflow syntax: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
- Contexts: https://docs.github.com/actions/learn-github-actions/contexts
- Awesome Actions: https://github.com/sdras/awesome-actions

---

## 💡 Полезные советы

1. **Минимальный pipeline** — build + test + deploy.
2. **Матрицы** — тестировать на нескольких версиях (Python, Node, OS).
3. **Кэширование** — зависимости, экономит минуты.
4. **`needs`** — параллельное выполнение (не ждите всю стадию).
5. **Secrets** — для чувствительных данных.
6. **Reusability** — templates (GitLab) / composite actions (GitHub).
7. **Manual gates** — `when: manual` / `environment` для продакшена.
8. **Docker layer caching** — для быстрых сборок.
9. **Coverage репорты** — отображаются в MR/PR.
10. **Self-hosted runner** — для приватных задач или своих инструментов.
11. **`workflow_dispatch` / ручные job'ы** — для запуска по требованию.
12. **Concurrency** — отменять старые запуски при пуше в PR.
13. **Деплой только на main/tag** — через `if`/`rules`.
14. **Fail fast** — ранние проверки (lint) перед долгими (tests).
15. **Мониторинг** — уведомления в Slack/Discord через webhooks.

---

*Сгенерировано как шпаргалка. CI/CD — отдельный мир —
углубляйтесь через docs.gitlab.com/ee/ci и docs.github.com/actions*

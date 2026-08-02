# 🐳 Docker & docker-compose — шпаргалка

> **Docker** — контейнеризация приложений. Изолированная среда с приложением и зависимостями.
> Документация: https://docs.docker.com · Compose: https://docs.docker.com/compose

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Image (образ)** | Шаблон только для чтения (с приложением и зависимостями) |
| **Container (контейнер)** | Запущенный экземпляр образа |
| **Dockerfile** | Инструкция по сборке образа |
| **Volume (том)** | Постоянное хранилище данных (переживает контейнер) |
| **Bind mount** | Монтирование каталога хоста в контейнер |
| **Network** | Виртуальная сеть для связи контейнеров |
| **Registry** | Хранилище образов (Docker Hub, GitLab, private) |
| **Tag** | Версия образа (`nginx:1.25`, `node:20-alpine`) |
| **Compose** | Описание multi-container приложения в YAML |

---

## 🚀 Базовый цикл

```bash
# Образы
docker pull nginx                    # скачать
docker images                        # список локальных
docker rmi nginx                     # удалить образ
docker image prune -a                # удалить все неиспользуемые
docker tag nginx:latest myrepo/nginx:v1   # тегировать

# Контейнеры (старый синтаксис)
docker run nginx                     # запустить (foreground)
docker run -d nginx                  # в фоне (detached)
docker run --name web nginx          # с именем
docker run -p 8080:80 nginx          # проброс порта хост:контейнер
docker run -p 127.0.0.1:8080:80 nginx   # ⚠️ ТОЛЬКО localhost!
docker run -v $(pwd):/app nginx      # монтирование каталога
docker run -e KEY=value nginx        # переменная окружения
docker run -it ubuntu bash           # интерактивно + TTY
docker run --rm ubuntu echo hi       # удалить после завершения

# Списки
docker ps                            # запущенные
docker ps -a                         # все (включая остановленные)
docker container ls -a               # новый синтаксис

# Управление контейнером
docker start <name>                  # запустить остановленный
docker stop <name>                   # остановить (SIGTERM, потом SIGKILL)
docker restart <name>
docker kill <name>                   # SIGKILL немедленно
docker rm <name>                     # удалить
docker rm -f <name>                  # принудительно (если запущен)

# Внутри контейнера
docker exec -it <name> bash          # войти в запущенный контейнер
docker exec <name> ls /app           # выполнить команду
docker logs <name>                   # логи
docker logs -f <name>                # следить (tail -f)
docker logs --tail 50 <name>         # последние 50
docker logs -t <name>                # с timestamp
docker top <name>                    # процессы в контейнере
docker stats                         # статистика ресурсов (top)
docker inspect <name>                # подробная информация (JSON)
docker cp file <name>:/path          # копировать в контейнер
docker cp <name>:/path/file .        # из контейнера
```

### ⚠️ Безопасность портов (важно!)
```bash
docker run -p 8080:80 nginx          # ❌ торчит на 0.0.0.0 (весь LAN!)
docker run -p 127.0.0.1:8080:80 nginx   # ✅ только localhost
```
В `docker-compose.yml`:
```yaml
ports:
  - "8080:80"               # ❌ 0.0.0.0:8080 (открыт в сеть)
  - "127.0.0.1:8080:80"     # ✅ только localhost
```

---

## 📝 Dockerfile

```dockerfile
# Базовый образ
FROM python:3.12-slim

# Метаданные
LABEL maintainer="you@example.com"
LABEL version="1.0"

# Рабочая директория
WORKDIR /app

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Установка системных зависимостей (сначала — для кэша слоёв)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование только зависимостей (кэш слоёв!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Создать непривилегированного пользователя
RUN useradd -m appuser
USER appuser

# Открыть порт (документация, не открывает на самом деле)
EXPOSE 8000

# Проверка здоровья
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Запуск
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver"]
```

### Команды Dockerfile
| Команда | Назначение |
|---|---|
| `FROM` | Базовый образ |
| `RUN` | Выполнить команду при сборке |
| `COPY` | Копировать файлы с хоста |
| `ADD` | Как COPY + URL + авто-распаковка (избегайте!) |
| `WORKDIR` | Рабочий каталог |
| `ENV` | Переменная окружения |
| `ARG` | Переменная только на время сборки |
| `EXPOSE` | Документация порта |
| `VOLUME` | Объявить точку монтирования |
| `USER` | От какого пользователя выполнять |
| `CMD` | Команда по умолчанию (можно переопределить) |
| `ENTRYPOINT` | Исполняемый файл (фиксированный) |
| `HEALTHCHECK` | Проверка здоровья |
| `LABEL` | Метаданные |
| `STOPSIGNAL` | Сигнал остановки |
| `SHELL` | Оболочка по умолчанию |
| `ONBUILD` | Инструкция для образов-наследников |

### Сборка образа
```bash
docker build -t myapp:1.0 .               # из текущего каталога
docker build -t myapp -f Dockerfile.prod . # другой Dockerfile
docker build --no-cache -t myapp .         # без кэша
docker build --build-arg VERSION=1.0 .     # передать ARG
docker build --target builder -t myapp .   # multi-stage конкретная стадия
```

### Multi-stage build (маленькие образы)
```dockerfile
# Стадия 1: сборка
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Стадия 2: runtime (только результат)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

---

## 📦 Управление образами и чистка

```bash
# Список
docker images
docker image ls
docker images --filter "dangling=true"   # висячие образы

# Удаление
docker rmi <image>
docker rmi $(docker images -q)            # удалить все
docker image prune                         # висячие
docker image prune -a                      # все неиспользуемые

# История образа (слои)
docker history myapp
docker history --no-trunc myapp

# Сохранить/загрузить
docker save myapp > myapp.tar
docker load < myapp.tar
docker save myapp | gzip > myapp.tar.gz

# Импорт/экспорт (контейнер, не образ)
docker export <container> > fs.tar         # файловая система
docker import fs.tar myimage

# Реестр
docker login registry.example.com
docker push myrepo/myapp:1.0
docker pull myrepo/myapp:1.0
docker search nginx
```

### Полная очистка (осторожно!)
```bash
docker system prune              # неиспользуемые контейнеры, сети, висячие образы
docker system prune -a           # + все образы без контейнера
docker system prune --volumes    # + тома (УДАЛИТ ДАННЫЕ!)
docker system df                 # занятое место
docker system events             # поток событий
```

---

## 🌐 Сети

```bash
docker network ls
docker network create mynet
docker network inspect mynet
docker network connect mynet <container>
docker network disconnect mynet <container>
docker network rm mynet
docker network prune
```

### Типы сетей
| Тип | Описание |
|---|---|
| `bridge` | По умолчанию. Изолированная сеть на хосте |
| `host` | Сеть хоста (нет изоляции) |
| `none` | Нет сети |
| `overlay` | Кластер Swarm |
| `macvlan` | Контейнер с MAC-адресом в физической сети |

### DNS между контейнерами
Контейнеры в **одной сети** могут обращаться друг к другу **по имени контейнера**:
```bash
docker network create appnet
docker run -d --name db --network appnet postgres
docker run -d --name web --network appnet nginx
# Внутри web: curl http://db:5432 (DNS по имени!)
```

---

## 💾 Тома и монтирование

```bash
# Тома (рекомендуется)
docker volume create mydata
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune

# Использование
docker run -v mydata:/var/lib/postgresql/data postgres
docker run --mount source=mydata,target=/var/lib/postgresql/data postgres

# Bind mount (каталог хоста)
docker run -v /host/path:/container/path nginx
docker run -v $(pwd):/app -w /app node npm install
docker run --mount type=bind,source=$(pwd),target=/app nginx

# tmpfs (в RAM)
docker run --tmpfs /cache nginx
docker run --mount type=tmpfs,target=/cache nginx
```

### Разница -v vs --mount
```bash
docker run -v myvol:/data nginx             # если myvol нет — создаст том
docker run --mount source=myvol,target=/data nginx   # ошибка если нет
docker run -v /opt/data:/data nginx         # абсолютный путь → bind mount
```

---

## 🐙 docker-compose

### docker-compose.yml (пример)
```yaml
version: "3.9"   # устаревает, но часто встречается

services:
  web:
    image: nginx:alpine
    ports:
      - "127.0.0.1:8080:80"     # ✅ только localhost
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - frontend

  app:
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        VERSION: 1.0
      target: production
    environment:
      - DEBUG=false
      - DB_HOST=db
      - DB_PASSWORD=${DB_PASSWORD}   # из .env
    env_file:
      - .env
    volumes:
      - app-data:/app/data
    depends_on:
      db:
        condition: service_healthy
    restart: always
    networks:
      - frontend
      - backend

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

volumes:
  app-data:
  db-data:

networks:
  frontend:
  backend:
```

### .env файл
```env
DB_PASSWORD=secretpassword
VERSION=1.0
```

### Команды docker-compose
```bash
docker compose up -d                 # запустить всё в фоне
docker compose up -d web db          # только некоторые
docker compose up --build            # пересобрать образы
docker compose up --force-recreate   # пересоздать контейнеры
docker compose down                  # остановить + удалить
docker compose down -v               # + удалить тома (ДАННЫЕ!)
docker compose down --rmi all        # + удалить образы
docker compose start / stop          # без удаления
docker compose restart web
docker compose pause / unpause
docker compose ps                    # статус
docker compose logs -f web
docker compose logs -f --tail=50
docker compose exec web bash         # войти
docker compose run --rm web npm test # одноразовый
docker compose build                 # собрать образы
docker compose pull                  # обновить образы
docker compose config                # результирующий конфиг (с подстановкой .env)
docker compose top                   # процессы
```

> `docker-compose` (с дефисом) — старая версия V1 (Python).
> `docker compose` (через пробел) — современная V2 (Go, встроена в Docker).

### profiles (запуск части сервисов)
```yaml
services:
  app:
    # ...
  debug-tools:
    profiles: ["debug"]
    image: nicolaka/netshoot
```
```bash
docker compose --profile debug up    # запустить с профилем
docker compose up                    # без debug-tools
```

---

## ⚙️ Конфигурация Docker

Файл: `/etc/docker/daemon.json` (Linux), `~/.docker/daemon.json`

```json
{
  "data-root": "/var/lib/docker",
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "userland-proxy": false,
  "storage-driver": "overlay2",
  "live-restore": true,
  "registry-mirrors": ["https://mirror.example.com"],
  "insecure-registries": ["192.168.1.100:5000"]
}
```

```bash
sudo systemctl restart docker
```

### Логи контейнеров
```bash
docker logs -f --tail 100 <container>
docker logs --since 2h <container>
docker logs --since 2024-01-15T10:00:00 <container>
docker logs --until 1h <container>
```

Лимит размера логов (в daemon.json):
```json
"log-opts": { "max-size": "10m", "max-file": "5" }
```

---

## 🛠️ Полезные образы

| Образ | Назначение |
|---|---|
| `alpine` | Минимальный Linux (5 МБ) |
| `busybox` | Unix-утилиты (1 МБ) |
| `nicolaka/netshoot` | Сетевая отладка |
| `traefik` | Reverse proxy |
| `portainer/portainer-ce` | Web-UI для Docker |
| `docker:24-dind` | Docker in Docker (CI/CD) |
| `postgres:16` | PostgreSQL |
| `redis:7` | Redis |
| `nginx:alpine` | Веб-сервер |
| `node:20-slim` | Node.js |
| `python:3.12-slim` | Python |
| `ubuntu:24.04` | Ubuntu |

---

## 🧩 Практические примеры

### 1. Быстрый БД для разработки
```bash
docker run -d --name dev-pg \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -p 127.0.0.1:5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

### 2. Запустить PostgreSQL + pgAdmin
```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
  admin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "127.0.0.1:5050:80"
volumes:
  pgdata:
```

### 3. Собрать и запустить Python-приложение
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```
```bash
docker build -t myapp .
docker run -p 127.0.0.1:8000:8000 myapp
```

### 4. Временная среда для тестирования
```bash
docker run -it --rm -v $(pwd):/app -w /app python:3.12 bash
# внутри: pip install pytest && pytest
```

### 5. Чистка системы
```bash
docker system df                      # что занимает место
docker system prune -a --volumes      # удалить всё (ОСТОРОЖНО!)
docker image prune -a                 # только образы
docker volume prune                   # только тома
```

---

## 🪤 Частые ошибки

1. **`-p 8080:80`** — пробрасывает на `0.0.0.0` (весь LAN!). Используйте `127.0.0.1:8080:80`.
2. **Данные в контейнере** — после `docker rm` исчезнут. Используйте volumes.
3. **Запуск от root** — по умолчанию процессы в контейнере root. Создавайте USER.
4. **`.env` в образе** — не копируйте секреты в образ. Передавайте через env/volume/secrets.
5. **Слои и кэш** — `COPY . .` перед `RUN pip install` инвалидирует кэш при любом изменении. Копируйте `requirements.txt` отдельно.
6. **BuildKit** — включите `DOCKER_BUILDKIT=1` (или `buildx`) для современных сборок.
7. **`depends_on` не ждёт готовности** — только запускает. Используйте `healthcheck` + `condition: service_healthy`.
8. **Имена контейнеров** — без `--name` Docker генерирует случайные (mystifying-фамилии).
9. **Один образ = один процесс** — не запускайте nginx+postgres+app в одном контейнере.
10. **alpine + Python** — musl libc, некоторые пакеты не собираются. Используйте `-slim`.

---

## 🔗 Полезные ссылки

- Документация: https://docs.docker.com
- Compose reference: https://docs.docker.com/compose/compose-file
- Docker Hub: https://hub.docker.com
- Play with Docker: https://labs.play-with-docker.com
- Awesome Compose: https://github.com/docker/awesome-compose
- Hadolint (линтер Dockerfile): https://github.com/hadolint/hadolint
- Dive (анализ слоёв): https://github.com/wagoodman/dive
- Lazydocker (TUI): https://github.com/jesseduffield/lazydocker

---

## 💡 Полезные советы

1. **`docker compose`** (V2) быстрее и современнее, чем `docker-compose` (V1).
2. **`-p 127.0.0.1:PORT:PORT`** — всегда для локальной разработки, не торчите в LAN.
3. **Multi-stage builds** — радикально уменьшают размер образа.
4. **`.dockerignore`** — как `.gitignore`, не копируйте мусор в образ.
5. **Layer caching** — тяжёлые и редкоменяющиеся операции (установка пакетов) — в начале Dockerfile.
6. **`healthcheck`** — критично для `depends_on: condition: service_healthy`.
7. **`.env` файл** — для секретов (не коммитьте его!).
8. **`docker compose config`** — проверяет результирующий YAML с подстановкой переменных.
9. **`docker exec -it`** — войти в работающий контейнер (как ssh).
10. **`docker system df`** — следите за занятым местом, Docker разрастается.
11. **Имена сервисов как DNS** — внутри compose-сети контейнеры доступны по имени сервиса.
12. **`restart: unless-stopped`** — для dev-окружения (не перезапускается после ручной остановки).
13. **BuildKit secrets** — `--secret` для безопасной передачи секретов при сборке.
14. **`docker scan`** — проверка образа на уязвимости.
15. **Lazydocker** — TUI-клиент для Docker (как lazygit для git).

---

*Сгенерировано как шпаргалка. Docker огромен — углубляйтесь через
https://docs.docker.com/reference/ и `docker <cmd> --help`*

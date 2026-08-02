# 🌐 HTTP / curl / Postman — шпаргалка

> **HTTP** — протокол прикладного уровня (request-response).
> **curl** — утилита командной строки для HTTP-запросов.
> **Postman** — GUI для тестирования API.

---

## 🔑 HTTP-протокол

### Структура запроса
```
POST /api/users HTTP/1.1              ← метод + путь + версия
Host: api.example.com                  ← заголовки
Content-Type: application/json
Authorization: Bearer xyz123
Content-Length: 42

{"name": "Alice", "age": 30}          ← тело (body)
```

### Структура ответа
```
HTTP/1.1 200 OK                        ← версия + статус + причина
Content-Type: application/json
Content-Length: 28

{"id": 1, "name": "Alice"}            ← тело
```

### Методы (verbs)
| Метод | Назначение | Идемпотентен | Безопасный |
|---|---|---|---|
| `GET` | Получить ресурс | ✅ | ✅ |
| `POST` | Создать ресурс | ❌ | ❌ |
| `PUT` | Заменить ресурс целиком | ✅ | ❌ |
| `PATCH` | Частично изменить | ❌ | ❌ |
| `DELETE` | Удалить | ✅ | ❌ |
| `HEAD` | Только заголовки (как GET без тела) | ✅ | ✅ |
| `OPTIONS` | Какие методы поддерживаются | ✅ | ✅ |
| `TRACE` | Эхо-запрос (для отладки) | ✅ | ✅ |
| `CONNECT` | Прокси-туннель | — | — |

### Статус-коды
| Диапазон | Что значит |
|---|---|
| **1xx** | Informational (редко) |
| **2xx** | Success |
| **3xx** | Redirection |
| **4xx** | Client error |
| **5xx** | Server error |

| Код | Имя | Описание |
|---|---|---|
| **200** | OK | Успех |
| **201** | Created | Ресурс создан |
| **202** | Accepted | Принято в обработку |
| **204** | No Content | Успех без тела |
| **301** | Moved Permanently | Постоянный редирект |
| **302** | Found | Временный редирект |
| **304** | Not Modified | Кэш валиден |
| **307** | Temporary Redirect | Временный (тот же метод) |
| **308** | Permanent Redirect | Постоянный (тот же метод) |
| **400** | Bad Request | Неверный запрос |
| **401** | Unauthorized | Не аутентифицирован |
| **403** | Forbidden | Нет прав |
| **404** | Not Found | Не найдено |
| **405** | Method Not Allowed | Метод не поддерживается |
| **409** | Conflict | Конфликт (уже существует) |
| **422** | Unprocessable Entity | Ошибка валидации |
| **429** | Too Many Requests | Rate limit |
| **500** | Internal Server Error | Внутренняя ошибка |
| **502** | Bad Gateway | Прокси upstream упал |
| **503** | Service Unavailable | Сервис недоступен |
| **504** | Gateway Timeout | Прокси upstream таймаут |

---

## 🚀 curl — установка

```bash
sudo pacman -S curl                 # Arch
sudo apt install curl               # Debian/Ubuntu
# macOS: уже встроен
# Windows 10+: уже встроен
```

---

## 🎯 Базовые запросы

```bash
# GET (по умолчанию)
curl https://example.com
curl -X GET https://api.example.com/users

# POST
curl -X POST https://api.example.com/users

# С заголовками и телом
curl -X POST https://api.example.com/users \
    -H "Content-Type: application/json" \
    -d '{"name":"Alice","age":30}'

# PUT
curl -X PUT https://api.example.com/users/1 \
    -H "Content-Type: application/json" \
    -d '{"name":"Alice Updated"}'

# DELETE
curl -X DELETE https://api.example.com/users/1

# PATCH
curl -X PATCH https://api.example.com/users/1 \
    -H "Content-Type: application/json" \
    -d '{"age":31}'
```

---

## ⚙️ Полезные флаги curl

| Флаг | Назначение |
|---|---|
| `-X METHOD` | Указать метод |
| `-H "Header: val"` | Заголовок (можно несколько) |
| `-d "data"` | Тело запроса (POST) |
| `-d @file` | Тело из файла |
| `--data-raw` | Как -d, без интерпретации @ |
| `-G` | Сделать данные query-параметрами GET |
| `-o file` | Вывод в файл |
| `-O` | Сохранить с тем же именем |
| `-i` | Показать заголовки ответа |
| `-I` | Только заголовки (HEAD) |
| `-v` | Verbose (заголовки запроса и ответа) |
| `-s` | Silent (без прогресса) |
| `-S` | Show errors even with -s |
| `-L` | Следовать редиректам |
| `-k` | Игнорировать SSL-ошибки |
| `-u user:pass` | Basic auth |
| `-u user:` | Запросить пароль интерактивно |
| `--max-time N` | Общий таймаут (сек) |
| `--connect-timeout N` | Таймаут подключения |
| `-A "UA"` | User-Agent |
| `-b "cookie"` | Cookie |
| `-b file` | Cookie из файла |
| `-c file` | Сохранить cookie |
| `--compressed` | Запросить сжатие (gzip) |
| `-x proxy` | Прокси |
| `-w FORMAT` | Свой формат вывода |
| `--resolve host:port:addr` | Подменить DNS |
| `--location` | Следовать редиректам |
| `-n` | Использовать ~/.netrc |
| `--url URL` | URL (когда несколько) |
| `-K config` | Читать опции из файла |
| `--retry N` | Повторов при ошибке |
| `--trace file` | Полный дамп в файл |

---

## 🔤 Передача данных

### Query-параметры
```bash
# Вручную
curl "https://api.example.com/search?q=python&page=2"

# Через -G + --data-urlencode
curl -G https://api.example.com/search \
    --data-urlencode "q=hello world" \
    --data-urlencode "page=2"

# urlencode значения
curl --data-urlencode "name=John Doe" https://...
```

### JSON
```bash
# Один заголовок + данные
curl -X POST https://api.example.com/users \
    -H "Content-Type: application/json" \
    -d '{"name":"Alice","age":30}'

# Из файла
curl -X POST https://api.example.com/users \
    -H "Content-Type: application/json" \
    -d @data.json

# Несколько заголовков
curl -X POST URL \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer token" \
    -H "Accept: application/json" \
    -d @data.json
```

### Form data
```bash
# application/x-www-form-urlencoded (по умолчанию для -d)
curl -X POST https://example.com/login \
    -d "username=alice&password=secret"

# multipart/form-data (для файлов)
curl -X POST https://example.com/upload \
    -F "file=@photo.jpg" \
    -F "name=Alice"

# Несколько файлов
curl -X POST https://example.com/upload \
    -F "files[]=@a.txt" \
    -F "files[]=@b.txt"
```

### Чтение из stdin
```bash
echo '{"key":"value"}' | curl -X POST URL -H "Content-Type: application/json" -d @-
```

---

## 🔐 Аутентификация

### Basic Auth
```bash
curl -u user:password https://api.example.com/
curl -u user https://api.example.com/      # спросит пароль
curl -u alice:secret -X POST URL
```

### Bearer Token (JWT)
```bash
TOKEN="eyJhbGc..."
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/
```

### API Key
```bash
# В заголовке
curl -H "X-API-Key: abc123" https://api.example.com/

# В query
curl "https://api.example.com/?api_key=abc123"
```

### OAuth 2.0
```bash
# Получить токен
curl -X POST https://auth.example.com/oauth/token \
    -d "grant_type=password" \
    -d "username=alice" \
    -d "password=secret" \
    -u client_id:client_secret

# Использовать
curl -H "Authorization: Bearer ACCESS_TOKEN" https://api.example.com/
```

### .netrc (для повторных запросов)
```bash
# ~/.netrc
machine api.example.com
login alice
password secret

# Использование
curl -n https://api.example.com/   # -n = использовать .netrc
chmod 600 ~/.netrc                 # права!
```

---

## 📋 Заголовки

### Частые заголовки запроса
| Заголовок | Что |
|---|---|
| `Host` | Имя хоста (обязательный в HTTP/1.1) |
| `User-Agent` | Идентификация клиента |
| `Accept` | Что клиент хочет получить |
| `Accept-Encoding` | gzip, br |
| `Content-Type` | Тип тела запроса |
| `Authorization` | Авторизация |
| `Cookie` | Куки |
| `Origin` / `Referer` | Для CORS |
| `Cache-Control` | no-cache |
| `If-None-Match` / `If-Modified-Since` | Кэширование |
| `X-Forwarded-For` | IP клиента (через прокси) |

### Content-Type
| Значение | Используется для |
|---|---|
| `application/json` | JSON |
| `application/x-www-form-urlencoded` | Формы |
| `multipart/form-data` | Загрузка файлов |
| `text/html` | HTML |
| `text/plain` | Простой текст |
| `application/xml` | XML |
| `application/octet-stream` | Бинарный |

```bash
# Посмотреть отправляемые/получаемые заголовки
curl -v https://example.com/
curl -I https://example.com/      # только заголовки ответа (HEAD)
curl -i https://example.com/      # заголовки + тело
```

---

## 📥 Вывод и сохранение

```bash
# В файл
curl -o output.html https://example.com/
curl -o /tmp/data.json https://api.example.com/

# С тем же именем (как в URL)
curl -O https://example.com/file.zip
curl -O URL1 -O URL2              # несколько файлов

# С 原来 именем
curl -O https://example.com/file.zip   # → ./file.zip

# Продолжить загрузку (если прервалась)
curl -C - -O https://example.com/bigfile.zip

# Скачать только если новее
curl -z file.zip -O https://example.com/file.zip

# Limit скорости
curl --limit-rate 100k -O https://example.com/bigfile
```

### Форматированный вывод
```bash
# Только статус-код
curl -s -o /dev/null -w "%{http_code}\n" https://example.com/

# Время запроса
curl -s -o /dev/null -w "%{time_total}s\n" https://example.com/

# Подробный формат
curl -w "@curl-format.txt" -o /dev/null -s https://example.com/

# curl-format.txt:
#    http_code: %{http_code}
#    time_namelookup: %{time_namelookup}
#    time_connect: %{time_connect}
#    time_total: %{time_total}
#    size_download: %{size_download}

# JSON через jq
curl -s https://api.github.com/users/torvalds | jq '.login'
```

---

## 🔄 Редиректы и прокси

### Редиректы
```bash
curl -L https://example.com/redirect    # следовать (3xx)
curl -L --max-redirs 5 URL              # лимит редиректов
```

### Прокси
```bash
curl -x http://proxy.example.com:8080 https://target.com
curl -x socks5://127.0.0.1:1080 https://target.com
curl -x http://user:pass@proxy:8080 URL

# Без прокси для конкретных хостов
curl --noproxy "localhost,127.0.0.1" https://example.com

# Tor
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/
```

### DNS
```bash
# Resolve override (для теста без DNS)
curl --resolve api.example.com:443:1.2.3.4 https://api.example.com/

# Нестандартный DNS
curl --dns-servers 8.8.8.8 https://example.com   # если curl с c-ares
```

---

## 🔒 HTTPS / SSL

```bash
# Игнорировать ошибки сертификата (НЕ для продакшена!)
curl -k https://self-signed.example.com/
curl --insecure URL

# Указать сертификат клиента
curl --cert client.pem --key client.key https://api.example.com/
curl --cert client.pem:password URL
curl -E client.pem URL

# CA bundle
curl --cacert /etc/ssl/certs/ca-certificates.crt URL

# Указать TLS-версию
curl --tlsv1.2 URL
curl --tlsv1.3 URL
curl --tls-max 1.2 URL
```

---

## 🛠️ Практические примеры

### 1. GitHub API
```bash
# Получить информацию о пользователе
curl -s https://api.github.com/users/torvalds | jq '.login, .bio'

# Список репозиториев
curl -s https://api.github.com/users/torvalds/repos | jq -r '.[].full_name'

# Создать репозиторий (нужен токен)
curl -X POST https://api.github.com/user/repos \
    -H "Authorization: token YOUR_TOKEN" \
    -d '{"name":"my-new-repo","private":true}'
```

### 2. REST API CRUD
```bash
BASE="https://jsonplaceholder.typicode.com"

# Create
curl -X POST "$BASE/posts" \
    -H "Content-Type: application/json" \
    -d '{"title":"foo","body":"bar","userId":1}'

# Read
curl "$BASE/posts/1"
curl "$BASE/posts?userId=1"

# Update
curl -X PUT "$BASE/posts/1" \
    -H "Content-Type: application/json" \
    -d '{"id":1,"title":"updated","body":"new","userId":1}'

# Delete
curl -X DELETE "$BASE/posts/1"
```

### 3. Проверка сайта
```bash
# Статус + время
curl -s -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n" https://example.com

# Headers
curl -I https://example.com/

# SSL-сертификат (истекает?)
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

### 4. Отправка файла
```bash
# Загрузить файл
curl -X POST https://uploads.example.com/ \
    -F "file=@report.pdf" \
    -F "description=Monthly report"

# Multipart с несколькими полями
curl -X POST https://api.example.com/submit \
    -F "name=Alice" \
    -F "email=alice@example.com" \
    -F "cv=@resume.pdf"
```

### 5. Локальный сервер
```bash
# Проверить локальный сервис
curl http://localhost:8000/
curl http://localhost:8000/api/health

# С разными эндпоинтами
curl http://localhost:8000/users
curl -X POST http://localhost:8000/users -d '{"name":"test"}' -H "Content-Type: application/json"
```

### 6. Скачивание с прогрессом
```bash
curl -# -O https://example.com/bigfile.zip       # прогресс-бар
curl --progress-bar -O URL
```

### 7. Имитация браузера
```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Accept: text/html,application/xhtml+xml" \
    -H "Accept-Language: en-US,en;q=0.9" \
    https://example.com/
```

### 8. Webhook (Discord/Slack)
```bash
curl -X POST https://discord.com/api/webhooks/... \
    -H "Content-Type: application/json" \
    -d '{"content":"Deploy successful!"}'
```

### 9. Пагинация / цикл
```bash
for page in 1 2 3; do
    curl -s "https://api.example.com/items?page=$page" >> all.json
done
```

### 10. Альтернатива Postman в CLI (httpie)
```bash
sudo pacman -S httpie
http https://example.com/
http POST api.example.com/users name=Alice age:=30     # := для чисел
http --download https://example.com/file.zip
```

---

## 📮 Postman / Insomnia / Bruno

### Postman — основные понятия
- **Collection** — набор запросов (группа)
- **Request** — один HTTP-запрос
- **Environment** — переменные окружения (dev/prod URL, токены)
- **Pre-request Script** — JS перед запросом (генерация токена)
- **Tests** — assertions на ответ
- **Variables** — `{{base_url}}`, `{{token}}`

### Tests (JavaScript)
```javascript
// Проверка статус-кода
pm.test("Status is 200", function () {
    pm.response.to.have.status(200);
});

// Проверка JSON-поля
pm.test("User has name", function () {
    pm.expect(pm.response.json().name).to.eql("Alice");
});

// Сохранить токен в переменную
let token = pm.response.json().token;
pm.environment.set("auth_token", token);

// Время ответа
pm.test("Fast response", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});
```

### Альтернативы
| Инструмент | Описание |
|---|---|
| **Postman** | Классика, electron, нужен аккаунт |
| **Insomnia** | Легче, меньше рекламы |
| **Bruno** | Open-source, хранит запросы в git |
| **HTTPie** | CLI, дружелюбный синтаксис |
| **curl** | CLI, везде есть |
| **xa** / **hurl** | CLI для тестирования (как pytest) |
| **vim-rest-console** | В Vim |
| **REST Client** (VS Code) | Расширение, `.http` файлы |

### .http файлы (REST Client / JetBrains)
```http
### Получить пользователей
GET https://api.example.com/users
Authorization: Bearer {{token}}

### Создать пользователя
POST https://api.example.com/users
Content-Type: application/json

{
    "name": "Alice",
    "age": 30
}

### Переменные
@token = abc123
@baseUrl = https://api.example.com
```

---

## 🌍 HTTP/2 и HTTP/3

```bash
# Проверить версию HTTP
curl -sI --http2 https://example.com/ | head -1
# HTTP/2 200

# Принудительно
curl --http2 URL
curl --http3 URL           # HTTP/3 (QUIC)
curl --http1.1 URL
```

### gRPC
```bash
# grpcurl
grpcurl -plaintext -d '{"name":"Alice"}' localhost:50051 my.Service/Method

# BloomRPC (GUI)
# Postman (с gRPC support)
```

---

## 🪤 Частые ошибки

1. **Не quoted URL** — `curl https://example.com/?a=1&b=2` → `&` в shell!
   Всегда `curl "https://..."`.
2. **`-d` без `-X POST`** — curl сам поставит POST, но привычнее явно.
3. **`-L` для редиректов** — без него получишь 3xx, а не финальный ответ.
4. **Content-Type** — без него сервер не поймёт формат.
5. **`-k` в продакшене** — опасно, отрубает проверку сертификата.
6. **`-u` в истории** — оставляет пароль в `.bash_history`.
7. **Пробелы в URL** — нужно `%20` или `--data-urlencode`.
8. **`-v` в логи** — выводит заголовки в stderr, не stdout.
9. **JSON в одинарных кавычках** — в shell нужны двойные внутри `-d`.
10. **Забыли `-s`** — прогресс-бар засоряет скрипты.

---

## 🔗 Полезные ссылки

- curl docs: https://curl.se/docs/manpage.html
- Everything curl: https://everything.curl.dev
- httpie: https://httpie.io
- httpbin (тестовый сервер): https://httpbin.org
- Postman: https://www.postman.com
- Insomnia: https://insomnia.rest
- Bruno: https://www.usebruno.com
- Mozilla HTTP: https://developer.mozilla.org/ru/docs/Web/HTTP
- HTTP status dogs: https://httpstatusdogs.com
- REST API Tutorial: https://restfulapi.net

---

## 💡 Полезные советы

1. **`-s` + `-o /dev/null` + `-w`** — для скриптов (только статус/время).
2. **`jq`** — парсить JSON-ответы в CLI.
3. **`.http` файлы** — для командной документации API (JetBrains, VS Code REST Client).
4. **Environment variables** в Postman — для dev/prod/testing.
5. **`-L`** — следовать редиректам (часто забывают).
6. **`-i`** — посмотреть заголовки ответа вместе с телом.
7. **`-v`** — отладка (видны и запрос, и ответ).
8. **`--data-urlencode`** — для query-параметров со спецсимволами.
9. **Bearer token в `-H`** — стандарт для JWT/OAuth.
10. **`.netrc`** — для повторных запросов к одному хосту.
11. **`httpie`** — дружелюбнее curl для повседневной работы.
12. **`curl --resolve`** — тестировать сайт без DNS (полезно для миграций).
13. **`-w "@format.txt"`** — кастомный вывод для бенчмарков.
14. **`--retry 3`** — повтор при сетевых ошибках.
15. **Webhooks** — типичный use case для curl в CI/CD.

---

*Сгенерировано как шпаргалка. HTTP/curl — основа веб-разработки —
углубляйтесь через https://developer.mozilla.org/ru/docs/Web/HTTP и `man curl`*

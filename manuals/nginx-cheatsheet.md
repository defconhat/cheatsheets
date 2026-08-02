# 🌐 nginx — шпаргалка по веб-серверу и reverse-proxy

> **nginx** (engine-x) — высокопроизводительный HTTP-сервер и reverse-proxy.
> Также: load balancer, mail proxy, TLS terminator, CDN.
> Документация: https://nginx.org/en/docs

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Directive** | Директива (настройка) |
| **Block (context)** | Блок настроек (`http {}`, `server {}`) |
| **Server** | Виртуальный хост (как `<VirtualHost>` в Apache) |
| **Location** | Правило для URL-пути |
| **Upstream** | Группа бэкенд-серверов |
| **Worker** | Процесс, обрабатывающий соединения |
| **Master** | Главный процесс, управляет worker'ами |
| **Module** | Расширение функциональности |

### Иерархия контекстов
```
main (глобальный)
└── events
└── http
    ├── server (виртуальный хост)
    │   └── location (URL-правила)
    └── upstream (группа серверов)
└── stream (TCP/UDP)
```

---

## 🚀 Установка и управление

```bash
sudo pacman -S nginx             # Arch / CachyOS
sudo apt install nginx           # Debian/Ubuntu

# Управление (systemd)
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx      # мягко перечитать конфиг
sudo systemctl status nginx
sudo systemctl enable nginx

# Прямые команды
nginx -t                          # проверить конфигурацию (ОБЯЗАТЕЛЬНО!)
nginx -T                          # показать итоговый конфиг
nginx -s reload                   # перезагрузить
nginx -s stop                     # остановить
nginx -s quit                     # мягко остановить
nginx -V                          # версия и опции сборки
nginx -c /path/to/nginx.conf      # свой конфиг
nginx -g "daemon off;"            # foreground (для Docker)
```

### Структура файлов
| Путь | Назначение |
|---|---|
| `/etc/nginx/nginx.conf` | Главный конфиг |
| `/etc/nginx/conf.d/*.conf` | Конфиги серверов (рекомендуется) |
| `/etc/nginx/sites-available/` | Debian: доступные сайты |
| `/etc/nginx/sites-enabled/` | Debian: включённые (symlinks) |
| `/etc/nginx/snippets/` | Переиспользуемые блоки |
| `/var/log/nginx/access.log` | Логи доступа |
| `/var/log/nginx/error.log` | Логи ошибок |
| `/usr/share/nginx/html/` | Корень по умолчанию |
| `/etc/nginx/mime.types` | MIME-типы |

---

## 📝 Базовая конфигурация

### `/etc/nginx/nginx.conf` (главный)
```nginx
user nginx;
worker_processes auto;            # по числу ядер
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;      # соединений на worker
    # use epoll;                  # Linux: epoll (по умолчанию)
    multi_accept on;              # принимать много за раз
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;            # скрыть версию nginx

    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    include /etc/nginx/conf.d/*.conf;
}
```

### Статический сайт
```nginx
# /etc/nginx/conf.d/mysite.conf
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/mysite;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
```

---

## 🔄 Reverse Proxy

### Проксирование на бэкенд
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Несколько location'ов
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;     # фронтенд
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;     # API
        rewrite ^/api/(.*)$ /$1 break;
    }

    location /static/ {
        alias /var/www/static/;               # файлы
        expires 30d;
    }

    location /grafana/ {
        proxy_pass http://127.0.0.1:3000/;    # Grafana
    }
}
```

---

## ⚖️ Load Balancing

```nginx
http {
    upstream backend {
        # Методы балансировки:
        # round-robin (по умолчанию)
        # least_conn;            — меньше соединений
        # ip_hash;               — по IP клиента (sticky)
        # hash $request_uri;     — по URL

        server backend1.example.com weight=3;
        server backend2.example.com;
        server backend3.example.com backup;     # запасной
        server backend4.example.com down;       # выключен

        keepalive 32;                           # keep-alive к бэкендам
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
        }
    }
}
```

### Health checks
```nginx
location /health {
    proxy_pass http://backend/health;
    proxy_next_upstream error timeout http_500 http_502 http_503 http_504;
}
```

---

## 🔒 HTTPS / SSL

### Получение сертификата Let's Encrypt
```bash
sudo pacman -S certbot certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
# Автоматически изменит nginx.conf

# Автообновление
sudo systemctl enable --now certbot.timer
```

### Ручная настройка HTTPS
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

# Редирект с HTTP на HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

---

## 🎨 Location и приоритеты

Порядок проверки location'ов (от высшего к низшему):
1. `=` точное совпадение (`location = /exact`)
2. `^~` префикс без regex (`location ^~ /static/`)
3. `~` / `~*` regex (с учётом/без регистра)
4. префикс (`location /api`)

```nginx
location = /exact {              # точное совпадение (приоритет 1)
    return 200 "exact match";
}

location ^~ /static/ {           # префикс, не проверять regex
    alias /var/www/static/;
}

location ~* \.php$ {             # regex (без регистра)
    fastcgi_pass unix:/run/php/php-fpm.sock;
}

location ~ \.jpg$ {              # regex (с учётом регистра)
    root /images;
}

location /api {                  # префикс (последний приоритет)
    proxy_pass http://backend;
}

location / {                     # дефолт
    try_files $uri $uri/ =404;
}
```

---

## 🔄 Rewrites и Redirects

```nginx
# Permanent redirect (301)
server {
    listen 80;
    server_name old.com;
    return 301 https://new.com$request_uri;
}

# Rewrite URL
location /old/ {
    rewrite ^/old/(.*)$ /new/$1 permanent;     # 301
    # rewrite ^/old/(.*)$ /new/$1 redirect;    # 302
    # rewrite ^/old/(.*)$ /new/$1 last;        # внутренний, ищет location заново
    # rewrite ^/old/(.*)$ /new/$1 break;       # внутренний, остаётся
}

# Убрать .html из URL
location / {
    rewrite ^(/.*)\.html$ $1 permanent;
    try_files $uri $uri.html $uri/ =404;
}

# Стандартный rewrite для фреймворков (Laravel, Django)
location / {
    try_files $uri $uri/ /index.php?$query_string;
}
```

---

## 🛠️ Переменные nginx

| Переменная | Что |
|---|---|
| `$host` | Имя хоста из запроса |
| `$remote_addr` | IP клиента |
| `$request_uri` | Полный URI |
| `$uri` | URI без query string |
| `$args` / `$query_string` | Query string |
| `$scheme` | http/https |
| `$request_method` | GET/POST/... |
| `$http_user_agent` | User-Agent |
| `$http_referer` | Referer |
| `$server_name` | Имя server'а |
| `$server_port` | Порт |
| `$document_root` | Корень |
| `$time_iso8601` | Время ISO |
| `$request_time` | Время обработки |
| `$body_bytes_sent` | Байт отправлено |

### Кастомные переменные
```nginx
location / {
    set $upstream "http://backend";
    proxy_pass $upstream;
}

# Map (преобразование)
map $http_host $backend {
    default "http://default";
    "api.com" "http://api";
    "web.com" "http://web";
}
```

---

## ⚡ Производительность

```nginx
http {
    # Sendfile (быстрая отдача файлов)
    sendfile on;
    tcp_nopush on;          # отправлять заголовки одним пакетом
    tcp_nodelay on;         # не ждать (Nagle)

    # Keep-alive
    keepalive_timeout 65;
    keepalive_requests 1000;

    # Буферы
    client_body_buffer_size 16K;
    client_max_body_size 50M;       # max upload
    client_body_timeout 30;
    client_header_timeout 30;

    # Gzip
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_proxied any;
    gzip_types
        application/javascript
        application/json
        application/xml
        text/css
        text/plain;
}

# Кэширование статических файлов
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff2?)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

### Настройка worker_processes
```nginx
worker_processes auto;        # = число CPU ядер
# worker_processes 8;

worker_rlimit_nofile 65535;   # лимит файловых дескрипторов

events {
    worker_connections 4096;  # соединений на worker
    multi_accept on;
    use epoll;
}
# max clients = worker_processes * worker_connections
```

---

## 🔐 Безопасность

```nginx
# Скрыть версию nginx
server_tokens off;

# Защита от clickjacking
add_header X-Frame-Options "SAMEORIGIN";

# XSS защита
add_header X-XSS-Protection "1; mode=block";

# Content-Type sniffing
add_header X-Content-Type-Options "nosniff";

# CSP
add_header Content-Security-Policy "default-src 'self'";

# Запретить доступ к скрытым файлам
location ~ /\. {
    deny all;
}

# Запретить выполнение PHP в uploads
location ~* /uploads/.*\.php$ {
    deny all;
}

# Basic Auth
location /admin {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
}

# Limit requests (rate limit)
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://backend;
}

# Limit connections
limit_conn_zone $binary_remote_addr zone=conn_per_ip:10m;
limit_conn conn_per_ip 10;
```

### Basic Auth — генерация пароля
```bash
sudo htpasswd -c /etc/nginx/.htpasswd user1
sudo htpasswd /etc/nginx/.htpasswd user2     # без -c (добавить)
```

---

## 📊 Логи

```nginx
# Формат лога
log_format main '$remote_addr - $remote_user [$time_local] '
                '"$request" $status $body_bytes_sent '
                '"$http_referer" "$http_user_agent" '
                'rt=$request_time uct="$upstream_connect_time" '
                'urt="$upstream_response_time"';

access_log /var/log/nginx/access.log main;
error_log /var/log/nginx/error.log warn;

# Условное логирование
location /health {
    access_log off;            # не логировать health checks
    return 200 "ok";
}

# Буферизация логов
access_log /var/log/nginx/access.log main buffer=32k flush=5s;
```

### Анализ логов
```bash
# Топ IP
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head

# Топ URL
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head

# Коды ответов
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# Ошибки 5xx
grep ' 5[0-9][0-9] ' access.log
```

---

## 🐍 PHP / Python / Node бэкенды

### PHP-FPM
```nginx
location ~ \.php$ {
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_index index.php;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}

# или TCP
fastcgi_pass 127.0.0.1:9000;
```

### Python (uWSGI / Gunicorn)
```nginx
# uWSGI
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:3031;
}

# Gunicorn (через proxy_pass)
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### Node.js
```nginx
location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

---

## 🐳 nginx в Docker

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/conf.d/default.conf
COPY dist/ /usr/share/nginx/html/
```

```yaml
# docker-compose.yml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/usr/share/nginx/html:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app

  app:
    image: myapp:latest
```

---

## 🪤 Частые ошибки

1. **Не проверили `nginx -t`** — config синтаксис после правки.
2. **`reload` вместо `restart`** — reload мягче, не разрывает соединения.
3. **`alias` vs `root`**:
   - `root /var/www; location /img/ {}` → `/var/www/img/...`
   - `alias /var/www/images/; location /img/ {}` → `/var/www/images/...`
4. **Trailing slash в `proxy_pass`**:
   - `proxy_pass http://backend;` → сохраняет URI
   - `proxy_pass http://backend/;` → заменяет location-часть
5. **CSS/JS не работают** — часто MIME-типы или пути.
6. **`client_max_body_size`** — по умолчанию 1MB, uploads ломаются.
7. **Переменные в `proxy_pass`** — нужны `resolver` и `resolver_timeout`.
8. **Regex `~` case-sensitive** — нужно `~*` для без учёта регистра.
9. **`server_name` не совпадает** — попадёт в default server.
10. **Let's Encrypt rate limit** — 5 сертификатов в неделю на домен.

---

## 🔗 Полезные ссылки

- Документация: https://nginx.org/en/docs
- Beginner's Guide: https://nginx.org/en/docs/beginners_guide.html
- Full example: https://www.nginx.com/resources/wiki/start/topics/examples/full/
- Mozilla SSL Config: https://ssl-config.mozilla.org
- ngx_conf playground: https://www.digitalocean.com/community/tools/nginx
- Nginx config generator: https://www.nginxconfig.io
- Awesome Nginx: https://github.com/agile6v/awesome-nginx

---

## 💡 Полезные советы

1. **`nginx -t`** — ВСЕГДА после правки конфига.
2. **`reload`** — мягче, чем `restart` (без обрыва соединений).
3. **`include conf.d/*.conf`** — разделяйте конфиги по файлам.
4. **Reverse proxy** — главное назначение nginx в микросервисах.
5. **`upstream` + load balancing** — для нескольких бэкендов.
6. **Let's Encrypt + certbot** — бесплатные SSL-сертификаты.
7. **`gzip on`** — ускоряет отдачу текста.
8. **`expires 1y`** — для статики (браузерное кэширование).
9. **`limit_req`** — защита от DDoS / брутфорса.
10. **`access_log off`** — для health checks (не засорять логи).
11. **`server_tokens off`** — скрыть версию nginx.
12. **HTTP/2** — `listen 443 ssl http2;` (или `http2 on;` в новых версиях).
13. **Docker + nginx** — отличный reverse-proxy для контейнеров.
14. **`try_files $uri $uri/ /index.php?$query_string`** — стандарт для PHP-фреймворков.
15. **`return 301`** — для редиректов (быстрее, чем `rewrite`).

---

*Сгенерировано как шпаргалка. nginx мощный и капризный —
углубляйтесь через https://nginx.org/en/docs и `nginx -t`*

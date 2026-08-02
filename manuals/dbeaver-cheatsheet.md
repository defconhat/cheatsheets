# 🗄️ DBeaver — шпаргалка

> **DBeaver** — бесплатный универсальный GUI-клиент для БД (PostgreSQL, MySQL, SQLite, Oracle, ClickHouse, DuckDB и др.).
> Поддерживает ER-диаграммы, редактор SQL, экспорт/импорт, SSH-туннели.
> Дом: https://dbeaver.io

---

## 📦 Версии и установка

| Версия | Назначение |
|---|---|
| **DBeaver Community** | Бесплатная (GPL), базы через JDBC-драйверы |
| **DBeaver Lite/Enterprise** | Платная, доп. NoSQL, облака, AI |
| **DBeaver Enterprise Team** | Корпоративная |

```bash
# Arch / CachyOS
sudo pacman -S dbeaver

# macOS
brew install --cask dbeaver-community

# Linux (snap)
sudo snap install dbeaver-ce

# Flatpak
flatpak install flathub io.dbeaver.DBeaverCommunity
```

> Используйте **Community Edition** — покрывает 95% задач, бесплатно.

---

## ⌨️ Горячие клавиши

### SQL-редактор
| Клавиша | Действие |
|---|---|
| `Ctrl+Enter` | Выполнить текущий запрос |
| `Ctrl+Shift+Enter` | Выполнить скрипт целиком |
| `Alt+X` | Выполнить всё |
| `Ctrl+/` | Закомментировать строку |
| `Ctrl+Shift+/` | Закомментировать блок (`/* */`) |
| `Ctrl+Space` | Автодополнение (таблицы, колонки) |
| `Ctrl+Click` на таблице | Перейти к объекту |
| `Ctrl+F` | Поиск |
| `Ctrl+H` | Глобальный поиск |
| `F3` | Открыть декларацию объекта |
| `Ctrl+Shift+F` | Форматировать SQL |
| `Ctrl+]` / `Ctrl+[` | Следующее / предыдущее выделение |
| `F4` | Открыть структуру таблицы |
| `Alt+←` / `Alt+→` | Назад / вперёд по истории переходов |

### Навигация и вкладки
| Клавиша | Действие |
|---|---|
| `F3` | Новый SQL-редактор |
| `Ctrl+Shift+T` | Открыть таблицу (по имени) |
| `Ctrl+Shift+R` | Открыть процедуру |
| `Ctrl+Shift+N` | Новое соединение |
| `Ctrl+W` | Закрыть вкладку |
| `Ctrl+Tab` | Следующая вкладка |
| `Ctrl+Shift+Tab` | Предыдущая вкладка |
| `F5` | Обновить навигатор |
| `F6` | Свернуть/развернуть навигатор |

### В таблице (Data view)
| Клавиша | Действие |
|---|---|
| `Ins` | Новая строка |
| `Del` | Удалить строку |
| `Ctrl+S` | Сохранить изменения (Post/Edit) |
| `Ctrl+Z` / `Ctrl+Y` | Отменить/вернуть |
| `Alt+PgDn` / `Alt+PgUp` | След./предыдущая страница данных |
| `Ctrl+F` | Фильтр по значениям |
| `F7` | Сортировка |
| `F8` | Фильтр строк (WHERE) |
| `Ctrl+Shift+P` | Панель фильтров |

---

## 🔌 Создание соединения

1. **Клик по иконке «розетка»** (или `Ctrl+Shift+N`) → New Connection.
2. Выбрать СУБД (PostgreSQL, MySQL, SQLite, …).
3. Ввести хост / порт / БД / пользователя / пароль.
4. **Test Connection** — DBeaver скачает JDBC-драйвер автоматически.
5. **Finish** → соединение появится в навигаторе.

### SSH-туннель (частый случай для прод-БД)
- В окне настроек → вкладка **SSH**.
- Указать: хост бастиона, порт, пользователь, ключ или пароль.
- Можно пробросить локальный порт на удалённую БД.

### SSL
- Вкладка **SSL** → выбрать режим (`require`, `verify-ca`, `verify-full`).
- Указать сертификаты (client, server, CA).

---

## 📊 Навигатор БД

Дерево слева: **Соединение → БД → Схема → Tables / Views / Procedures / Functions**.

| Действие | Что |
|---|---|
| Двойной клик по таблице | Открыть вкладку структуры |
| Клик по `Data`-вкладке | Просмотр данных |
| Правый клик → `View Data` | Расширенный просмотр (с фильтром, лимитом) |
| Правый клик → `Generate SQL` | `SELECT/INSERT/UPDATE` по шаблону |
| Правый клик → `Export Data` | CSV, JSON, SQL, XLSX |
| Правый клик → `Import Data` | Загрузить данные |
| Drag таблицы в редактор | Вставить её имя или `SELECT *` |

---

## 🧮 ER-диаграммы

- Двойной клик по схеме/БД → вкладка **ER Diagram**.
- DBeaver строит диаграмму по foreign keys.
- Перетаскивайте таблицы мышкой, можно экспортировать в PNG/SVG.
- В Enterprise есть **реверс-инжиниринг** для больших схем.

---

## 📤 Экспорт / имппорт

### Экспорт
1. Правый клик по таблице / результату → **Export Data**.
2. Форматы: **CSV, JSON, SQL (INSERT), HTML, XLSX, XML, Markdown**.
3. Настроить разделители, заголовки, кодировку.
4. Можно экспортировать и результат произвольного `SELECT`.

### Импорт
1. Правый клик по таблице → **Import Data**.
2. Источник: CSV, JSON, XLSX, SQL-скрипт, другая таблица.
3. Маппинг колонок, обработка конфликтов (INSERT/UPDATE/IGNORE).

### Резервные копии
- Для **PostgreSQL**: правый клик → `Backup` (`pg_dump`) / `Restore` (`pg_restore`).
- Для **MySQL**: `Backup` (`mysqldump`) / `Restore`.
- DBeaver оборачивает нативные утилиты — нужно, чтобы они стояли в системе.

---

## 🔍 SQL-редактор: фишки

- **Автодополнение**: `Ctrl+Space` — подсказки по таблицам, колонкам, алиасам, функциям.
- **Hyperlink**: `Ctrl+Click` по имени таблицы → переход в её определение.
- **Параметры скрипта**: `:var` или `${var}` — DBeaver спросит значение перед запуском.
  ```sql
  SELECT * FROM users WHERE id = :user_id;
  ```
- **Statement delimiter** `;` — выполняется только текущий стейтмент (`Ctrl+Enter`).
- **Result Set** поддерживает несколько панелей: несколько `SELECT` в одном скрипте → несколько результатов.

### Сохранение запросов
- `Snippets` (окно слева снизу) — переиспользуемые шаблоны SQL.
- Можно перетаскивать в редактор.

---

## 🎨 Оформление и темы

- **Settings → User Interface → Appearance** → Darkest Dark, Light и др.
- **Editor → SQL Editor → Formatting** — настроить отступы/регистр.
- Шрифты: `Window → Preferences → General → Appearance → Colors and Fonts`.

---

## ⚡ Производительность

| Что | Совет |
|---|---|
| Большая таблица | Не открывайте `SELECT *` без лимита — используйте фильтр `F8` |
| Авто-commit | Отключите (`Auto-commit` в тулбаре) для транзакционных правок |
| Кэш метаданных | `Refresh` (`F5`) после структурных изменений на сервере |
| Connection pool | В Enterprise — пул соединений для тяжёлых нагрузок |
| Lazy load | Включён по умолчанию — данные грузятся страницами |

---

## 🐛 Частые проблемы

| Симптом | Решение |
|---|---|
| `No suitable driver` | `Test Connection` — драйвер скачается. Или скачать вручную в **Drivers** |
| `Public Key Retrieval is not allowed` (MySQL 8) | В свойствах соединения → `allowPublicKeyRetrieval=true` |
| `Connection refused` | Проверить хост/порт, фаервол, SSH-туннель |
| Долгий первый коннект | DBeaver качает JDBC — подождать или поставить драйвер заранее |
| Не видит таблицы | `F5` (refresh) или включить `Show only user objects` |
| Кириллица знаками `?` | Настроить кодировку в свойствах соединения (UTF-8) |

---

## 🔐 Безопасность

- **Пароли** хранятся локально (зашифрованы мастер-паролем).
  - `Preferences → Connections → Credentials` → включить мастер-пароль.
- **Не светите пароли** в скриншотах / экспортах.
- Для прод-БД: соединение **Read-Only** (`Mark as read-only` в свойствах) — DBeaver не даст править данные.
- **SSH-ключи** предпочтительнее паролей для бастионов.

---

## 🧩 Плагины (Eclipse-based)

DBeaver построен на Eclipse RCP. Можно ставить плагины в папку `dropins`:
- **SQL Editor Pro** — расширенный редактор.
- **Office Integration** — экспорт в Office-форматы (в Enterprise).
- **AI Assistant** (Enterprise) — генерация SQL из текста.

---

## 📚 Поддерживаемые СУБД (неполный список)

| Категория | Примеры |
|---|---|
| Реляционные | PostgreSQL, MySQL, MariaDB, Oracle, MS SQL, SQLite, DB2 |
| Big Data | ClickHouse, Hive, Presto, Trino, Impala, Spark |
| Columnar | ClickHouse, Vertica, Greenplum, Redshift |
| Time-series | TimescaleDB, InfluxDB (Enterprise) |
| Embedded | H2, HSQLDB, Derby, DuckDB |
| Cloud | Snowflake, BigQuery (Enterprise), AWS Athena |

---

## 🆚 DBeaver vs альтернативы

| Клиент | Плюсы | Минусы |
|---|---|---|
| **DBeaver** | Универсальный, бесплатно, JDBC | Тяжёлый (Java/Eclipse) |
| **pgAdmin** | Родной для PostgreSQL | Только PostgreSQL, устаревший UI |
| **DataGrip** | Очень мощный, JetBrains-quality | Платный |
| **TablePlus** | Лёгкий, быстрый | Лимиты бесплатной версии |
| **Beekeeper Studio** | Простой, красивый | Меньше фич |
| **HeidiSQL / MySQL Workbench** | Только MySQL/MariaDB | Узкая специализация |

---

## 🔗 Источники

- Дом: https://dbeaver.io
- GitHub: https://github.com/dbeaver/dbeaver
- Документация: https://github.com/dbeaver/dbeaver/wiki
- Горячие клавиши: https://github.com/dbeaver/dbeaver/wiki/Shortcuts

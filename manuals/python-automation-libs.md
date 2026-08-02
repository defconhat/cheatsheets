# 🐍 Python: 10 библиотек для автоматизации

> Компактные утилиты, которые экономят время при написании скриптов: интерфейс, системная автоматизация, работа с данными и архитектурой. Источник: [Хабр](https://habr.com/ru/articles/983158/).

**Идея:** Python известен концепцией «batteries included», но стандартные решения иногда громоздки. Эти 10 небольших библиотек делают интерфейс понятнее, сисадминство — проще, а архитектуру — надёжнее.

---

## Часть 1. Интерфейс и визуализация

Признак профессионального скрипта — обратная связь. Если процесс долгий, без индикации непонятно: завис или работает.

### 1. tqdm — прогресс-бары, которые не бесят

Название с арабского — «прогресс». Простой способ добавить индикатор в любой цикл.

**Проблема:** непонимание, сколько займёт обработка большого массива данных.

```python
from tqdm import tqdm
import time

# Оборачиваем итератор
for i in tqdm(range(100), desc="Обработка файлов"):
    time.sleep(0.1)  # Имитация работы
```

**Плюсы:** почти не нагружает систему, сама считает скорость и примерное время завершения, поддерживает вложенность.

```bash
pip install tqdm
```

---

### 2. Rich — терминал как искусство

Если `tqdm` отвечает только за полоски прогресса, то **Rich** берёт на себя вообще всё оформление консоли.

**Проблема:** чтение сплошного потока текста из `print()` утомляет, данные сливаются.

**Возможности:** таблицы, подсветка синтаксиса (JSON, SQL и др.), цветные логи.

```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Отчет по автоматизации")

table.add_column("Задача", style="cyan", no_wrap=True)
table.add_column("Статус", style="magenta")
table.add_column("Время", justify="right", style="green")

table.add_row("Парсинг логов", "✅ Успешно", "1.2s")
table.add_row("Очистка кэша", "✅ Успешно", "0.05s")
table.add_row("Бэкап БД", "❌ Ошибка", "—")

console.print(table)
```

В терминале это отобразится аккуратной выровненной таблицей с цветами.

```bash
pip install rich
```

---

### 3. Humanize — машинные данные → человекочитаемые

Переводит машинные величины (байты, секунды, числа) в понятный формат.

**Проблема:** скрипт выводит сырые данные вроде «Осталось 14567 секунд».

```python
import humanize
import datetime

# Конвертация размера
print(humanize.naturalsize(1024 * 1024 * 50))
# Результат: 50.0 MB

# Конвертация времени
delta = datetime.timedelta(seconds=3665)
print(humanize.naturaldelta(delta))
# Результат: an hour

# Работа с числами
print(humanize.apnumber(1))
# Результат: one
```

**Особенность:** поддерживает локализацию (i18n) для перевода на нужный язык.

```bash
pip install humanize
```

---

## Часть 2. Системная автоматизация и скриптинг

Скрипты часто выступают связующим звеном между программами. Инструменты для надёжного «клея».

### 4. sh — замена subprocess для лаконичности

Синтаксис `subprocess` бывает избыточен. Библиотека **sh** позволяет вызывать консольные утилиты как функции Python.

**Проблема:** громоздкий код для запуска внешних процессов.

```python
import sh

# Вызов команды как функции
print(sh.ls("-l", "/usr/bin"))

# Канал (pipe): ls /etc | grep python
print(sh.grep(sh.ls("/etc"), "python"))

# Работа с git
sh.git.checkout("master")
sh.git.pull()
```

**Плюсы:** любая команда из `$PATH` доступна как функция; при ошибке выбрасывается исключение. Работает преимущественно на UNIX.

```bash
pip install sh
```

---

### 5. Watchdog — слежка за папкой без polling

Выполнять действие при появлении файла в директории — частая задача. Вместо постоянного опроса ФС **Watchdog** использует события ОС для мгновенной реакции.

**Проблема:** неэффективный polling директорий.

**Сценарий:** автоматическая сортировка скачанных файлов.

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Обнаружен новый файл: {event.src_path}")

observer = Observer()
observer.schedule(MyHandler(), path='./my_folder', recursive=False)
observer.start()

try:
    while True:
        pass  # Фоновая работа
except KeyboardInterrupt:
    observer.stop()
```

```bash
pip install watchdog
```

---

### 6. Schedule — планировщик с человеческим лицом

Для запуска задач по расписанию не обязательно тащить Crontab. **Schedule** настраивает периодичность прямо в коде.

**Проблема:** сложность настройки периодических задач.

```python
import schedule
import time

def job():
    print("Делаю бэкап базы данных...")

# Интуитивный синтаксис
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

**Плюсы:** код легко читается, нет тяжёлых зависимостей как в Celery.

```bash
pip install schedule
```

---

## Часть 3. Работа с данными и архитектурой

С ростом скрипта важнее становятся безопасность кода и его чистота.

### 7. python-dotenv — прощай, хардкод

Хранить пароли/токены в коде — плохая практика. **python-dotenv** загружает секреты из локального файла `.env`.

**Проблема:** случайная утечка ключей в систему контроля версий.

> ⚠️ **Важно:** файл `.env` обязательно добавить в `.gitignore`.

Содержимое `.env`:
```ini
API_KEY=your_secret_token_here
DB_URL=postgresql://user:password@localhost/db
```

Использование:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка файла

api_key = os.getenv("API_KEY")
print(f"Ключ загружен: {api_key[:4]}...")
```

```bash
pip install python-dotenv
```

---

### 8. Beartype — проверка типов на скорости света

Аннотации типов в Python по умолчанию **не проверяются** во время выполнения. **Beartype** добавляет такую проверку без существенной потери производительности.

**Проблема:** ошибки из-за передачи в функции данных неверных типов.

```python
from beartype import beartype

@beartype
def process_data(count: int, names: list[str]):
    print(f"Обрабатываю {count} имен")

process_data(5, ["Alice", "Bob"])   # Успешно
process_data("5", "Alice")          # BeartypeCallHintViolationError
```

```bash
pip install beartype
```

---

### 9. Loguru — логирование, приносящее радость

Стандартный модуль `logging` требует долгой настройки. **Loguru** позволяет начать логирование сразу.

**Проблема:** мучительная настройка логирования и его ротации.

```python
from loguru import logger

# Запись в файл с ротацией по размеру
logger.add("debug.log", rotation="500 MB", compression="zip")

logger.info("Скрипт запущен")
logger.error("Что-то пошло не так!")

@logger.catch  # Декоратор для отлова ошибок
def critical_function():
    return 1 / 0

critical_function()
```

```bash
pip install loguru
```

---

### 10. IceCream — забудьте о print() при дебаге

При отладке часто используют `print()`, но в куче вывода легко запутаться. **IceCream** (`ic`) упрощает этот процесс.

**Проблема:** необходимость вручную подписывать выводимые переменные.

```python
from icecream import ic

def complex_function(a, b):
    result = a + b
    ic(result)  # Выведет имя переменной, её значение, строку и файл
    return result

data = {"id": 1, "status": "active"}
ic(data)  # Удобный вывод словаря
```

```bash
pip install icecream
```

---

## 📊 Сводная таблица

| # | Библиотека | Назначение | Категория |
|---|---|---|---|
| 1 | **tqdm** | Прогресс-бары в циклах | Интерфейс |
| 2 | **Rich** | Таблицы, подсветка, цветные логи | Интерфейс |
| 3 | **Humanize** | Человекочитаемые размеры/время | Интерфейс |
| 4 | **sh** | Консольные утилиты как функции | Системное |
| 5 | **Watchdog** | Реакция на события ФС | Системное |
| 6 | **Schedule** | Планировщик задач в коде | Системное |
| 7 | **python-dotenv** | Секреты из `.env` | Архитектура |
| 8 | **Beartype** | Проверка типов в рантайме | Архитектура |
| 9 | **Loguru** | Логирование без настройки | Архитектура |
| 10 | **IceCream** | Удобный дебаг вместо `print()` | Архитектура |

---

## 🚀 Установка всего сразу

```bash
pip install tqdm rich humanize sh watchdog schedule python-dotenv beartype loguru icecream
```

---

## 🎯 Когда что использовать

- **Визуализация:** `tqdm` + `Rich` — прогресс и красивый вывод.
- **Системные задачи:** `sh` + `Watchdog` — вызовы команд и слежение за файлами.
- **Порядок в архитектуре:** `Loguru` + `python-dotenv` — логи и секреты.
- **Дебаг:** `IceCream` — быстрая отладка без `print()`.
- **Надёжность:** `Beartype` — проверка типов без потерь скорости.

> Умение автоматизировать заключается в выборе правильного инструмента, превращающего сложную задачу в простую.

---

*Источник: [Хабр — 10 полезных Python-библиотек](https://habr.com/ru/articles/983158/)*

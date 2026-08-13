# 🐍 Python: 14 интересных фич

> Возможности языка, которые делают код выразительнее: типизация, синтаксис, производительность и «глубокая магия». Часть фич — не совсем pythonic, но знать их полезно. Источник: [Хабр — ruvds](https://habr.com/ru/companies/ruvds/articles/905832/).

**Идея:** Python давно вышел за рамки простого скриптового языка. Современные версии (3.10–3.12) принесли нативные дженерики, сопоставление с образцом, протоколы и перегрузки. Ниже — 14 фич, которые стоит держать под рукой.

---

## Часть 1. Типизация

Аннотации типов делают код самодокументируемым и ловят ошибки до запуска.

### 1. Перегрузка типизации (`@overload`)

Декоратор `@overload` из `typing` задаёт несколько сигнатур для одной функции — статический анализатор понимает, какой тип вернётся при разных аргументах.

```python
from typing import overload, Literal

@overload
def process(data: str, mode: Literal["upper"]) -> str: ...
@overload
def process(data: str, mode: Literal["split"]) -> list[str]: ...

def process(data: str, mode: str):
    if mode == "upper":
        return data.upper()       # list[str] в одной ветке, str в другой
    return data.split()
```

`Literal` работает как облегчённая версия `Enum` — разрешает только заданные строковые значения. А синтаксис `...` в теле `@overload` помечает параметр как опциональный, но требующий значения.

---

### 2. Только именованные и только позиционные аргументы

Жёстко задать способ передачи аргументов — особенно полезно при проектировании API.

- `*` — всё после него **только по имени** (keyword-only).
- `/` — всё до него **только по позиции** (positional-only).

```python
def foo(a, b, /, c, d, *, e, f):
    ...

foo(1, 2, 3, d=4, e=5, f=6)   # OK
foo(1, 2, c=3, d=4, e=5, f=6) # OK
# foo(a=1, b=2, ...)           # ❌ a, b — только позиционные
# foo(1, 2, 3, 4, 5, 6)        # ❌ e, f — только именованные
```

Здесь `a`, `b` — позиционные, `e`, `f` — именованные, `c`, `d` — как угодно.

---

### 3. Future-аннотации (`from __future__ import annotations`)

Откладывает вычисление типов: аннотации превращаются в строки и разбираются только статическим анализатором. Решает проблему прямых ссылок (класс ссылается на самого себя до определения).

```python
from __future__ import annotations

class Node:
    def __init__(self, value: int, parent: Node | None = None):
        #                    ^^^^^^^^^^ без future это NameError
        self.value = value
        self.parent = parent
```

> ⚠️ **Минус:** библиотеки, читающие типы в рантайме (ORM, валидаторы), получат строки вместо классов. С Python 3.14 (PEP 649) появится ленивое вычисление через дескрипторы, а с 3.11 для ссылки на свой класс можно использовать `Self`.

---

### 4. Дженерики (PEP 695, Python 3.12)

Нативный синтаксис дженериков заменил громоздкий `TypeVar`:

```python
# Раньше: T = TypeVar("T"); class Box(Generic[T]): ...
class Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value

# С ограничениями и variadic-параметрами
class Foo[UnBounded, Bounded: int, Constrained: int | float]: ...

class Tuple[*Ts]:        # произвольное число типов
    ...

# Псевдоним типа одной строкой (вместо TypeAlias)
type Vector = list[float]
```

---

### 5. Протоколы (Structural Subtyping)

Типизация «утиной» типизации: протокол описывает **поведение**, а не наследование. Если у класса есть нужные методы — он подходит.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

class Button:            # ничего не наследует от Renderable
    def render(self) -> str:
        return "[OK]"

print(isinstance(Button(), Renderable))  # True (благодаря @runtime_checkable)
```

Протоколы отвечают на вопрос «что объект **умеет делать**», а не «чем он **является**».

---

## Часть 2. Синтаксис и структуры

### 6. Менеджеры контекста (`@contextlib.contextmanager`)

Вместо класса с `__enter__`/`__exit__` — генератор с `yield`: до `yield` подготовка, после — очистка.

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield                       # управление в блок with
    finally:
        print(f"{label}: {time.perf_counter() - start:.3f}s")

with timer("обработка"):
    sum(range(1_000_000))
```

---

### 7. Сопоставление с образцом (`match-case`, Python 3.10)

Продвинутый `switch`, сила которого — в **деструктуризации**. Оператор `|` объединяет паттерны, `if` добавляет условие, а `:=` (морж) захватывает значение прямо в шаблоне.

```python
def describe(cmd):
    match cmd:
        case ["go", direction] if direction in ("nord", "south"):
            return f"Идём на {direction}"
        case ["take", item]:          # распаковка списка
            return f"Берём {item}"
        case [first, *middle, last]:  # первый, середина, последний
            return f"{first} ... ({len(middle)} шт.) ... {last}"
        case {"type": "exit", "code": c}:
            return f"Выход {c}"
        case _:
            return "Не понял"
```

---

### 8. Слоты (`__slots__`)

Фиксирует набор атрибутов класса. Вместо `__dict__` (хэш-таблица) используется массивоподобная структура — доступ за O(1) и серьёзная экономия памяти.

```python
class Point:
    __slots__ = ("x", "y")           # только эти два атрибута

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p = Point(1, 2)
# p.z = 3   # ❌ AttributeError — динамически добавить нельзя
```

> Побочный эффект: пропадает возможность навешивать произвольные атрибуты и `__dict__`. Зато миллион таких объектов съест в разы меньше RAM.

---

### 9. Синтаксические мелочи

Несколько коротких, но ценных приёмов:

```python
# for-else: else сработает, только если цикл НЕ прерван break
for n in [3, 7, 2]:
    if n < 0:
        break
else:
    print("Отрицательных не было")

# Моржовый оператор := — присваивание внутри выражения
if (text := input()).startswith("/"):
    print("команда:", text)

# Короткая схема or — первый истинный или значение по умолчанию
display_name = username or full_name or "Anonymous"

# Цепочки сравнений вместо 0 < x and x < 10
if 0 < x < 10:
    ...
```

---

## Часть 3. Производительность и concurrency

### 10. Расширенное форматирование f-строк

Помимо вставки переменных, f-строки поддерживают Format Mini-Language:

```python
name = "score"
big_num = 1_234_567
progress = 0.876
val = 3.14159

print(f"{name=}")            # name='score'   — имя и значение сразу
print(f"{big_num:,}")        # 1,234,567      — разделитель тысяч
print(f"{progress:.1%}")     # 87.6%          — проценты
print(f"{val:+.2f}")         # +3.14          — флаг знака
print(f"{'заголовок':_^30}") # ______заголовок______  выравнивание
```

---

### 11. `cache` / `lru_cache`

Мемоизация результатов функции одной строкой. `@cache` (Python 3.9+) — это `@lru_cache(maxsize=None)`.

```python
from functools import cache, lru_cache

@cache
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=128)      # ограниченный кэш
def heavy(x: int) -> int:
    ...

fib(200)   # мгновенно, хотя без кэша — экспоненциальный взрыв
```

---

### 12. Python Futures

Объекты `Future` из `concurrent.futures` и `asyncio` — аналог `Promise` в JS: можно задать результат, навесить колбэк, дождаться с таймаутом.

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as pool:
    future = pool.submit(sum, range(1_000_000))  # возвращает Future
    future.add_done_callback(lambda f: print("готово"))
    result = future.result(timeout=5)            # ждём с таймаутом
```

В `asyncio` то же самое — `loop.create_future()`, `set_result()`, `set_exception()`.

---

## Часть 4. Глубокая магия

### 13. Прокси-свойства (Descriptor Protocol)

Через `__get__`/`__set__` можно сделать атрибут, который ведёт себя и как свойство (при `obj.value`), и как метод (при `obj.value(7)`).

```python
class ProxyProperty:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._name, None)

    def __call__(self, obj, value):       # вызов как метода
        setattr(obj, self._name, value)

class Config:
    value = ProxyProperty()

c = Config()
# c.value            → свойство (чтение)
# c.value(c, 42)     → запись через вызов
```

> Это концептуальная реализация. Для продакшена лучше взять готовое — например, `ProxyProperty` из библиотеки Codegen.

---

### 14. Метаклассы

Метакласс — это то, что **создаёт классы** (ведь классы сами по себе объекты). По умолчанию это `type`. Метакласс позволяет вмешаться в создание: модифицировать атрибуты, зарегистрировать класс.

```python
class Doubler(type):
    def __new__(mcs, name, bases, namespace):
        # удвоим все целочисленные значения-атрибуты
        for key, val in list(namespace.items()):
            if isinstance(val, int) and not key.startswith("__"):
                namespace[key] = val * 2
        return super().__new__(mcs, name, bases, namespace)

class Settings(metaclass=Doubler):
    width = 100
    height = 50

print(Settings.width)    # 200
```

> 🧙 **99% случаев метаклассы не нужны.** Ту же задачу обычно решает обычный декоратор. Как говорил Тим Питерс: *«Метаклассы — это такая глубокая магия, что 99% пользователей не стоит о ней думать».*

---

## 📊 Сводная таблица

| # | Фича | Версия | Назначение |
|---|---|---|---|
| 1 | `@overload` | 3.5+ | Несколько сигнатур одной функции |
| 2 | `/` и `*` в сигнатуре | 3.8+ | Позиционные / именованные аргументы |
| 3 | `from __future__ import annotations` | 3.7+ | Отложенные аннотации |
| 4 | Дженерики `class Foo[T]` | **3.12** | Нативный синтаксис PEP 695 |
| 5 | `Protocol` | 3.8+ | Структурная типизация |
| 6 | `@contextmanager` | stdlib | Контекст-менеджер через генератор |
| 7 | `match-case` | **3.10** | Сопоставление с образцом |
| 8 | `__slots__` | stdlib | Экономия памяти, фиксация атрибутов |
| 9 | `for-else`, `:=`, цепочки | stdlib | Синтаксические мелочи |
| 10 | f-string Mini-Language | 3.6+ | Тонкое форматирование |
| 11 | `@cache` | 3.9+ | Мемоизация |
| 12 | `Future` | stdlib | Асинхронные результаты |
| 13 | Descriptor Protocol | stdlib | Гибрид свойство+метод |
| 14 | Метаклассы | stdlib | Кастомизация создания классов |

---

## 🎯 Когда что применять

- **Типизация:** `@overload` + `Protocol` + PEP 695 дженерики — выразительные контракты.
- **API:** `/` и `*` фиксируют способ вызова и не дают сломать код рефакторингом.
- **Чистый код:** `@contextmanager` и `match-case` заменяют десятки строк boilerplate.
- **Память:** `__slots__` для миллионов легковесных объектов.
- **Скорость:** `@cache` на чистых функциях и тяжёлой рекурсии.
- **Глубокая магия:** метаклассы и кастомные дескрипторы — только когда декоратор реально не справляется.

> Язык должен работать на тебя, а не ты на него. Эти фичи — инструменты, а не цель: бери то, что делает код проще.

---

*Источник: [Хабр — ruvds: 14 интересных фич Python](https://habr.com/ru/companies/ruvds/articles/905832/)*

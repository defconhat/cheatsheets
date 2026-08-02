# 🐍 Python — шпаргалка по языку и стандартной библиотеке

> **Python** — высокоуровневый язык общего назначения.
> Документация: https://docs.python.org · Учебник: https://docs.python.org/3/tutorial
>
> Философия: `import this` (The Zen of Python). Код должен быть читаемым.

---

## 🚀 Запуск и окружение

| Команда | Действие |
|---|---|
| `python file.py` | Запустить скрипт |
| `python -V` / `python --version` | Версия |
| `python -c "print(1+1)"` | Выполнить строку |
| `python -i` | Интерактивный REPL |
| `python -m http.server 8000` | Локальный HTTP-сервер |
| `python -m pdb file.py` | Запустить под отладчиком |
| `python -m venv .venv` | Создать виртуальное окружение |
| `python -m pip install pkg` | Установить пакет |
| `python -m json.tool file.json` | Красиво отформатировать JSON |
| `python -m http.server` / `smtpd` / `telnetlib` | Встроенные модули-серверы |

### Виртуальные окружения
```bash
# Стандартное (venv)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
deactivate

# uv (современный, в 10-100× быстрее) — РЕКОМЕНДУЕТСЯ
uv venv
uv pip install requests
uv pip install -r requirements.txt
uv pip freeze > requirements.txt
uv run script.py                 # авто-создание окружения
```

### Менеджеры пакетов и зависимости
```bash
# pip
pip install requests==2.31.0
pip install "django>=4.0,<5.0"
pip install -r requirements.txt
pip install -e .                 # установить локальный пакет (editable)
pip uninstall requests
pip list
pip show requests
pip freeze > requirements.txt
pip check                        # проверить зависимости

# uv (быстрее)
uv pip install requests
uv pip compile requirements.in   # в requirements.txt с lock-файлами
uv pip sync requirements.txt     # установить ровно как в файле

# poetry (для проектов)
poetry init
poetry add requests
poetry install
poetry run python script.py

# pipx (для CLI-утилит)
pipx install black
pipx install ruff
```

### pyproject.toml (современный стандарт)
```toml
[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["requests>=2.31", "rich>=13.0"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## 🔤 Типы данных

### Неизменяемые (immutable)
| Тип | Пример | Описание |
|---|---|---|
| `int` | `42`, `0b1010`, `0xFF`, `1_000_000` | Целое (произвольной длины) |
| `float` | `3.14`, `2e10`, `1.5e-3` | С плавающей точкой |
| `complex` | `3+4j` | Комплексное |
| `bool` | `True`, `False` | Логическое (подтип int) |
| `str` | `"hello"`, `'hi'` | Строка (Unicode) |
| `tuple` | `(1, 2, 3)` | Кортеж |
| `frozenset` | `frozenset({1,2})` | Неизменяемое множество |
| `bytes` | `b"data"` | Байты |
| `NoneType` | `None` | Отсутствие значения |

### Изменяемые (mutable)
| Тип | Пример | Описание |
|---|---|---|
| `list` | `[1, 2, 3]` | Список |
| `dict` | `{"a": 1}` | Словарь |
| `set` | `{1, 2, 3}` | Множество |
| `bytearray` | `bytearray(b"x")` | Изменяемые байты |

### Проверки и преобразования
```python
type(42)                # <class 'int'>
isinstance(42, int)     # True
isinstance(42, (int, float))  # несколько типов

int("42")        # 42
int("ff", 16)    # 255
float("3.14")    # 3.14
str(42)          # "42"
bool(0)          # False (0, "", [], {}, None — falsy)
list("abc")      # ['a', 'b', 'c']
tuple([1,2])     # (1, 2)
set([1,1,2])     # {1, 2}
dict([("a",1)])  # {'a': 1}
```

---

## 🔢 Числа

```python
# Арифметика
2 + 3      # 5
7 - 2      # 5
3 * 4      # 12
7 / 2      # 3.5   (всегда float!)
7 // 2     # 3     (целочисленное)
7 % 2      # 1     (остаток)
2 ** 10    # 1024  (степень)
divmod(7, 2)  # (3, 1) — (частное, остаток)
abs(-5)    # 5
round(3.7) # 4
round(3.14159, 2)  # 3.14
pow(2, 10) # 1024
pow(2, 10, 100)    # 24   (2**10 % 100, эффективно)

# Битовые операции
5 & 3      # 1   (AND)
5 | 3      # 7   (OR)
5 ^ 3      # 6   (XOR)
~5         # -6  (NOT)
1 << 4     # 16  (сдвиг влево)
256 >> 2   # 64  (сдвиг вправо)
bin(10)    # '0b1010'
hex(255)   # '0xff'
oct(8)     # '0o10'
int('0xff', 16)  # 255
```

### math и decimal
```python
import math
math.pi            # 3.141592...
math.e             # 2.71828...
math.sqrt(16)      # 4.0
math.log(100, 10)  # 2.0
math.log2(8)       # 3.0
math.ceil(3.1)     # 4
math.floor(3.9)    # 3
math.gcd(12, 8)    # 4
math.lcm(4, 6)     # 12  (3.9+)
math.factorial(5)  # 120
math.inf, math.nan # бесконечность, NaN
math.isfinite(x), math.isnan(x)

# Десятичные (для денег!)
from decimal import Decimal, getcontext
Decimal("0.1") + Decimal("0.2")   # Decimal('0.3') — точно!
getcontext().prec = 28

# Дроби
from fractions import Fraction
Fraction(1, 3) + Fraction(1, 6)   # Fraction('1', '2')
```

---

## 📝 Строки

```python
s = "Hello, World"

# Доступ и срезы
s[0]            # 'H'   (первый)
s[-1]           # 'd'   (последний)
s[0:5]          # 'Hello'   (срез 0..4)
s[7:]           # 'World'
s[:5]           # 'Hello'
s[::-1]         # 'dlroW ,olleH'  (реверс)
s[::2]          # 'HloWrd'   (каждый 2-й)

# Длина и проверки
len(s)                       # 13
"hello".upper()              # 'HELLO'
"HELLO".lower()              # 'hello'
"Hello".capitalize()         # 'Hello'
"hello world".title()        # 'Hello World'
"  hi  ".strip()             # 'hi'   (lstrip, rstrip)
"aaa".center(10, '-')        # '---aaa----'
"42".zfill(5)                # '00042'

# Поиск и замена
"hello".find("l")            # 2 (индекс или -1)
"hello".rfind("l")           # 3
"hello".count("l")           # 2
"hello".replace("l", "L")    # 'heLLo'
"hello".startswith("he")     # True
"hello".endswith("lo")       # True
"a,b,c".split(",")           # ['a', 'b', 'c']
"a, b, c".split(", ")        # ['a', 'b', 'c']
",".join(["a","b","c"])      # 'a,b,c'
"hello world".partition(" ") # ('hello', ' ', 'world')

# Проверка содержимого
"123".isdigit()              # True
"abc".isalpha()              # True
"abc123".isalnum()           # True
"ABC".isupper()              # True
"  ".isspace()              # True
```

### Форматирование строк
```python
name, age = "Alice", 30

# f-strings (рекомендуется, 3.6+)
f"Hello, {name}! You are {age}."
f"{2 + 2 = }"                  # '2 + 2 = 4'   (3.8+)
f"{name:>10}"                  # '     Alice'  (выравнивание вправо)
f"{name:<10}"                  # 'Alice     '  (влево)
f"{name:^10}"                  # '  Alice   '  (центр)
f"{3.14159:.2f}"               # '3.14'
f"{255:x}"                     # 'ff'         (hex)
f"{255:b}"                     # '11111111'   (bin)
f"{1000000:,}"                 # '1,000,000'  (разделители)
f"{0.15:.1%}"                  # '15.0%'      (проценты)
f"{'':-^20}"                   # '--------------------'

# f-string с выражением (3.12+)
items = [1, 2, 3]
f"sum = {sum(items)}"

# str.format() (старый способ)
"{} {}".format("Hello", "World")
"{0} {1} {0}".format("a", "b")     # 'a b a'
"{name}".format(name="Alice")

# % форматирование (самый старый, избегать)
"%s %d" % ("Alice", 30)
```

### f-string datetime
```python
import datetime
now = datetime.datetime.now()
f"{now:%Y-%m-%d %H:%M:%S}"   # '2024-01-15 14:30:00'
f"{now:%d.%m.%Y}"            # '15.01.2024'
```

---

## 📋 Списки (list)

```python
lst = [1, 2, 3, 4, 5]

# Доступ
lst[0]            # 1
lst[-1]           # 5
lst[1:3]          # [2, 3]
lst[::-1]         # [5, 4, 3, 2, 1]  (реверс)

# Изменение
lst.append(6)         # [1, 2, 3, 4, 5, 6]
lst.insert(0, 0)      # [0, 1, 2, 3, 4, 5, 6]
lst.extend([7, 8])    # добавить несколько
lst += [9, 10]        # то же самое
lst.pop()             # 10 (удалить и вернуть последний)
lst.pop(0)            # 0 (удалить по индексу)
lst.remove(3)         # удалить первое вхождение значения
del lst[0]            # удалить по индексу
lst.clear()           # очистить

# Поиск
lst.index(3)          # индекс значения (или ValueError)
lst.count(2)          # сколько раз встречается
3 in lst              # True/False

# Сортировка
lst.sort()            # на месте (in-place)
lst.sort(reverse=True)
lst.sort(key=lambda x: -x)
lst.sort(key=len)     # по длине (для строк)
sorted(lst)           # вернуть новый отсортированный
sorted(lst, reverse=True)

# Прочее
lst.reverse()         # на месте
list(reversed(lst))   # вернуть новый
len(lst)
min(lst), max(lst), sum(lst)
any(lst), all(lst)    # True если хотя бы один / все True
```

### List comprehension
```python
# Базовое
[x**2 for x in range(10)]
[x for x in range(20) if x % 2 == 0]      # с условием
[x if x > 0 else 0 for x in numbers]      # тернарный

# Вложенные
[(x, y) for x in range(3) for y in range(3)]
[[0 for _ in range(cols)] for _ in range(rows)]  # матрица

# С функцией
[word.upper() for word in "hello world".split()]
[len(w) for w in words]

# С распаковкой (3.8+)
[(x, y, x*y) for x, y in pairs]

# Сложное
{x: len(x) for x in words}      # dict comprehension
{c for c in "hello"}            # set comprehension
```

---

## 📚 Кортежи (tuple)

```python
# Неизменяемые последовательности
t = (1, 2, 3)
t = 1, 2, 3        # скобки опциональны
t = ()             # пустой
t = (1,)           # кортеж из одного элемента (запятая!)

# Доступ как у списка
t[0], t[-1], t[1:3]

# Упаковка/распаковка
point = (10, 20)
x, y = point           # распаковка
x, y = y, x            # обмен значениями
a, *rest = [1, 2, 3, 4]   # a=1, rest=[2,3,4]
first, *, last = [1, 2, 3, 4]  # first=1, last=4

# Named tuples (именованные кортежи)
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
p.x, p.y               # 10, 20

# typing.NamedTuple (с типами)
from typing import NamedTuple
class Point(NamedTuple):
    x: int
    y: int
    label: str = "origin"
```

---

## 📖 Словари (dict)

```python
d = {"name": "Alice", "age": 30}

# Доступ
d["name"]              # 'Alice'
d.get("name")          # 'Alice'
d.get("email")         # None (без KeyError)
d.get("email", "n/a")  # 'n/a' (значение по умолчанию)
d.keys()               # dict_keys(['name', 'age'])
d.values()             # dict_values(['Alice', 30])
d.items()              # dict_items([('name', 'Alice'), ...])

# Изменение
d["email"] = "a@x.com"      # добавить/изменить
d.update({"age": 31, "city": "NYC"})
d.setdefault("phone", "000")  # добавить если нет
del d["email"]               # удалить
d.pop("city")                # удалить и вернуть
d.popitem()                  # удалить и вернуть последнее (3.7+)

# Проверка
"name" in d                  # True

# Перебор
for key in d: ...            # ключи
for k, v in d.items(): ...   # пары

# Dict comprehension
{v: k for k, v in d.items()}        # обратный словарь
{x: x**2 for x in range(10)}        # квадраты
{c: s.count(c) for c in set(s)}     # частоты символов
```

### Специальные словари
```python
from collections import defaultdict, OrderedDict, Counter, ChainMap

# defaultdict — значение по умолчанию
words = ["a", "b", "a", "c", "b", "a"]
counts = defaultdict(int)
for w in words: counts[w] += 1    # нет KeyError
# defaultdict(<class 'int'>, {'a': 3, 'b': 2, 'c': 1})

groups = defaultdict(list)
groups["fruits"].append("apple")

# Counter — подсчёт
c = Counter("abracadabra")
c.most_common(3)         # [('a', 5), ('b', 2), ('r', 2)]
c.update("xxx")          # добавить
c.subtract({"a": 1})     # вычесть
c.most_common()

# OrderedDict (с 3.7 обычный dict помнит порядок)
# Но у OrderedDict есть move_to_end, popitem(last=False)
od = OrderedDict()
od.move_to_end("key")

# ChainMap — объединение словарей
defaults = {"color": "red", "size": 10}
user = {"color": "blue"}
merged = ChainMap(user, defaults)
merged["color"]   # 'blue' (из user)
```

---

## 🎯 Множества (set)

```python
s = {1, 2, 3}
s = set([1, 2, 2, 3])   # {1, 2, 3} (уникальные)

s.add(4)
s.update([5, 6])
s.remove(4)         # KeyError если нет
s.discard(4)        # безопасно (без ошибки)
s.pop()             # случайный элемент
s.clear()

# Операции (как в математике)
a = {1, 2, 3}
b = {3, 4, 5}
a | b              # {1, 2, 3, 4, 5}   объединение (union)
a & b              # {3}                пересечение (intersection)
a - b              # {1, 2}             разность (difference)
a ^ b              # {1, 2, 4, 5}       симметрическая разность
a <= b             # False              подмножество
a.issubset(b), a.issuperset(b), a.isdisjoint(b)

# Уникальные элементы списка
list(set([1, 1, 2, 3, 3]))   # [1, 2, 3]  (порядок не сохраняется!)

# frozenset — неизменяемое множество (хешируемое, можно ключом)
fs = frozenset({1, 2, 3})
```

---

## 🔀 Управляющие конструкции

### if / elif / else
```python
if age < 18:
    print("minor")
elif age == 18:
    print("exactly 18")
else:
    print("adult")

# Тернарный (условное выражение)
status = "adult" if age >= 18 else "minor"

# walrus operator (3.8+) — присваивание в условии
if (n := len(data)) > 10:
    print(f"Long data: {n}")
```

### Циклы
```python
# for
for i in range(5): print(i)        # 0 1 2 3 4
for i in range(2, 10): ...          # 2..9
for i in range(0, 10, 2): ...       # 0 2 4 6 8
for c in "hello": print(c)
for k, v in d.items(): ...
for i, x in enumerate(lst): ...     # с индексом
for a, b in zip(lst1, lst2): ...    # параллельно

# while
while condition: ...
while True:
    if done: break
    if skip: continue

# else выполняется, если цикл завершился без break
for n in range(2, 100):
    for i in range(2, n):
        if n % i == 0: break
    else:
        print(f"{n} — простое")
```

### Полезные итераторы
```python
# enumerate — индекс + значение
for i, x in enumerate(lst, start=1):
    print(i, x)

# zip — параллельный перебор
for name, age in zip(names, ages): ...
list(zip([1,2,3], ["a","b","c"]))    # [(1,'a'), (2,'b'), (3,'c')]
# zip_longest — до самого длинного
from itertools import zip_longest
list(zip_longest([1,2,3], [4,5], fillvalue=0))

# itertools — мощный модуль
from itertools import chain, product, combinations, permutations, groupby
list(chain([1,2], [3,4]))            # [1,2,3,4]
list(product("AB", "12"))            # [('A','1'),('A','2'),('B','1'),('B','2')]
list(combinations("ABC", 2))         # [('A','B'),('A','C'),('B','C')]
list(permutations("ABC", 2))         # все перестановки
list(groupby(sorted(data, key=...), key=...))
```

---

## 🧮 Функции

```python
# Обычная
def greet(name):
    return f"Hello, {name}"

# Значения по умолчанию
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

# Именованные аргументы
greet(name="Alice", greeting="Hi")

# *args — произвольное число позиционных
def sum_all(*args):
    return sum(args)
sum_all(1, 2, 3)       # 6

# **kwargs — произвольное число именованных
def config(**kwargs):
    for k, v in kwargs.items():
        print(f"{k} = {v}")
config(debug=True, port=8080)

# Распаковка при вызове
args = (1, 2, 3)
func(*args)
kwargs = {"a": 1, "b": 2}
func(**kwargs)

# Только позиционные / только ключевые (3.8+)
def f(a, b, /, c, d, *, e, f): ...   # a,b — только позиционные; e,f — только ключевые

# Аннотации типов
def add(a: int, b: int) -> int:
    return a + b

# Возврат нескольких значений (через кортеж)
def minmax(lst):
    return min(lst), max(lst)
lo, hi = minmax([3, 1, 4, 1, 5])

# Лямбды (анонимные)
square = lambda x: x**2
sorted(lst, key=lambda x: x.name)
sorted(lst, key=lambda x: (x.age, x.name))  # по нескольким полям
```

### Замыкания и декораторы
```python
# Замыкание
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply
double = make_multiplier(2)
double(5)   # 10

# Декоратор
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper

@log
def greet(name):
    print(f"Hello, {name}")

# С аргументами
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hi(): print("hi")

# functools.wraps — сохранить метаданные
from functools import wraps
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 📦 Классы и ООП

```python
class Animal:
    # Атрибут класса (общий для всех)
    species = "Unknown"

    def __init__(self, name, age):
        self.name = name        # атрибут экземпляра
        self.age = age
        self._private = "h"     # конвенция: защищённое
        self.__secret = "x"     # name mangling: _ClassName__secret

    # Строковое представление
    def __str__(self):
        return f"{self.name}, {self.age} years"

    def __repr__(self):
        return f"Animal(name={self.name!r}, age={self.age})"

    # Метод экземпляра
    def speak(self):
        return "..."

    # Метод класса
    @classmethod
    def create_baby(cls, name):
        return cls(name, 0)

    # Статический метод
    @staticmethod
    def is_valid_age(age):
        return age >= 0

    # property — геттер/сеттер
    @property
    def human_age(self):
        return self.age * 7

    @human_age.setter
    def human_age(self, value):
        self.age = value // 7


# Наследование
class Dog(Animal):
    species = "Canine"

    def __init__(self, name, age, breed):
        super().__init__(name, age)   # вызов родителя
        self.breed = breed

    def speak(self):                  # переопределение
        return "Woof!"

    def fetch(self):                  # новый метод
        return f"{self.name} fetches!"


dog = Dog("Rex", 3, "Lab")
dog.speak()           # 'Woof!'
dog.fetch()           # 'Rex fetches!'
isinstance(dog, Animal)   # True


# Dataclasses (3.7+) — автоматически генерирует __init__, __repr__, __eq__
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = "point"
    tags: list = field(default_factory=list)

    def distance_to(self, other):
        return ((self.x-other.x)**2 + (self.y-other.y)**2)**0.5

p = Point(1.0, 2.0)
```

### Магические методы (dunder)
| Метод | Назначение |
|---|---|
| `__init__` | Конструктор |
| `__str__` | `str(obj)`, `print(obj)` |
| `__repr__` |_repr(obj)`, отладка |
| `__len__`, `__getitem__`, `__setitem__` | `len()`, `obj[k]` |
| `__iter__`, `__next__` | итерация |
| `__contains__` | `x in obj` |
| `__eq__`, `__lt__`, `__hash__` | сравнение, хеширование |
| `__add__`, `__mul__`, ... | арифметика |
| `__enter__`, `__exit__` | context manager (`with`) |
| `__call__` | `obj()` — вызов как функции |
| `__getattr__`, `__setattr__` | доступ к атрибутам |

---

## 📨 Исключения

```python
# Базовая конструкция
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Ошибка: {e}")
except (ValueError, TypeError) as e:
    print(f"Другая: {e}")
except Exception as e:        # ловушка всего
    print(f"Неизвестная: {e}")
else:
    print("Без ошибок")       # если не было исключения
finally:
    print("Всегда")           # выполняется всегда

# Возбуждение
raise ValueError("invalid value")
raise ValueError("msg") from original_exception   # цепочка

# Свой класс исключения
class MyError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

# Утверждения
assert x > 0, "x must be positive"

# Общие исключения
# ValueError, TypeError, KeyError, IndexError, AttributeError
# FileNotFoundError, PermissionError, RuntimeError
# StopIteration, NotImplementedError, ImportError
```

---

## 📁 Работа с файлами

```python
# Чтение
with open("file.txt") as f:        # 'r' по умолчанию
    content = f.read()             # весь файл строкой

with open("file.txt") as f:
    for line in f:                 # построчно (память эффективно)
        process(line)

lines = f.readlines()              # список строк
line = f.readline()                # одна строка

# Запись
with open("out.txt", "w") as f:    # 'w' — перезапись
    f.write("text\n")
    f.writelines(["a\n", "b\n"])

with open("log.txt", "a") as f:    # 'a' — дописать
    f.write("new line\n")

# Кодировка (ВСЕГДА указывайте явно!)
with open("file.txt", encoding="utf-8") as f: ...

# Бинарные файлы
with open("image.png", "rb") as f:    # read binary
    data = f.read()
with open("out.bin", "wb") as f:
    f.write(b"\x00\x01")
```

### pathlib — современная работа с путями
```python
from pathlib import Path

p = Path("/home/user/docs/file.txt")
p.name          # 'file.txt'
p.stem          # 'file'
p.suffix        # '.txt'
p.parent        # PosixPath('/home/user/docs')
p.parts         # ('/', 'home', 'user', 'docs', 'file.txt')

p.exists()      # True/False
p.is_file(), p.is_dir()
p.mkdir(parents=True, exist_ok=True)   # создать каталог
p.touch()                              # создать пустой файл
p.unlink()                             # удалить файл
p.rename("newname.txt")
p.resolve()                            # абсолютный путь

# Glob
list(Path(".").glob("*.py"))
list(Path(".").rglob("*.py"))          # рекурсивно
sorted(Path("src").glob("**/*.py"))

# Читать/писать через pathlib
text = p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")
bytes_data = p.read_bytes()
```

### JSON, CSV, pickle
```python
import json

# JSON
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data, indent=2, ensure_ascii=False)
loaded = json.loads(json_str)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
with open("data.json", encoding="utf-8") as f:
    data = json.load(f)


import csv

# CSV
with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader: print(row)
    # или
    reader = csv.DictReader(f)
    for row in reader: print(row["name"])

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerows([["Alice", 30], ["Bob", 25]])


import pickle
# pickle (только Python, опасно для чужих файлов!)
with open("data.pkl", "wb") as f:
    pickle.dump(obj, f)
with open("data.pkl", "rb") as f:
    obj = pickle.load(f)
```

---

## 📊 Стандартная библиотека (must-know)

### os, sys
```python
import os
os.getcwd()              # текущий каталог
os.chdir("/tmp")         # сменить
os.listdir(".")          # список файлов
os.makedirs("a/b/c", exist_ok=True)
os.remove("file")
os.rmdir("dir")          # пустой
os.rename("old", "new")
os.path.exists, os.path.isfile, os.path.isdir
os.path.join("a", "b")   # 'a/b' (платформонезависимо)
os.path.basename, os.path.dirname
os.path.expanduser("~")  # домашний каталог
os.environ["HOME"]
os.environ.get("MY_VAR", "default")
os.system("ls")          # выполнить команду (просто)

import sys
sys.argv                 # аргументы командной строки
sys.exit(0)              # выйти с кодом
sys.stdin, sys.stdout, sys.stderr
sys.path                 # пути поиска модулей
sys.platform             # 'linux' / 'win32' / 'darwin'
sys.version_info         # версия Python
```

### subprocess — выполнение команд
```python
import subprocess

# Простой запуск
subprocess.run(["ls", "-la"])
subprocess.run("ls -la", shell=True)

# Захват вывода
result = subprocess.run(["echo", "hi"], capture_output=True, text=True)
result.stdout      # 'hi\n'
result.returncode  # 0
result.stderr

# С проверкой кода возврата
subprocess.run(["ls"], check=True)   # raise если не 0

# Pipe между командами
p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "txt"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
out, _ = p2.communicate()
```

### re — регулярные выражения
```python
import re

# Поиск
re.search(r"\d+", "abc123def")     # Match или None
re.match(r"\d+", "123abc")         # только с начала
re.fullmatch(r"\d+", "123")        # вся строка
re.findall(r"\d+", "a1 b22 c333")  # ['1', '22', '333']
re.finditer(r"\d+", text)          # итератор Match

# Замена
re.sub(r"\d+", "#", "a1b2c3")      # 'a#b#c#'
re.sub(r"(\w+)@(\w+)", r"\2/\1", s)  # с группами

# Разделение
re.split(r"[,\s]+", "a, b c,d")    # ['a', 'b', 'c', 'd']

# Группы
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "2024-01-15")
m.group(0)    # '2024-01-15' (всё)
m.group(1)    # '2024'
m.groups()    # ('2024', '01', '15')

# Именованные группы
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", s)
m.group("year")

# Флаги
re.IGNORECASE   # re.I — без учёта регистра
re.MULTILINE    # re.M — ^ и $ на каждой строке
re.DOTALL       # re.S — . включает \n
re.VERBOSE      # re.X — многострочные рег. с комментариями

# Скомпилированное регулярное (быстрее в цикле)
pattern = re.compile(r"\d+")
pattern.findall(text)
```

### datetime
```python
from datetime import datetime, date, time, timedelta, timezone

now = datetime.now()                # локальное время
utcnow = datetime.now(timezone.utc) # с timezone
today = date.today()

# Создание
dt = datetime(2024, 1, 15, 14, 30, 0)
d = date(2024, 1, 15)

# Разбор строки
dt = datetime.strptime("2024-01-15", "%Y-%m-%d")
dt = datetime.fromisoformat("2024-01-15T14:30:00")   # 3.7+

# Форматирование
dt.strftime("%Y-%m-%d %H:%M:%S")
dt.isoformat()                      # '2024-01-15T14:30:00'

# Арифметика
tomorrow = today + timedelta(days=1)
diff = datetime(2024,2,1) - datetime(2024,1,1)   # timedelta(days=31)
diff.days, diff.seconds

# Из timestamp
datetime.fromtimestamp(1700000000)
datetime.now().timestamp()

# Частые форматы strftime
# %Y-%m-%d, %H:%M:%S, %d.%m.%Y, %B (месяц словом), %A (день недели)
```

### collections
```python
from collections import Counter, defaultdict, deque, OrderedDict, namedtuple

# deque — двусторонняя очередь (быстрее list для очереди)
dq = deque([1, 2, 3], maxlen=5)
dq.append(4); dq.appendleft(0)
dq.pop(); dq.popleft()
dq.rotate(2)    # повернуть

# Counter — см. раздел dict
# defaultdict — см. раздел dict
```

### functools, itertools
```python
from functools import lru_cache, reduce, partial, wraps

# lru_cache — кэширование (мемоизация)
@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# reduce — свёртка
reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10

# partial — зафиксировать аргументы
add5 = partial(lambda x, y: x + y, 5)
add5(10)  # 15

from itertools import chain, groupby, count, cycle, repeat, islice, starmap
list(count(10))       # [10, 11, 12, ...] бесконечно
list(islice(count(), 5))   # [0, 1, 2, 3, 4]
```

---

## 🌐 HTTP и сеть

```python
# urllib (встроенный)
from urllib.request import urlopen
from urllib.parse import urlencode

response = urlopen("https://api.github.com")
data = response.read().decode()
print(response.status)

# requests (сторонний, намного удобнее)
import requests
r = requests.get("https://api.github.com")
r.status_code
r.json()             # распарсить JSON
r.text               # как строка
r.headers["Content-Type"]

# POST
r = requests.post(url, json={"key": "value"})
r = requests.post(url, data={"form": "field"})
r = requests.get(url, params={"q": "python"})
r = requests.get(url, headers={"Authorization": "Bearer xxx"})
r = requests.get(url, timeout=10)

# Сессии (cookie, соединения)
with requests.Session() as s:
    s.auth = ("user", "pass")
    r = s.get(url)
```

### asyncio — асинхронное программирование
```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)   # имитация запроса
    return f"data from {url}"

async def main():
    # Параллельно
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )
    print(results)

asyncio.run(main())

# Создать задачу
task = asyncio.create_task(fetch("url"))
result = await task
```

---

## 🧵 Многопоточность и процессы

```python
import threading

# Потоки (для I/O-bound задач)
def worker(name):
    print(f"Worker {name}")

t = threading.Thread(target=worker, args=("A",))
t.start()
t.join()             # дождаться

# concurrent.futures (высокоуровневый API)
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(worker, i) for i in range(10)]
    results = [f.result() for f in futures]

    # или через map
    results = list(executor.map(worker, range(10)))

# ProcessPoolExecutor — для CPU-bound (обходит GIL)
with ProcessPoolExecutor() as executor:
    ...
```

---

## 🧪 Тестирование

```python
# unittest (встроенный)
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_split(self):
        with self.assertRaises(ValueError):
            "hello".split(",")

if __name__ == "__main__":
    unittest.main()


# pytest (сторонний, проще и мощнее)
# test_file.py:
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"

# Фикстуры
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3]

def test_sum(sample_data):
    assert sum(sample_data) == 6

# Параметризация
@pytest.mark.parametrize("input,expected", [
    (1, 1), (2, 4), (3, 9),
])
def test_square(input, expected):
    assert input**2 == expected
```

Запуск pytest:
```bash
pytest                          # все тесты
pytest -v                       # подробно
pytest -k "string"              # по имени
pytest --cov=mypackage          # с покрытием
pytest tests/test_file.py::test_func   # конкретный
```

---

## 📝 type hints (аннотации типов)

```python
from typing import List, Dict, Optional, Union, Tuple, Any, Callable

# Базовые (3.9+ можно использовать встроенные)
def process(items: list[int], config: dict[str, Any]) -> bool: ...

names: list[str] = []
config: dict[str, int] = {}

# Optional — может быть None
def find(key: str) -> Optional[int]:
    return None     # или int

# Union — один из типов
def parse(x: Union[int, str]) -> int: ...
# 3.10+: x: int | str

# Tuple
point: tuple[int, int] = (10, 20)

# Callable
def apply(func: Callable[[int], int], x: int) -> int:
    return func(x)

# TypeVar и Generic
from typing import TypeVar, Generic
T = TypeVar("T")
class Stack(Generic[T]):
    def push(self, item: T) -> None: ...

# TypedDict — типизированный словарь
from typing import TypedDict
class User(TypedDict):
    name: str
    age: int

# Pydantic (сторонний) — валидация данных
from pydantic import BaseModel
class User(BaseModel):
    name: str
    age: int = 0
    email: str | None = None

user = User(name="Alice", age=30)
user.name       # 'Alice' (строка, валидирована)
```

Проверка типов:
```bash
mypy file.py            # проверка типов
mypy --strict .
pyright                 # от Microsoft (быстрее)
```

---

## 🛠️ Линтинг и форматирование

```bash
# ruff — современный линтер+форматер (заменяет flake8, isort, pylint)
uv tool install ruff
ruff check .                # проверить
ruff check --fix .          # исправить
ruff format .               # отформатировать (заменяет black)

# black — форматер (классика)
black file.py
black --line-length 100 .

# isort — сортировка импортов
isort .

# mypy / pyright — проверка типов
mypy file.py

# pre-commit — хуки перед коммитом
pre-commit install
```

### pyproject.toml для ruff
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

---

## 🪤 Частые ошибки и грабли

1. **Изменяемый аргумент по умолчанию** — `def f(x=[])`: список создаётся
   один раз, все вызовы делят его. Используйте `x=None` + `x = []` внутри.
2. **Late binding в замыканиях** — `lambda: i` в цикле возьмёт последнее `i`.
   Используйте `lambda i=i: i`.
3. **`==` vs `is`** — `==` сравнивает значения, `is` — идентичность (тождество).
   `a is None` — правильно, `a == None` — работает, но не идиоматично.
4. **Копирование списков** — `b = a` не копирует, а ссылается. Используйте
   `b = a.copy()`, `b = a[:]`, `b = list(a)`. Для вложенных — `copy.deepcopy()`.
5. **`/` vs `//`** — `7/2 = 3.5`, `7//2 = 3`.
6. **Конкатенация строк в цикле** — медленно. Используйте `"".join(list)`.
7. **`__name__ == "__main__"`** — проверяйте, чтобы код не выполнялся при импорте.
8. **global/nonlocal** — изменяйте внешние переменные осторожно.
9. **f-string с кавычками** — `f"{d['key']}"` работает в 3.12+, иначе разные кавычки.
10. **`Exception` ловит всё** — включая `KeyboardInterrupt`. Ловите конкретные.
11. **`== True`** — избыточно. Пишите `if flag:` вместо `if flag == True:`.
12. **Импорты** — `from module import *` засоряет пространство имён.

---

## 🔗 Полезные ссылки

- Официальная документация: https://docs.python.org/3/
- Учебник: https://docs.python.org/3/tutorial/
- Python Awesome: https://github.com/vinta/awesome-python
- Real Python: https://realpython.com
- Python Tutor (визуализация): https://pythontutor.com
- PEP 8 (стиль): https://peps.python.org/pep-0008/
- uv: https://github.com/astral-sh/uv
- Pydantic: https://docs.pydantic.dev

---

## 💡 Полезные советы

1. **Используйте `uv`** вместо pip/venv — в 10-100 раз быстрее.
2. **`pyproject.toml`** — современный стандарт конфигурации проекта.
3. **ruff** заменяет flake8 + isort + black — один быстрый инструмент.
4. **type hints + mypy** — ловит баги до запуска.
5. **pathlib** вместо `os.path` — удобнее и читаемее.
6. **f-strings** — самый читаемый способ форматирования.
7. **list/dict comprehensions** — питонично и быстро.
8. **`with` (context manager)** — для файлов и ресурсов (закроет автоматически).
9. **enumerate/zip** — вместо ручного индексирования.
10. **`if __name__ == "__main__":`** — в скриптах для запускаемых функций.
11. **dataclasses** — для классов-данных (вместо рутины `__init__`).
12. **pytest** вместо unittest — проще и мощнее.
13. **`__repr__`** — делайте информативным, поможет в отладке.
14. **asyncio** — для I/O-bound (сети), не для CPU-bound.
15. **Не изобретайте велосипед** — сначала проверьте stdlib и PyPI.

---

*Сгенерировано как шпаргалка. Python огромен —
углубляйтесь через https://docs.python.org/3/ и https://peps.python.org/*

# 🔨 Make / CMake — шпаргалка по системам сборки

> **Make** — классическая утилита сборки (описывает зависимости и команды).
> **CMake** — генератор систем сборки (создаёт Makefile/Ninja/VS-проекты из `CMakeLists.txt`).
>
> Документация:
> - Make: https://www.gnu.org/software/make/manual
> - CMake: https://cmake.org/cmake/help/latest

---

# 🛠️ ЧАСТЬ 1. MAKE

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Makefile** | Файл с правилами сборки |
| **target (цель)** | То, что можно собрать (`make all`, `make clean`) |
| **prerequisite (зависимость)** | Файлы/цели, от которых зависит target |
| **recipe (рецепт)** | Команды для сборки target (с TAB!) |
| **variable** | `CC = gcc` |
| **automatic variable** | `$@`, `$<`, `$^` |
| **.PHONY** | Цель, не являющаяся файлом (always run) |

**Главное правило Make**: цель пересобирается, если она старше любой зависимости.

---

## 📝 Структура Makefile

```makefile
# Комментарий

# Переменные
CC = gcc
CFLAGS = -Wall -Wextra -g -O2
LDFLAGS = -lm
TARGET = myapp
SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

# Правило (внимание: TAB перед командой, НЕ пробелы!)
target: prerequisites
<TAB>command1
<TAB>command2

# Первое правило — цель по умолчанию (make без аргументов)
all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $@ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all clean
```

> ⚠️ **КРИТИЧНО**: рецепты (команды) должны начинаться с **TAB**, а не пробелами.
> Самая частая ошибка: `make: *** missing separator. Stop.`

---

## 🚀 Команды make

| Команда | Действие |
|---|---|
| `make` | Собрать первую цель (обычно `all`) |
| `make target` | Собрать конкретную цель |
| `make -j4` | Параллельно (4 процесса) |
| `make -j$(nproc)` | Использовать все ядра |
| `make -f MyMakefile` | Указать файл |
| `make -C dir` | Перейти в каталог и запустить make |
| `make -C dir target` | С конкретной целью |
| `make clean` | Удалить артефакты сборки |
| `make install` | Установить (часто требует sudo) |
| `make -n` / `--dry-run` | Только показать команды, не выполнять |
| `make -t` / `--touch` | Отметить цели как свежие |
| `make -B` / `--always-make` | Принудительно пересобрать |
| `make -d` | Подробный отладочный вывод |
| `make --trace` | Показать порядок выполнения |
| `make VAR=value` | Переопределить переменную |
| `make -p` | База правил (все встроенные) |
| `make help` | (если в Makefile есть цель help) |

### Установка
```bash
# Arch / CachyOS
sudo pacman -S make gcc

# Debian/Ubuntu
sudo apt install build-essential

# macOS (с Xcode Command Line Tools)
xcode-select --install

# Windows: через MSYS2, WSL или Chocolatey
choco install make
```

---

## 🔤 Переменные

```makefile
# Присваивание
CC = gcc               # рекурсивное (ленивое, может быть медленным)
CC := gcc              # простое (немедленное вычисление)
CC ?= gcc              # только если не задана
CC += -O2              # добавить к значению

# Использование
$(CC)                  # разворачивается в значение
${CC}                  # альтернативный синтаксис
$X                     # односимвольное имя (избегайте)

# Встроенные переменные
CC                     # C compiler (по умолчанию cc)
CXX                    # C++ compiler (g++)
CFLAGS                 # флаги C
CXXFLAGS               # флаги C++
LDFLAGS                # флаги линкера
LDLIBS                 # библиотеки
MAKE                   # имя make (для рекурсивных вызовов)
MAKEFLAGS              # флаги для вложенных вызовов

# Переопределение из командной строки (ПРИОРИТЕТ)
make CC=clang CFLAGS="-O3"
```

### Автоматические переменные
| Переменная | Значение |
|---|---|
| `$@` | Имя цели |
| `$<` | Имя первой зависимости |
| `$^` | Все зависимости (без дублей) |
| `$+` | Все зависимости (с дублями) |
| `$?` | Зависимости новее цели |
| `$*` | Stem (без расширения) для pattern rules |
| `$(@D)` | Каталог цели |
| `$(@F)` | Имя файла цели |
| `$$` | Буквальный `$` (для shell-переменных) |
| `$(MAKE)` | Имя make (рекомендуется для рекурсии) |

---

## 🎯 Виды целей

### 1. Файловые цели (связаны с файлами)
```makefile
app: main.o utils.o
	gcc $^ -o $@

main.o: main.c utils.h
	gcc -c $< -o $@

utils.o: utils.c utils.h
	gcc -c $< -o $@
```

### 2. Phony-цели (не файлы)
```makefile
.PHONY: all clean install test

all: app

clean:
	rm -f *.o app

install: app
	install -m 755 app $(DESTDIR)/usr/bin/

test:
	./app --test
```

> `.PHONY` гарантирует, что цель выполнится всегда, даже если есть файл с таким именем.

### 3. Pattern rules (шаблонные правила)
```makefile
# Скомпилировать любой .c → .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Несколько расширений
%.html: %.md
	pandoc $< -o $@

# Stem (для нестандартных)
%: %.in
	sed -e 's/@VERSION@/1.0/g' $< > $@
```

### 4. Static pattern rules (для конкретных файлов)
```makefile
OBJ = main.o utils.o config.o

$(OBJ): %.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```

---

## 🛠️ Функции make

```makefile
# Подстановка значений
SRC = $(wildcard src/*.c)        # все .c в src/
OBJ = $(patsubst src/%.c,build/%.o,$(SRC))   # src/a.c → build/a.o
OBJ = $(SRC:.c=.o)               # короткая форма
OBJ = $(SRC:%.c=%.o)             # явная форма

# Текстовые функции
$(strip $(VAR))                  # убрать пробелы
$(subst from,to,text)            # замена
$(patsubst %.c,%.o,$(SRC))       # по шаблону
$(filter %.c,$(FILES))           # только .c
$(filter-out %.h,$(FILES))       # всё кроме .h
$(words $(LIST))                 # число слов
$(word 2,$(LIST))                # 2-е слово
$(firstword $(LIST))
$(sort $(LIST))                  # уникальные отсортированные

# Пути
$(dir src/a.c)                   # src/
$(notdir src/a.c)                # a.c
$(basename src/a.c)              # src/a
$(suffix src/a.c)                # .c
$(addprefix build/,$(OBJ))       # добавить префикс
$(addsuffix .o,$(BASES))         # добавить суффикс
$(abspath ./file)                # абсолютный путь
$(realpath file)                 # реальный путь (resolve symlinks)

# Shell
$(shell date +%Y)                # вывод команды
$(shell pwd)
TODAY := $(shell date +%Y-%m-%d)

# Условия
ifeq ($(CC),gcc)
    CFLAGS += -std=c11
else ifeq ($(CC),clang)
    CFLAGS += -std=c11
else
    $(error Unknown compiler $(CC))
endif

ifneq ($(DEBUG),)
    CFLAGS += -g -O0
endif

ifdef VERBOSE
    Q =
else
    Q = @
endif

# Цикл
DIRS := a b c
dirs:
	@for d in $(DIRS); do echo $$d; done

# foreach
LIBS = $(foreach dir,$(DIRS),$(dir)/lib.a)
```

---

## 📦 Полный пример Makefile для C-проекта

```makefile
# ── Конфигурация ─────────────────────────────────────
CC      := gcc
CFLAGS  := -Wall -Wextra -Werror -std=c11 -g
LDFLAGS := -lm
PREFIX  ?= /usr/local

# ── Файлы ────────────────────────────────────────────
SRC_DIR  := src
BUILD_DIR:= build
BIN      := myapp

SRC := $(wildcard $(SRC_DIR)/*.c)
OBJ := $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRC))
DEP := $(OBJ:.o=.d)

# ── Цели ─────────────────────────────────────────────
.PHONY: all clean install uninstall run test help

all: $(BUILD_DIR)/$(BIN)

$(BUILD_DIR)/$(BIN): $(OBJ)
	@mkdir -p $(@D)
	$(CC) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

-include $(DEP)        # авто-зависимости

run: all
	./$(BUILD_DIR)/$(BIN)

test: all
	./$(BUILD_DIR)/$(BIN) --test

clean:
	rm -rf $(BUILD_DIR)

install: all
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(BUILD_DIR)/$(BIN) $(DESTDIR)$(PREFIX)/bin/

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/$(BIN)

help:
	@echo "Targets:"
	@echo "  all       - build $(BIN) (default)"
	@echo "  run       - build and run"
	@echo "  test      - run tests"
	@echo "  clean     - remove build artifacts"
	@echo "  install   - install to $(PREFIX)"
	@echo "  uninstall - remove installed binary"
```

### Авто-зависимости (`.d` файлы)
```makefile
# Ключ -MMD генерирует .d-файл рядом с .o
CFLAGS += -MMD -MP
-include $(DEP)
```
Это автоматически отслеживает зависимости от `.h` файлов (правило пересобирается при изменении заголовка).

---

## 🐚 Make как task runner (не только для C!)

Makefile — отличный раннер задач для любого проекта:

```makefile
.PHONY: dev build test lint fmt deploy docker-up docker-down

# Python проект
venv:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

dev: venv
	.venv/bin/python -m flask run --reload

test:
	pytest -v

lint:
	ruff check .
	mypy .

fmt:
	ruff format .
	isort .

# Node проект
node_modules:
	npm install

dev-js:
	npm run dev

build-js:
	npm run build

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

# Деплой
deploy:
	rsync -avz --delete ./dist/ user@server:/var/www/app/
	ssh user@server "systemctl restart myapp"
```

Использование:
```bash
make dev          # запуск дев-сервера
make test         # тесты
make deploy       # деплой
```

---

## 🪤 Частые ошибки Make

1. **TAB vs пробелы** — рецепты должны быть с TAB. `missing separator`.
2. **Файл с именем цели** — например, если есть файл `clean`, цель не выполнится.
   Всегда добавляйте `.PHONY`.
3. **`=` vs `:=`** — `=` ленивое (рекурсивное), может дать неожиданный результат.
   Используйте `:=` (простое присваивание).
4. **Параллельность** — `make -j` требует корректных зависимостей, иначе гонки.
5. **`$@` vs `$$@`** — `$$` для shell-переменных, `$` для make-переменных.
6. **Длинные строки** — продолжение через `\` (backslash).
7. **Изменение переменной** — командная строка переопределяет `=`, но не `override`.

---

# 🔨 ЧАСТЬ 2. CMAKE

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **CMakeLists.txt** | Конфигурационный файл (скрипт на CMake-языке) |
| **generator** | Что генерировать: Makefiles, Ninja, VS, Xcode |
| **build directory** | Отдельный каталог для сборки (out-of-source) |
| **target** | Цель сборки: executable, library, custom |
| **variable / cache** | `set(VAR value)` / переменные в кэше |
| **property** | Свойства target'а, файла, каталога |
| **find_package** | Найти стороннюю библиотеку |
| **toolchain** | Файл кросс-компиляции |

---

## 🚀 Базовый цикл работы

```bash
# 1. Конфигурация (генерация Makefile/Ninja в build/)
cmake -B build                     # -B = build directory (современный синтаксис)
# или
cmake -S . -B build                # -S = source directory

# С опциями
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake -B build -DCMAKE_INSTALL_PREFIX=/opt/myapp

# С конкретным генератором
cmake -B build -G "Ninja"
cmake -B build -G "Unix Makefiles"
cmake -B build -G "Visual Studio 17 2022"

# 2. Сборка
cmake --build build                # современный универсальный синтаксис
cmake --build build -j4            # параллельно
cmake --build build --target myapp # конкретная цель
cmake --build build --config Release  # для multi-config (VS, Xcode)

# 3. Установка
cmake --install build              # в CMAKE_INSTALL_PREFIX
sudo cmake --install build

# 4. Очистка
rm -rf build                       # полностью пересоздать
```

### Установка
```bash
sudo pacman -S cmake ninja         # Arch
sudo apt install cmake ninja-build # Debian/Ubuntu
```

---

## 📝 Структура CMakeLists.txt

### Минимальный пример (один файл)
```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(MyApp
    VERSION 1.0.0
    DESCRIPTION "My awesome app"
    LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)

# Создать исполняемый файл
add_executable(myapp src/main.c src/utils.c)

# Опции компиляции
target_compile_options(myapp PRIVATE -Wall -Wextra)

# Линковка библиотек
target_link_libraries(myapp PRIVATE m)

# Включить директории с заголовками
target_include_directories(myapp PRIVATE include)

# Установка
install(TARGETS myapp DESTINATION bin)
```

### Сборка и запуск
```bash
cmake -B build
cmake --build build
./build/myapp
```

---

## 🎯 Цели (targets)

### Исполняемый файл
```cmake
add_executable(myapp main.c)
add_executable(myapp main.cpp utils.cpp)        # несколько файлов
add_executable(myapp ${SOURCES})                # из переменной
```

### Статическая библиотека (.a)
```cmake
add_library(mylib STATIC src/lib.c)
```

### Динамическая библиотека (.so)
```cmake
add_library(mylib SHARED src/lib.c)
```

### Модуль (плагин, загружается dlopen)
```cmake
add_library(myplugin MODULE src/plugin.c)
```

### Interface library (только заголовки, header-only)
```cmake
add_library(myheader INTERFACE)
target_include_directories(myheader INTERFACE include/)
```

### Object library (только объектные файлы, для переиспользования)
```cmake
add_library(common OBJECT src/common.c)
```

---

## 🔗 Зависимости и видимость (PRIVATE/PUBLIC/INTERFACE)

**Ключевая концепция CMake**: **transitive dependencies**.

| Ключевое слово | Используется в самом target | Используется зависящими |
|---|---|---|
| `PRIVATE` | ✅ | ❌ |
| `PUBLIC` | ✅ | ✅ |
| `INTERFACE` | ❌ | ✅ |

```cmake
# mylib использует json внутренне (PRIVATE)
target_link_libraries(mylib PRIVATE nlohmann_json)

# myapp использует mylib публично (myapp видит API mylib)
target_link_libraries(myapp PUBLIC mylib)

# Header-only library — только INTERFACE
target_include_directories(myheader INTERFACE include/)
```

**Правило**:
- `PRIVATE` — для внутренней реализации
- `PUBLIC` — если ваше API использует эту зависимость (передаётся в заголовках)
- `INTERFACE` — для header-only библиотек

---

## 📦 Поиск библиотек (find_package)

```cmake
# Найти установленную библиотеку
find_package(OpenSSL REQUIRED)
find_package(ZLIB REQUIRED)
find_package(Threads REQUIRED)

# После find_package используем импортированный target
target_link_libraries(myapp PRIVATE OpenSSL::SSL OpenSSL::Crypto)
target_link_libraries(myapp PRIVATE ZLIB::ZLIB)
target_link_libraries(myapp PRIVATE Threads::Threads)

# Найти с опциями
find_package(Qt6 COMPONENTS Core Widgets REQUIRED)
target_link_libraries(myapp PRIVATE Qt6::Core Qt6::Widgets)

# Найти в конкретном месте
set(CMAKE_PREFIX_PATH "/opt/Qt/6.5/gcc_64")
find_package(Qt6 COMPONENTS Core REQUIRED)

# Свои модули поиска
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
find_package(MyLib REQUIRED)        # ищет FindMyLib.cmake
```

### find_package режимы
- **Module mode**: ищет `FindXXX.cmake` (в `CMAKE_MODULE_PATH` или встроенные)
- **Config mode**: использует `XXXConfig.cmake` из установленного пакета (рекомендуется авторами библиотек)

### Полезные встроенные find_package
```cmake
find_package(Threads REQUIRED)       # pthreads
find_package(OpenMP REQUIRED)        # OpenMP
find_package(ZLIB)                   # zlib
find_package(PNG)                    # libpng
find_package(OpenGL)                 # OpenGL
find_package(SDL2)                   # SDL2
find_package(Boost COMPONENTS system filesystem REQUIRED)
```

---

## ⚙️ Опции и переменные кэша

### Свои опции (как в больших проектах)
```cmake
option(BUILD_TESTS "Build unit tests" ON)
option(USE_OPENGL "Enable OpenGL support" OFF)
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)

if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

if(USE_OPENGL)
    find_package(OpenGL REQUIRED)
    target_link_libraries(myapp PRIVATE OpenGL::GL)
    target_compile_definitions(myapp PRIVATE USE_OPENGL=1)
endif()
```

Использование:
```bash
cmake -B build -DBUILD_TESTS=OFF -DUSE_OPENGL=ON
```

### Полезные переменные CMake
| Переменная | Назначение |
|---|---|
| `CMAKE_BUILD_TYPE` | Debug/Release/RelWithDebInfo/MinSizeRel |
| `CMAKE_INSTALL_PREFIX` | Куда ставить (`/usr/local` по умолчанию) |
| `CMAKE_C_COMPILER` | Компилятор C |
| `CMAKE_CXX_COMPILER` | Компилятор C++ |
| `CMAKE_C_FLAGS` | Флаги C |
| `CMAKE_CXX_STANDARD` | Стандарт C++ (11/14/17/20/23) |
| `CMAKE_PREFIX_PATH` | Где искать библиотеки |
| `CMAKE_MODULE_PATH` | Где искать FindXXX.cmake |
| `CMAKE_SOURCE_DIR` | Корень проекта |
| `CMAKE_BINARY_DIR` | Каталог сборки |
| `CMAKE_CURRENT_SOURCE_DIR` | Текущий каталог |
| `BUILD_SHARED_LIBS` | Глобально: shared vs static |
| `CMAKE_TOOLCHAIN_FILE` | Файл toolchain (кросс-компиляция) |

### Типы сборки (CMAKE_BUILD_TYPE)
| Тип | Флаги | Назначение |
|---|---|---|
| `Debug` | `-g -O0` | Отладка |
| `Release` | `-O3 -DNDEBUG` | Релиз |
| `RelWithDebInfo` | `-O2 -g -DNDEBUG` | Релиз с дебаг-инфо |
| `MinSizeRel` | `-Os -DNDEBUG` | Минимальный размер |

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
# Для multi-config (VS, Xcode) — при сборке:
cmake --build build --config Release
```

---

## 🗂️ Многокаталожный проект

```
project/
├── CMakeLists.txt
├── src/
│   ├── CMakeLists.txt
│   ├── main.c
│   └── lib/
│       ├── CMakeLists.txt
│       └── utils.c
└── tests/
    └── CMakeLists.txt
```

**Корневой `CMakeLists.txt`**:
```cmake
cmake_minimum_required(VERSION 3.15)
project(MyProject VERSION 1.0 LANGUAGES C)

add_subdirectory(src)
add_subdirectory(src/lib)

option(BUILD_TESTS "Build tests" ON)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
```

**`src/CMakeLists.txt`**:
```cmake
add_executable(myapp main.c)
target_link_libraries(myapp PRIVATE mylib)
```

**`src/lib/CMakeLists.txt`**:
```cmake
add_library(mylib STATIC utils.c)
target_include_directories(mylib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
```

---

## 🧪 Тесты (CTest)

```cmake
# Включить CTest
enable_testing()

# Простой тест (запуск исполняемого файла)
add_executable(test_math tests/test_math.c)
target_link_libraries(test_math PRIVATE mylib)
add_test(NAME math_test COMMAND test_math)

# Тест с аргументами
add_test(NAME mytest COMMAND myapp --test --verbose)

# Тест в конкретной рабочей директории
add_test(NAME config_test COMMAND myapp --config
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/tests)

# Пропустить тест
set_tests_properties(broken_test PROPERTIES DISABLED TRUE)

# Зависимости тестов
set_tests_properties(test_b PROPERTIES DEPENDS test_a)
```

Запуск тестов:
```bash
cd build && ctest                   # все тесты
ctest -V                            # подробно (verbose)
ctest -VV                           # очень подробно
ctest -j4                           # параллельно
ctest -R math                       # по имени (regex)
ctest -E slow                       # исключить
ctest --output-on-failure           # вывод при падении
ctest -L unit                       # по label
```

---

## 📥 Установка (install)

```cmake
# Установка исполняемого файла
install(TARGETS myapp
    RUNTIME DESTINATION bin)

# Библиотеки и заголовки
install(TARGETS mylib
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin)        # для Windows DLL

install(DIRECTORY include/
    DESTINATION include/mylib
    FILES_MATCHING PATTERN "*.h")

# Конфиги, man-страницы
install(FILES myapp.conf DESTINATION etc)
install(FILES myapp.1 DESTINATION share/man/man1)

# Свои скрипты
install(PROGRAMS scripts/setup.sh DESTINATION bin)

# Целевой install (с экспортом для других проектов)
install(TARGETS mylib EXPORT MyLibTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib)
install(EXPORT MyLibTargets
    FILE MyLibTargets.cmake
    NAMESPACE MyLib::
    DESTINATION lib/cmake/MyLib)
```

```bash
cmake --install build                    # в CMAKE_INSTALL_PREFIX
cmake --install build --prefix /opt/app  # переопределить
sudo cmake --install build               # системно
```

---

## 🔤 Команды CMake (основные)

### Команды для target'ов (современный CMake)
```cmake
add_executable(name sources...)
add_library(name [STATIC|SHARED|MODULE|INTERFACE] sources...)

# Настройки target'а (рекомендуется вместо глобальных)
target_include_directories(name PUBLIC include/)
target_compile_definitions(name PRIVATE DEBUG=1 VERSION="1.0")
target_compile_features(name PRIVATE cxx_std_17)
target_compile_options(name PRIVATE -Wall -Wextra)
target_link_libraries(name PRIVATE otherlib)
target_link_directories(name PRIVATE /opt/lib)   # избегайте, используйте find_package
target_link_options(name PRIVATE -static)
target_sources(name PRIVATE src/new.c)
target_include_directories(name SYSTEM PRIVATE /opt/include)
```

### Работа с переменными
```cmake
set(MYVAR "value")
set(LIST a b c)
list(APPEND LIST d)                    # добавить
list(REMOVE_ITEM LIST b)               # удалить
list(SORT LIST)
list(JOIN LIST "," STRING)
set(MYVAR ${MYVAR} extra)              # конкатенация

# Условия
if(USE_FEATURE)
    ...
elseif(OTHER)
    ...
else()
    ...
endif()

# Циклы
foreach(item IN LISTS ITEMS)
    message(STATUS "Item: ${item}")
endforeach()

foreach(i RANGE 0 10 2)                # 0, 2, 4, ..., 10
    ...
endforeach()

while(CONDITION)
    ...
endwhile()
```

### Условия в if()
```cmake
if(VAR)                    # true если определена и не пустая/0/false/NO/OFF
if(NOT VAR)
if(A AND B) / if(A OR B)

if(DEFINED VAR)            # переменная определена
if(EXISTS path)            # файл/каталог существует
if(IS_DIRECTORY path)
if(COMMAND name)           # команда существует

if(A STREQUAL B)           # строки равны
if(A MATCHES regex)        # регулярка

if(A LESS B) / GREATER / EQUAL    # числа
if(VERSION_LESS 3.15)

if(${CMAKE_SYSTEM_NAME} STREQUAL "Linux")
    ...
endif()
```

### Прочее
```cmake
message(STATUS "Message")              # информационное
message(WARNING "Warning")             # предупреждение
message(FATAL_ERROR "Error")           # ошибка + остановка
message(AUTHOR_WARNING "...")          # только разработчику

file(GLOB SOURCES src/*.cpp)           # не использовать для источников!
file(GLOB_RECURSE SOURCES src/**/*.cpp)
# ❌ CMake не пересоздаст список при добавлении новых файлов
# ✅ Используйте явно: add_executable(a.cpp b.cpp)

file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/logs)
file(COPY config/ DESTINATION ${CMAKE_BINARY_DIR}/config)
file(WRITE file.txt "content")
file(READ file.txt CONTENT)

include_directories(include/)          # глобально (избегайте, используйте target_include_directories)
link_libraries(m)                      # глобально (избегайте)
add_definitions(-DDEBUG=1)             # глобально (избегайте)
```

---

## 🛠️ Практический пример CMakeLists.txt

Полный пример для проекта на C++:

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp
    VERSION 1.2.0
    LANGUAGES CXX)

# ── Стандарт C++ ────────────────────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ── Опции ───────────────────────────────────────────
option(BUILD_TESTS "Build tests" OFF)
option(BUILD_SHARED_LIBS "Build shared" OFF)

# ── По умолчанию Release если не задано ─────────────
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# ── Источники ───────────────────────────────────────
set(LIB_SOURCES
    src/database.cpp
    src/network.cpp
    src/utils.cpp)

# ── Библиотека ──────────────────────────────────────
add_library(mylib ${LIB_SOURCES})
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

# Предупреждения
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(mylib PRIVATE -Wall -Wextra -Wpedantic)
elseif(MSVC)
    target_compile_options(mylib PRIVATE /W4)
endif()

# ── Зависимости ─────────────────────────────────────
find_package(Threads REQUIRED)
target_link_libraries(mylib PUBLIC Threads::Threads)

# SQLite3 через pkg-config
find_package(PkgConfig REQUIRED)
pkg_check_modules(SQLITE3 REQUIRED sqlite3)
target_link_libraries(mylib PRIVATE ${SQLITE3_LIBRARIES})
target_include_directories(mylib PRIVATE ${SQLITE3_INCLUDE_DIRS})

# ── Исполняемый файл ────────────────────────────────
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)

# ── Тесты ───────────────────────────────────────────
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# ── Установка ───────────────────────────────────────
include(GNUInstallDirs)
install(TARGETS myapp mylib
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

---

## 🌍 Кроссплатформенность

```cmake
# Определить ОС
if(WIN32)
    # Windows (вкл. 64-bit)
    target_compile_definitions(myapp PRIVATE PLATFORM_WIN)
elseif(UNIX AND APPLE)
    # macOS
    target_compile_definitions(myapp PRIVATE PLATFORM_MAC)
elseif(UNIX)
    # Linux/Unix
    target_compile_definitions(myapp PRIVATE PLATFORM_LINUX)
endif()

# Compiler ID
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(myapp PRIVATE -Wall)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(myapp PRIVATE /W4)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(myapp PRIVATE -Wall -Wextra)
endif()

# Разные источники по платформе
if(WIN32)
    target_sources(myapp PRIVATE src/windows_specific.cpp)
else()
    target_sources(myapp PRIVATE src/posix_specific.cpp)
endif()

# Архитектура
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(STATUS "64-bit")
else()
    message(STATUS "32-bit")
endif()
```

### GNUInstallDirs — стандартные пути
```cmake
include(GNUInstallDirs)
# Доступны:
# CMAKE_INSTALL_BINDIR      - bin
# CMAKE_INSTALL_LIBDIR      - lib или lib64
# CMAKE_INSTALL_INCLUDEDIR  - include
# CMAKE_INSTALL_DATADIR     - share
# CMAKE_INSTALL_MANDIR      - share/man

install(TARGETS myapp
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})
```

---

## 🎯 Generator Expressions

Мощный механизм для условных значений:

```cmake
# Различные пути для сборки и установки
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Условные флаги
target_compile_options(myapp PRIVATE
    $<$<CXX_COMPILER_ID:GNU>:-Wall>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<CONFIG:Debug>:-g -O0>
    $<$<CONFIG:Release>:-O3>
)

# Платформо-зависимые библиотеки
target_link_libraries(myapp PRIVATE
    $<$<PLATFORM_ID:Windows>:ws2_32>
    $<$<PLATFORM_ID:Linux>:rt>
)
```

Частые generator expressions:
| Выражение | Значение |
|---|---|
| `$<CONFIG:Debug>` | True если конфиг Debug |
| `$<PLATFORM_ID:Linux>` | True если Linux |
| `$<CXX_COMPILER_ID:GNU>` | True если компилятор GCC |
| `$<BOOL:value>` | Преобразовать в true/false |
| `$<STREQUAL:a,b>` | Сравнение строк |
| `$<TARGET_FILE:mylib>` | Путь к собранному файлу |
| `$<TARGET_PROPERTY:t,PROP>` | Свойство target'а |
| `$<BUILD_INTERFACE:...>` | Только при сборке |
| `$<INSTALL_INTERFACE:...>` | Только при установке |

---

## 🐛 Дебаг и анализ

```bash
# Подробный вывод при конфигурации
cmake -B build --debug-output
cmake -B build --trace                # показать выполнение всех команд
cmake -B build --trace-expand         # + раскрытие переменных

# Посмотреть финальные команды компилятора
make VERBOSE=1                        # в build/
cmake --build build -- VERBOSE=1

# Изучить кэш
cmake -L -B build                     # некэшированные переменные
cmake -LA -B build                    # все
cat build/CMakeCache.txt              # напрямую

# Сменить опцию без перенастройки
cmake -B build -DBUILD_TESTS=ON       # обновит кэш

# Очистить кэш
rm build/CMakeCache.txt               # сохранить структуру, сбросить опции

# Полный rebuild
rm -rf build && cmake -B build

# Граф зависимостей
cmake --graphviz=deps.dot -B build    # создать Graphviz
```

### Полезные инструменты
```bash
ccmake -B build          # TUI для редактирования кэша ( curses )
cmake-gui                # GUI для Windows/macOS

# Анализ собранного
ldd build/myapp          # зависимости (Linux)
otool -L myapp           # (macOS)
```

---

## 🔗 FetchContent — скачать зависимости (модерн)

```cmake
include(FetchContent)

# Скачать GoogleTest
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.14.0
)
FetchContent_MakeAvailable(googletest)

target_link_libraries(myapp PRIVATE gtest_main)
```

Преимущества:
- Не нужно `find_package` + предварительная установка
- Воспроизводимые сборки
- Версия зафиксирована в репозитории

---

## 🆚 Сравнение Make и CMake

| | Make | CMake |
|---|---|---|
| Уровень | Низкий (правила) | Высокий (метасборка) |
| Файл | `Makefile` | `CMakeLists.txt` |
| Кроссплатформенность | ❌ Unix-ориентирован | ✅ Win/Mac/Linux |
| IDE-интеграция | базовая | ✅ VS, Xcode, CLion |
| Поиск библиотек | вручную | ✅ find_package |
| Многоконфигурация | ❌ | ✅ Debug/Release |
| Сложность | просто для маленьких | сложнее, но мощнее |

**Когда что использовать**:
- **Make**: маленькие проекты, скриптовые языки (как task runner), простой C.
- **CMake**: средние и большие C/C++ проекты, кроссплатформа, библиотеки.

---

## 🪤 Частые ошибки CMake

1. **`file(GLOB)` для источников** — CMake не узнает о новых файлах без rerun.
   Явно перечисляйте `add_executable(a.cpp b.cpp)`.
2. **Глобальные команды** — `include_directories`, `link_libraries`,
   `add_definitions` влияют на всё. Используйте `target_*`.
3. **In-source build** — не собирайте в корне (`cmake .`).
   Всегда `cmake -B build`.
4. **Забыли `target_link_libraries`** — `undefined reference` при линковке.
5. **PUBLIC vs PRIVATE** — неправильная видимость раздувает зависимости.
6. **Не указали `CMAKE_CXX_STANDARD`** — разные компиляторы, разные дефолты.
7. **`add_subdirectory` до `add_library`** — порядок важен.
8. **Кэш не обновился** — после правки CMakeLists иногда нужно `rm -rf build`.
9. **Hardcoded paths** — `${CMAKE_SOURCE_DIR}` вместо абсолютных.
10. **Смешение старого и нового стиля** — `include_directories` + `target_*`.

---

## 🔗 Полезные ссылки

### Make
- GNU Make manual: https://www.gnu.org/software/make/manual
- Makefile tutorial: https://makefiletutorial.com
- Awesome Makefile: https://github.com/thockin/makefile-tutorial

### CMake
- Официальный tutorial: https://cmake.org/cmake/help/latest/guide/tutorial
- CMake reference: https://cmake.org/cmake/help/latest/manual/cmake-commands.7.html
- Modern CMake: https://cliutils.gitlab.io/modern-cmake
- Professional CMake: https://crascit.com/professional-cmake
- Effective CMake (Daniel Pfeifer): https://www.youtube.com/watch?v=bsXLMQ6WgIk

---

## 💡 Полезные советы

### Make
1. **TAB, не пробелы** — самая частая ошибка.
2. **`.PHONY`** для целей, не являющихся файлами.
3. **`:=` вместо `=`** — избегайте сюрпризов ленивых переменных.
4. **`-MMD -MP`** — авто-зависимости от заголовков.
5. **`make -j$(nproc)`** — параллельная сборка.
6. **Make как task runner** — для Python/Node тоже удобен.
7. **`$@ $< $^`** — запомните автоматические переменные.

### CMake
1. **Out-of-source build** — всегда `cmake -B build`, не собирайте в корне.
2. **Target-based** — используйте `target_*`, не глобальные `include_directories`.
3. **PRIVATE/PUBLIC/INTERFACE** — правильно задавайте видимость.
4. **find_package + imported targets** — современный способ зависимостей.
5. **FetchContent** — для управления исходниками зависимостей.
6. **GNUInstallDirs** — стандартные пути установки.
7. **`CMAKE_CXX_STANDARD`** — зафиксируйте стандарт C++.
8. **Generator expressions** — для платформо-зависимой логики.
9. **CTest** — встроенный раннер тестов.
10. **Modern CMake (3.x+)** — не используйте устаревшие практики 2.x.

---

*Сгенерировано как шпаргалка. Системы сборки сложны —
углубляйтесь через `man make`, `cmake --help` и официальные туториалы.*

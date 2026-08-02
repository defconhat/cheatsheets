# 🔎 fzf + zoxide — шпаргалка по fuzzy-поиску и переходам

> **fzf** —通用 fuzzy finder (поиск файлов, команд, истории).
> **zoxide** — умный cd (запоминает часто посещаемые каталоги).
>
> fzf: https://github.com/junegunn/fzf · zoxide: https://github.com/ajitid/zoxide

---

# 🔎 ЧАСТЬ 1. fzf

## 🚀 Установка

```bash
# Arch / CachyOS
sudo pacman -S fzf

# Debian/Ubuntu
sudo apt install fzf

# macOS
brew install fzf
$(brew --prefix)/opt/fzf/install

# Через git (самая свежая версия)
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# Через cargo (Rust)
cargo install --locked skim     # skim — Rust-альтернатива
```

### Интеграция с shell
После установки добавьте строки в `~/.bashrc` / `~/.zshrc`:
```bash
# Если ставили через pacman/apt — обычно уже автоматически
source /usr/share/fzf/key-bindings.bash
source /usr/share/fzf/completion.bash

# Для zsh
source /usr/share/fzf/key-bindings.zsh
source /usr/share/fzf/completion.zsh

# Если ставили через git/install script — автоматически
[ -f ~/.fzf.bash ] && source ~/.fzf.bash
```

---

## 🎯 Базовое использование

```bash
# Интерактивный поиск
fzf                                # файлы в текущем каталоге
find . -type f | fzf               # через find
fd --type f | fzf                  # через fd (быстрее)

# С другим источником
ls -la | fzf
cat /etc/passwd | fzf
pacman -Qq | fzf                   # выбор пакетов

# Мульти-выбор (Tab)
fzf -m                             # выбрать несколько

# Выбрать и использовать
file=$(fzf) && xdg-open "$file"
nvim $(fzf)                        # открыть выбранный в nvim
code $(fzf)
cd $(find . -type d | fzf)

# Предпросмотр
fzf --preview 'cat {}'
fzf --preview 'bat --color=always {}'    # с подсветкой
fzf --preview 'head -100 {}'

# С привязкой клавиш
fzf --bind "ctrl-r:reload(find . -type f)"
```

---

## ⌨️ Встроенные горячие клавиши (после интеграции)

| Клавиша | Действие |
|---|---|
| `Ctrl-T` | Найти файл (вставить путь в командную строку) |
| `Ctrl-R` | Поиск по истории команд |
| `Alt-C` | Интерактивный cd (найти каталог и перейти) |

### Примеры
```bash
# Ctrl-T — вставить путь файла
vim <Ctrl-T>                       # выберите файл → вставится путь

# Ctrl-R — история
<Ctrl-R>                           # начните печатать для поиска
# Стрелки ↑↓ — выбор, Enter — выполнить

# Alt-C — каталог
<Alt-C>                            # выберите каталог → cd в него
```

### Внутри fzf
| Клавиша | Действие |
|---|---|
| `↑` `↓` или `Ctrl-J/K` | Навигация |
| `Enter` | Выбрать |
| `Tab` | Мультивыбор (с `-m`) |
| `Shift-Tab` | Снять выделение |
| `Ctrl-A` / `Ctrl-D` | Выбрать все / снять все |
| `Ctrl-R` | Включить/выключить reverse sort |
| `Ctrl-S` | Включить/выключить sort |
| `Esc` / `Ctrl-C` / `Ctrl-G` | Выйти |
| `Ctrl-W` | Стереть слово назад |
| `Ctrl-U` | Стереть строку |
| `Ctrl-Y` | Прокрутить preview вниз |
| `Ctrl-E` | Прокрутить preview вверх |
| `?` | Toggle help |

---

## 🎨 Цвета и кастомизация

```bash
# Встроенные темы
fzf --color=dark
fzf --color=light
fzf --color=16      # 16 цветов

# Свои цвета (24-bit)
fzf --color='fg:#ffffff,bg:#18181b,hl:#a3e635,fg+:#ffffff,bg+:#27272a,hl+:#a3e635,info:#71717a,prompt:#fbbf24,pointer:#f87171,marker:#a3e635,spinner:#06b6d4,header:#71717a'

# Через переменную окружения (для всех запусков)
export FZF_DEFAULT_OPTS='
    --height 40%
    --layout=reverse
    --info=inline
    --color=fg:#e4e4e7,bg:#18181b,hl:#a3e635,fg+:#fafafa,bg+:#27272a,hl+:#a3e635
    --color=info:#71717a,prompt:#fbbf24,pointer:#f87171,marker:#a3e635,spinner:#06b6d4,header:#71717a
    --bind="ctrl-d:half-page-down,ctrl-u:half-page-up"
'
```

### Полезные опции
| Опция | Что |
|---|---|
| `--height N%` | Высота окна (не на весь экран) |
| `--reverse` | Ввод сверху, результаты снизу |
| `--inline-info` | Инфа в одной строке с промптом |
| `--preview CMD` | Окно предпросмотра |
| `--preview-window=right:50%` | Расположение/размер preview |
| `--multi` / `-m` | Мультивыбор |
| `--prompt=">"` | Свой промпт |
| `--header="..."` | Заголовок |
| `--bind=...` | Горячие клавиши |
| `--tiebreak=index` | Тай-брейк при равном score |
| `--no-sort` | Не сортировать |
| `--exact` | Точное совпадение |
| `--tac` | Reverse order (для истории) |

---

## 🔗 Интеграция с инструментами

### fzf + ripgrep (поиск по содержимому)
```bash
# Найти файл с текстом
RG_PREFIX="rg --column --line-number --no-heading --color=always --smart-case"
INITIAL_QUERY="${*:-}"
IFS=: read -ra selected < <(
    FZF_DEFAULT_COMMAND="$RG_PREFIX '$INITIAL_QUERY'" \
    fzf --ansi \
        --color="hl:-1:underline,hl+:-1:underline:reverse" \
        --disabled --query "$INITIAL_QUERY" \
        --bind "change:reload:sleep 0.1; $RG_PREFIX {q} || true" \
        --delimiter : \
        --preview 'bat --color=always {1} --highlight-line {2}' \
        --preview-window 'right,60%,border-left,+{2}+3/3'
)
[file, line] = "${selected[0]}" "${selected[1]}"
```

### fzf + bat (предпросмотр с подсветкой)
```bash
fzf --preview 'bat --style=numbers --color=always {} | head -100'
```

### fzf + git
```bash
# Переключиться на ветку
git branch | fzf | xargs git checkout

# Посмотреть коммит
git log --oneline | fzf | awk '{print $1}' | xargs git show

# Интерактивный git checkout
gco() {
    git branch --format='%(refname:short)' | fzf | xargs git checkout
}

# Выбрать файлы из git status
git status -s | fzf -m | awk '{print $2}' | xargs git add
```

### fzf + pacman / yay
```bash
# Установить пакет
pacman -Slq | fzf -m --preview 'pacman -Si {1}' | xargs -ro sudo pacman -S

# Удалить установленный
pacman -Qq | fzf -m --preview 'pacman -Qi {1}' | xargs -ro sudo pacman -Rns
```

### fzf + kill
```bash
# Убить процесс
ps aux | fzf | awk '{print $2}' | xargs kill -9

# Функция
fkill() {
    pid=$(ps -ef | sed 1d | fzf -m | awk '{print $2}')
    [ -n "$pid" ] && kill -9 ${pid[@]}
}
```

### fzf + docker
```bash
# Зайти в контейнер
docker ps | fzf | awk '{print $1}' | xargs -I{} docker exec -it {} bash

# Убить контейнер
docker ps -a | fzf -m | awk '{print $1}' | xargs docker rm -f
```

### fzf + ssh
```bash
# Выбрать хост из ~/.ssh/config
ssh $(grep "^Host " ~/.ssh/config | awk '{print $2}' | fzf)
```

### fzf + environment variables
```bash
# Выбрать переменную окружения
printenv | fzf
env | fzf | cut -d= -f1
```

### fzf + dirs (cd в часто посещаемые)
```bash
# С zoxide (см. ниже)
cd $(zoxide query -l | fzf)
```

---

## 🐚 Shell-функции с fzf

```bash
# Открыть файл в nvim
fe() {
    local files
    IFS=$'\n' files=($(fzf --query="$1" --multi --select-1 --exit-0))
    [[ -n "$files" ]] && ${EDITOR:-nvim} "${files[@]}"
}

# cd с предпросмотром
fd() {
    local dir
    dir=$(find ${1:-.} -type d 2> /dev/null | fzf +m) && cd "$dir"
}

# История команд с fzf (если Ctrl-R не работает)
fh() {
    print -z $( ([ -n "$ZSH_NAME" ] && fc -l 1 || history) | fzf +s --tac | sed 's/ *[0-9]* *//')
}

# Grep с fzf
fg() {
    grep -rn "$1" . | fzf
}
```

---

## 📦 fzf.vim (для Neovim/Vim)

В LazyVim уже есть fzf.lua или telescope. Для vanilla:
```vim
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" Горячие клавиши
nnoremap <leader>f :Files<CR>
nnoremap <leader>g :Rg<CR>
nnoremap <leader>b :Buffers<CR>
nnoremap <leader>h :History<CR>
```

---

# 🌍 ЧАСТЬ 2. zoxide

## 🚀 Установка

```bash
# Arch / CachyOS
sudo pacman -S zoxide

# Debian/Ubuntu
sudo apt install zoxide

# macOS
brew install zoxide

# Через cargo
cargo install zoxide --locked

# Windows
scoop install zoxide
```

### Интеграция с shell

Добавьте в `~/.bashrc`:
```bash
eval "$(zoxide init bash)"
```

`~/.zshrc`:
```zsh
eval "$(zoxide init zsh)"
```

`~/.config/fish/config.fish`:
```fish
zoxide init fish | source
```

### Опции init
```bash
eval "$(zoxide init bash --cmd cd)"      # заменить cd на z
eval "$(zoxide init zsh --hook prompt)"  # обновлять БД при каждом prompt
```

---

## 🎯 Использование

```bash
# Базовый переход (заменяет cd)
z myproject                        # перейти в каталог с "myproject" в имени
z foo bar                          # foo + bar
z ..                               # на уровень вверх
z -                                # предыдущий каталог

# Интерактивный выбор (с fzf)
zi                                 # выбрать из всех известных каталогов
zi myproject                       # отфильтровать по "myproject"

# Самый часто посещаемый
z reports                          # перейдёт в наиболее релевантный

# Абсолютный путь
z /var/log

# Использовать обычный cd (если z = cd)
\cd mydir                          # обойти алиас
```

### Команды zoxide
```bash
z foo                       # cd с fuzzy
zi foo                      # интерактивно через fzf
zoxide query foo            # показать лучший результат без перехода
zoxide query -l             # список всех известных каталогов
zoxide query -l -s          # + очки (score)
zoxide add /path/to/dir     # добавить каталог вручную
zoxide remove /path         # удалить из БД
zoxide edit                 # интерактивно редактировать БД
zoxide reset                # сбросить базу
```

---

## 📊 Как работает zoxide

- Записывает каждый `z`/`cd` в базу (`~/.local/share/zoxide/db.zo`).
- Каждому каталогу присваивается **score** (важность).
- Score растёт при частом посещении + уменьшается со временем.

```
> zoxide query -l -s
/path/to/project        50.5      # часто посещаемый
/path/to/old/project    20.0      # реже
/tmp                    5.0       # редко
```

Алгоритм: `age_decay * frequency`.
- Новый каталог → score растёт быстро.
- Старый/редкий → затухает.

---

## ⚙️ Настройка

### Переменные окружения
```bash
# .bashrc / .zshrc
export _ZO_DATA_DIR="$HOME/.local/share/zoxide"   # где хранить БД
export _ZO_MAXAGE=10000                            # лимит записей (по умолчанию 10000)
export _ZO_ECHO=1                                  # выводить путь при переходе
export _ZO_RESOLVE_SYMLINKS=1                      # resolve symlinks
export _ZO_EXCLUDE_DIRS="$HOME/.git:$HOME/Trash"   # исключить каталоги
```

### Сменить команду (например, на cd)
```bash
eval "$(zoxide init bash --cmd cd)"
# теперь cd /path/to/project работает с fuzzy
# но и обычный cd в подкаталог тоже работает
```

---

## 🆚 zoxide vs z vs autojump

| | zoxide | z (rupa/z) | autojump |
|---|---|---|---|
| Язык | Rust | Bash | Python |
| Скорость | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| Поддержка | Активно | Брошен | Старый |
| Сравнение | умнее | проще | базовое |
| Cross-platform | ✅ | только Unix | Unix |

**Рекомендуется**: zoxide (Rust, активно развивается).

---

# 🌟 Комбо fzf + zoxide

```bash
# Установить fzf и zoxide
sudo pacman -S fzf zoxide

# В ~/.bashrc / ~/.zshrc:
eval "$(zoxide init bash)"
source /usr/share/fzf/key-bindings.bash
source /usr/share/fzf/completion.bash

# Полезные алиасы
alias cd='z'                   # если заменили
alias zoxide-query='zoxide query -l -s'

# Функция: открыть проект
proj() {
    local dir
    dir=$(zoxide query -l | fzf --preview 'tree -C {} | head -50') && cd "$dir"
}

# Функция: перейти и открыть nvim
v() {
    local dir
    dir=$(zoxide query -l | fzf) && cd "$dir" && nvim .
}
```

---

## 🪤 Частые ошибки

### fzf
1. **Не работают `Ctrl-T`/`Ctrl-R`/`Alt-C`** — не подключены key-bindings.
   Добавьте `source /usr/share/fzf/key-bindings.bash` в `.bashrc`.
2. **Медленный поиск в больших каталогах** — используйте `fd` вместо `find`.
3. **Нет предпросмотра** — добавьте `--preview 'cat {}'`.
4. **Цвета не работают** — терминал должен поддерживать 256/true color.
5. **Мусор в списке** — фильтруйте источник: `fd --type f | fzf`.

### zoxide
1. **База пустая** — сначала надо переходить, чтобы zoxide запомнил.
2. **Не реагирует** — забыт `eval "$(zoxide init ...)"` в rc-файле.
3. **Хочет в `/tmp`** — фильтруйте через `_ZO_EXCLUDE_DIRS`.
4. **Старые записи** — `zoxide reset` или `zoxide edit` для очистки.
5. **z как cd** — если нужно обычный cd, `\cd` или `command cd`.

---

## 🔗 Полезные ссылки

### fzf
- GitHub: https://github.com/junegunn/fzf
- Wiki: https://github.com/junegunn/fzf/wiki
- Examples: https://github.com/junegunn/fzf/wiki/Examples
- fzf.vim: https://github.com/junegunn/fzf.vim
- skim (Rust alt): https://github.com/lotabout/skim

### zoxide
- GitHub: https://github.com/ajitid/zoxide
- Документация: https://github.com/ajitid/zoxide#examples
- z (альтернатива): https://github.com/rupa/z
- autojump: https://github.com/wting/autojump

---

## 💡 Полезные советы

1. **Ctrl-R** — лучший способ искать по истории команд.
2. **Alt-C** — быстрый cd с fuzzy.
3. **Ctrl-T** — вставить путь файла в текущую команду.
4. **`--preview 'bat --color=always {}'`** — для предпросмотра с подсветкой.
5. **fzf + fd** — быстрее, чем fzf + find.
6. **fzf + ripgrep** — поиск по содержимому.
7. **z `zi`** — интерактивный выбор через fzf.
8. **zoxide `--cmd cd`** — заменить cd на умный cd.
9. **Aliases** — `alias cd=z` для бесшовного перехода.
10. **fzf в скриптах** — для интерактивного выбора.
11. **`fzf -m`** — мультивыбор через Tab.
12. **Цвета через FZF_DEFAULT_OPTS** — настройте один раз.
13. **fzf.vim / fzf-lua** — для Neovim.
14. **`z foo bar`** — fuzzy по нескольким словам.
15. **Регулярно `zoxide reset`** — если база засорилась.

---

*Сгенерировано как шпаргалка. fzf и zoxide — основа продуктивности в терминале —
углубляйтесь через https://github.com/junegunn/fzf/wiki/Examples*

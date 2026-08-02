# 🔀 Git — шпаргалка по командам и workflow

> **Git** — распределённая система контроля версий.
> Документация: https://git-scm.com/docs · Книга: https://git-scm.com/book/ru/v2

---

## ⚙️ Первичная настройка

```bash
# Имя и email (попадают в коммиты)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Имя основной ветки по умолчанию
git config --global init.defaultBranch main

# Редактор для коммитов/merge
git config --global core.editor "nvim"
git config --global core.editor "code --wait"

# Визуальный diff/merge инструмент
git config --global merge.tool vimdiff

# Цвета
git config --global color.ui auto

# Кэш пароля (HTTPS) — 1 час / на диск
git config --global credential.helper 'cache --timeout=3600'
git config --global credential.helper store      # навсегда в ~/.git-credentials

# Алиасы (см. ниже блок про алиасы)
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all --decorate"

# Автопуш текущей ветки
git config --global push.default current

# Pull с rebase вместо merge
git config --global pull.rebase true

# Показать все настройки
git config --list
git config --list --global
```

### Где хранятся настройки
| Файл | Область |
|---|---|
| `~/.gitconfig` | `--global` (пользователь) |
| `.git/config` (в репо) | `--local` (только этот репо) |
| `/etc/gitconfig` | `--system` (вся система) |

Приоритет: local > global > system.

---

## 🆕 Создание репозитория

```bash
# Создать новый локальный репозиторий
mkdir myproject && cd myproject
git init
git init -b main                # сразу с веткой main

# Клонировать существующий
git clone <url>
git clone <url> mydir           # в указанную папку
git clone --depth 1 <url>       # shallow clone (только последний коммит)
git clone --recursive <url>     # с подмодулями
git clone git@github.com:user/repo.git     # по SSH
git clone https://github.com/user/repo.git # по HTTPS

# Клонировать только одну ветку
git clone -b develop --single-branch <url>
```

---

## 📋 Статус и базовый цикл

Жизненный цикл файла: **untracked → staged → committed**

```bash
git status                     # текущее состояние
git status -s                  # компактный вид
git status -sb                 # + инфо о ветке/upstream

# Стадия
git add file.txt               # добавить файл
git add .                      # всё в текущей папке
git add -A                     # все изменения (вкл. удаления) во всём репо
git add -u                     # только отслеживаемые (без новых)
git add -p                     # интерактивно по кускам (hunks)
git add -i                     # интерактивное меню

# Коммит
git commit -m "Сообщение"
git commit -m "Заголовок" -m "Подробное описание"
git commit -am "msg"           # add + commit (только tracked)
git commit                     # откроет редактор для сообщения
git commit --amend             # изменить последний коммит (сообщение + staged)
git commit --amend --no-edit   # дополнить коммит, не меняя сообщение
git commit --date="2024-01-01T12:00:00" -m "msg"   # своя дата

# История
git log                        # вся история
git log --oneline              # кратко
git log --oneline --graph --all   # дерево всех веток
git log -p                     # с diff'ом каждого коммита
git log --stat                 # со статистикой файлов
git log -5                     # последние 5
git log --author="Alice"
git log --since="2 weeks ago"
git log -- path/to/file        # история конкретного файла
git log -S "functionName"      # когда добавили/удалили строку
git show <commit>              # детали конкретного коммита
git show HEAD                  # последний коммит
git show HEAD~1                # предпоследний
git blame file.txt             # кто и когда написал каждую строку
```

---

## 🌿 Ветвление

```bash
# Просмотр
git branch                     # локальные ветки
git branch -a                  # все (включая remote)
git branch -r                  # только remote
git branch -v                  # + последний коммит
git branch -vv                 # + upstream

# Создание
git branch feature             # создать
git branch feature main        # от main
git checkout feature           # переключиться
git checkout -b feature        # создать + переключиться (классика)
git switch feature             # переключиться (новая команда)
git switch -c feature          # создать + переключиться (новая)

# Переименование
git branch -m new-name         # текущую
git branch -m old new          # любую

# Удаление
git branch -d feature          # безопасно (если слита)
git branch -D feature          # принудительно (даже если не слита)

# Удалить все слитые локальные ветки
git branch --merged | grep -v '*' | xargs git branch -d

# Удалить remote-ветку
git push origin --delete feature
git push origin :feature       # короткая форма
```

---

## 🔄 Получение и отправка изменений

```bash
# Получить изменения без слияния
git fetch                      # от upstream
git fetch origin               # явно
git fetch --all                # от всех remote
git fetch --prune              # + удалить мёртвые remote-ссылки

# Получить и слить с текущей
git pull                       # = fetch + merge
git pull --rebase              # = fetch + rebase (чище история)
git pull origin main

# Отправить
git push                       # в upstream
git push origin feature        # в конкретную ветку
git push -u origin feature     # установить upstream (-u)
git push --force-with-lease    # безопасный force-push (если никто не запушил)
git push --force               # ❗ перетирает чужую историю
git push --tags                # отправить теги
git push --all                 # все ветки
```

### Разница merge / rebase / pull
- **`git pull`** = `fetch` + `merge` (появляется merge-commit)
- **`git pull --rebase`** = `fetch` + `rebase` (линейная история)
- **Rebase** переписывает историю — НЕ делайте на публичных ветках!

---

## 🔀 Слияние (merge) и rebase

### merge
```bash
git checkout main              # перейти в целевую ветку
git merge feature              # влить feature в main
git merge --no-ff feature      # всегда создавать merge-commit
git merge --squash feature     # собрать все коммиты в один (без merge-commit)
git merge --abort              # отменить конфликтующий merge
```

### rebase
```bash
git checkout feature
git rebase main                # перенести feature поверх main
git rebase -i HEAD~5           # интерактивный rebase (5 коммитов)
git rebase --abort             # отменить
git rebase --continue          # продолжить после разрешения конфликта
git rebase --skip              # пропустить проблемный коммит
```

### Интерактивный rebase (`-i`) — что можно делать
```bash
git rebase -i HEAD~4
```
Откроется редактор со списком коммитов и командами:
| Команда | Действие |
|---|---|
| `pick` (или `p`) | оставить как есть |
| `reword` (`r`) | изменить сообщение |
| `edit` (`e`) | остановиться для правок |
| `squash` (`s`) | объединить с предыдущим |
| `fixup` (`f`) | объединить, выбросив сообщение |
| `exec` (`x`) | запустить команду |
| `drop` (`d`) | удалить коммит |
| `squash` + reorder | менять порядок строками |

---

## ⚔️ Конфликты

```bash
# Возникают при merge/rebase/pull
# Файлы с конфликтами помечены в git status

# В файле будет:
# <<<<<<< HEAD
# ваша версия
# =======
# чужая версия
# >>>>>>> feature

# Действия
git status                     # увидеть conflicted файлы
# 1. Откройте файл, разрешите конфликт вручную (или через merge.tool)
# 2. git add file.txt         (отметить как разрешённый)
# 3. git commit               (для merge) или git rebase --continue

# Если хочется откатиться
git merge --abort              # отменить merge
git rebase --abort             # отменить rebase
git checkout --ours file       # оставить свою версию
git checkout --theirs file     # оставить чужую версию

# Простой merge-инструмент для разрешения
git mergetool
```

---

## 🗑️ Отмена и изменение

```bash
# Изменить последний коммит (добавить файлы или поменять сообщение)
git add forgotten_file
git commit --amend --no-edit

# Отменить staging (unstage)
git restore --staged file.txt       # современно
git reset HEAD file.txt             # классика

# Отменить локальные изменения файла
git restore file.txt                # современно
git checkout -- file.txt            # классика

# Отменить ВСЕ локальные изменения
git restore .
git checkout -- .

# Сбросить к конкретному коммиту
git reset --soft HEAD~1         # удалить коммит, оставить изменения staged
git reset HEAD~1                # mixed: изменения unstaged
git reset --hard HEAD~1         # ❗ удалить коммит И изменения
git reset --hard origin/main    # ❗ стать точно как remote (локал потерян)

# Отменить коммит, сохранив его в истории (безопасно)
git revert <commit>             # создаёт обратный коммит
git revert HEAD                 # отменить последний
git revert <c1> <c2>            # несколько

# Сравнение reset режимов
# --soft   HEAD двигается, staged и working tree остаются
# --mixed  HEAD двигается, staged сбрасывается, working остаётся
# --hard   HEAD двигается, staged И working сбрасываются (❗ потеря)
```

---

## 🔍 Разница (diff)

```bash
git diff                       # working tree vs staged (незакоммиченные)
git diff --staged              # staged vs HEAD (что попадёт в коммит)
git diff --cached              # то же, что --staged
git diff HEAD                  # working vs HEAD (всё незакоммиченное)
git diff main feature          # между ветками
git diff <c1> <c2>             # между коммитами
git diff <c1> <c2> -- file     # конкретный файл
git diff --stat                # только статистика
git diff --name-only           # только имена файлов
git diff -w                    # игнорировать пробелы
git diff --word-diff           # пословно
git diff branch1..branch2      # разница между tips
git diff branch1...branch2     # от общего предка
```

---

## 🏷️ Теги

```bash
git tag v1.0.0                    # lightweight tag
git tag -a v1.0.0 -m "Релиз 1.0"  # annotated (рекомендуется)
git tag v1.0.0 <commit>           # тег на конкретный коммит

git tag                           # список
git tag -l "v1.*"                 # по шаблону
git show v1.0.0                   # детали тега

git push origin v1.0.0            # отправить один тег
git push origin --tags            # все теги

git tag -d v1.0.0                 # удалить локально
git push origin --delete v1.0.0   # удалить на remote
```

---

## 📦 Stash — спрятать изменения

```bash
git stash                       # спрятать tracked-изменения
git stash -u                    # + untracked
git stash -a                    # + ignored
git stash save "message"        # с сообщением (старый синтаксис)
git stash push -m "message"     # новый синтаксис

git stash list                  # список стэшей
git stash show                  # что в верхнем стэше
git stash show -p               # с diff
git stash show stash@{2}        # конкретный

git stash pop                   # применить верхний и удалить
git stash apply                 # применить, но оставить в стэше
git stash apply stash@{2}       # конкретный
git stash drop                  # удалить верхний
git stash clear                 # удалить все

# Частичный стэш
git stash -p                    # выбрать hunks интерактивно
```

---

## 🗂️ Remote-репозитории

```bash
git remote -v                   # список remote
git remote show origin          # детали
git remote add upstream <url>   # добавить
git remote rename origin o      # переименовать
git remote remove origin        # удалить
git remote set-url origin <url> # сменить URL

# Сменить HTTPS → SSH
git remote set-url origin git@github.com:user/repo.git

# Fetch из upstream (форк)
git fetch upstream
git merge upstream/main
```

---

## 📚 Подмодули (submodules)

```bash
# Добавить подмодуль
git submodule add <url> path/to/sub

# Клонировать репо с подмодулями
git clone --recursive <url>
# или после клонирования:
git submodule update --init --recursive

# Обновить все подмодули до remote-версий
git submodule update --remote --merge

# Выполнить команду во всех подмодулях
git submodule foreach 'git status'

# Удалить подмодуль
git submodule deinit -f path/to/sub
git rm path/to/sub
rm -rf .git/modules/path/to/sub
```

---

## 🔬 Продвинутые команды

### cherry-pick
```bash
git cherry-pick <commit>        # применить коммит из другой ветки
git cherry-pick <c1>..<c2>      # диапазон (не вкл. c1)
git cherry-pick --abort
```

### bisect — бинарный поиск бага
```bash
git bisect start
git bisect bad                  # текущий коммит — плохой
git bisect good v1.0.0          # v1.0.0 — хороший
# git сам будет чекать коммиты, вы отмечаете:
git bisect good   # или
git bisect bad
git bisect reset                 # выйти
```

### reflog — спасение потерянного
```bash
git reflog                      # журнал ВСЕХ перемещений HEAD
git reflog --all
# найти хэш потерянного коммита и:
git reset --hard <hash>
```

### blame / grep
```bash
git blame file                  # кто написал каждую строку
git blame -L 10,20 file         # диапазон строк
git grep "pattern"              # поиск по tracked-файлам
git grep -n "pattern"           # с номерами строк
git log -S "func(" -- '*.py'    # когда появилась/исчезла строка
```

### worktree — несколько рабочих деревьев
```bash
git worktree add ../project-feature feature
git worktree list
git worktree remove ../project-feature
```

### restore (новые команды)
```bash
git restore file                # отменить изменения в файле
git restore --staged file       # unstage
git restore --source=HEAD~1 file  # из конкретного коммита
git restore --source=main file
```

---

## 📊 Игнорирование файлов (`.gitignore`)

```gitignore
# Комментарий
*.log              # все .log
node_modules/      # каталог
build/             # каталог
.env               # конкретный файл
!important.env     # исключение из игнора

# Языки
*.pyc
__pycache__/
.venv/
dist/
*.o
*.exe

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Управление ignore
```bash
# Файл уже закоммичен, но теперь в gitignore
git rm --cached file             # удалить из индекса, оставить локально
git rm -r --cached node_modules  # рекурсивно

# Глобальный gitignore
git config --global core.excludesfile ~/.gitignore_global

# Кто игнорирует этот файл?
git check-ignore -v file
```

---

## 🎯 Алиасы (полезные)

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# Красивый лог
git config --global alias.lg "log --color --graph --pretty=format:'%C(auto)%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# В виде одних хэшей
git config --global alias.ll "log --oneline --decorate"
```

Использование: `git lg`, `git ci -m "..."`, `git co main`.

---

## 🌟 Лучшие практики (workflow)

### 1. Классический feature-branch
```bash
git checkout main
git pull
git checkout -b feature/add-login
# ... работа, коммиты ...
git push -u origin feature/add-login
# создать Pull Request на GitHub/GitLab
```

### 2. Коммиты: как писать сообщения
**Conventional Commits:**
```
<type>(<scope>): <subject>

<body>

<footer>
```
Типы: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`.

Примеры:
```
feat(auth): add OAuth2 login
fix(api): handle null response
docs: update README
chore: bump dependencies
```

- Заголовок **до 50 символов**, в повелительном наклонении («add», не «added»).
- Тело — что и зачем (не как), до 72 символов в строке.
- Один коммит = одно логическое изменение.

### 3. Перед коммитом
```bash
git status                  # что изменилось
git diff                    # посмотреть
git diff --staged           # что попадёт в коммит
```

### 4. Синхронизация с remote
```bash
git fetch --prune           # получить + убрать мёртвые ветки
git pull --rebase           # чище история
```

### 5. Чистая история перед PR
```bash
git rebase -i HEAD~5        # объединить/переименовать коммиты
git push --force-with-lease # безопасный force-push
```

---

## 🐙 GitHub / GitLab через CLI (`gh`)

```bash
# Установка (Arch)
sudo pacman -S github-cli
gh auth login                 # авторизация

# Клонировать репо
gh repo clone user/repo

# Создать PR
gh pr create --fill           # из текущей ветки, с авто-заполнением
gh pr create --title "..." --body "..."
gh pr list
gh pr view 123
gh pr checkout 123            # переключиться на PR
gh pr merge 123 --squash --delete-branch

# Issues
gh issue create
gh issue list
gh issue view 5

# Релизы
gh release create v1.0.0 ./build/*.zip --title "..." --notes "..."
```

---

## 🚨 Аварийные ситуации

### «Я закоммитил не туда»
```bash
git reset --soft HEAD~1       # отменить коммит, изменения staged
git checkout correct-branch
git commit -m "..."
```

### «Я потерял коммит после reset --hard»
```bash
git reflog                    # найти хэш
git reset --hard <hash>       # вернуть
```

### «Случайно сделал commit --amend и запушил»
```bash
# Если запушен — попросите коллег pull --rebase, ничего страшного
# Если ещё не запушен — ничего делать не надо
```

### «Хочу удалить файл из истории» (например, секрет)
```bash
git filter-repo --path secrets.txt --invert-paths
# или старый (медленный) способ:
git filter-branch --force --index-filter \
    'git rm --cached --ignore-unmatch secrets.txt' \
    --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

### «Слияние пошло не так, хочу всё вернуть»
```bash
git merge --abort             # для merge
git rebase --abort            # для rebase
git reset --merge ORIG_HEAD   # универсально к состоянию до merge
```

### «Случайно удалил ветку»
```bash
git reflog                    # найти последний коммит ветки
git branch recovered <hash>   # создать ветку на этом коммите
```

---

## 📊 Полезные запросы

```bash
# Кто сколько коммитов (топ контрибьюторов)
git shortlog -sn

# Статистика по автору
git log --author="Alice" --oneline | wc -l

# Файлы, изменённые между коммитами
git diff --name-only <c1> <c2>

# Размер репозитория
git count-objects -vH

# Найти Largest-файлы в истории
git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    awk '/^blob/ {print substr($0,6)}' | sort -k2 -rn | head

# Показать файл из другого коммита, не переключаясь
git show main:file.txt

# Список всех файлов в репо на HEAD
git ls-files

# История файла (даже удалённого)
git log --follow -- path/to/file
```

---

## 🪝 Git Hooks (хуки)

Хуки живут в `.git/hooks/` (не версонируются) или через core.hooksPath.

| Хук | Когда срабатывает |
|---|---|
| `pre-commit` | перед коммитом (линтер, форматирование) |
| `commit-msg` | проверка сообщения |
| `pre-push` | перед push |
| `post-merge` | после merge/pull |
| `pre-rebase` | перед rebase |

Рекомендация: **husky** / **pre-commit** / **lefthook** для управления хуками
(с поддержкой конфига в репозитории).

---

## 💡 Полезные советы

1. **Commit часто, мелкими порциями** — легче откатывать и ревьюить.
2. **`git pull --rebase`** — чистая линейная история без merge-коммитов.
3. **`git push --force-with-lease`** вместо `--force` — не перетрете чужое.
4. **`git reflog`** — ваш спасатель; почти ничего не теряется навсегда.
5. **`.gitignore` с первого дня** — не коммитьте `node_modules`, `.env`, `build/`.
6. **`git stash`** — спрятать изменения, чтобы переключиться на другую ветку.
7. **`git add -p`** — добавлять изменения по кускам, а не целыми файлами.
8. **`git cherry-pick`** — перенести коммит между ветками без merge.
9. **Один коммит — одна логика** — не мешайте фичу с рефакторингом.
10. **Conventional Commits** — стандартизирует историю и помогает changelog'у.
11. **Pull Request ASAP** — даже WIP, чтобы получить обратную связь.
12. **`git bisect`** — найдёт коммит, который сломал сборку, бинарным поиском.
13. **Не rebas'ьте публичные ветки** (main, develop) — только свои feature.
14. **`gh` CLI** — мощно упрощает работу с GitHub прямо из терминала.
15. **Lazygit / `tig`** — TUI-клиенты сильно ускоряют рутину.

---

## 🔗 Ссылки

- Официальная книга (RU): https://git-scm.com/book/ru/v2
- Документация: https://git-scm.com/docs
- Интерактивный туториал: https://learngitbranching.js.org
- Визуальный reference: https://onlywei.github.io/explain-git-with-d3
- GitHub Cheatsheet: https://training.github.com
- Atlassian Tutorial: https://www.atlassian.com/git/tutorials
- First Aid Git: https://firstaidgit.ru
- Lazygit: https://github.com/jesseduffield/lazygit
- `gh` CLI: https://cli.github.com

---

*Сгенерировано как шпаргалка. Git огромен —
углубляйтесь через `man git`, `git <cmd> --help` и книгу.*

# Форк n8node: как это устроено

Этот репозиторий — **полная копия исходников Baserow** (ветка `develop`), с которой можно работать как с обычным форком.

- **Апстрим (оригинал):** [github.com/baserow/baserow](https://github.com/baserow/baserow)  
- **Ваш репозиторий:** [github.com/n8node/baserow](https://github.com/n8node/baserow)

## Remotes в Git

После клона у вас должно быть:

- `origin` → `https://github.com/n8node/baserow.git` (ваш форк, сюда `git push`)
- `upstream` → `https://github.com/baserow/baserow.git` (оригинал, сюда только `git fetch`)

Настройка один раз:

```bash
git remote rename origin upstream
git remote add origin https://github.com/n8node/baserow.git
git push -u origin develop
```

На GitHub в настройках репозитория при необходимости выставьте **default branch: develop** (как у Baserow).

## Локальная разработка

См. официальную документацию: [Development environment](https://baserow.io/docs/development/development-environment) и файлы `README.md`, `CONTRIBUTING.md` в корне.

Кратко (Linux / WSL, с установленными зависимостями по их гайду):

```bash
just dc-dev build --parallel
just dc-dev up -d
```

## Подтянуть обновления из оригинального Baserow

```bash
git fetch upstream
git checkout develop
git merge upstream/develop
# при конфликтах — разрешить, затем
git push origin develop
```

## Связь «правки кода → сервер»

1. **Только конфиги/скрипты деплоя** — лежат в `deploy/n8node/`. Меняете локально → `git push` → на сервере `git pull` и `./deploy/n8node/scripts/deploy.sh`.

2. **Изменения в коде Baserow** — нужно **собрать свой Docker-образ** из форка и указать его в `deploy/n8node/docker-compose.yml` вместо `baserow/baserow:2.1.6`. В репозитории Baserow есть `docker-compose.build.yml` и документация по сборке; часто настраивают GitHub Actions: push в `develop` → build → push в GitHub Container Registry → на сервере `docker compose pull && up -d`.

Пока образ не свой, сервер использует **стоковый** релиз с Hub; ваши коммиты в backend/web-frontend **не попадут** на сервер автоматически.

## Папка `deploy/n8node/`

Ваш прежний сценарий с Nginx на `127.0.0.1:8080` и внешним томом `baserow_data` — перенесён сюда, чтобы жил рядом с кодом форка.

# Деплой n8node (официальный образ)

Пока вы **не собираете свой образ** из исходников форка, на сервере крутится образ `baserow/baserow` с Docker Hub.

После правок кода форка и настройки CI/сборки замените `image:` в `docker-compose.yml` на свой registry.

## Сервер

```bash
cd /path/to/clone/baserow/deploy/n8node
cp .env.example .env
docker volume create baserow_data   # если тома ещё не было
docker compose up -d
```

Nginx + Certbot — см. комментарии в `nginx/baserow.ru.conf`.

Обновление после `git pull`:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

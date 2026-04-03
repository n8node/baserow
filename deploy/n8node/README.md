# Деплой n8node (Baserow + WordPress)

Baserow работает как приложение, WordPress — как CMS для главной страницы.

## Архитектура

```
Nginx (порт 80/443)
  ├─ /              → WordPress (127.0.0.1:8081) — главная страница
  ├─ /wp-admin/*    → WordPress — админка
  ├─ /wp-content/*  → WordPress — ресурсы
  └─ всё остальное  → Baserow (127.0.0.1:8080) — приложение
```

## Первый запуск

```bash
cd /opt/baserow/deploy/n8node
cp .env.example .env
nano .env                           # задайте пароли!
docker volume create baserow_data
docker compose up -d
```

## Настройка Nginx

```bash
sudo cp nginx/baserow.ru.conf /etc/nginx/sites-available/baserow.ru
sudo ln -sf /etc/nginx/sites-available/baserow.ru /etc/nginx/sites-enabled/
sudo certbot --nginx -d baserow.ru
sudo nginx -t && sudo systemctl reload nginx
```

## Настройка WordPress

1. Откройте `https://baserow.ru/` — появится мастер установки WordPress
2. Задайте язык, название сайта, логин/пароль админа
3. Установите тему и page builder (Elementor, Divi и т.д.)
4. Создайте главную страницу по дизайну baserow.io
5. Добавьте кнопки со ссылками на `/signup` и `/login`

## Обновление после git pull

```bash
cd /opt/baserow/deploy/n8node
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## Полезные команды

```bash
# Статус контейнеров
docker compose ps

# Логи Baserow
docker logs baserow --tail 50

# Логи WordPress
docker logs wordpress --tail 50

# Перезапуск только WordPress
docker compose restart wordpress

# Зайти в WordPress-контейнер (для wp-cli и т.д.)
docker compose exec wordpress bash
```

#!/usr/bin/env bash
# Запуск из каталога deploy/n8node после git pull репозитория форка.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  echo "cp .env.example .env && отредактируйте .env"
  exit 1
fi

docker compose pull
docker compose up -d

if command -v nginx >/dev/null 2>&1; then
  sudo nginx -t && sudo systemctl reload nginx
fi

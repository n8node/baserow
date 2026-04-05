#!/usr/bin/env bash
# Полный бэкап кода (/opt/baserow) и встроенной PostgreSQL (контейнер baserow).
# Запуск на сервере из корня репозитория:  bash deploy/scripts/baserow-full-backup.sh
# Результат: ./backup/YYYYMMDD_HHMMSS/{code.tar.gz,postgres.dump,BACKUP_INFO.txt}
#
# Не входит: тома WordPress (wordpress_data, wordpress_db_data) — при необходимости:
#   docker run --rm -v wordpress_db_data:/v -v "$OUT":/out alpine tar czf /out/wordpress_mysql.tar.gz -C /v .
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_PARENT="${BASEROW_BACKUP_DIR:-$REPO_ROOT/backup}"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$BACKUP_PARENT/$TS"
CONTAINER="${BASEROW_CONTAINER_NAME:-baserow}"

mkdir -p "$OUT"

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  echo "Ошибка: контейнер «$CONTAINER» не запущен. Запусти stack и повтори." >&2
  exit 1
fi

echo "Бэкап в: $OUT"

# --- код (без папки backup, без тяжёлых артефактов; .git включён) ---
tar -czf "$OUT/code.tar.gz" \
  -C "$REPO_ROOT" \
  --exclude='./backup' \
  --exclude='./**/node_modules' \
  --exclude='./**/.venv' \
  --exclude='./**/venv' \
  --exclude='./**/__pycache__' \
  --exclude='./**/.pytest_cache' \
  --exclude='./web-frontend/.output' \
  --exclude='./web-frontend/.nuxt' \
  .

# --- PostgreSQL (встроенная в all-in-one) ---
docker exec "$CONTAINER" bash -c '
  set -euo pipefail
  : "${DATABASE_USER:=baserow}"
  : "${DATABASE_NAME:=baserow}"
  export PGPASSWORD="${DATABASE_PASSWORD:?DATABASE_PASSWORD не задан в контейнере}"
  pg_dump -h localhost -U "$DATABASE_USER" -Fc -f /tmp/baserow_pg.dump "$DATABASE_NAME"
'
docker cp "$CONTAINER:/tmp/baserow_pg.dump" "$OUT/postgres.dump"
docker exec "$CONTAINER" rm -f /tmp/baserow_pg.dump

{
  echo "timestamp=$TS"
  echo "host=$(hostname 2>/dev/null || true)"
  echo "repo=$REPO_ROOT"
  if command -v git >/dev/null && [[ -d "$REPO_ROOT/.git" ]]; then
    echo "git_commit=$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  fi
  echo "container=$CONTAINER"
  echo "image=$(docker inspect "$CONTAINER" --format '{{.Config.Image}}' 2>/dev/null || true)"
  echo "note=WordPress Docker volumes not included; see script header."
} > "$OUT/BACKUP_INFO.txt"

echo "Готово: $OUT"
ls -la "$OUT"

#!/usr/bin/env bash
# Полный бэкап: код репозитория, PostgreSQL (baserow all-in-one), файлы WordPress, дамп MySQL (wordpress-db).
# Запуск:  cd /opt/baserow && bash deploy/scripts/baserow-full-backup.sh
# Результат: backup/YYYYMMDD_HHMMSS/{code.tar.gz, postgres.dump, wordpress_files.tar.gz, wordpress_mysql.sql, BACKUP_INFO.txt}
#
# Если WordPress не нужен в снимке:  BASEROW_BACKUP_SKIP_WORDPRESS=1 bash deploy/scripts/baserow-full-backup.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_PARENT="${BASEROW_BACKUP_DIR:-$REPO_ROOT/backup}"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$BACKUP_PARENT/$TS"
CONTAINER="${BASEROW_CONTAINER_NAME:-baserow}"
WP_C="${WORDPRESS_CONTAINER_NAME:-wordpress}"
WP_DB_C="${WORDPRESS_DB_CONTAINER_NAME:-wordpress-db}"
SKIP_WP="${BASEROW_BACKUP_SKIP_WORDPRESS:-}"

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

WP_NOTE="wordpress=skipped (BASEROW_BACKUP_SKIP_WORDPRESS=1)"
if [[ -z "$SKIP_WP" ]]; then
  if ! docker ps --format '{{.Names}}' | grep -qx "$WP_C" || ! docker ps --format '{{.Names}}' | grep -qx "$WP_DB_C"; then
    echo "Ошибка: для бэкапа WordPress должны быть запущены контейнеры «$WP_C» и «$WP_DB_C»." >&2
    echo "Или выполни: BASEROW_BACKUP_SKIP_WORDPRESS=1 bash deploy/scripts/baserow-full-backup.sh" >&2
    exit 1
  fi

  # --- WordPress: файлы (/var/www/html) ---
  echo "Архив WordPress (файлы)…"
  docker exec "$WP_C" tar czf - -C /var/www/html . > "$OUT/wordpress_files.tar.gz"

  # --- WordPress: MySQL ---
  echo "Дамп MySQL (wordpress)…"
  docker exec "$WP_DB_C" sh -c \
    'exec mysqldump --single-transaction --routines --triggers -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"' \
    > "$OUT/wordpress_mysql.sql"

  WP_NOTE="wordpress=files+mysql"
fi

{
  echo "timestamp=$TS"
  echo "host=$(hostname 2>/dev/null || true)"
  echo "repo=$REPO_ROOT"
  if command -v git >/dev/null && [[ -d "$REPO_ROOT/.git" ]]; then
    echo "git_commit=$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  fi
  echo "container=$CONTAINER"
  echo "image=$(docker inspect "$CONTAINER" --format '{{.Config.Image}}' 2>/dev/null || true)"
  echo "$WP_NOTE"
} > "$OUT/BACKUP_INFO.txt"

echo "Готово: $OUT"
ls -la "$OUT"

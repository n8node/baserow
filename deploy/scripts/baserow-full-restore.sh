#!/usr/bin/env bash
# Восстановление из снимка deploy/scripts/baserow-full-backup.sh
#
# Использование:
#   bash deploy/scripts/baserow-full-restore.sh --code-only DIR
#   bash deploy/scripts/baserow-full-restore.sh --db-only DIR          # только PostgreSQL (baserow)
#   bash deploy/scripts/baserow-full-restore.sh --wordpress-only DIR  # файлы WP + MySQL (контейнеры wordpress / wordpress-db)
#
# Полный цикл (после down → code-only → up baserow+wp):
#   --db-only DIR
#   --wordpress-only DIR
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONTAINER="${BASEROW_CONTAINER_NAME:-baserow}"
WP_C="${WORDPRESS_CONTAINER_NAME:-wordpress}"
WP_DB_C="${WORDPRESS_DB_CONTAINER_NAME:-wordpress-db}"

usage() {
  echo "Usage: $0 [--code-only|--db-only|--wordpress-only|--all] BACKUP_DIR" >&2
  echo "  BACKUP_DIR — папка с code.tar.gz, postgres.dump, опционально wordpress_*.tar.gz / .sql" >&2
  exit 1
}

MODE=""
SNAP=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --code-only)      MODE=code; shift ;;
    --db-only)        MODE=db; shift ;;
    --wordpress-only) MODE=wordpress; shift ;;
    --all)            MODE=all; shift ;;
    -*)
      usage ;;
    *)
      SNAP="$1"
      shift
      ;;
  esac
done

[[ -n "$SNAP" ]] || usage
[[ -n "$MODE" ]] || usage

CODE_TAR="$SNAP/code.tar.gz"
DUMP="$SNAP/postgres.dump"
WP_FILES="$SNAP/wordpress_files.tar.gz"
WP_SQL="$SNAP/wordpress_mysql.sql"

restore_code() {
  [[ -f "$CODE_TAR" ]] || { echo "Нет файла: $CODE_TAR" >&2; exit 1; }
  echo "Восстановление кода из $CODE_TAR в $REPO_ROOT (существующие файлы перезапишутся)"
  read -r -p "Продолжить? [y/N] " a
  [[ "${a:-}" =~ ^[yY]$ ]] || { echo "Отменено."; exit 1; }
  tar -xzf "$CODE_TAR" -C "$REPO_ROOT"
  echo "Код восстановлен."
}

restore_db() {
  [[ -f "$DUMP" ]] || { echo "Нет файла: $DUMP" >&2; exit 1; }
  if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "Ошибка: контейнер «$CONTAINER» не запущен. Подними baserow и повтори (--db-only)." >&2
    exit 1
  fi
  echo "ВНИМАНИЕ: текущая база PostgreSQL в контейнере будет перезаписана из $DUMP"
  read -r -p "Продолжить? [y/N] " a
  [[ "${a:-}" =~ ^[yY]$ ]] || { echo "Отменено."; exit 1; }

  docker cp "$DUMP" "$CONTAINER:/tmp/baserow_pg.restore.dump"
  docker exec "$CONTAINER" bash -c '
    set -euo pipefail
    : "${DATABASE_USER:=baserow}"
    : "${DATABASE_NAME:=baserow}"
    export PGPASSWORD="${DATABASE_PASSWORD:?DATABASE_PASSWORD не задан}"
    psql -h localhost -U "$DATABASE_USER" -d postgres -v ON_ERROR_STOP=1 \
      -c "DROP DATABASE IF EXISTS \"$DATABASE_NAME\" WITH (FORCE);" \
      -c "CREATE DATABASE \"$DATABASE_NAME\" OWNER \"$DATABASE_USER\";"
    pg_restore -h localhost -U "$DATABASE_USER" -d "$DATABASE_NAME" --no-owner /tmp/baserow_pg.restore.dump
    rm -f /tmp/baserow_pg.restore.dump
  '
  echo "PostgreSQL восстановлен. Перезапусти baserow при необходимости: docker compose ... up -d --force-recreate"
}

restore_wordpress() {
  if [[ ! -f "$WP_FILES" ]] && [[ ! -f "$WP_SQL" ]]; then
    echo "В снимке нет wordpress_files.tar.gz / wordpress_mysql.sql — шаг WordPress пропущен."
    return 0
  fi

  if [[ -f "$WP_FILES" ]]; then
    if ! docker inspect "$WP_C" >/dev/null 2>&1; then
      echo "Ошибка: нет контейнера «$WP_C»." >&2
      exit 1
    fi
    WP_VOL="$(docker inspect "$WP_C" --format '{{range .Mounts}}{{if eq .Destination "/var/www/html"}}{{.Name}}{{end}}{{end}}')"
    [[ -n "$WP_VOL" ]] || { echo "Не удалось определить volume WordPress для $WP_C" >&2; exit 1; }

    echo "ВНИМАНИЕ: содержимое тома WordPress ($WP_VOL) будет заменено из $WP_FILES"
    read -r -p "Продолжить? [y/N] " a
    [[ "${a:-}" =~ ^[yY]$ ]] || { echo "Отменено."; exit 1; }

    docker stop "$WP_C" >/dev/null
    docker run --rm \
      -v "$WP_VOL:/var/www/html" \
      -v "$SNAP:/ro:ro" \
      alpine:3.20 \
      sh -c 'find /var/www/html -mindepth 1 -delete && tar xzf /ro/wordpress_files.tar.gz -C /var/www/html'
    docker start "$WP_C" >/dev/null
    echo "Файлы WordPress восстановлены."
  fi

  if [[ -f "$WP_SQL" ]]; then
    if ! docker ps --format '{{.Names}}' | grep -qx "$WP_DB_C"; then
      echo "Ошибка: контейнер «$WP_DB_C» не запущен." >&2
      exit 1
    fi
    echo "ВНИМАНИЕ: база MySQL wordpress будет перезаписана из $WP_SQL"
    read -r -p "Продолжить? [y/N] " a
    [[ "${a:-}" =~ ^[yY]$ ]] || { echo "Отменено."; exit 1; }

    docker exec -i "$WP_DB_C" sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' < "$WP_SQL"
    echo "MySQL WordPress восстановлен."
  fi
}

case "$MODE" in
  code)      restore_code ;;
  db)        restore_db ;;
  wordpress) restore_wordpress ;;
  all)
    restore_code
    echo "--- Подними контейнеры, затем: $0 --db-only $SNAP && $0 --wordpress-only $SNAP"
    ;;
esac

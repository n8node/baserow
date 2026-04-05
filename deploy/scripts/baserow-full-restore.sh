#!/usr/bin/env bash
# Восстановление из снимка deploy/scripts/baserow-full-backup.sh
#
# Использование:
#   bash deploy/scripts/baserow-full-restore.sh /opt/baserow/backup/20260205_120000
#
# Порядок:
#   1) Останови stack:  docker compose ... down
#   2) Восстанови код:   bash deploy/scripts/baserow-full-restore.sh --code-only DIR
#   3) Подними только baserow (без лишних сервисов при необходимости), затем БД:
#      bash deploy/scripts/baserow-full-restore.sh --db-only DIR
#
# Или одной командой (код + БД), контейнер baserow должен быть запущен для шага БД:
#   bash deploy/scripts/baserow-full-restore.sh --all DIR
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONTAINER="${BASEROW_CONTAINER_NAME:-baserow}"

usage() {
  echo "Usage: $0 [--code-only|--db-only|--all] BACKUP_DIR" >&2
  echo "  BACKUP_DIR — папка с code.tar.gz и postgres.dump" >&2
  exit 1
}

MODE=""
SNAP=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --code-only) MODE=code; shift ;;
    --db-only)   MODE=db; shift ;;
    --all)       MODE=all; shift ;;
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
  echo "ВНИМАНИЕ: текущая база в контейнере будет перезаписана из $DUMP"
  read -r -p "Продолжить? [y/N] " a
  [[ "${a:-}" =~ ^[yY]$ ]] || { echo "Отменено."; exit 1; }

  docker cp "$DUMP" "$CONTAINER:/tmp/baserow_pg.restore.dump"
  docker exec "$CONTAINER" bash -c '
    set -euo pipefail
    : "${DATABASE_USER:=baserow}"
    : "${DATABASE_NAME:=baserow}"
    export PGPASSWORD="${DATABASE_PASSWORD:?DATABASE_PASSWORD не задан}"
    # PostgreSQL 13+: WITH (FORCE) обрывает сессии к этой БД
    psql -h localhost -U "$DATABASE_USER" -d postgres -v ON_ERROR_STOP=1 \
      -c "DROP DATABASE IF EXISTS \"$DATABASE_NAME\" WITH (FORCE);" \
      -c "CREATE DATABASE \"$DATABASE_NAME\" OWNER \"$DATABASE_USER\";"
    pg_restore -h localhost -U "$DATABASE_USER" -d "$DATABASE_NAME" --no-owner /tmp/baserow_pg.restore.dump
    rm -f /tmp/baserow_pg.restore.dump
  '
  echo "База восстановлена. Перезапусти контейнер: docker compose ... up -d --force-recreate"
}

case "$MODE" in
  code) restore_code ;;
  db)   restore_db ;;
  all)
    restore_code
    echo "--- Теперь подними baserow и снова запусти: $0 --db-only $SNAP"
    ;;
esac

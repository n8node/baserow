#!/usr/bin/env bash
# Run on the server (e.g. /opt/baserow) to see why the homepage might still redirect to /login.
set -euo pipefail
BASE="${1:-https://baserow.ru}"

echo "=== 1) HTTP headers for $BASE/ (first redirects) ==="
curl -sSIL "$BASE/" | head -40

echo ""
echo "=== 2) Public landing API ==="
curl -sS "${BASE%/}/api/landing/blocks/?locale=ru" | head -c 400
echo ""

echo ""
echo "=== 3) Fresh bundle: search for landing marker in web-frontend container ==="
if docker compose -f docker-compose.yml -f docker-compose.build.yml ps web-frontend --status running -q 2>/dev/null | grep -q .; then
  docker compose -f docker-compose.yml -f docker-compose.build.yml exec -T web-frontend sh -c \
    'grep -R "publicGuestHome\|landing-home-blocks" /baserow/web-frontend/.output/public/_nuxt 2>/dev/null | head -3' \
    || echo "(no matches — old image or different output path)"
else
  echo "web-frontend container not running; skip grep"
fi

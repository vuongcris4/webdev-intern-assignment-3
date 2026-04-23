#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
APP_URL="${APP_URL:-http://127.0.0.1:5000/}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-20}"
SLEEP_SECONDS="${SLEEP_SECONDS:-3}"

cd "$ROOT_DIR"

echo "Deploying G-Scores with compose file: $COMPOSE_FILE"
docker compose -f "$COMPOSE_FILE" down --remove-orphans || true
docker compose -f "$COMPOSE_FILE" up --build -d

echo "Waiting for application health at $APP_URL"
for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  status="$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL" || true)"
  if [ "$status" = "200" ]; then
    echo "Deployment succeeded on attempt $attempt."
    docker compose -f "$COMPOSE_FILE" ps
    exit 0
  fi

  echo "Attempt $attempt/$MAX_ATTEMPTS returned HTTP ${status:-000}."
  sleep "$SLEEP_SECONDS"
done

echo "Deployment failed. Recent container logs:"
docker compose -f "$COMPOSE_FILE" logs --tail=80
exit 1

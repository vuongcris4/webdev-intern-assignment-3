#!/bin/bash
# G-Scores Deploy Script
# Usage: ./deploy.sh

set -e

echo "🚀 Deploying G-Scores..."

# Stop old container if running
docker compose down 2>/dev/null || true

# Build and run
docker compose up --build -d

# Wait for health
echo "⏳ Waiting for container..."
sleep 3

# Verify
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
if [ "$STATUS" = "200" ]; then
  echo "✅ G-Scores is live at http://localhost:5000"
  echo "📦 Container: $(docker ps --filter name=gscores --format '{{.Status}}')"
else
  echo "❌ Deploy failed (HTTP $STATUS)"
  docker logs gscores --tail 20
  exit 1
fi

#!/usr/bin/env sh

set -eu

if [ "${GSCORES_AUTO_MIGRATE:-true}" = "true" ]; then
  python manage.py migrate --noinput
fi

if [ "${GSCORES_AUTO_SEED:-true}" = "true" ]; then
  python manage.py shell -c "from django.conf import settings; from scores.models import StudentScore; raise SystemExit(0 if (StudentScore.objects.exists() or not settings.DATASET_PATH.exists()) else 1)" \
    || python manage.py seed_scores --reset
fi

exec "$@"

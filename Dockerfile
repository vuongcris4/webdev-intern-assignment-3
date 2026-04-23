FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_DEBUG=false \
    PORT=5000

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .
RUN pip install --no-warn-script-location -r requirements.txt

COPY . .

RUN chmod +x /app/deploy/entrypoint.sh \
    && chown -R appuser:appuser /app \
    && python manage.py collectstatic --noinput

USER appuser

EXPOSE 5000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["gunicorn", "-c", "deploy/gunicorn.conf.py", "config.wsgi:application"]

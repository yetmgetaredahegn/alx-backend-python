#!/bin/sh
# entrypoint.sh - dev entrypoint that waits for DB, runs migrations, then starts dev server

set -e

# Simple wait-for-db: if MYSQL_HOST is set, probe it.
if [ -n "$MYSQL_HOST" ]; then
  echo "Waiting for MySQL at ${MYSQL_HOST}:${MYSQL_PORT:-3306} ..."
  tries=0
  until nc -z "$MYSQL_HOST" "${MYSQL_PORT:-3306}" || [ $tries -ge 30 ]; do
    tries=$((tries+1))
    echo "  waiting for db... ($tries)"
    sleep 1
  done
fi

# Run migrations (ignore errors so entrypoint won't crash if something odd)
echo "Applying database migrations..."
python manage.py migrate --noinput || true

# Optionally collect static (uncomment if you want)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start Django dev server bound to 0.0.0.0 so it's reachable outside the container
exec python manage.py runserver 0.0.0.0:8000

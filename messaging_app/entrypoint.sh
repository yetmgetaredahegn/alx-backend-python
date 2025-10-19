#!/bin/sh
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
until nc -z db 3306; do
  sleep 1
done
echo "MySQL is up!"

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

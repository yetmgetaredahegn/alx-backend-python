#!/bin/sh
set -e

# Use DB_HOST from environment, default to 'db' for Docker Compose
DB_HOST=${DB_HOST:-db}

echo "Waiting for MySQL at $DB_HOST to be ready..."
until nc -z $DB_HOST 3306; do
  echo "MySQL at $DB_HOST is unavailable - sleeping"
  sleep 5
done

echo "MySQL at $DB_HOST is up!"

echo "Applying database migrations..."
python manage.py migrate

# Remove existing staticfiles directory and recreate with proper permissions
echo "Setting up staticfiles directory..."
rm -rf /app/staticfiles
mkdir -p /app/staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

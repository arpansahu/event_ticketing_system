#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - running migrations..."
python manage.py migrate

echo "Seeding database using Django management command..."
python manage.py seed  # Run the Django management command

echo "Starting Django server..."
exec "$@"

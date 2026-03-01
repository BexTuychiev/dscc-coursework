#!/bin/bash
set -e

echo "Waiting for database..."
while ! python -c "
import os, sys
import psycopg2
try:
    psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'gymtracker'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        host=os.environ.get('DB_HOST', 'db'),
        port=os.environ.get('DB_PORT', '5432'),
    )
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    sleep 1
done
echo "Database ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"

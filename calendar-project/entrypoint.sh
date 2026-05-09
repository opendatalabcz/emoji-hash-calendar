#!/bin/sh
echo "Waiting for database..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "Running migrations..."
flask db upgrade

echo "Starting Flask..."
flask --app main run --host=0.0.0.0 --port=5000

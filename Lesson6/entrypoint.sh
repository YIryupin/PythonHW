#!/bin/sh
set -e

#echo "Running database migrations..."
python -m app.migrate

echo "Starting bot..."
exec python -m MyFirstGameBot



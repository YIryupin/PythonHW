#!/bin/sh
set -e

echo "Running database migrations..."
python -m migrate

echo "Starting bot..."
exec python -m MyFirstGameBot



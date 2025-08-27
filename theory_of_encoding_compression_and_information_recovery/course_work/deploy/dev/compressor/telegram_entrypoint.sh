#!/bin/sh
set -e

echo 'Running migrations to database'
python -m alembic upgrade head

echo 'Starting telegram bot...'
python -m src.compressor.telegram_bot

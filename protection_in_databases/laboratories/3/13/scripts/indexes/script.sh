#!/bin/sh

set -e  # выход при первой ошибке

# Переменные
DB_HOST=postgres-lab-3-question-13
DB_PORT=5432
DB_NAME=$DATABASE_NAME
DB_USER=$DATABASE_USER
DB_PASSWORD=$DATABASE_PASSWORD

# Ждём, пока Postgres станет доступен
until PGPASSWORD="$DB_PASSWORD" psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null; do
  echo "⏳ Ожидание PostgreSQL перед применением индексов..."
  sleep 2
done

echo "🔧 Применение индексов..."
PGPASSWORD="$DB_PASSWORD" psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f /scripts/03_init_indexes.sql
echo "✅ Индексы успешно применены!"
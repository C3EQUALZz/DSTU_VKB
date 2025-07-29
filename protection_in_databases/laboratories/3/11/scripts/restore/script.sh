#!/bin/sh

set -e  # выход при первой ошибке

# Переменные
DB_HOST=postgres-lab-3-question-11
DB_PORT=5432
DB_NAME=$DATABASE_NAME
DB_USER=$DATABASE_USER
DB_PASSWORD=$DATABASE_PASSWORD

# Ждём, пока Postgres станет доступен
until PGPASSWORD="$DB_PASSWORD" psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null; do
  echo "⏳ Ожидание PostgreSQL..."
  sleep 5
done

echo "🔄 Начинаем восстановление в схему istudents..."

# Восстанавливаем дамп в указанную схему
if PGPASSWORD=$DB_PASSWORD pg_restore \
     -h $DB_HOST \
     -p $DB_PORT \
     -U $DB_USER \
     -d $DB_NAME \
     --clean \
     --if-exists \
     --schema=istudents \
     /dump/istudents_lab.backup; then
  echo "✅ Восстановление успешно!"
else
  echo "❌ Ошибка при восстановлении бэкапа"
  exit 1
fi
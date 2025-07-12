#!/bin/bash
set -e

# Выполнение скриптов
for script in /docker-entrypoint-initdb.d/*.sql; do
  echo "Executing: $script"
  /opt/mssql-tools18/bin/sqlcmd -S mssql-server -U sa -P YourStrong!Passw0rd -C -d master -i "$script"
done

echo "All initialization scripts completed!"
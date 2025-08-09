-- Создаём таблицу
CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Метка безопасности для таблицы
SECURITY LABEL FOR selinux ON TABLE clients IS 'system_u:object_r:sepgsql_table_t:s0';

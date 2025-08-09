-- Заполняем тестовыми данными с меткой confidential
INSERT INTO clients (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com');

-- Назначаем метку для всех строк таблицы как confidential
SECURITY LABEL ON COLUMN clients.name IS 'system_u:object_r:sepgsql_column_t:s0';
SECURITY LABEL ON COLUMN clients.email IS 'system_u:object_r:sepgsql_column_t:s0';

-- DAC: роль manager_role может вставлять новые строки
GRANT INSERT ON clients TO manager_role;
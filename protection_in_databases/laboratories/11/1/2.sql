-- Создаём роль manager_role
CREATE ROLE manager_role;

-- Создаём пользователей
CREATE USER confidential_user WITH PASSWORD 'pass1';
CREATE USER manager WITH PASSWORD 'pass2';

-- Привязываем manager к роли
GRANT manager_role TO manager;

-- Настройка MAC: метка для пользователя confidential_user
-- Этот пользователь сможет только читать строки с меткой confidential
SECURITY LABEL ON ROLE confidential_user IS 'system_u:object_r:sepgsql_unconfined_dbuser_t:s0';

-- Настройка MAC: метка для пользователя manager
-- Уровень допуска secret (условно, чтобы позволить изменения)
SECURITY LABEL ON ROLE manager IS 'system_u:object_r:sepgsql_unconfined_dbuser_t:s0-s0:c1.c1023';
-- Проверяем и устанавливаем расширение
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE USER user2 WITH PASSWORD '123';

GRANT CONNECT ON DATABASE ninth_laboratory_database_var_2 TO user2;
GRANT USAGE ON SCHEMA public TO user2;
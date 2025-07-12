-- Включим расширение для шифрования
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE USER user2 WITH PASSWORD '123';
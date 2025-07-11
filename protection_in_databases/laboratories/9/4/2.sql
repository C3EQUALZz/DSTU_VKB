CREATE TABLE user_accounts (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password BYTEA NOT NULL  -- Зашифрованный пароль
);

GRANT SELECT, UPDATE, INSERT ON user_accounts TO user2;
COMMENT ON TABLE user_accounts IS 'Таблица пользователей с зашифрованными паролями';
COMMENT ON COLUMN user_accounts.password IS 'Пароль, зашифрованный симметричным методом';
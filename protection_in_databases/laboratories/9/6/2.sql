-- Создаем таблицу для защищенных сообщений
CREATE TABLE secure_messages (
    id SERIAL PRIMARY KEY,
    message BYTEA NOT NULL,  -- Зашифрованное сообщение
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE secure_messages IS 'Таблица для хранения зашифрованных сообщений';
COMMENT ON COLUMN secure_messages.message IS 'Сообщение, зашифрованное симметричным ключом';

GRANT INSERT, SELECT ON secure_messages TO user2;
GRANT USAGE, SELECT ON SEQUENCE secure_messages_id_seq TO user2;
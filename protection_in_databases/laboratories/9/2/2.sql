-- Создаем таблицу платежных записей
CREATE TABLE payment_records (
    payment_id SERIAL PRIMARY KEY,
    account_number BYTEA NOT NULL,  -- Зашифрованный номер счета
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE payment_records IS 'Таблица платежных записей с зашифрованными номерами счетов';
COMMENT ON COLUMN payment_records.account_number IS 'Номер счета, зашифрованный симметричным ключом';

GRANT SELECT, INSERT ON payment_records TO user2;
GRANT USAGE, SELECT ON SEQUENCE payment_records_payment_id_seq TO user2;
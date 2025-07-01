CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user2') THEN
        CREATE USER user2 WITH PASSWORD '123';
    END IF;
END $$;

CREATE TABLE payment_records (
    payment_id SERIAL PRIMARY KEY,
    account_number BYTEA NOT NULL,  -- Зашифрованные данные
    amount DECIMAL(10, 2) NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE payment_records TO user2;


CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS audit_log;

set pgaudit.role = 'auditor';

CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00 CHECK (balance >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'frozen', 'closed')),
    last_activity DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE audit_log
(
    id         SERIAL PRIMARY KEY,
    table_name TEXT        NOT NULL,
    operation  TEXT        NOT NULL,
    username   TEXT        NOT NULL,
    old_value  JSONB,
    new_value  JSONB,
    timestamp  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS audit_log CASCADE;

set pgaudit.role = 'auditor';

CREATE TABLE transactions
(
    transaction_id   SERIAL PRIMARY KEY,
    amount           DECIMAL(10, 2) NOT NULL,
    transaction_date DATE           NOT NULL
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

GRANT SELECT ON transactions TO auditor;
REVOKE DELETE ON transactions FROM auditor;
REVOKE UPDATE ON transactions FROM auditor;
REVOKE INSERT ON transactions FROM auditor;
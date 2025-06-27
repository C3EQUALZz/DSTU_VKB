CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS sales CASCADE;

set pgaudit.role = 'auditor';

CREATE TABLE sales
(
    sale_id    SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    quantity   INT NOT NULL
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

REVOKE SELECT ON sales FROM auditor;
REVOKE DELETE ON sales FROM auditor;
GRANT UPDATE ON sales TO auditor;
GRANT INSERT ON sales TO auditor;
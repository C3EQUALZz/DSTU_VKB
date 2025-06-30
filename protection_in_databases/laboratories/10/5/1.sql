CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS audit_log CASCADE;

set pgaudit.role = 'auditor';

CREATE TABLE inventory
(
    item_id      SERIAL PRIMARY KEY,
    item_name    VARCHAR(100) NOT NULL,
    category     VARCHAR(50)  NOT NULL,
    quantity     INT          NOT NULL CHECK (quantity >= 0),
    price        DECIMAL(10, 2) CHECK (price > 0)
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
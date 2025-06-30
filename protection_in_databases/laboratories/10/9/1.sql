CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS logistics;
DROP TABLE IF EXISTS audit_log;

set pgaudit.role = 'auditor';

CREATE TABLE logistics (
    shipment_id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    last_updated TIMESTAMPTZ DEFAULT NOW()
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

REVOKE SELECT ON logistics FROM auditor;
REVOKE INSERT ON logistics FROM auditor;

GRANT DELETE ON logistics TO auditor;
GRANT UPDATE ON logistics TO auditor;

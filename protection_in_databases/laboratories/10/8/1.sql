CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS users;

set pgaudit.role = 'auditor';

CREATE TABLE users
(
    client_id SERIAL PRIMARY KEY,
    name      VARCHAR(100)        NOT NULL,
    email     VARCHAR(100) UNIQUE NOT NULL
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

REVOKE SELECT ON users FROM auditor;
GRANT DELETE ON users TO auditor;
REVOKE UPDATE ON users FROM auditor;
REVOKE INSERT ON users FROM auditor;
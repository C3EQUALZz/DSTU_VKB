CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;

set pgaudit.role = 'auditor';

DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

GRANT INSERT, SELECT (name, email) ON public.clients TO auditor;
REVOKE UPDATE, DELETE ON public.clients FROM auditor;

CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    log_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;

set pgaudit.role = 'auditor';

DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS orders CASCADE;

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
    order_date DATE NOT NULL
);

GRANT INSERT ON public.orders TO auditor;
GRANT SELECT ON public.orders TO auditor;
GRANT UPDATE ON public.orders TO auditor;
GRANT DELETE ON public.orders TO auditor;

CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    log_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


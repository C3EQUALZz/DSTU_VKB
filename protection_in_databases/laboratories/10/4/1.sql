CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS audit_log;

set pgaudit.role = 'auditor';

CREATE TABLE employees
(
    employee_id SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE               NOT NULL,
    position    VARCHAR(100)                      NOT NULL,
    salary      DECIMAL(10, 2) CHECK (salary > 0) NOT NULL
);

-- Создание таблицы audit_log
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    change_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

GRANT UPDATE ON public.employees TO auditor;
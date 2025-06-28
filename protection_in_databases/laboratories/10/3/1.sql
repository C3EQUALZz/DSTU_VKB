CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS products;

set pgaudit.role = 'auditor';

CREATE TABLE products
(
    product_id   SERIAL PRIMARY KEY,
    product_name VARCHAR(100) UNIQUE              NOT NULL,
    price        DECIMAL(10, 2) CHECK (price > 0) NOT NULL
);
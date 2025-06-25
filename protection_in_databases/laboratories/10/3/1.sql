CREATE EXTENSION IF NOT EXISTS pgaudit;
CREATE ROLE auditor;

set pgaudit.role = 'auditor';

DROP TABLE IF EXISTS products;

CREATE TABLE products
(
    product_id   SERIAL PRIMARY KEY,
    product_name VARCHAR(100) UNIQUE              NOT NULL,
    price        DECIMAL(10, 2) CHECK (price > 0) NOT NULL
);
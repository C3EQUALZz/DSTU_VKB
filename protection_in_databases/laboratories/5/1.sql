-- 1. Создание последовательности для автоматического ввода кода товара
CREATE SEQUENCE products_product_id_seq START 1;

-- 2. Создание таблицы "Группы товаров"
CREATE TABLE product_groups (
    group_id INTEGER PRIMARY KEY,
    group_name TEXT NOT NULL,
    total_quantity INTEGER NOT NULL DEFAULT 0,
    total_retail_value NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    markup NUMERIC(5,2) CHECK (markup BETWEEN 0 AND 1) NOT NULL
);

-- 3. Создание таблицы "Товары"
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY DEFAULT nextval('products_product_id_seq'),
    product_name TEXT NOT NULL,
    group_id INTEGER REFERENCES product_groups(group_id) ON UPDATE CASCADE,
    purchase_price NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    retail_price NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    quantity INTEGER NOT NULL DEFAULT 0
);
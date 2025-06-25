DROP TABLE IF EXISTS inventory CASCADE;

CREATE TABLE inventory (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price DECIMAL(10, 2) CHECK (price > 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
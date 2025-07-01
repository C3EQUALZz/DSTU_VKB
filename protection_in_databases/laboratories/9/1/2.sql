CREATE TABLE client_data (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email BYTEA NOT NULL  -- поле для зашифрованных данных
);

GRANT SELECT ON client_data TO user2;
-- Шифруем email симметричным ключом 'secret_key'
INSERT INTO client_data (name, email)
VALUES
    ('Иван Петров', pgp_sym_encrypt('ivan@example.com', 'secret_key')),
    ('Мария Сидорова', pgp_sym_encrypt('maria@example.com', 'secret_key'));
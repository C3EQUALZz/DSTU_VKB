INSERT INTO user_accounts (username, password)
VALUES
    ('alexey', encrypt_password('strongPass123!')),
    ('maria', encrypt_password('m@riaSecure2025')),
    ('admin', encrypt_password('Adm!nP@ssw0rd'));
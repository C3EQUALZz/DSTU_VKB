INSERT INTO payment_records (account_number, amount)
VALUES
    (pgp_sym_encrypt('40817810500000000001', 'my_strong_key_123!'), 1500.75),
    (pgp_sym_encrypt('40817810500000000002', 'my_strong_key_123!'), 3200.50);

-- Функция для расшифровки (для тестирования)
CREATE OR REPLACE FUNCTION decrypt_account(encrypted BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted, 'my_strong_key_123!');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Даем права на функцию
GRANT EXECUTE ON FUNCTION decrypt_account(bytea) TO user2;
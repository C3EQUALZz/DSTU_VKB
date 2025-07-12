CREATE OR REPLACE FUNCTION encrypt_account(account_number TEXT)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(account_number, 'payment_secret_key_2025', 'cipher-algo=aes256');
END;
$$ LANGUAGE plpgsql;

-- Функция для дешифровки номера счета
CREATE OR REPLACE FUNCTION decrypt_account(encrypted_account BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted_account, 'payment_secret_key_2025');
END;
$$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION encrypt_account(TEXT) TO user2;
GRANT EXECUTE ON FUNCTION decrypt_account(BYTEA) TO user2;
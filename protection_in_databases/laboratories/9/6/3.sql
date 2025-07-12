-- Функция для шифрования сообщения
CREATE OR REPLACE FUNCTION encrypt_message(msg TEXT)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(msg, 'super-key', 'cipher-algo=aes256');
END;
$$ LANGUAGE plpgsql;

-- Функция для дешифровки сообщения
CREATE OR REPLACE FUNCTION decrypt_message(encrypted BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted, 'super-key');
END;
$$ LANGUAGE plpgsql;

GRANT EXECUTE ON FUNCTION encrypt_message(TEXT) TO user2;
GRANT EXECUTE ON FUNCTION decrypt_message(BYTEA) TO user2;
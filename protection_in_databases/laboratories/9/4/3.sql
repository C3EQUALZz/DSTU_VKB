CREATE OR REPLACE FUNCTION encrypt_password(plain_password TEXT)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(plain_password, 'password_encryption_key_2025', 'compress-algo=1, cipher-algo=aes256');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION decrypt_password(encrypted_data BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted_data, 'password_encryption_key_2025');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Права на функции
GRANT EXECUTE ON FUNCTION encrypt_password(TEXT) TO user2;
GRANT EXECUTE ON FUNCTION decrypt_password(bytea) TO user2;
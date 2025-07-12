-- Функция для шифрования диагноза
CREATE OR REPLACE FUNCTION encrypt_diagnosis(text)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt($1, 'medical_secret_key', 'compress-algo=1, cipher-algo=aes256');
END;
$$ LANGUAGE plpgsql;

-- Функция для дешифровки диагноза
CREATE OR REPLACE FUNCTION decrypt_diagnosis(encrypted_data BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted_data, 'medical_secret_key');
END;
$$ LANGUAGE plpgsql;


-- Даем права на таблицу и функции
GRANT EXECUTE ON FUNCTION encrypt_diagnosis(text) TO user2;
GRANT EXECUTE ON FUNCTION decrypt_diagnosis(bytea) TO user2;

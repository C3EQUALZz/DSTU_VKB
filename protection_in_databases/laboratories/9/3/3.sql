CREATE OR REPLACE FUNCTION decrypt_salary(encrypted BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted, 'my_strong_key_123!');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION encrypt_salary(salary numeric)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(salary::text, 'my_strong_key_123!');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

GRANT EXECUTE ON FUNCTION decrypt_salary(bytea) TO user2;
GRANT EXECUTE ON FUNCTION encrypt_salary(numeric) TO user2;


INSERT INTO employee_info (first_name, last_name, email, salary)
VALUES
    ('Иван', 'Иванов', 'ivanov@company.com', encrypt_salary(100000)),
    ('Мария', 'Петрова', 'petrova@company.com', encrypt_salary(85000)),
    ('Алексей', 'Сидоров', 'sidorov@company.com', encrypt_salary(92000));
-- Создаем таблицу с зашифрованным полем salary
CREATE TABLE employee_info (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    salary BYTEA NOT NULL,  -- Зашифрованное поле
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE
);

GRANT SELECT, UPDATE, INSERT ON employee_info TO user2;
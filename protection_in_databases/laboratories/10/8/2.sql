-- Создание триггерной функции
CREATE OR REPLACE FUNCTION log_user_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
    VALUES (
        TG_TABLE_NAME,
        'INSERT',
        current_user,
        NULL,  -- Для INSERT старое значение отсутствует
        to_jsonb(NEW)  -- Всё содержимое новой строки
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER users_insert_audit_trigger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_insert();
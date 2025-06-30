-- Создание функции триггера
CREATE OR REPLACE FUNCTION log_employees_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Для операции вставки фиксируем только новые значения
        INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
        VALUES (TG_TABLE_NAME, TG_OP, current_user,
                NULL,
                jsonb_build_object(
                    'position', NEW.position,
                    'salary', NEW.salary
                ));
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        -- Для обновления фиксируем старые и новые значения
        INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
        VALUES (TG_TABLE_NAME, TG_OP, current_user,
                jsonb_build_object(
                    'position', OLD.position,
                    'salary', OLD.salary
                ),
                jsonb_build_object(
                    'position', NEW.position,
                    'salary', NEW.salary
                ));
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        -- Для удаления фиксируем только старые значения
        INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
        VALUES (TG_TABLE_NAME, TG_OP, current_user,
                jsonb_build_object(
                    'position', OLD.position,
                    'salary', OLD.salary
                ),
                NULL);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера для всех операций
CREATE TRIGGER employees_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON employees
FOR EACH ROW
EXECUTE FUNCTION log_employees_changes();
-- Функция триггера для аудита
CREATE OR REPLACE FUNCTION log_orders_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
        VALUES (
            TG_TABLE_NAME,
            'INSERT',
            current_user,
            NULL,
            row_to_json(NEW)::JSONB
        );
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
        VALUES (
            TG_TABLE_NAME,
            'UPDATE',
            current_user,
            row_to_json(OLD)::JSONB,
            row_to_json(NEW)::JSONB
        );
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
        VALUES (
            TG_TABLE_NAME,
            'DELETE',
            current_user,
            row_to_json(OLD)::JSONB,
            NULL
        );
        RETURN OLD;

    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER orders_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW
EXECUTE FUNCTION log_orders_changes();
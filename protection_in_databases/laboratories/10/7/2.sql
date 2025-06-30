-- Триггерная функция
CREATE OR REPLACE FUNCTION log_sales_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
    VALUES (
        'sales',
        'UPDATE',
        current_user,
        jsonb_build_object(
            'amount', OLD.amount,
            'status', OLD.status
        ),
        jsonb_build_object(
            'amount', NEW.amount,
            'status', NEW.status
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер
CREATE TRIGGER sales_update_audit_trigger
AFTER UPDATE OF amount, status ON sales  -- Срабатывает только при изменении указанных колонок
FOR EACH ROW
EXECUTE FUNCTION log_sales_update();
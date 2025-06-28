-- Триггерная функция
CREATE OR REPLACE FUNCTION log_account_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
        VALUES (
            TG_TABLE_NAME,
            'UPDATE',
            current_user,
            to_jsonb(OLD),  -- Все поля старой версии
            to_jsonb(NEW)   -- Все поля новой версии
        );
        RETURN NEW;

    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
        VALUES (
            TG_TABLE_NAME,
            'DELETE',
            current_user,
            to_jsonb(OLD),  -- Все поля удаляемой записи
            NULL
        );
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Триггер
CREATE TRIGGER accounts_audit_trigger
AFTER UPDATE OR DELETE ON accounts
FOR EACH ROW
EXECUTE FUNCTION log_account_changes();
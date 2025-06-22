CREATE OR REPLACE FUNCTION log_clients_update()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
    VALUES (TG_TABLE_NAME,
            'UPDATE',
            current_user,
            row_to_json(OLD)::JSONB,
            row_to_json(NEW)::JSONB);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER clients_audit_trigger
    AFTER UPDATE
    ON clients
    FOR EACH ROW
EXECUTE FUNCTION log_clients_update();
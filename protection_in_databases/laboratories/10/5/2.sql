CREATE OR REPLACE FUNCTION log_inventory_changes()
    RETURNS TRIGGER AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
        VALUES (TG_TABLE_NAME,
                'INSERT',
                current_user,
                NULL,
                to_jsonb(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
        VALUES (TG_TABLE_NAME,
                'UPDATE',
                current_user,
                to_jsonb(OLD),
                to_jsonb(NEW));
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER inventory_audit_trigger
AFTER INSERT OR UPDATE ON inventory
FOR EACH ROW
EXECUTE FUNCTION log_inventory_changes();

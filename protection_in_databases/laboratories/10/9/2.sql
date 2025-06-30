-- Триггерная функция
CREATE OR REPLACE FUNCTION log_logistics_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, username, old_value, new_value)
    VALUES (
        'logistics',
        'UPDATE',
        current_user,
        jsonb_build_object(
            'location', OLD.location,
            'status', OLD.status,
            'shipment_id', OLD.shipment_id
        ),
        jsonb_build_object(
            'location', NEW.location,
            'status', NEW.status,
            'shipment_id', NEW.shipment_id
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер
CREATE TRIGGER logistics_update_audit_trigger
AFTER UPDATE OF location, status ON logistics
FOR EACH ROW
EXECUTE FUNCTION log_logistics_update();
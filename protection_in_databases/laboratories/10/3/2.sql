CREATE TABLE IF NOT EXISTS audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    log_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Функция триггера для логирования DELETE операций
CREATE OR REPLACE FUNCTION log_products_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, user_name, old_value, new_value)
    VALUES (
        TG_TABLE_NAME,
        'DELETE',
        current_user,
        row_to_json(OLD)::JSONB,
        NULL
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера для таблицы products
CREATE TRIGGER products_delete_trigger
AFTER DELETE ON products
FOR EACH ROW
EXECUTE FUNCTION log_products_delete();
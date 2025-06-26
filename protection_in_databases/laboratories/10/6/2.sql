-- Создание триггерной функции для логирования удалений
CREATE OR REPLACE FUNCTION log_transaction_deletes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (
                           table_name,
                           operation,
                           username,
                           old_value,
                           new_value
    )
    VALUES (
        TG_TABLE_NAME,
        'DELETE',
        current_user,
        to_jsonb(OLD),  -- Захват всей удалённой строки
        NULL            -- Для DELETE нового значения нет
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера на таблице transactions
CREATE TRIGGER transactions_delete_trigger
AFTER DELETE ON transactions
FOR EACH ROW
EXECUTE FUNCTION log_transaction_deletes();
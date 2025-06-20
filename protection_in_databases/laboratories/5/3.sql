-- 5. Триггерная функция для обновления данных группы при изменении товаров
CREATE OR REPLACE FUNCTION update_group_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Пересчет после удаления товара
    IF (TG_OP = 'DELETE') THEN
        UPDATE product_groups
        SET
            total_quantity = total_quantity - OLD.quantity,
            total_retail_value = total_retail_value - (OLD.retail_price * OLD.quantity)
        WHERE group_id = OLD.group_id;

    -- Пересчет после вставки нового товара
    ELSIF (TG_OP = 'INSERT') THEN
        UPDATE product_groups
        SET
            total_quantity = total_quantity + NEW.quantity,
            total_retail_value = total_retail_value + (NEW.retail_price * NEW.quantity)
        WHERE group_id = NEW.group_id;

    -- Пересчет после обновления товара
    ELSIF (TG_OP = 'UPDATE') THEN
        -- Обновление старой группы
        IF OLD.group_id <> NEW.group_id THEN
            UPDATE product_groups
            SET
                total_quantity = total_quantity - OLD.quantity,
                total_retail_value = total_retail_value - (OLD.retail_price * OLD.quantity)
            WHERE group_id = OLD.group_id;

            -- Обновление новой группы
            UPDATE product_groups
            SET
                total_quantity = total_quantity + NEW.quantity,
                total_retail_value = total_retail_value + (NEW.retail_price * NEW.quantity)
            WHERE group_id = NEW.group_id;
        ELSE
            -- Обновление в рамках одной группы
            UPDATE product_groups
            SET
                total_quantity = total_quantity + (NEW.quantity - OLD.quantity),
                total_retail_value = total_retail_value +
                    ((NEW.retail_price * NEW.quantity) - (OLD.retail_price * OLD.quantity))
            WHERE group_id = NEW.group_id;
        END IF;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Триггер для обновления данных группы
CREATE TRIGGER group_stats_trigger
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION update_group_stats();
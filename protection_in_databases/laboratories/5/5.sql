-- 7. Триггер для пересчета сводной стоимости при изменении розничной цены
CREATE OR REPLACE FUNCTION update_total_value_on_price_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Пересчет стоимости группы при изменении цены товара
    UPDATE product_groups
    SET total_retail_value = total_retail_value +
        ((NEW.retail_price * NEW.quantity) - (OLD.retail_price * OLD.quantity))
    WHERE group_id = NEW.group_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для обновления сводной стоимости
CREATE TRIGGER price_change_trigger
AFTER UPDATE OF retail_price ON products
FOR EACH ROW
EXECUTE FUNCTION update_total_value_on_price_change();
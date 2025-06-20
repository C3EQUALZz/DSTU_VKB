-- 6. Триггер для пересчета цен при изменении наценки группы
CREATE OR REPLACE FUNCTION update_prices_on_markup_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Обновление розничных цен товаров группы
    UPDATE products
    SET retail_price = purchase_price * (1 + NEW.markup)
    WHERE group_id = NEW.group_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для реакции на изменение наценки
CREATE TRIGGER markup_change_trigger
AFTER UPDATE ON product_groups
FOR EACH ROW
WHEN (OLD.markup IS DISTINCT FROM NEW.markup)
EXECUTE FUNCTION update_prices_on_markup_change();
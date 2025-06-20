-- 4. Триггерная функция для автоматического расчета розничной цены
CREATE OR REPLACE FUNCTION update_retail_price()
RETURNS TRIGGER AS $$
BEGIN
    -- Пересчет цены при вставке/обновлении товара
    NEW.retail_price = NEW.purchase_price * (1 + (SELECT markup FROM product_groups WHERE group_id = NEW.group_id));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоматического расчета цены
CREATE TRIGGER retail_price_trigger
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION update_retail_price();
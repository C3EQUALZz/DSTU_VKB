/**
  Определить триггерную функцию(-и), которая(-ые) при добавлении новой записи в таблицу БД проверяет наличие такой записи
  среди существующих объектов (сравнение по id).
  Если запись с таким id найдена, то для этой записи устанавливается время смерти, а добавляемая запись содержит в себе
  соответственные значения атрибутов найденной записи (кроме тех, которые заданы для новой записи),
  пустое значение времени смерти и новое значение времени рождения, равное текущему моменту.
  Таким образом, у новой записи время рождения равно, времени смерти ее предка.
  Если запись с таким id на найдена, то происходит ее добавление в БД с установлением в качестве времени рождения текущего
  момента времени.
 */

CREATE OR REPLACE FUNCTION handle_insert_object()
RETURNS TRIGGER AS $$
DECLARE
    existing_record my_object%ROWTYPE;
BEGIN
    -- Проверка наличия записи с таким же id и без времени смерти
    SELECT * INTO existing_record
    FROM my_object
    WHERE id = NEW.id AND time_dead IS NULL
    ORDER BY time_create DESC
    LIMIT 1;

    IF FOUND THEN
        -- Если запись найдена, установить время смерти предка
        UPDATE my_object
        SET time_dead = now()
        WHERE id = existing_record.id AND time_create = existing_record.time_create;

        -- Перенос значений времени и сброс времени смерти
        NEW.time_create = now();  -- Новое время создания записи
        NEW.time_dead = NULL;     -- Сбрасываем время смерти

    ELSE
        -- Если запись не найдена, просто устанавливаем время создания
        NEW.time_create = now();
        NEW.time_dead = NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE TRIGGER handle_insert_electronic_equipment
BEFORE INSERT ON electronic_equipment
FOR EACH ROW EXECUTE FUNCTION handle_insert_object();

CREATE OR REPLACE TRIGGER handle_insert_furniture
BEFORE INSERT ON furniture
FOR EACH ROW EXECUTE FUNCTION handle_insert_object();

CREATE OR REPLACE TRIGGER handle_insert_consumables
BEFORE INSERT ON consumables
FOR EACH ROW EXECUTE FUNCTION handle_insert_object();

-- Вставляем новую запись в таблицу furniture
INSERT INTO furniture (id, material, dimensions)
VALUES (1, 'Wood', '100x50x75');

-- Вставляем запись с таким же id (это вызовет обновление времени смерти первой записи)
INSERT INTO furniture (id, material, dimensions)
VALUES (1, 'Metal', '120x60x75');

-- Проверяем записи в my_object
SELECT * FROM my_object;

-- Проверяем записи в furniture
SELECT * FROM furniture;

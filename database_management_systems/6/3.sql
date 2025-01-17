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

CREATE OR REPLACE FUNCTION handle_object_insert()
RETURNS TRIGGER
LANGUAGE plpgsql AS
$$
BEGIN
    -- Проверяем, существует ли запись с таким же id
    IF EXISTS (
        SELECT 1
        FROM ONLY my_object
        WHERE id = NEW.id
          AND time_dead IS NULL -- Только "активные" записи
    ) THEN
        -- Обновляем время смерти существующей записи
        UPDATE ONLY my_object
        SET time_dead = NOW()
        WHERE id = NEW.id
          AND time_dead IS NULL;

        -- Наследуем значения атрибутов существующей записи (кроме заданных в новой)
        NEW.time_create = NOW(); -- Устанавливаем время рождения
    ELSE
        -- Если записи с таким id не найдено, просто задаем текущее время рождения
        NEW.time_create = NOW();
    END IF;

    -- Убедиться, что время смерти новой записи остается NULL
    NEW.time_dead = NULL;

    RETURN NEW;
END;
$$;

-- Триггер для таблицы electronic_equipment
CREATE TRIGGER before_insert_electronic_equipment
BEFORE INSERT ON electronic_equipment
FOR EACH ROW
EXECUTE FUNCTION handle_object_insert();

-- Триггер для таблицы furniture
CREATE TRIGGER before_insert_furniture
BEFORE INSERT ON furniture
FOR EACH ROW
EXECUTE FUNCTION handle_object_insert();

-- Триггер для таблицы consumables
CREATE TRIGGER before_insert_consumables
BEFORE INSERT ON consumables
FOR EACH ROW
EXECUTE FUNCTION handle_object_insert();

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

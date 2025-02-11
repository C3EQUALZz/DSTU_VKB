/**
  Создать таблицы БД (от 3х до 5ти), объявив их наследниками my_object;
 */

DROP TABLE IF EXISTS electronic_equipment CASCADE;
DROP TABLE IF EXISTS furniture CASCADE;
DROP TABLE IF EXISTS consumables CASCADE;

-- Таблица для техники. Техника может включать компьютеры, мониторы, принтеры и т.д.
CREATE TABLE electronic_equipment (
    warranty_period INTEGER NOT NULL,
    manufacturer VARCHAR(100)
) INHERITS (my_object);

-- Таблица для мебели. Мебель, такая как стулья, столы, шкафы.
CREATE TABLE furniture (
    material VARCHAR(50) NOT NULL,
    dimensions VARCHAR(50)
) INHERITS (my_object);

-- Таблица для расходных материалов. Расходные материалы, такие как канцелярия, бумага или картриджи.
CREATE TABLE consumables (
    quantity INTEGER NOT NULL,        -- Количество
    unit VARCHAR(20) NOT NULL         -- Единица измерения (шт., пачки и т.д.)
) INHERITS (my_object);

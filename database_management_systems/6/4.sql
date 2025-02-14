/**
  Напишите собственную агрегатную функцию, которая производит конкатенацию всех строк в атрибуте, передаваемом в функцию
  в качестве аргумента, с заданным в качестве параметра функции символом-разделителем. Например, если в качестве значений
  атрибутов-аргументов агрегатной функции будут выступать строки ‘123’, ‘456’ и ‘789’, а в качестве символа разделителя
  будет задан ‘_’, то агрегатная функция вернет значение ‘123_456_789’ в результате группирования этих трех кортежей
  (порядок сортировки по возрастанию);
 */

-- Функция для обновления состояния (конкатенация строк с разделителем)
CREATE OR REPLACE FUNCTION concat_with_delimiter_agg(
    state TEXT,         -- Текущее состояние (аккумулятор)
    value TEXT,         -- Значение из текущей строки
    delimiter TEXT      -- Разделитель
)
RETURNS TEXT
LANGUAGE plpgsql AS
'
BEGIN
    -- Если текущее состояние NULL, возвращаем текущее значение
    IF state IS NULL THEN
        RETURN value;
    END IF;

    -- Если текущее значение NULL, возвращаем состояние
    IF value IS NULL THEN
        RETURN state;
    END IF;

    -- Конкатенируем состояние и значение через разделитель
    RETURN state || delimiter || value;
END;
';

-- Функция для возврата итогового результата (в данном случае просто возвращает результат state)
CREATE OR REPLACE FUNCTION concat_with_delimiter_final(state TEXT)
RETURNS TEXT
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN state;
END;
$$;

-- Создание агрегатной функции
CREATE OR REPLACE AGGREGATE concat_with_delimiter(TEXT, TEXT) (
    SFUNC = concat_with_delimiter_agg,  -- State transition function
    STYPE = TEXT,                      -- Тип состояния (аккумулятор)
    FINALFUNC = concat_with_delimiter_final -- Final function
);

-- Пример таблицы
CREATE TEMP TABLE test_data (
    value TEXT
);

-- Заполнение тестовыми данными
INSERT INTO test_data (value)
VALUES
    ('123'),
    ('456'),
    ('789');

-- Использование агрегатной функции
SELECT concat_with_delimiter(value, '_') AS concatenated_result
FROM test_data;

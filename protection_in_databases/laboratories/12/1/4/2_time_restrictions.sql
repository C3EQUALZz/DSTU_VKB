-- Лабораторная работа № 12: Временные ограничения доступа
-- Вариант 1: Ограничение операций INSERT в нерабочее время (9:00-18:00)

-- ============================================================================
-- 1. ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ВРЕМЕНИ ДОСТУПА
-- ============================================================================

CREATE OR REPLACE FUNCTION restrict_insert_by_time()
RETURNS TRIGGER AS $$
DECLARE
    current_hour INTEGER;
BEGIN
    -- Получаем текущий час
    current_hour := EXTRACT(HOUR FROM CURRENT_TIMESTAMP);

    -- Проверяем, находится ли текущее время в рабочем диапазоне (9:00 - 18:00)
    IF current_hour < 9 OR current_hour >= 18 THEN
        RAISE EXCEPTION 'Доступ запрещен: операции INSERT разрешены только в рабочее время (9:00 - 18:00). Текущее время: %',
            TO_CHAR(CURRENT_TIMESTAMP, 'HH24:MI:SS');
    END IF;

    -- Логируем успешную попытку доступа
    RAISE NOTICE 'Доступ разрешен. Время: %, Пользователь: %',
        TO_CHAR(CURRENT_TIMESTAMP, 'HH24:MI:SS'),
        CURRENT_USER;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION restrict_insert_by_time() IS
'Функция ограничивает операции INSERT в таблицу clients вне рабочего времени (9:00-18:00)';

-- ============================================================================
-- 2. ТРИГГЕР ДЛЯ ОГРАНИЧЕНИЯ ОПЕРАЦИЙ INSERT
-- ============================================================================

CREATE OR REPLACE TRIGGER check_insert_time
    BEFORE INSERT ON clients
    FOR EACH ROW
    EXECUTE FUNCTION restrict_insert_by_time();

COMMENT ON TRIGGER check_insert_time ON clients IS
'Триггер проверяет время перед выполнением INSERT и блокирует операцию вне рабочих часов';

-- ============================================================================
-- 3. ДОПОЛНИТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ РАСШИРЕННОЙ ПРОВЕРКИ ВРЕМЕНИ
-- ============================================================================

-- Функция для проверки всех операций (INSERT, UPDATE, DELETE)
CREATE OR REPLACE FUNCTION restrict_all_operations_by_time()
RETURNS TRIGGER AS $$
DECLARE
    current_hour INTEGER;
    current_day INTEGER;
    operation_type TEXT;
BEGIN
    -- Получаем текущий час и день недели
    current_hour := EXTRACT(HOUR FROM CURRENT_TIMESTAMP);
    current_day := EXTRACT(DOW FROM CURRENT_TIMESTAMP); -- 0=Воскресенье, 6=Суббота

    -- Определяем тип операции
    operation_type := TG_OP;

    -- Проверяем, не выходные ли (опционально)
    IF current_day = 0 OR current_day = 6 THEN
        RAISE EXCEPTION 'Доступ запрещен: операции % не разрешены в выходные дни', operation_type;
    END IF;

    -- Проверяем рабочее время
    IF current_hour < 9 OR current_hour >= 18 THEN
        RAISE EXCEPTION 'Доступ запрещен: операции % разрешены только в рабочее время (9:00 - 18:00). Текущее время: %',
            operation_type,
            TO_CHAR(CURRENT_TIMESTAMP, 'HH24:MI:SS');
    END IF;

    -- Логируем успешную операцию
    RAISE NOTICE '% выполнена успешно. Время: %, Пользователь: %',
        operation_type,
        TO_CHAR(CURRENT_TIMESTAMP, 'HH24:MI:SS'),
        CURRENT_USER;

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION restrict_all_operations_by_time() IS
'Расширенная функция для ограничения всех операций (INSERT/UPDATE/DELETE) вне рабочего времени и в выходные';

-- ============================================================================
-- 4. ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ТЕКУЩЕГО ВРЕМЕНИ И СТАТУСА ДОСТУПА
-- ============================================================================

CREATE OR REPLACE FUNCTION check_current_access_status()
RETURNS TABLE(
    current_timestamp_value TIMESTAMP,  -- Изменено с current_time
    current_hour INTEGER,
    day_of_week TEXT,
    is_working_hours BOOLEAN,
    is_weekend BOOLEAN,
    access_allowed BOOLEAN,
    message TEXT
) AS $$
DECLARE
    hour_now INTEGER;
    day_now INTEGER;
    working_hours BOOLEAN;
    weekend BOOLEAN;
BEGIN
    hour_now := EXTRACT(HOUR FROM CURRENT_TIMESTAMP);
    day_now := EXTRACT(DOW FROM CURRENT_TIMESTAMP);

    working_hours := (hour_now >= 9 AND hour_now < 18);
    weekend := (day_now = 0 OR day_now = 6);

    RETURN QUERY SELECT
        CURRENT_TIMESTAMP,
        hour_now,
        TO_CHAR(CURRENT_TIMESTAMP, 'Day'),
        working_hours,
        weekend,
        working_hours AND NOT weekend,
        CASE
            WHEN weekend THEN 'Выходной день - доступ запрещен'
            WHEN working_hours THEN 'Рабочее время - доступ разрешен'
            ELSE 'Нерабочее время - доступ запрещен'
        END;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION check_current_access_status() IS
'Функция для проверки текущего статуса доступа на основе времени';

-- ============================================================================
-- 5. ТАБЛИЦА ДЛЯ ЛОГИРОВАНИЯ ПОПЫТОК ДОСТУПА
-- ============================================================================

CREATE TABLE IF NOT EXISTS access_log (
    log_id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    operation VARCHAR(10),
    table_name VARCHAR(100),
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN,
    client_addr INET,
    error_message TEXT
);

COMMENT ON TABLE access_log IS 'Журнал попыток доступа к таблице clients';

-- Функция для логирования попыток доступа
CREATE OR REPLACE FUNCTION log_access_attempt()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO access_log (username, operation, table_name, success, client_addr)
    VALUES (CURRENT_USER, TG_OP, TG_TABLE_NAME, TRUE, inet_client_addr());

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Триггер для логирования всех операций
CREATE TRIGGER log_operations
    AFTER INSERT OR UPDATE OR DELETE ON clients
    FOR EACH ROW
    EXECUTE FUNCTION log_access_attempt();


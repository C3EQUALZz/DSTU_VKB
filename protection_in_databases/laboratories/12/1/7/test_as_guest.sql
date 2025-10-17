-- Тестирование от имени пользователя guest_user
-- Подключитесь как: psql -U guest_user -d postgres

\echo '========================================'
\echo 'ТЕСТИРОВАНИЕ ОТ ИМЕНИ GUEST_USER'
\echo '========================================'
\echo ''

-- Проверка текущего пользователя
\echo 'Текущий пользователь:'
SELECT CURRENT_USER, SESSION_USER;
\echo ''

-- Диагностика доступа
\echo 'Диагностика доступа:'
SELECT * FROM diagnose_access();
\echo ''

-- Попытка прочитать данные
\echo 'Чтение данных (гость видит все записи в режиме только для чтения):'
SELECT client_id, name, email FROM clients ORDER BY client_id LIMIT 5;
\echo ''
\echo 'Количество видимых записей:'
SELECT COUNT(*) AS visible_records FROM clients;
\echo ''

-- Попытка вставить запись (должно быть заблокировано)
\echo 'Попытка вставки записи (должно быть заблокировано):'
DO $$
BEGIN
    INSERT INTO clients (name, email) 
    VALUES ('Гость Тест', 'guest_test@example.com');
    
    RAISE NOTICE '✗ ОШИБКА: Гостю удалось вставить запись!';
EXCEPTION
    WHEN insufficient_privilege THEN
        RAISE NOTICE '✓ Правильно: Вставка заблокирована (недостаточно прав)';
    WHEN OTHERS THEN
        RAISE NOTICE '✓ Правильно: Вставка заблокирована (%)', SQLERRM;
END $$;
\echo ''

-- Попытка обновить запись (должно быть заблокировано)
\echo 'Попытка обновления записи (должно быть заблокировано):'
DO $$
BEGIN
    UPDATE clients 
    SET name = 'Попытка изменить'
    WHERE client_id = (SELECT MIN(client_id) FROM clients);
    
    IF FOUND THEN
        RAISE NOTICE '✗ ОШИБКА: Гостю удалось обновить запись!';
    ELSE
        RAISE NOTICE '✓ Правильно: Обновление заблокировано';
    END IF;
EXCEPTION
    WHEN insufficient_privilege THEN
        RAISE NOTICE '✓ Правильно: Обновление заблокировано (недостаточно прав)';
    WHEN OTHERS THEN
        RAISE NOTICE '✓ Правильно: Обновление заблокировано (%)', SQLERRM;
END $$;
\echo ''

-- Попытка удалить запись (должно быть заблокировано)
\echo 'Попытка удаления записи (должно быть заблокировано):'
DO $$
BEGIN
    DELETE FROM clients 
    WHERE client_id = (SELECT MIN(client_id) FROM clients);
    
    IF FOUND THEN
        RAISE NOTICE '✗ ОШИБКА: Гостю удалось удалить запись!';
    ELSE
        RAISE NOTICE '✓ Правильно: Удаление заблокировано';
    END IF;
EXCEPTION
    WHEN insufficient_privilege THEN
        RAISE NOTICE '✓ Правильно: Удаление заблокировано (недостаточно прав)';
    WHEN OTHERS THEN
        RAISE NOTICE '✓ Правильно: Удаление заблокировано (%)', SQLERRM;
END $$;
\echo ''

\echo 'ОЖИДАЕМЫЙ РЕЗУЛЬТАТ для гостя:'
\echo '  ✓ Может читать все записи'
\echo '  ✗ НЕ может добавлять записи'
\echo '  ✗ НЕ может изменять записи'
\echo '  ✗ НЕ может удалять записи'
\echo ''


-- Тестирование от имени пользователя employee_user
-- Подключитесь как: psql -U employee_user -d postgres

\echo '========================================'
\echo 'ТЕСТИРОВАНИЕ ОТ ИМЕНИ EMPLOYEE_USER'
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
\echo 'Чтение данных (сотрудник видит только свои записи):'
SELECT client_id, name, email, created_by FROM clients ORDER BY client_id;
\echo ''
\echo 'Количество видимых записей:'
SELECT COUNT(*) AS visible_records FROM clients;
\echo ''

-- Попытка вставить запись
\echo 'Вставка новой записи:'
INSERT INTO clients (name, email) 
VALUES ('Сотрудник Тест', 'employee_test_' || EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::TEXT || '@example.com')
RETURNING *;
\echo ''

-- Проверка видимости только что созданной записи
\echo 'После вставки сотрудник видит свою запись:'
SELECT client_id, name, email, created_by FROM clients WHERE name LIKE '%Сотрудник Тест%';
\echo ''

-- Попытка обновить свою запись
\echo 'Обновление своей записи:'
UPDATE clients 
SET name = name || ' [изменено]'
WHERE name LIKE '%Сотрудник Тест%'
RETURNING *;
\echo ''

-- Попытка обновить чужую запись (должно быть заблокировано)
\echo 'Попытка обновить чужую запись (должно быть заблокировано):'
DO $$
BEGIN
    UPDATE clients 
    SET name = 'Попытка изменить'
    WHERE created_by != CURRENT_USER
    AND client_id = (SELECT MIN(client_id) FROM clients WHERE created_by != CURRENT_USER);
    
    IF FOUND THEN
        RAISE NOTICE '✗ ОШИБКА: Удалось обновить чужую запись!';
    ELSE
        RAISE NOTICE '✓ Правильно: Обновление чужой записи заблокировано';
    END IF;
END $$;
\echo ''

-- Очистка: удаление тестовой записи
\echo 'Удаление своей тестовой записи:'
DELETE FROM clients 
WHERE name LIKE '%Сотрудник Тест%'
RETURNING client_id, name;
\echo ''

\echo 'ОЖИДАЕМЫЙ РЕЗУЛЬТАТ для сотрудника:'
\echo '  ✓ Видит только свои записи (created_by = employee_user)'
\echo '  ✓ Может добавлять записи (в рабочее время)'
\echo '  ✓ Может изменять только свои записи'
\echo '  ✗ НЕ может изменять чужие записи'
\echo ''


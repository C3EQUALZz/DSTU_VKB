-- Тестирование от имени пользователя manager_user
-- Подключитесь как: psql -U manager_user -d postgres

\echo '========================================'
\echo 'ТЕСТИРОВАНИЕ ОТ ИМЕНИ MANAGER_USER'
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
\echo 'Чтение данных (менеджер должен видеть все записи):'
SELECT client_id, name, email, created_by FROM clients ORDER BY client_id;
\echo ''

-- Попытка вставить запись
\echo 'Вставка новой записи:'
INSERT INTO clients (name, email) 
VALUES ('Менеджер Тест', 'manager_test_' || EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::TEXT || '@example.com')
RETURNING *;
\echo ''

-- Попытка обновить запись
\echo 'Обновление записи:'
UPDATE clients 
SET name = name || ' [изменено менеджером]'
WHERE client_id = (SELECT MAX(client_id) FROM clients)
RETURNING *;
\echo ''

-- Попытка удалить запись
\echo 'Удаление тестовой записи:'
DELETE FROM clients 
WHERE name LIKE '%Менеджер Тест%'
RETURNING client_id, name;
\echo ''

\echo 'ОЖИДАЕМЫЙ РЕЗУЛЬТАТ для менеджера:'
\echo '  ✓ Доступ ко всем записям'
\echo '  ✓ Возможность INSERT (в рабочее время)'
\echo '  ✓ Возможность UPDATE'
\echo '  ✓ Возможность DELETE'
\echo ''


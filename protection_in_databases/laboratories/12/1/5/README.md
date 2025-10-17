## 5.  Проверьте корректность работы триггера, выполняя запросы в разные временные интервалы.

Подключитесь к базе данных от лица пользователя `postgres` и выполните запрос, который представлен ниже:

```sql
DO $$
DECLARE
    test_email TEXT;
    current_hour INTEGER;
BEGIN
    current_hour := EXTRACT(HOUR FROM CURRENT_TIMESTAMP);
    test_email := 'time_test_' || EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::TEXT || '@example.com';
    
    RAISE NOTICE 'Текущий час: %', current_hour;
    RAISE NOTICE 'Попытка вставки записи...';
    
    BEGIN
        INSERT INTO clients (name, email) 
        VALUES ('Тест временных ограничений', test_email);
        
        RAISE NOTICE '✓ УСПЕХ: Запись добавлена (текущее время в рабочих часах)';
        RAISE NOTICE 'Email: %', test_email;
        
        -- Удаляем тестовую запись
        DELETE FROM clients WHERE email = test_email;
        RAISE NOTICE 'Тестовая запись удалена';
        
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE '✗ БЛОКИРОВКА: %', SQLERRM;
            RAISE NOTICE 'Это нормально, если сейчас нерабочее время (не 9:00-18:00)';
    END;
END $$;
```


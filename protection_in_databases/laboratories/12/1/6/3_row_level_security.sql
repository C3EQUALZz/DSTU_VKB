-- Лабораторная работа № 12: Row Level Security (RLS)
-- Вариант 1: Политики безопасности на основе IP и ролей

-- ============================================================================
-- 1. ВКЛЮЧЕНИЕ ROW LEVEL SECURITY ДЛЯ ТАБЛИЦЫ CLIENTS
-- ============================================================================

ALTER TABLE clients ENABLE ROW LEVEL SECURITY;

-- Важно: владелец таблицы (обычно postgres) обходит RLS по умолчанию
-- Для применения RLS ко всем пользователям, включая владельца:
ALTER TABLE clients FORCE ROW LEVEL SECURITY;

\echo '✓ Row Level Security включена для таблицы clients'

-- ============================================================================
-- 2. ПОЛИТИКА ДОСТУПА НА ОСНОВЕ IP-АДРЕСА
-- ============================================================================

-- Политика: разрешить доступ только с IP из сети 192.168.1.0/24
CREATE POLICY ip_based_access ON clients
    FOR ALL
    TO PUBLIC
    USING (
        -- Проверяем, что IP клиента находится в разрешенной подсети
        inet_client_addr() << '192.168.1.0/24'::inet
        OR
        -- Разрешаем локальные подключения (когда inet_client_addr() возвращает NULL)
        inet_client_addr() IS NULL
        OR
        -- Разрешаем подключения с localhost
        inet_client_addr() = '127.0.0.1'::inet
        OR
        inet_client_addr() = '::1'::inet
    );

COMMENT ON POLICY ip_based_access ON clients IS 
'Ограничивает доступ к таблице clients только для IP из сети 192.168.1.0/24';

\echo '✓ Политика ip_based_access создана (доступ только с 192.168.1.0/24)'

-- ============================================================================
-- 3. ПОЛИТИКА ДОСТУПА НА ОСНОВЕ РОЛИ ПОЛЬЗОВАТЕЛЯ
-- ============================================================================

-- Политика для менеджеров: полный доступ ко всем записям
CREATE POLICY manager_full_access ON clients
    FOR ALL
    TO manager_role
    USING (true)
    WITH CHECK (true);

COMMENT ON POLICY manager_full_access ON clients IS 
'Менеджеры имеют полный доступ ко всем записям';

-- Политика для сотрудников: доступ к записям, созданным ими
CREATE POLICY employee_own_records ON clients
    FOR ALL
    TO employee_role
    USING (created_by = CURRENT_USER)
    WITH CHECK (created_by = CURRENT_USER);

COMMENT ON POLICY employee_own_records ON clients IS 
'Сотрудники видят только свои записи';

-- Политика для гостей: только чтение всех записей
CREATE POLICY guest_read_only ON clients
    FOR SELECT
    TO guest_role
    USING (true);

COMMENT ON POLICY guest_read_only ON clients IS 
'Гости имеют доступ только на чтение';

\echo '✓ Политика manager_full_access создана'
\echo '✓ Политика employee_own_records создана'
\echo '✓ Политика guest_read_only создана'

-- ============================================================================
-- 4. КОМБИНИРОВАННАЯ ПОЛИТИКА: РОЛЬ + IP + ВРЕМЯ
-- ============================================================================

-- Создаем функцию для проверки комбинированных условий
CREATE OR REPLACE FUNCTION check_combined_access()
RETURNS BOOLEAN AS $$
DECLARE
    current_hour INTEGER;
    user_role TEXT;
    client_ip INET;
BEGIN
    current_hour := EXTRACT(HOUR FROM CURRENT_TIMESTAMP);
    client_ip := inet_client_addr();
    
    -- Получаем роль текущего пользователя
    SELECT rolname INTO user_role 
    FROM pg_roles 
    WHERE rolname IN ('manager_role', 'employee_role', 'guest_role')
    AND pg_has_role(CURRENT_USER, oid, 'member');
    
    -- Менеджеры имеют доступ всегда
    IF user_role = 'manager_role' THEN
        RETURN TRUE;
    END IF;
    
    -- Для остальных проверяем время и IP
    IF (current_hour >= 9 AND current_hour < 18) AND 
       (client_ip << '192.168.1.0/24'::inet OR client_ip IS NULL OR 
        client_ip = '127.0.0.1'::inet OR client_ip = '::1'::inet) THEN
        RETURN TRUE;
    END IF;
    
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION check_combined_access() IS 
'Проверяет комбинированные условия доступа: роль + IP + время';

-- ============================================================================
-- 5. ФУНКЦИЯ ДЛЯ ПРОСМОТРА АКТИВНЫХ ПОЛИТИК
-- ============================================================================

CREATE OR REPLACE FUNCTION view_table_policies(table_name_param TEXT DEFAULT 'clients')
RETURNS TABLE(
    policy_name NAME,
    table_schema NAME,
    table_name NAME,
    command TEXT,
    roles TEXT,
    qual TEXT,
    with_check TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pol.polname::NAME AS policy_name,
        n.nspname::NAME AS table_schema,
        c.relname::NAME AS table_name,
        CASE pol.polcmd
            WHEN 'r' THEN 'SELECT'
            WHEN 'a' THEN 'INSERT'
            WHEN 'w' THEN 'UPDATE'
            WHEN 'd' THEN 'DELETE'
            WHEN '*' THEN 'ALL'
        END AS command,
        array_to_string(ARRAY(
            SELECT rolname FROM pg_roles WHERE oid = ANY(pol.polroles)
        ), ', ') AS roles,
        pg_get_expr(pol.polqual, pol.polrelid) AS qual,
        pg_get_expr(pol.polwithcheck, pol.polrelid) AS with_check
    FROM pg_policy pol
    JOIN pg_class c ON c.oid = pol.polrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = table_name_param
    ORDER BY pol.polname;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION view_table_policies(TEXT) IS 
'Выводит все политики безопасности для указанной таблицы';

-- ============================================================================
-- 6. ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ДИАГНОСТИКИ
-- ============================================================================

CREATE OR REPLACE FUNCTION diagnose_access()
RETURNS TABLE(
    parameter TEXT,
    value TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'Текущий пользователь'::TEXT, CURRENT_USER::TEXT
    UNION ALL
    SELECT 'IP-адрес клиента'::TEXT, COALESCE(inet_client_addr()::TEXT, 'NULL (локальное подключение)')
    UNION ALL
    SELECT 'Текущее время'::TEXT, TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS')
    UNION ALL
    SELECT 'Текущий час'::TEXT, EXTRACT(HOUR FROM CURRENT_TIMESTAMP)::TEXT
    UNION ALL
    SELECT 'Рабочее время?'::TEXT, 
        CASE 
            WHEN EXTRACT(HOUR FROM CURRENT_TIMESTAMP) BETWEEN 9 AND 17 
            THEN 'Да' 
            ELSE 'Нет' 
        END
    UNION ALL
    SELECT 'Роли пользователя'::TEXT, 
        array_to_string(ARRAY(
            SELECT rolname FROM pg_roles 
            WHERE pg_has_role(CURRENT_USER, oid, 'member') 
            AND rolname IN ('manager_role', 'employee_role', 'guest_role')
        ), ', ')
    UNION ALL
    SELECT 'RLS включена для clients?'::TEXT,
        CASE 
            WHEN EXISTS(
                SELECT 1 FROM pg_class WHERE relname = 'clients' AND relrowsecurity
            ) THEN 'Да'
            ELSE 'Нет'
        END;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION diagnose_access() IS 
'Диагностическая функция для проверки параметров доступа';


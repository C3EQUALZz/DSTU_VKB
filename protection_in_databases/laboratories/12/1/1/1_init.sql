-- Лабораторная работа № 12: Динамическое управление доступом на основе контекста
-- Вариант 1: Таблица clients с ограничениями по IP и времени

-- ============================================================================
-- 1. СОЗДАНИЕ РОЛЕЙ И ПОЛЬЗОВАТЕЛЕЙ
-- ============================================================================

-- Создаем роли для разных уровней доступа
CREATE ROLE manager_role;
CREATE ROLE employee_role;
CREATE ROLE guest_role;

-- Создаем пользователей и назначаем их к ролям
-- Пароли: manager123, employee123, guest123
CREATE USER manager_user WITH PASSWORD 'manager123';
CREATE USER employee_user WITH PASSWORD 'employee123';
CREATE USER guest_user WITH PASSWORD 'guest123';

-- Назначаем пользователей к ролям
GRANT manager_role TO manager_user;
GRANT employee_role TO employee_user;
GRANT guest_role TO guest_user;

-- Предоставляем базовые права на подключение к базе данных
GRANT CONNECT ON DATABASE postgres TO manager_role, employee_role, guest_role;

-- ============================================================================
-- 2. СОЗДАНИЕ ТАБЛИЦЫ CLIENTS (Вариант 1)
-- ============================================================================

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) DEFAULT CURRENT_USER
);

-- Создаем индекс для ускорения поиска по email
CREATE INDEX idx_clients_email ON clients(email);

-- Комментарии к таблице и полям
COMMENT ON TABLE clients IS 'Таблица клиентов с динамическим управлением доступом';
COMMENT ON COLUMN clients.client_id IS 'Уникальный идентификатор клиента';
COMMENT ON COLUMN clients.name IS 'Имя клиента';
COMMENT ON COLUMN clients.email IS 'Email клиента';
COMMENT ON COLUMN clients.created_at IS 'Время создания записи';
COMMENT ON COLUMN clients.created_by IS 'Пользователь, создавший запись';

-- ============================================================================
-- 3. ПРЕДОСТАВЛЕНИЕ БАЗОВЫХ ПРАВ НА ТАБЛИЦУ
-- ============================================================================

-- Даем права на использование схемы public
GRANT USAGE ON SCHEMA public TO manager_role, employee_role, guest_role;

-- Права для менеджеров (полный доступ)
GRANT ALL PRIVILEGES ON TABLE clients TO manager_role;
GRANT USAGE, SELECT ON SEQUENCE clients_client_id_seq TO manager_role;

-- Права для сотрудников (чтение и добавление)
GRANT SELECT, INSERT, UPDATE ON TABLE clients TO employee_role;
GRANT USAGE, SELECT ON SEQUENCE clients_client_id_seq TO employee_role;

-- Права для гостей (только чтение)
GRANT SELECT ON TABLE clients TO guest_role;

-- ============================================================================
-- 4. ВСТАВКА ТЕСТОВЫХ ДАННЫХ
-- ============================================================================

INSERT INTO clients (name, email) VALUES
    ('Иван Иванов', 'ivanov@example.com'),
    ('Петр Петров', 'petrov@example.com'),
    ('Мария Сидорова', 'sidorova@example.com'),
    ('Анна Смирнова', 'smirnova@example.com'),
    ('Дмитрий Козлов', 'kozlov@example.com');




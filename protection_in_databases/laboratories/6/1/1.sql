-- Создаем пользователей
CREATE USER user1 WITH PASSWORD 'pass1';
CREATE USER user2 WITH PASSWORD 'pass2';

-- Предоставляем права user1
GRANT CREATE ON DATABASE sixth_laboratory_database TO user1; -- Право создавать объекты в БД
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO user1; -- Чтение/запись таблиц

-- Предоставляем права user2
GRANT CONNECT ON DATABASE sixth_laboratory_database TO user2; -- Только подключение к БД
GRANT SELECT ON ALL TABLES IN SCHEMA public TO user2; -- Только чтение таблиц


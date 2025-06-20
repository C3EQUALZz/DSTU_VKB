-- От имени user1 (создаем таблицу и вставляем данные)
-- \c test_db user1
CREATE TABLE employees (id SERIAL PRIMARY KEY, name TEXT);
INSERT INTO employees (name) VALUES ('Alice');

-- От имени user2 (только чтение)
-- \c test_db user2
SELECT * FROM employees; -- Успешно
INSERT INTO employees (name) VALUES ('Bob'); -- Ошибка: нет прав
# 6 лабораторная работа

> [!IMPORTANT]
> Если вы используете `Docker`, то создайте файл `.env` в директории, где находится данный `README.md` файл. 
> Все значения нужно скопировать из `.env.example`.

Перейдите в нужную директорию, где находится файл `docker-compose.yaml` данной лабораторной,
после этого выполните команду в терминале, которая представлена ниже: 

```bash
docker compose --env-file .env up
```

Для демонстрации 1 задания: 

```sql
-- От имени user1 (создаем таблицу и вставляем данные)
-- \c test_db user1
CREATE TABLE employees (id SERIAL PRIMARY KEY, name TEXT);
INSERT INTO employees (name) VALUES ('Alice');

-- От имени user2 (только чтение)
-- \c test_db user2
SELECT * FROM employees; -- Успешно
INSERT INTO employees (name) VALUES ('Bob'); -- Ошибка: нет прав
```

Для демонстрации 2 задания:

```sql
-- От имени user1
\c test_db user1
CREATE TABLE salaries (id INT, salary INT);
INSERT INTO salaries VALUES (1, 1000), (2, 2000);

-- Создаем представление, скрывающее sensitive-данные
CREATE VIEW employee_summary AS 
SELECT e.id, e.name, s.salary 
FROM employees e 
JOIN salaries s ON e.id = s.id;

-- Даем права на представление user2
GRANT SELECT, UPDATE ON employee_summary TO user2;

-- Проверка доступа user2
-- \c test_db user2
SELECT * FROM employee_summary; -- Успешно
UPDATE employee_summary SET salary = 1500 WHERE id = 1; -- Успешно (через представление)
SELECT * FROM salaries; -- Ошибка: нет доступа к таблице
```


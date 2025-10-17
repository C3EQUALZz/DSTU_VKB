## 1.  Создайте пользователей и роли, которые будут использоваться для проверки доступа. Назначьте пользователей к соответствующим ролям.

Для создания ролей используется код: 

```sql
CREATE ROLE manager_role;
CREATE ROLE employee_role;
CREATE ROLE guest_role;
```

Для создания пользователей используется код: 

```sql
CREATE USER manager_user WITH PASSWORD 'manager123';
CREATE USER employee_user WITH PASSWORD 'employee123';
CREATE USER guest_user WITH PASSWORD 'guest123';
```

Теперь назначаем пользователей к ролям, используя код, который описан ниже:

```sql
-- Назначаем пользователей к ролям
GRANT manager_role TO manager_user;
GRANT employee_role TO employee_user;
GRANT guest_role TO guest_user;

-- Предоставляем базовые права на подключение к базе данных
GRANT CONNECT ON DATABASE postgres TO manager_role, employee_role, guest_role;
```

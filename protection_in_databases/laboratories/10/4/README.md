# Вариант 4

Настроить `pgAudit` для логирования операций `UPDATE` в таблице `employees`. Создать триггер, который фиксирует изменения в
`employees` и записывает в `audit_log` как старое, так и новое значения полей `position` и `salary`.

> [!IMPORTANT]
> Для запуска скопируйте значения из `.env` в `.env.example`, после этого выполните команду `docker compose up --build`.

Должно быть видно в логах:

```sql
UPDATE employees SET position = 'Senior Developer', salary = 95000.00 WHERE name = 'Алексей Козлов';
```

Не должно быть видно в логах, но видно в триггере: 

```sql
DELETE FROM employees WHERE name = 'Алексей Козлов';
```
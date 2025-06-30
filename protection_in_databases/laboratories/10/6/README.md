# Вариант 6

Настроить `pgAudit` для логирования операций `SELECT` в таблице `transactions`. 
Создать триггер, который фиксирует все `DELETE` операции в `transactions` и записывает их в
`audit_log`.

> https://kesh.kz/blog/%D0%B0%D1%83%D0%B4%D0%B8%D1%82-postgresql/

Проверка логов на операцию `SELECT`:

```sql
SELECT * FROM transactions;
```

Теперь проверим триггер и заодно то, что в логах не видно информацию о удалении элемента:

```sql
DELETE FROM transactions WHERE amount = 100.00 AND transaction_date = '2023-04-01';
```


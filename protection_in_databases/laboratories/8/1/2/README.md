# Hash index

Для проверки на целостность используем команду, которая представлена ниже: 

```sql
INSERT INTO clients VALUES (email, name)
  ('egestas.nunc@icloud.com','Danil Kovalev'),
```

Для проверки скорости здесь можно использовать только оператор `=`

```sql
EXPLAIN ANALYZE
SELECT * FROM clients
WHERE email = 'gravida.nunc@yahoo.com'
```
# SP-GIST index

Для проверки на целостность используем команду, которая представлена ниже: 

```sql
INSERT INTO clients (email, name) VALUES 
  ('egestas.nunc@icloud.com','Danil Kovalev');
```

```sql
EXPLAIN ANALYZE
SELECT * FROM clients WHERE email LIKE 'gravida.nunc@yahoo.com';
```

![img.png](images/img.png)
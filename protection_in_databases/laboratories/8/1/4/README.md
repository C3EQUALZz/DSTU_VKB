# Gist Index

Для проверки на целостность используем команду, которая представлена ниже: 

```sql
INSERT INTO clients (email, name) VALUES 
  ('egestas.nunc@icloud.com','Danil Kovalev');
```

Для тестирования производительности: 

```sql
EXPLAIN ANALYZE
SELECT * FROM clients 
WHERE email_tsvector @@ to_tsquery('simple', 'gravida.nunc@yahoo.com');
```

![img.png](images/img.png)
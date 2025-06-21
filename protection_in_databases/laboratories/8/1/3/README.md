# Gin Index

Для проверки на целостность используем команду, которая представлена ниже: 

```sql
INSERT INTO clients (email, name) VALUES 
  ('egestas.nunc@icloud.com','Danil Kovalev');
```


```sql
EXPLAIN ANALYZE
SELECT * FROM clients 
WHERE email_tsvector @@ to_tsquery('simple', 'gravida.nunc@yahoo.com');
```

![img.png](images/1.png)
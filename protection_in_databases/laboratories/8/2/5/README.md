# Gist индекс

Для проверки на целостность используем команду, которая представлена ниже: 

```sql
INSERT INTO clients (email, name) VALUES 
  ('egestas.nunc@icloud.com','Danil Kovalev');
```

```sql
INSERT INTO orders (order_date, client_id) VALUES
('2025-05-09',500)
```

Для дат у `PostgreSQL` нет поддержки Sp-GIST. В принципе он и не предназначен для них

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date = '2023-02-20';
```

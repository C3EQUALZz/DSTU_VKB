# B tree индекс

Для проверки целостности:

```sql
INSERT INTO products (product_name, price) VALUES ('Смартфон', 25000.000);
```

```sql
INSERT INTO products (product_name, price) VALUES ('Телефон', -25000.000);
```

```sql
INSERT INTO products (product_name, price) VALUES (NULL, NULL);
```

Для проверки производительности:

```sql
EXPLAIN ANALYZE SELECT * FROM products WHERE product_name = 'Смартфон';
```


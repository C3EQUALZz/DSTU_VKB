# BRIN

Проверка целостности:

```sql
INSERT INTO sales (product_id, quantity)
VALUES (5891231, 192586),
       (133, 532223);
```

```sql
INSERT INTO sales (product_id, quantity)
VALUES (NULL, NULL);
```

Проверка скорости выполнения:

```sql
EXPLAIN ANALYZE SELECT * FROM sales WHERE product_id = 2;
```

![img.png](images/img.png)
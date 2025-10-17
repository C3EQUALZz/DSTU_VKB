## 7. Протестируйте политику, выполняя запросы от имени разных пользователей и ролей.


#### Менеджер

Попробуем подключиться из-под менеджера:  

```bash
docker exec -it lab12_postgres psql -U manager_user -d postgres
```

> manager123

#### Сотрудник (видит только свои)

```bash
docker exec -it lab12_postgres psql -U employee_user -d postgres
```

> employee123

#### Гость (видит все)

```bash
docker exec lab12_postgres psql -U guest_user -d postgres
```

> guest123
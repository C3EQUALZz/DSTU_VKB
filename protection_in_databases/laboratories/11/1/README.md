# Вариант 1

Создайте таблицу `clients` с полями `client_id`, `name`, `email`. 
Реализуйте мандатное управление доступом: пользователи с уровнем допуска `confidential` могут просматривать данные,
но не изменять их. Настройте дискреционное управление для предоставления права на вставку данных роли `manager_role`.

### Выполнение лабораторной работы

Создадим главного пользователя для подключения к базе данных: 

```bash
sudo -u postgres psql -c "CREATE USER eleventh_laboratory_first_variant_user WITH PASSWORD 'eleventh_laboratory_first_variant_password';"
```

Создайте базу данных через терминал, используя команду, которая представлена ниже: 

```bash
sudo -u postgres psql -c "CREATE DATABASE eleventh_laboratory_first_variant_db OWNER eleventh_laboratory_first_variant_user;"
```

После ручного создания теперь можно подключиться из-под `Dbeaver`, используя параметры:

- порт: `5432`
- хост: `localhost`
- имя базы данных: `eleventh_laboratory_first_variant_db`
- пользователь: `eleventh_laboratory_first_variant_user`
- пароль: `eleventh_laboratory_first_variant_password`

После этого у вас откроется окно скрипта, здесь можно использовать ``

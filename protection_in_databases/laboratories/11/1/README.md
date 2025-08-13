# Вариант 1

Создайте таблицу `clients` с полями `client_id`, `name`, `email`. 
Реализуйте мандатное управление доступом: пользователи с уровнем допуска `confidential` могут просматривать данные,
но не изменять их. Настройте дискреционное управление для предоставления права на вставку данных роли `manager_role`.

### Выполнение лабораторной работы

Создадим главного пользователя для подключения к базе данных: 

```bash
sudo -u postgres psql -c "CREATE USER eleventh_laboratory_first_variant_user WITH PASSWORD 'eleventh_laboratory_first_variant_password';"
```

> [!NOTE]
> После выполнения команды должно высветиться `CREATE ROLE`. 

Создайте базу данных через терминал, используя команду, которая представлена ниже: 

```bash
sudo -u postgres psql -c "CREATE DATABASE eleventh_laboratory_first_variant_db OWNER eleventh_laboratory_first_variant_user;"
```

> [!NOTE]
> После этой команды должно высветиться `CREATE DATABASE`.
> Если возникают проблемы, то временно отключите `SELinux`, используя команду: `sudo setenforce 0`.

Если есть проблемы с созданием роли, то перейдите от пользователя `postgres` и выполните команду, которая представлена ниже:

```bash
ALTER USER eleventh_laboratory_first_variant_user CREATEROLE;
```

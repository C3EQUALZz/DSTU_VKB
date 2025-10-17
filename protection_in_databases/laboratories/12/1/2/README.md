## 2. Настройте файл `pg_hba.conf` для ограничения доступа на основе IP-адреса.

Создадим `pg_hba.conf` для ограничения доступа на основе `IP-адреса`.

В моем случае нужно настроить только доступ из сети `192.168.1.0/24`, это было выполнено, как представлено ниже:

```
# Локальные подключения
local   all             postgres                                trust
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# Доступ из сети 192.168.1.0/24 (Вариант 1)
host    postgres        manager_user    192.168.1.0/24          md5
host    postgres        employee_user   192.168.1.0/24          md5
host    postgres        guest_user      192.168.1.0/24          md5
host    postgres        postgres        192.168.1.0/24          md5

# Для подключения с хоста (Docker-сеть)
host    all             all             172.17.0.0/16           md5
```

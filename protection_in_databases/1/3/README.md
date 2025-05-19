# Установить СУБД `MySQL`

> [!IMPORTANT]
> Если вы используете `Docker`, как и я, то вам нет смысла смотреть то, что написано ниже.

Для установки `MySQL` на `Ubuntu` выполните последовательность команд, которые представлены ниже: 

В начале обновим, чтобы у пакетника были последние изменения подвезены: 

```bash
sudo apt update
```

Установим `MySQL`:

```bash
sudo apt install mysql-server
```

Проверим, что все работает: 

```bash
sudo systemctl status mysql
```

Вывод после последней команды должен быть примерно такой: 


```bash
mysql.service - MySQL Community Server
     Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2023-11-29 16:50:28 UTC; 49s ago
    Process: 2238 ExecStartPre=/usr/share/mysql/mysql-systemd-start pre (code=exited, status=0/SUCCESS)
   Main PID: 2246 (mysqld)
     Status: "Server is operational"
      Tasks: 38 (limit: 2220)
     Memory: 365.3M
        CPU: 1.199s
     CGroup: /system.slice/mysql.service
             2246 /usr/sbin/mysqld
     ...
```

Более подробный гайд установки можете найти здесь: 

- https://linuxize.com/post/how-to-install-mysql-on-ubuntu-22-04/
# Вариант 1

Создайте таблицу `client_data` с полями `client_id`, `name`, и `email`. Поле `email` должно быть зашифровано при вставке с
использованием симметричного шифрования. Настройте `PostgreSQL` так, чтобы подключение к базе данных было
возможно только через `SSL`-соединение.

> [!IMPORTANT]
> Перед запуском скопируйте содержимое `.env.example` в `.env` файл. 
> После этого можете запустить, используя `docker compose up --build`.

> [!NOTE]
> В `IDEA` / `Pycharm` нестабильный драйвер для подключения по `SSL`. 
> В `pgadmin4` нет функционала по подключению через `SSL`.
> Из вариантов - использование только командой строки. 

### Настройка `psql` в Windows

Скачайте клиент `PostgreSQL` с официального сайта, после этого проставьте переменные окружения, как сказано на фото. 

Теперь из-под `Windows` `Powershell` можно подключиться, используя команду: 

```bash
psql "host=localhost port=5432 dbname=ninth_laboratory_database_var_1 user=user2 \
      sslmode=verify-full \
      sslrootcert=certs/ca.pem \
      sslcert=certs/client-cert.pem \
      sslkey=certs/client-key.pem"
```

> [!NOTE]
> На данный момент у автора не работает подключение, выдает `EOF`. 

![img.png](images/img.png)

### Выполнение лабораторной работы

Пример для выполнения запроса: 

```sql
SELECT 
    client_id,
    name,
    pgp_sym_decrypt(email::bytea, 'secret_key') AS decrypted_email
FROM client_data;
```

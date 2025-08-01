# 2 лабораторная по предмету: "Защита в базах данных"

> [!IMPORTANT]
> Для работы текущей лабораторной вам нужен `Docker` в системе, `openssl`.

Здесь вам нужно по условию лабораторной работы настроить `SSL` сертификаты для подключения к базе данных.
Для создания сертификатов используйте скрипт из директории `scripts`.

Перед запуском вам нужно настроить переменные окружения. Для этого выполните шаги, которые представлены ниже:

1. Создайте файл `.env`.
2. Скопируйте значения [отсюда](.env.example) и вставьте в файл `.env`.
3. Установите `openssl`, обязательно добавив его в переменные окружения (гайд ниже).
4. Запустите нужный скрипт. Например, `scripts/gen_windows.ps1`. У вас появится папочка с сертификатами.  
5. Перенесите папочку `certs` просто в `resources`. (Опять-таки на `Git` данную папку добавил, чтобы меньше было мучений с `openssl`)
6. Запустите `Docker` на вашем ПК. В случае `Windows` вам нужно запустить приложение `Docker Desktop`. 
7. Выполните команду в терминале `docker compose up --build`
8. Откройте 2 терминал, выполните команду: `uvicorn --factory app.main:create_app --reload --host 0.0.0.0 --port 8005`

> [!IMPORTANT]
> [Представлю гайд как установить правильно [`openssl`](
> https://thesecmaster.com/blog/procedure-to-install-openssl-on-the-windows-platform
> )

> [!NOTE]
> Я очень долго долбался с настройкой `SSL` в случае `MySQL`. Из-за его непопулярности на рынке, его мало тестируют и
> пробуют.
> Позже выяснил опытным путем, что библиотеки `aiomysql`, `asyncmy` просто не хотят работать с `SSL`... Есть внутренние
> баги...
> В итоге, нормально заработала только синхронная библиотека `pymysql`... Я просто так потратил целый день...
> А `SQLAlchemy` как-то криво пробрасывает `SSL` параметры, поэтому я уже забил, честное слово... 

> [!IMPORTANT]
> Если подключаться в приложении к `MySQL` через `Docker`, то почему-то он жалуется...
> В итоге, все нормально работает, если запускать `MySQL` из-под `Docker`, а приложение нативно через команду
`uvicorn --factory app.main:create_app --reload --host 0.0.0.0 --port 8005`

> [!NOTE]
> За основу я взял вот [это](https://github.com/jGundermann/ssl-mysql)... Спасибо, что выложил свое решение.
> Тут если проблемы с cертификатами будут [тык](https://tecadmin.net/mysql-connection-error-certificate-verify-failed/)
> Настройки с [алхимией](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#ssl-connections)

> [!NOTE]
> Если хотите показать неправильный сертификат, то просто в `client-key` можете переделать что-то.
> У вас вылетит ошибка подключения - это правильное поведение. 

Для подключения из-под терминала можно использовать такой вот пример: 

```bash
docker exec -it second-laboratory-database mysql -u root -p"secure_password" --ssl-ca=/etc/mysql/certs/ca.pem --ssl-cert=/etc/mysql/certs/client-cert.pem --ssl-key=/etc/mysql/certs/client-key.pem
```

Если хотите продемонстрировать неправильное, то можно просто поставить не тот сертификат:

```bash
docker exec -it second-laboratory-database mysql -u root -p"secure_password" --ssl-ca=/etc/mysql/certs/ca.pem --ssl-cert=/etc/mysql/certs/server-cert.pem --ssl-key=/etc/mysql/certs/client-key.pem
```
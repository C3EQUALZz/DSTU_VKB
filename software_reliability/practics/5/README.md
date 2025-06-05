# Лабораторная 5

### Как установить данную лабораторную? 

#### `.env`

Создайте `.env` файл рядом с файлом `.env.example`. Ваша задача просто скопировать значения из примера и вставить в `.env`

#### Создание виртуального окружения

Создайте виртуальное окружение с названием `.venv`, используя `Pycharm` или командную строку. 

#### Установка зависимостей

Теперь установите `uv`, используя команду, которая представлена ниже: 

```bash
pip install uv
```

Теперь остается поставить все библиотеки, используя команду ниже: 

```bash
uv sync
```

### Как запустить данную лабораторную? 

#### Cтарт базы данных

Для этого нам нужно поднять базу данных `PostgreSQL` через `Docker`.
В терминале введите команду, которая представлена ниже:

```bash
docker compose up
```

#### Миграции

```bash
python sitewomen/manage.py migrate --no-input
```

#### Загрузка первичных данных

```bash
python sitewomen/manage.py loaddata resources/database/db.json
```

#### Запуск приложения

```bash
python sitewomen/manage.py runserver
```

#### Запуск тестов

```bash
python sitewomen/manage.py test sitewomen
```

#### Создание админки

```bash
python sitewomen/manage.py createsuperuser
```

В моем случае логин: `user`, пароль `user`. 
## Создать  аутентифицированный  локальный  репозиторий,  добавить  этот репозиторий  к  программным  источникам  и  разместить  там  собранный пакет. Показать возможность обновления из локального репозитория.

1. Для начала скачайте необходимые зависимости. Не страшно, если они были у Вас до этого. 

```bash
sudo apt update
sudo apt install dpkg-dev
```

2. Создайте папку, где у Вас будет лежать Ваш репозиторий. Я помещю локальный репозиторий в `var/local`

```bash
sudo mkdir -p /var/local/repository
cd /var/local/repository
```

3. Скопируйте `deb` пакет, который вы создали в прошлом задании в локальный репозиторий. 

```bash
sudo cp /home/c3equalz/Рабочий стол/Projects/DSTU_VKB/operation_systems/1/9_laboratory/5_question/calculator.deb /var/local/repository
```

[IMPORTANT!]
> Добавьте ещё подписанный туда файл, который является `deb.gpg`, используя вышеописанную команду 

4. Теперь нужно запустить команду для генерации информации о репозитории.

```bash
cd /var/local/repository
dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
```

5. Теперь надо сконфигурировать `apt`. Для этого выполните действия ниже

- Создайте файл с помощью команды ниже

```bash
sudo nano /etc/apt/sources.list.d/local.list
```

- Добавьте строчку в этот файл

```bash
deb [trusted=yes] file:/var/local/repository/ /
```

6. Теперь надо обновить индекс для `apt`

```bash
sudo apt update
```


## Добавьте в файл еще одну строку так, чтобы получились следующие правила: `auth requisite pam_wheel.so`, `auth required pam_unix.so`. Модуль `pam_wheel.so` возвращает успех если учетная запись пользователя принадлежит группе `wheel` (в некоторых версиях группе `root`). Выполнить команду `su`, что произошло? Скриншот. Команду `su` смогут выполнить только пользователи, который входят в группу `wheel` и знают пароль учетной записи `root`. Создайте группу `wheel` и добавьте туда свою учетную запись, выполните команду `su`. Скриншот. После выполнения задания удалите из группы учетную запись и удалите группу `wheel`.

> [!IMPORTANT]
> Для выполнения данного задания я использовал терминал, который называется `Konsole`. 

Добавление строк в файл `/etc/pam.d/su`:

```bash
nano /etc/pam.d/su
```

Теперь добавим строки в файл:

```bash
auth requisite pam_wheel.so
auth required pam_unix.so
```

Теперь создадим пользователя, который принадлжит группе `wheel`, для этого используйте команды, которые представлены ниже: 

Создаем пользователя:

```bash
sudo useradd wheeluser
```

Ставим пароль:

```bash
sudo passwd wheeluser
```

> [!NOTE]
> Я для удобства поставил пароль `123`

Теперь создаем группу `wheel`:

```bash
sudo groupadd wheel
```

Теперь добавляем пользователя в группу, используя команду ниже:

```bash
sudo usermod -aG wheel wheeluser
```

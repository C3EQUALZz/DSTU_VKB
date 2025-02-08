## Используйте команду `find`, чтобы определить местонахождение всех файлов, принадлежащих пользователю `root` в домашней директории пользователя `student`, а затем создайте архив с помощью команды `tar`. Архив должен находиться в каталоге `/tmp`

Вариант 1:

Воспользуйтесь командой: 

```bash
find /home/student -user root -type f -print0 | xargs -0 tar -czf /tmp/root_files.tar.gz
```

Вариант 2:

```bash
cd /home/student
find . -user root -type f -print0 | tar --null -cvf /tmp/root_files.tar --files-from=-
```

> [!IMPORTANT]
> `tar` не создает пустой архив, до этого создайте какие-нибудь файлы из-под `root`.
> Например, можно создать файл какой-нибудь `txt`, который можно заполнить с помощью [кодо-генерации](https://ru.lipsum.com/feed/html)

В моем случае нет пользователя `student`, поэтому напишу для своего:

```bash
cd /home/c3equalz
find . -user root -type f -print0 | tar --null -cvf /tmp/root_files.tar --files-from=-
```

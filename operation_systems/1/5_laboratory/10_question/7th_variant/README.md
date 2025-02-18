## Создать жесткую и символическую ссылки для одного из созданных в п.2 файлов

---

### Жесткая ссылка (Hard Link)

Жесткая ссылка — это дополнительное имя для существующего файла.
Она указывает на тот же самый файл на диске, и изменения в файле будут видны через все жесткие ссылки на него.
Жесткие ссылки не могут быть созданы для каталогов и не могут пересекать границы файловых систем.

Создание жесткой ссылки 

```bash
ln original_file hard_link
```

Пример: 

```bash
ln file1.txt file2.txt
```

Теперь `file2.txt` — это жесткая ссылка на `file1.txt`.

--- 

### Символические ссылки (Symbolic Links)

Символическая ссылка — это файл, который указывает на другой файл или каталог.
Она содержит путь к целевому файлу или каталогу.
Символические ссылки могут пересекать границы файловых систем и могут указывать на каталоги.

Создание символической ссылки

```bash
ln -s original_file symbolic_link
```

Пример:

```bash
ln -s file1.txt file2.txt
```

Теперь `file2.txt` — это символическая ссылка на `file1.txt`.

---

Для проверки символической ссылки можно использовать команду `ls -l`
Для проверки твердой ссылки можно использовать команду `ls -li` или `stat`

---

## Вывести список имен файлов из `/usr`, используя ключ `-l`. Список упорядочить по размерам файлов. 

От большего к меньшему 

```bash
ls -lS /usr
```

От меньшего к большему

```bash
ls -lSr /usr
```

---

## Найти файлы, размеры которых превышают 25к (запись +25к) и имена начинаются на s, а заканчиваются на jpg

Пример команды

```bash
find /path/to/search -type f -size +25k -name 's*.jpg'
```

- `/path/to/search`: путь к каталогу, в котором вы хотите выполнить поиск. Вы можете заменить его на конкретный путь, например, /usr.
- `type f`: ищет только файлы.
- `size +25k`: ищет файлы, размер которых превышает 25 килобайт.
- `name 's*.jpg`: ищет файлы, имена которых начинаются на "s" и заканчиваются на ".jpg".

В моем случае для поиска во всей системе сделаю следующую команду

```bash
sudo find / -type f -size +25k -name 's*.jpg'
```

Я рядом положил jpg для поиска 

```bash
find ./ -type f -size +25k -name "s*.jpg"
```
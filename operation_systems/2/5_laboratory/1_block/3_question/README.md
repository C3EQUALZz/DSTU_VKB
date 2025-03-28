## Создайте две жестких ссылки `hardlink` и `hardlink1` на скопированный файл `passwd`. Проверьте что ссылки работают.

Для решения, поставленной задачи, используйте команды, которые представлены ниже: 

```bash
ln /home/student/passwd /home/student/hardlink
ln /home/student/passwd /home/student/hardlink1
```

> [!NOTE]
> Вместо `student` может быть имя любого пользователя. 

Можно проверить существование жесткой ссылки, используя команды ниже: 

```bash
cat /home/student/hardlink
cat /home/student/hardlink1
```

<details>
  <summary>Если забыли что такое жесткие ссылки. </summary>

  Жесткая ссылка — это другой тип ссылки на файл в файловой системе, который указывает на тот же inode, что и оригинальный файл.
  Это означает, что жесткая ссылка и оригинальный файл фактически являются разными именами для одного и того же файла на диске. 
  Вот несколько ключевых моментов о жестких ссылках:
    
  - Общий `inode`: Жесткая ссылка ссылается на тот же `inode`, что и оригинальный файл.
Это означает, что изменения, внесенные в файл через одну ссылку, будут видны через другую ссылку, 
поскольку они указывают на одно и то же физическое представление данных.

  - Отличие от жесткой ссылки: В отличие от жесткой ссылки, которая ссылается на тот же `inode` (физическое представление файла на диске), 
символическая ссылка может указывать на файл или директорию, находящиеся в другом месте файловой системы. 
Если оригинальный файл удален, символическая ссылка становится "висячей" (`broken link`) и не будет работать.

  - Удобство: Символические ссылки полезны для создания удобных путей к файлам, упрощения доступа к часто используемым 
ресурсам или организации структуры каталогов.

</details>

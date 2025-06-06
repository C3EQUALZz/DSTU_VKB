## С правами пользователя `user2` с помощью команды `ср` создайте в каталогах `/home/temp1` и `/home/temp2` по одной копии файла `dec` с другим именем (`dec_copyl`). Чем отличаются исходный файл и его копия (обратите внимание на то, кто является владельцем исходного файла и его копии)? Чем отличаются права доступа на эти файлы?

> [!IMPORTANT]
> Откройте терминал через комбинацию (`CTRL + ALT + F<number>`), где `number` - это число от 1 до 6. Если вы авторизированы за другого пользователя, то вбейте в терминале команду `exit`.
> После этого введите данные от `user2`, которые вы задали.
 
Теперь делаем копии файлов `dec`:

```bash
cp /home/user1/qu4/dec /home/temp1/dec_copy1
cp /home/user1/qu4/dec /home/temp2/dec_copy2
```

Теперь проверяем оригинальный файл: 

```bash
ls -l /home/student9/qu4/dec
```

А теперь проверяем копию файла:

```bash
ls -l /home/temp1/dec_copy1
```

Если вы сделали всё правильно, то владельцы файлов будут различаться. Можно сделать вывод, что если доступ позволяет создавать копию файла, то копия, которая была создана новым другим пользователем, будет принадлежать ему. В данном случае владелец оригинала `user1`, а копии `user2`. 

> [!NOTE]
> Вместо `user1` у вас может быть абсолютно другой, которого вы задали. 

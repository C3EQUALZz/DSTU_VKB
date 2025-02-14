## C помощью команды `chmod` измените нужные права доступа в "недоступные" каталоги `qu2`, `qu4` и создайте там указанные файлы. После этого верните каталогам прежние права доступа. 

Меняем права к директории `qu2`, используя команду ниже: 

```bash
sudo chmod 777 /home/user1/qu2
```

Меняем права к диретории `qu4`, используя команду ниже: 

```bash
sudo chmod 777 /home/student9/qu4
```

Создаем файлы в нужных директориях теперь: 

```bash
date > /home/user1/qu2/apr
date > /home/user1/qu2/may
date > /home/user1/qu2/jun

date > /home/user1/qu4/oct
date > /home/user1/qu4/nov
date > /home/user1/qu4/dec
```

Меняем права на прежние: 

```bash
sudo chmod 404 /home/user1/qu2
sudo chmod 505 /home/user1/qu4
```

> [!NOTE]
> Вместо `user1` у вас может быть любой пользователь, за которого вы создали директории и файлы. 

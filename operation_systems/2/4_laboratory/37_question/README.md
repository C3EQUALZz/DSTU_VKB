## С помощью команды `md5sum` вычислите и запишите контрольную сумму для одного из файлов в каталоге `/home/user1/qul`. Добавьте один символ в этот файл с помощью команды echo (например, `echo a >> /home/userl/qul/jan`). Вновь вычислите контрольную сумму файла и сравните два результата.

> [!IMPORTANT]
> Откройте терминал через приложение `Konsole`. 

Выполняем действия, сказанные в методичке: 

```bash
md5sum /home/user1/qu1/jan > jan.md5
```

Проверяем, ЧТО файл не пустой, используя команду ниже:

```bash
cat jan.md5
```

Добавляем символ, используя команду ниже:

```bash
echo a >> /home/user1/qu1/jan
```

Теперь проверяем контрольную сумму. 

Сначала выполните команду ниже: 

```bash
md5sum /home/user1/qu1/jan > jan_modified.md5
```

Теперь просмотрим файл. Используйте команду ниже: 

```bash
cat jan_modified.md5
```

> [!NOTE]
> Если вы сделали все правильно, то контрольные суммы должны отличаться. 

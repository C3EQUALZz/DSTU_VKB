## Найдите все файлы в системе размером более 200Mб

Команда, которая Вам нужна:

```bash
find / -type f -size +200M
```

> [!NOTE]
> `-size +200M` - фильтр на то, что файлы больше 200Мб. 

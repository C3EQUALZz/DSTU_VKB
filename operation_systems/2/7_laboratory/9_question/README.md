## Проверьте, используется ли в вашей системе аутентификация через `PAM`. Для этого посмотрите содержимое файла `/etc/nsswitch.conf`. Первые три строки этого файла как раз и задают какая система аутентификации будет работать в системе. Ключевое слово `compat` показывает, что в качестве системы аутентификации будет использована система `PAM`. Скриншот.

> [!IMPORTANT]
> Для выполнения данного задания я использовал консоль, которая открывается через терминал `Konsole`. 

Проверка использования аутентификации через `PAM` в файле `/etc/nsswitch.conf`:

```bash
grep "^passwd:" /etc/nsswitch.conf 
```

> [!NOTE]
> Лично у меня слова `compat` не было, но это настройки системы по умолчанию. Так-то я ничего не менял.
> Результат можете увидеть на фото, это все актуально на `Astra Linux 1.8`. 

![изображение](https://github.com/user-attachments/assets/3822892b-4d4a-48fc-b289-8251cca10a3c)

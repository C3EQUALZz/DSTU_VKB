## Проверьте, используется ли в вашей системе аутентификация через `PAM`. Для этого посмотрите содержимое файла `/etc/nsswitch.conf`. Первые три строки этого файла как раз и задают какая система аутентификации будет работать в системе. Ключевое слово `compat` показывает, что в качестве системы аутентификации будет использована система `PAM`. Скриншот.

Проверка использования аутентификации через PAM в файле /etc/nsswitch.conf:

grep "^passwd:" /etc/nsswitch.conf 

--да, используется
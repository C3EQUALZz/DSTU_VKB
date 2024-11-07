## Подписать пакет ключом. 

1. Установите все зависимости, которые приложил ниже 

```bash
sudo apt update
sudo apt install dpkg-dev && gpg
```

2. Посмотрите и скопируйте имена ключей или идентификаторы. 

Вот у вас будет примерный вывод:

```bash
pub   rsa2048 2021-01-01 [SC] [expires: 2023-01-01]
      ABCD1234EFGH5678IJKL9012MNOP3456QRST7890
uid           [ultimate] Ваше Имя <ваш.email@example.com>
sub   rsa2048 2021-01-01 [E] [expires: 2023-01-01]
```

3. Подпишите deb пакет, используя ID ключа

Пример: 

```bash
gpg --local-user ваш_ключ --sign имя_файла.deb
```

В моем случае: 

```bash
gpg --local-user 4F8FD2C5A2761D02904A73EC2EE1CD65A4B5D0AE --sign calculator.deb
```

У вас появится рядом файл с расширением `deb.gpg`

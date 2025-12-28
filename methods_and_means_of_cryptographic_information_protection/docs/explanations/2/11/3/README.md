# Задание 3. 

## Условие

С помощью `OpenSSL` сгенерируйте ключ шифрования для алгоритма `DES`.
Для этого введите команду: `genrsa [-out file] [-des] [-rand file] [bits]`

## Практическая реализация

Для выполнения задания воспользуемся командой: 

```bash
openssl genpkey -algorithm RSA -out D:\Progrramming\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\11\3\privateRSA.pem -cipher DES -provider default -provider legacy -pkeyopt rsa_keygen_bits:2048
```

> [!NOTE]
> Можно вместо `DES` использовать `AES`, как у некоторых было в отчетах. 
> Но я на всякий случай оставлю `DES`, потому что Сафарьян

> [!IMPORTANT]
> Пути к файлам могут абсолютно иные, поменяйте на свой. 
# Задание 7. 

## Условие

Убедитесь, что при передаче правильного ключа текст расшифровывается корректно (расшифрованный текст совпадает с исходным).

## Практическая реализация

Для выполнения задания воспользуемся командой, которая представлена ниже:

```bash
openssl enc -d -des-cbc -provider-path "D:\tools\openssl\OpenSSL-Win64\bin" -provider default -provider legacy -in "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\11\4\warandpeace.enc" -out "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\11\7\warandpeace.txt" -pass pass:D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\11\4\publicRSA.pem -nosalt -md sha1
```

> [!IMPORTANT]
> У вас совершенно иные пути могут быть

![img.png](1.png)


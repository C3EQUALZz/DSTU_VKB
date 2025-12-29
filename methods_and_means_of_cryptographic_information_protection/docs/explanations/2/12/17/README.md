# Задание 17. 

## Условие

Проверка электронной подписи файла. 
Для начала нам надо преобразовать сертификат, с помощью которого мы будем проверять подпись в открытый ключ.

## Практическая реализация

Получим открытый ключ:

```bash
openssl x509 -pubkey -noout -in D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\15\cert.pem > D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\17\pubkey.pem
```

![img.png](1.png)

> [!IMPORTANT]
> У вас могут быть совершенно иные пути для данного задания
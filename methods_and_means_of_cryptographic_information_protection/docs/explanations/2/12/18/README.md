# Задание 18. 

## Условие

Затем, с помощью этого ключа, произведём проверку подписи. 

## Практическая реализация

> [!IMPORTANT]
> Подпись была создана через `openssl dgst -sha1 -sign`, поэтому для проверки необходимо использовать `openssl dgst -verify`, а не `openssl pkeyutl -verify`. Команды `dgst` и `pkeyutl` используют разные форматы подписей и несовместимы друг с другом.

```bash
openssl dgst -sha1 -verify D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\17\public_key.pem -signature D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\16\sign.cr D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\6\dok.txt
```

![img.png](1.png)

### Почему не работает `pkeyutl -verify`?

Команда `openssl pkeyutl -verify` работает с "сырыми" подписями (raw signatures), которые создаются через `pkeyutl -sign`. Она не может проверить подписи, созданные через `dgst -sign`, так как:

1. **`dgst -sign`** создает подпись в формате PKCS#1 с включенной информацией о хеше
2. **`pkeyutl -sign`** создает "сырую" подпись без информации о хеше
3. Эти форматы несовместимы между собой

> [!IMPORTANT]
> У вас могут быть совершенно иные пути для выполнения данного задания
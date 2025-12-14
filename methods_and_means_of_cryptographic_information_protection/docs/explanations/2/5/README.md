# Лабораторная 5 (RSA)

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

Все действия нужно выполнять вот в данной директории, то есть используем данную команду:

```bash
cd src/cryptography_methods
```

Для генерации ключей можно использовать код, который представлен ниже:

```bash
python cli.py rsa generate-keys -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\public_key.txt" -pr "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\private_key.txt"
```

Для шифрования сообщения теперь можно использовать команду, которая представлена ниже:

```bash
python cli.py rsa encrypt -m "КОВАЛЕВ ДАНИЛ ВКБ43" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\public_key.txt" -o "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\encrypted_data.txt"
```

Для дешифрования сообщения теперь можно использовать команду, которая представлена ниже:

```bash
python cli.py rsa decrypt -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\private_key.txt" -i "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\encrypted_data.txt"
```
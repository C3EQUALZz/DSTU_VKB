# Лабораторная 6 (Реализация элементов схемы шифрования Эль-Гамаля)

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

Все действия нужно выполнять вот в данной директории, то есть используем данную команду:

```bash
cd src/cryptography_methods
```

Для генерации ключей можно использовать код, который представлен ниже:

```bash
python cli.py elgamal generate-keys -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\public_elgamal.txt" -pr "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\private_elgamal.txt" -s 1024 -c 10
```

Чтобы зашифровать используем данную команду:

```bash
python cli.py elgamal encrypt -m "Сообщение" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\public_elgamal.txt" -o "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\elgamal_cipher.txt"
```

Чтобы дешифровать используем данную команду:

```bash
python cli.py elgamal decrypt -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\private_elgamal.txt" -i "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\elgamal_cipher.txt"
```




# 7 лабораторная работа (RSA ЭЦП)

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

Все действия нужно выполнять вот в данной директории, то есть используем данную команду:

```bash
cd src/cryptography_methods
```

Генерация ключей:

```bash
python cli.py rsa-sign generate-keys -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\rsa_pub.txt" -pr "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\rsa_priv.txt" -s 2048 -d 64
```

Подписать документ (war and piece original):

```bash
python cli.py rsa-sign sign -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\rsa_sign\warandpeace.txt" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\rsa_priv.txt" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\document.sig" -h "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\hash_document.sha256.txt"
```

Подписать документ (war and piece modified - 2):

```bash
python cli.py rsa-sign sign -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\rsa_sign\warandpeace2.txt" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\rsa_priv.txt" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\document2.sig" -h "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\hash_document2.sha256.txt"
```

Проверить подпись (war and piece original):

```bash
python cli.py rsa-sign verify -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\rsa_sign\warandpeace.txt" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\document.sig" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\rsa_pub.txt"
```

Проверить подпись (war and piece modified - 2):

```bash
python cli.py rsa-sign verify -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\rsa_sign\warandpeace2.txt" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\document2.sig" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\rsa_pub.txt"
```

Сравнить хеши:

```bash
python cli.py rsa-sign compare-hashes -h1 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\hash_document.sha256.txt" -h2 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\hash_document2.sha256.txt"
```

Сравнить подписи:

```bash
python cli.py rsa-sign compare-signatures -s1 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\document.sig" -s2 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\document2.sig"
```
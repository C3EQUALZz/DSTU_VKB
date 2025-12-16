# 8 лабораторная работа (ЭЦП ГОСТ Р 34.10–94)

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

Все действия нужно выполнять вот в данной директории, то есть используем данную команду:

```bash
cd src/cryptography_methods
```

### Взаимодействие с `docx`

Генерация параметров и ключей:

```bash
python cli.py gost-3410-94 generate-keys -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_params.txt" -pr "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_private.txt" -pub "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_public.txt" -s 512
```

Подписание документа (`Оригинал`):

```bash
python cli.py gost-3410-94 sign -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9.docx" -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_params.txt" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_private.txt" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9.txt" -h "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_hash.txt"
```

Подписание документа (`Модификация`):

```bash
python cli.py gost-3410-94 sign -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_1.docx" -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_params.txt" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_private.txt" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_1.txt" -h "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_1_hash.txt"
```

Проверка подписи (`Оригинал`):

```bash
python cli.py gost-3410-94 verify -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9.docx" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9.txt" -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_params.txt" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_public.txt"
```

Проверка подписи (`Модификация`):

```bash
python cli.py gost-3410-94 verify -d "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_1.docx" -s "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_1.txt" -p "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_params.txt" -k "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\gost_public.txt"
```

Сравнение хешей: 

```bash
python cli.py gost-3410-94 compare-hashes -h1 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_hash.txt" -h2 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\resources\gost_sign\Лабораторная_9_1_hash.txt"
```
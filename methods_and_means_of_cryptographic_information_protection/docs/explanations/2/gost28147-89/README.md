# 2 лабораторная работа (ГОСТ 28147-89)

> [!NOTE]
> Ниже описаны гайды для запуска алгоритмов через `cli`. Я лично использую `Powershell` в `Pycharm`. 

Для запуска генерации ключей используем код, который представлен ниже: 

```bash
python -m cryptography_methods.cli gost-28147 generate-key
```

Копируем ключ, который представлен в 16СС, его нам будет удобно использовать для шифрования и дешифрования. 
Например, вот такой ключ можно использовать: `f86be0ccba8032cfd26d9ce3b020c8caec97c662ef9de95a99b54d10ceb2e64c`

Для запуска шифрования используем команду, которая представлена ниже:

```bash
python -m cryptography_methods.cli gost-28147 encrypt -t "КОВАЛЕВ" -k "f86be0ccba8032cfd26d9ce3b020c8caec97c662ef9de95a99b54d10ceb2e64c"
```

```bash
python -m cryptography_methods.cli gost-28147 encrypt -t "КОВАЛЕВ" -k "88df0e05230c35da86307fc1ad73e3a4669dbd4adb6a1cd5ff9a751bdaac5d7e"
```

Для запуска расшифрования используем команду, которая представлена ниже:

```bash
python -m cryptography_methods.cli gost-28147 decrypt -t "01d5e0cd408e5fe8b0cb6c0b81641d1a" -k "f86be0ccba8032cfd26d9ce3b020c8caec97c662ef9de95a99b54d10ceb2e64c"
```

```bash
python -m cryptography_methods.cli gost-28147 decrypt -t "e63e9a198310bf2ae7b0a2d03d9a7d65" -k "88df0e05230c35da86307fc1ad73e3a4669dbd4adb6a1cd5ff9a751bdaac5d7e"
```
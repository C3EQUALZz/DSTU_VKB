# Задание 4. 

## Условие

Выполните действие 3 для алгоритма `SHA1`.

## Практическая реализация

Для реализации данного задания воспользуемся командой, которая представлена ниже:

```bash
openssl dgst -sha1 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\2\dok.txt"
```

![img.png](1.png)

Для измерения времени хэширования можно использовать команду, которая представлена ниже: 

```powershell
Measure-Command { openssl dgst -sha1 "D:\PycharmProjects\DSTU_VKB\methods_and_means_of_cryptographic_information_protection\docs\explanations\2\12\2\dok.txt" }
```

![img.png](2.png)

> [!IMPORTANT]
> У вас будут совершенно иные пути до файлов. 

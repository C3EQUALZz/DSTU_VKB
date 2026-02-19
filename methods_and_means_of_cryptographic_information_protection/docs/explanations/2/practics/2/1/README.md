## Задание 1. 

Проверить на простоту два произвольных целых числа разрядностью не менее 5.

### Выполнение

Для запуска через программу `Python` можно воспользоваться командой, которая представлена ниже: 

Пример простого числа: 

```bash
python -m cryptography_methods.cli primality-check check -n 104729
```

Пример составного числа: 

```bash
python -m cryptography_methods.cli primality-check check -n 104730
```

Пример простого числа: 

```bash
python -m cryptography_methods.cli primality-check check -n 137713
```

> [!NOTE]
> Для проверки простоты числа использовался алгоритм Миллера-Рябина
# Генерация псевдослучайных последовательностей над эллиптическими кривыми

> [!IMPORTANT]
> Перейдите в директорию с файлом `cli.py` в терминале. `cd src/mathematical_algorithms_of_geometry_in_cryptography`

Пример для нахождения порядка всех точек для варианта 1:

```bash
python cli.py elliptic-curve-gfp all-orders -a 1 -b 2 -p 17
```

Пример для генерации последовательности для варианта 1:

```bash
python cli.py elliptic-curve-gfp generate-sequence -a 1 -b 2 -p 17 -c 5 --px 5 --py 8 --x0-x 13 --x0-y 6 -n 15
```
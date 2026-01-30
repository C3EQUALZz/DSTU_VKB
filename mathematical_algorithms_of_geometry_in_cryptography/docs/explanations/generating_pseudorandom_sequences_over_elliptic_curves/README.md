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

Пример для генерации ЛКГ последовательности для варианта 11: 

```bash
python cli.py elliptic-curve-gfp generate-sequence -a 2 -b 2 -p 17 -c 5 --px 6 --py 3 --x0-x 9 --x0-y 1 -n 10
```

Пример для генерации ИГ последовательности для варианта 11: 

```bash
python cli.py elliptic-curve-gfp generate-sequence -a 2 -b 2 -p 17 -c 5 --px 13 --py 7 --x0-x 5 --x0-y 1 -n 10
```
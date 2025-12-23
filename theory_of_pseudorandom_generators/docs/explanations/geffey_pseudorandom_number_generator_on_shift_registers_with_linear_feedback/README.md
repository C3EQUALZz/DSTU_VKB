# Генератор Геффе псевдослучайных чисел на регистрах сдвига с линейной обратной связью

> [!IMPORTANT]
> Перейдите в директорию с файлом `cli.py` в терминале. 
> `cd src/theory_of_pseudorandom_generators`

Для запуска лабораторной работы используем команду, которая представлена ниже: 

```bash
python cli.py geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p1 "1 1 0 1 1 1" -k1 4 -c1 1 -s1 "1 0 1 0 1" -p2 "1 1 1" -k2 5 -c2 0 -s2 "1 0" -p3 "1 0 1 1 0 1 1" -k3 4 -c3 2 -s3 "1 0 1 0 1 0"
```

Для варианта 1:

```bash
python cli.py geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p1 "1 0 1 0 0 1" -k1 2 -c1 0 -s1 "1 0 0 0 0" -p2 "1 0 0 1 1" -k2 4 -c2 0 -s2 "1 0 0 0" -p3 "1 1 0 0 0 0 1" -k3 1 -c3 0 -s3 "1 0 0 0 0 0"
```

Для варианта 2:

```bash
python cli.py geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p1 "1 0 1 1 1 1" -k1 4 -c1 0 -s1 "1 0 0 0 0" -p2 "1 1 1" -k2 2 -c2 0 -s2 "1 0" -p3 "1 1 0 0 1 1 1" -k3 5 -c3 2 -s3 "1 1 0 0 0 0"
```

Для варианта 11:

```bash
python cli.py geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p1 "1 0 1 1 1 1" -k1 3 -c1 0 -s1 "1 0 0 0 0" -p2 "1 1 1" -k2 2 -c2 0 -s2 "1 0" -p3 "1 1 0 0 1 1 1" -k3 2 -c3 0 -s3 "1 0 0 0 0 0"
```
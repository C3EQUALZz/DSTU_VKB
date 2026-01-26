# Генератор Фибоначчи псевдослучайных чисел на регистрах сдвига с линейной обратной связью

> [!IMPORTANT]
> Перейдите в директорию с файлом `cli.py` в терминале. 
> `cd src/theory_of_pseudorandom_generators`

Для запуска лабораторной работы используем команду, которая представлена ниже: 

```bash
python cli.py fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p "1 1 1 0 1 1" -k 2 -s "1 0 0 0 0"
```

Для варианта 1:

```bash
python cli.py fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p "1 0 0 1 0 1" -k 2 -s "1 0 0 0 0" -c 4
```

Для варианта 11:

```bash
python cli.py fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate -p "1 1 1 0 1 1" -k 3 -s "0 1 0 0 0"
```
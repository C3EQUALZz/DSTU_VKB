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

## Рекомендуемые параметры для NIST‑тестов

Для проверки последовательностей генератора Фибоначчи с помощью NIST‑подобных тестов (частотно‑побитовый, блочный, тест на серии) важно получить достаточную длину битовой последовательности.

Практически удобно использовать параметры варианта 11 и затем ограничивать длину в NIST‑команде через `--max-bits`:

1. Сначала сгенерировать последовательность:

```bash
python cli.py fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback generate \
  -p "1 1 1 0 1 1" -k 3 -s "0 1 0 0 0"
```

2. Затем запустить проверку несцепленных серий (пример):

```bash
python cli.py methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series run ^
  --fibonacci-file "D:\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\Fibonacci.txt" ^
  -m 24 --max-bits 2000
```

- **Назначение:** параметры выше дают M‑последовательность длиной `2⁵−1 = 31`, которая в файле `Fibonacci.txt` представлена в виде десятичных чисел; ограничение `--max-bits` позволяет получить сопоставимую по длине битовую выборку с другими генераторами для NIST‑тестов.***
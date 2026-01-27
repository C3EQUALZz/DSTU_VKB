# Полиномиальный конгруэнтный генератор псевдослучайных чисел

> [!IMPORTANT]
> Перейдите в директорию с файлом `cli.py` в терминале. 
> `cd src/theory_of_pseudorandom_generators`

Для запуска лабораторной работы используем команду, которая представлена ниже: 

```bash
python cli.py polynomial_congruent_pseudorandom_number_generator generate -a1 25 -a2 106 -b 1075 -x0 1 -m 6075
```

Для варианта 1:

```bash
python cli.py polynomial_congruent_pseudorandom_number_generator generate -a1 106 -a2 200 -b 1283 -x0 10 -m 6075 -s 10
```

Для варианта 11: 

```bash
python cli.py polynomial_congruent_pseudorandom_number_generator generate -a1 5 -a2 8 -b 3 -x0 7 -m 16 -s 10
```

> [!NOTE]
> Для графиков в следующих лабах можно по 200 элементов ставить

## Рекомендуемые параметры для NIST‑тестов

Для методики оценки качества ГПСП (частотно‑побитовые и блочные NIST‑тесты) имеет смысл использовать более «длинные» и хорошо распределённые последовательности.

Пример набора параметров, дающего предсказуемо длинный период и удобный для NIST‑тестов:

```bash
python cli.py polynomial_congruent_pseudorandom_number_generator generate \
  -a1 25 -a2 106 -b 1075 -x0 1 -m 6075 -s 5000
```

- **Назначение:** подготовка данных для команды  
  `methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series`  
  через файл `polynomial_congruent.txt`.
- **Комментарий:** модуль `m = 6075` и длина последовательности `s = 5000` дают несколько тысяч десятичных значений, которые после перевода в двоичный вид образуют достаточно длинную битовую последовательность для NIST‑подобных тестов.*** End Patch`}`} %}
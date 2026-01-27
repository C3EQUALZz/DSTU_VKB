# Методика оценки качества ГПСП. Графический тест: распределение на плоскости

> [!IMPORTANT]
> Перейдите в директорию с файлом `cli.py` в терминале. 
> `cd src/theory_of_pseudorandom_generators`

> [!IMPORTANT]
> При запуске поменяйте на ваши абсолютные пути для файлов, которые используются для анализа. 

Запустите другие работы, мануал которых описан в директориях (с данных работ нужен будет материал): 

- polynomial_congruent_pseudorandom_number_generator
- linear_congruent_pseudorandom_number_generator
- geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback
- fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback

Для запуска лабораторной работы используем команду, которая представлена ниже: 

```bash
python cli.py methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane generate --linear-congruent-file "D:\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\linear_congruent.txt" --square-congruent-file "D:\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\polynomial_congruent.txt" --fibonacci-file "D:\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\Fibonacci.txt" --geffe-file "D:\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\Geffe.txt"
```

```bash
python cli.py methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane generate --linear-congruent-file "D:\Progrramming\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\linear_congruent.txt" --square-congruent-file "D:\Progrramming\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\polynomial_congruent.txt" --fibonacci-file "D:\Progrramming\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\Fibonacci.txt" --geffe-file "D:\Progrramming\PycharmProjects\DSTU_VKB\theory_of_pseudorandom_generators\Geffey.txt"
```

> [!NOTE]
> После запуска у вас появится файл `planes.png`
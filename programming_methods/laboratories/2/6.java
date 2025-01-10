/*
Задача №1664. Суперсумма

Дано N натуральных чисел.
Требуется для каждого числа найти количество вариантов разбиения его на сумму двух других чисел из данного набора.

Входные данные

В первой строке дано число N (1 ≤ N ≤ 10000). Далее заданы N натуральных чисел, не превосходящих 10^9.
Для каждого числа количество разбиений меньше 2^31.

Выходные данные

Вывести N чисел – количество разбиений, в порядке, соответствующем исходному.
*/

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

public class SuperSum {

    /**
     * Подсчитывает количество разбиений, которое нужно узнать у числа.
     * Для начала мы формируем словарь, где ключ — это число из массива, а значение — количество его вхождений.
     * Создаем массив results, который будет хранить количество разбиений для каждого числа.
     *
     * В цикле проходимся, для каждого числа из массива numbers мы инициализируем переменную count,
     * которая будет хранить количество разбиений.
     */
    public static int[] countPartitions(int[] numbers) {
        Map<Integer, Long> countMap = Arrays.stream(numbers)
                .boxed()
                .collect(Collectors.groupingBy(n -> n, Collectors.counting()));

        int[] results = new int[numbers.length];

        for (var i = 0; i < numbers.length; i++) {
            int number = numbers[i];
            int count = 0;

            for (Map.Entry<Integer, Long> entry : countMap.entrySet()) {
                var x = entry.getKey();
                var y = number - x;

                // Избегаем дублирования
                if (y < x) {
                    continue;
                }

                var xCount = entry.getValue();

                if (x == y) {
                    // Если x и y одинаковые, то выбираем 2 из countMap[x]
                    count += xCount * (xCount - 1) / 2;
                } else if (countMap.containsKey(y)) {
                    // Если x и y разные, то просто перемножаем их количества
                    count += xCount * countMap.get(y);
                }
            }

            results[i] = count;
        }

        return results;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] numbers = new int[n];

        for (int i = 0; i < n; i++) {
            numbers[i] = scanner.nextInt();
        }

        int[] partitions = countPartitions(numbers);

        for (int result : partitions) {
            System.out.println(result);
        }

        scanner.close();
    }
}


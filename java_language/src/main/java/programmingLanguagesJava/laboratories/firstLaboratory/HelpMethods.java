package programmingLanguagesJava.laboratories.firstLaboratory;

import java.util.Arrays;
import java.util.Random;

public class HelpMethods {
    public static int algorithm_stein(int a, int b) {

        // GCD(0, b) == b; GCD(a, 0) == a,
        // GCD(0, 0) == 0
        if (a == 0)
            return b;
        if (b == 0)
            return a;

        // Finding K, where K is the greatest
        // power of 2 that divides both a and b
        int k;
        for (k = 0; ((a | b) & 1) == 0; ++k) {
            a >>= 1;
            b >>= 1;
        }

        // Dividing a by 2 until a becomes odd
        while ((a & 1) == 0)
            a >>= 1;

        // From here on, 'a' is always odd.
        do {
            // If b is even, remove
            // all factor of 2 in b
            while ((b & 1) == 0)
                b >>= 1;

            // Now a and b are both odd. Swap
            // if necessary so a <= b, then set
            // b = b - a (which is even)
            if (a > b) {
                // Swap u and v.
                int temp = a;
                a = b;
                b = temp;
            }

            b = (b - a);
        } while (b != 0);

        // restore common factors of 2
        return a << k;
    }

    /**
     * Вспомогательный статический метод, который используется для создания случайной матрицы.
     *
     * @param CountRows    количество строк в матрице.
     * @param CountColumns количество колонок в матрице.
     * @return Возвращает матрицу
     */

    public static int[][] generateRandomMatrix(int CountRows, int CountColumns) {
        Random random = new Random();
        // map: Этот метод используется для преобразования элементов потока в примитивные типы данных (int, long, double).
        // Например, если вы имеете дело с IntStream, LongStream или DoubleStream,
        // то map применяется для преобразования элементов в другой примитивный тип данных.
        return Arrays.stream(new int[CountRows][CountColumns])
                .map(row -> Arrays.stream(row)
                        .map(col -> random.nextInt(100)) // Здесь 100 - верхняя граница случайных чисел
                        .toArray())
                .toArray(int[][]::new);
    }

    /**
     * Вспомогательный статический метод для вывода матрицы в консоль
     *
     * @param matrix матрица, которую хотим распечатать
     */
    public static void printMatrix(int[][] matrix) {
        Arrays.stream(matrix)
                .forEach(row -> {
                    Arrays.stream(row)
                            .forEach(cell -> System.out.print(cell + " "));
                    System.out.println(); // Переход на новую строку для каждой строки матрицы
                });
    }
}

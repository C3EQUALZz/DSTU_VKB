package laboratories.firstLaboratory;

import java.util.Scanner;
import java.util.Random;
import java.util.stream.IntStream;

public class Solution {
    static final IntStream firstArray = new Random().ints(20, -100, 21);
    static final IntStream secondArray = new Random().ints(15, -100, 16);
    static final IntStream thirdArray = new Random().ints(10, -100, 11);
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введите номер задания, чье решения вы хотите получить");

        Object result = switch (scanner.nextInt()) {
            case 1 -> firstQuestion();
            case 2 -> secondQuestion();
            default -> "Вы выбрали неверное задание";
        };
        System.out.println(result);
    }

    /**
     * 1. Вычислить z = Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt((Math.abs(max_x * max_y)))
     * где - наибольший элемент массива X(20); - наибольший элемент массива Y(15).
     * Для вычисления наибольшего элемента массива использовать функцию.
     * @return значение после вычисления
     */

    public static double firstQuestion() {
        int max_x = Solution.firstArray.max().orElseThrow();
        int max_y = Solution.secondArray.max().orElseThrow();

        return (Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt(Math.abs(max_x * max_y));
    }

    /**
     * Вычислить M = (S+T+K)/2, где S, T, K – суммы положительных элементов массивов А, В, С соответственно.
     * Для вычисления суммы положительных элементов использовать функцию.
     * @return значение полученного выражения
     */

    public static double secondQuestion() {
        return (Solution.firstArray.filter(n -> n > 0).sum() +
                Solution.secondArray.filter(n -> n > 0).sum() +
                Solution.thirdArray.filter(n -> n > 0).sum()) / 2.0;
    }

    /**
     * 3.	Даны целые числа m, n. Вычислить с = m!/(n! * (m-n)!). Для вычисления факториала использовать функцию.
     */
    public static int thirdQuestion() {
        return 1;
    }

}

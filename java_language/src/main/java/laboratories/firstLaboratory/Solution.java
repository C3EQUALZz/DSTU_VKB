/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package laboratories.firstLaboratory;


import java.math.BigInteger;
import java.util.Arrays;
import java.util.Scanner;
import java.util.Random;
import java.util.stream.IntStream;
import java.util.stream.Collectors;

import org.paukov.combinatorics3.Generator;

import com.google.common.math.BigIntegerMath;

public class Solution {
    static final IntStream firstIntStream = new Random().ints(20, -100, 21);
    static final IntStream secondIntStream = new Random().ints(15, -100, 16);
    static final IntStream thirdIntStream = new Random().ints(10, -100, 11);

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введите номер задания, чье решения вы хотите получить");

        Object result = switch (scanner.nextInt()) {
            case 1 -> firstQuestion();
            case 2 -> secondQuestion();
            case 3 -> thirdQuestion();
            case 4 -> fourthQuestion();
            case 5 -> fifthQuestion();
            case 6 -> sixthQuestion();
            case 7 -> seventhQuestion();
            default -> "Вы выбрали неверное задание";
        };
        System.out.println(result);
    }

    /**
     * 1. Вычислить z = Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt((Math.abs(max_x * max_y)))
     * где - наибольший элемент массива X(20); - наибольший элемент массива Y(15).
     * Для вычисления наибольшего элемента массива использовать функцию.
     *
     * @return значение после вычисления
     */

    public static double firstQuestion() {
        // orElseTrow возвращает значение, если оно существует, в ином случае будет возмущена ошибка
        var max_x = Solution.firstIntStream.max().orElseThrow();
        var max_y = Solution.secondIntStream.max().orElseThrow();

        return (Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt(Math.abs(max_x * max_y));
    }

    /**
     * 2. Вычислить M = (S+T+K)/2, где S, T, K – суммы положительных элементов массивов А, В, С соответственно.
     * Для вычисления суммы положительных элементов использовать функцию.
     *
     * @return значение полученного выражения
     */

    public static double secondQuestion() {
        // -> - это лямбда выражение, как в .net
        return (Solution.firstIntStream.filter(n -> n > 0).sum() +
                Solution.secondIntStream.filter(n -> n > 0).sum() +
                Solution.thirdIntStream.filter(n -> n > 0).sum()) / 2.0;
    }

    /**
     * 3. Даны целые числа m, n. Вычислить с = m!/(n! * (m-n)!).
     * Для вычисления факториала использовать функцию.
     *
     * @return Возвращает целое число, то есть результат сочетания.
     */
    public static BigInteger thirdQuestion() {
        int m = 4, n = 2;
        // в Java, к сожалению, нет перегрузки операторов, поэтому тут математические действия делаются через методы
        // Взято с библиотеки
        return BigIntegerMath.factorial(m).divide(
                BigIntegerMath.factorial(n).multiply(BigIntegerMath.factorial(m - n)));
    }

    /**
     * 4. Даны действительные х, у, z. Составить программу вычисления значения
     * Math.sqrt(pow_x + pow_y + Math.pow(Math.sin(x * y), 2)) + Math.sqrt(pow_x + pow_z + Math.pow(Math.sin(x * z), 2))
     * + Math.sqrt(pow_z + pow_y + Math.pow(Math.sin(z * y), 2))
     */
    public static double fourthQuestion() {
        // Здесь я нашел библиотеку, которая генерирует комбинации из (1, 2, 3) по 2 элемента.
        // map здесь делается то же самое, но есть небольшие разновидности, которые переделывают нам элементы к
        // нужному типу данных. По умолчанию generator возвращает итератор, где каждый элемент - это список с числами.
        return Generator.combination(1, 2, 3).simple(2).stream().mapToDouble(x ->
                Math.sqrt(Math.pow(x.getFirst(), 2) + Math.pow(x.getLast(), 2) +
                        Math.pow(Math.sin(x.getFirst() * x.getLast()), 2))).sum();
    }

    /**
     * 5. Составить программу для вычисления среднего арифметического положительных элементов массивов Х(20), Y(15),
     * Z(10), используя в качестве подпрограммы функцию.
     *
     * @return Возвращает строку, где написаны средние значения в каждом массиве.
     */
    public static String fifthQuestion() {
        IntStream[] arrays = {firstIntStream, secondIntStream, thirdIntStream};
        // Нет аналога enumerate, поэтому воспользовался таким костылем.
        return IntStream.range(0, arrays.length)
                .mapToObj(index -> "Среднее значение массива " + (index + 1) + ": " +
                        String.format("%.3f", arrays[index].filter(x -> x > 0).average().orElseThrow()))
                .collect(Collectors.joining("\n"));
    }

    /**
     * 6. Даны массивы А(15), Y(15), C(12).
     * Вычислить l = min(b_i) + min(c_i) if abs(min(a_i)) > 10 else 1 + min(abs(c_i))
     */
    public static String sixthQuestion() {
        var result = Math.abs(firstIntStream.min().orElseThrow()) > 10 ?
                secondIntStream.min().orElseThrow() + thirdIntStream.min().orElseThrow() :
                1 + thirdIntStream.map(Math::abs).min().orElseThrow();
        return String.format("Значение задания номер 6: %d", result);
    }

    /**
     * 7. Дан массив D(40) вещественных чисел. Найти среднее геометрическое его элементов,
     * которые удовлетворяют условию 0 < di <12. Для вычислений использовать функцию.
     */
    public static String seventhQuestion() {
        double[] D = new Random().doubles(40).toArray();
        var result = Math.pow(
                Arrays.stream(D).filter(x -> x > 0 && x < 12).reduce(1, (a, b) -> a * b),
                1.0 / D.length
        );

        return String.format("Значение задания номер 7: %.3f", result);
    }

    /**
     * 8.	Дан массив А(80) целых  чисел. Найти сумму и количество теx элементов массива, которые отрицательны и нечетны. Использовать в качестве подпрограммы процедуру.
     */

}


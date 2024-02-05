/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package programmingLanguagesJava.laboratories.firstLaboratory;


import com.google.common.math.BigIntegerMath;
import org.paukov.combinatorics3.Generator;
import programmingLanguagesJava.laboratories.ConsoleReader;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.time.DayOfWeek;
import java.time.format.TextStyle;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Solution {
    static final int[] firstIntStream = new Random().ints(20, -100, 21).toArray();
    static final int[] secondIntStream = new Random().ints(15, -100, 16).toArray();
    static final int[] thirdIntStream = new Random().ints(10, -100, 11).toArray();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите номер задания: ");
        var question = scanner.nextInt();

        System.out.printf("Результат %d задания: ", question);

        Object result = switch (question) {
            case 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ->
                    ConsoleReader.executeTask(Solution.class, String.valueOf(question), " ");

            case 12, 13 -> {
                System.out.print("Введите ваше число: ");
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.next());
            }

            case 14, 15 -> {
                System.out.print("Введите строку: ");
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.nextLine());
            }

            case 16 -> {
                System.out.println("Введите два числа через пробел: ");
                yield sixteenthQuestion(scanner.nextLine());
            }

            case 17 -> {
                System.out.println("Введите номер фигуры:\n1.Круг\n2.Прямоугольник\n3.Треугольник");
                var numberOfFigure = scanner.next();
                yield seventhQuestion(numberOfFigure);

            }

            default -> "Вы выбрали неверное задание";
        };

        scanner.close();
        System.out.println(result);
    }

    /**
     * 1. Вычислить z = Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt((Math.abs(max_x * max_y)))
     * где - max_x наибольший элемент массива X(20); max_y - наибольший элемент массива Y(15).
     * Для вычисления наибольшего элемента массива использовать функцию.
     */
    @SuppressWarnings("unused")
    public static String firstQuestion(String ignoredUnused) {
        // orElseTrow возвращает значение, если оно существует, в ином случае будет возмущена ошибка
        var max_x = Arrays.stream(Solution.firstIntStream).max().orElseThrow();
        var max_y = Arrays.stream(Solution.secondIntStream).max().orElseThrow();
        var result = (Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt(Math.abs(max_x * max_y));

        return String.format("z = ( e ^ |%d| - e ^ |%d| ) / sqrt(| %d * %d |) = %f", max_x, max_y, max_x, max_y, result);
    }

    /**
     * 2. Даны массивы действительных чисел А(20), B(15), C(10).
     * Вычислить M = (S+T+K)/2, где S, T, K – суммы положительных элементов массивов А, В, С соответственно.
     * Для вычисления суммы положительных элементов использовать функцию.
     */
    @SuppressWarnings("unused")
    public static String secondQuestion(String ignoredUnused) {
        // -> - это лямбда выражение, как в .net
        var s = Arrays.stream(Solution.firstIntStream).filter(n -> n > 0).sum();
        var t = Arrays.stream(Solution.secondIntStream).filter(n -> n > 0).sum();
        var k = Arrays.stream(Solution.thirdIntStream).filter(n -> n > 0).sum();
        var result = (s + t + k) / 2.0;

        return String.format("М = (%d + %d + %d) / 2 = %f", s, t, k, result);
    }

    /**
     * 3. Даны целые числа m, n. Вычислить с = m!/(n! * (m-n)!).
     * Для вычисления факториала использовать функцию.
     */
    @SuppressWarnings("unused")
    public static String thirdQuestion(String ignoredUnused) {
        // когда мы определяем так самые базовые типы, то нельзя var писать.
        int m = 4, n = 2;
        BigInteger factorialM = BigIntegerMath.factorial(m), factorialN = BigIntegerMath.factorial(n), factDiff = BigIntegerMath.factorial(m - n);
        // в Java, к сожалению, нет перегрузки операторов, поэтому тут математические действия делаются через методы
        // Взято с библиотеки
        var result = factorialM.divide(factorialN.multiply(factDiff));
        return String.format("c = %d! / (%d! * (%d - %d)!) = %d", m, n, m, n, result);
    }

    /**
     * 4. Даны действительные х, у, z. Составить программу вычисления значения
     * Math.sqrt(pow_x + pow_y + Math.pow(Math.sin(x * y), 2)) + Math.sqrt(pow_x + pow_z + Math.pow(Math.sin(x * z), 2))
     * + Math.sqrt(pow_z + pow_y + Math.pow(Math.sin(z * y), 2))
     */
    @SuppressWarnings("unused")
    public static String fourthQuestion(String ignoredUnused) {
        // Здесь я нашел библиотеку, которая генерирует комбинации из (1, 2, 3) по 2 элемента.
        // map здесь делается то же самое, но есть небольшие разновидности, которые переделывают нам элементы к
        // нужному типу данных. По умолчанию generator возвращает итератор, где каждый элемент - это список с числами.
        var result = Generator.combination(1, 2, 3).simple(2).stream().mapToDouble(x ->
                Math.sqrt(Math.pow(x.getFirst(), 2) + Math.pow(x.getLast(), 2) +
                        Math.pow(Math.sin(x.getFirst() * x.getLast()), 2))).sum();
        return String.format("s = sqrt(1 + 4 + sin(2)^2) + sqrt(1 + 9 + sin(9)^2) + sqrt(4 + 9 + sin(6)^2 = %f", result);
    }

    /**
     * 5. Составить программу для вычисления среднего арифметического положительных элементов массивов Х(20), Y(15),
     * Z(10), используя в качестве подпрограммы функцию.
     */
    @SuppressWarnings("unused")
    public static String fifthQuestion(String ignoredUnused) {
        // var не дает прописать, надо явно указать
        int[][] arrays = {firstIntStream, secondIntStream, thirdIntStream};
        // Нет аналога enumerate, поэтому воспользовался таким костылем.
        try {

            return "\n" + Arrays.stream(arrays).map(array ->
                            "Среднее значение массива " +
                                    Arrays.toString(array) + ": " +
                                    String.format("%.3f", Arrays.stream(array).filter(x -> x > 0).average().orElseThrow()))

                    .collect(Collectors.joining("\n"));

        } catch (NoSuchElementException e) {
            return "Перезапустите задание, в случайном массиве только отрицательные элементы";
        }

    }

    /**
     * 6. Даны массивы А(15), Y(15), C(12).
     * Вычислить l = min(b_i) + min(c_i) if abs(min(a_i)) > 10 else 1 + min(abs(c_i))
     */
    @SuppressWarnings("unused")
    public static String sixthQuestion(String ignoredUnused) {

        var min_a = Math.abs(Arrays.stream(firstIntStream).min().orElseThrow());

        if (min_a > 10) {
            var min_b = Arrays.stream(secondIntStream).min().orElseThrow();
            var min_c = Arrays.stream(thirdIntStream).min().orElseThrow();
            return String.format("min_a = %d -> %d + %d = %d", min_a, min_b, min_c, min_b + min_c);
        }

        var min_abc_c = Arrays.stream(thirdIntStream).map(Math::abs).min().orElseThrow();
        return String.format("min_a = %d -> 1 + %d = %d", min_a, min_abc_c, 1 + min_abc_c);
    }

    /**
     * 7. Дан массив D(40) вещественных чисел. Найти среднее геометрическое его элементов,
     * которые удовлетворяют условию 0 < di < 12. Для вычислений использовать функцию.
     */
    @SuppressWarnings("unused")
    public static String seventhQuestion(String ignoredUnused) {
        var D = new Random().doubles(40).toArray();

        var result = Math.pow(
                Arrays.stream(D).filter(x -> x > 0 && x < 12).reduce(1, (a, b) -> a * b),
                1.0 / D.length
        );

        return String.format("Массив %s, где среднее геометрическое - %.3f", Arrays.toString(D), result);
    }

    /**
     * 8. Дан массив А(80) целых чисел.
     * Найти сумму и количество тех элементов массива, которые отрицательны и нечетны.
     * Использовать в качестве подпрограммы процедуру.
     */
    @SuppressWarnings("unused")
    public static String eighthQuestion(String ignoredUnused) {
        var A = new Random().ints(80).toArray();

        var result = Arrays.stream(A).filter(n -> n < 0 && Math.abs(n) % 2 == 1).sum();
        return "Результат 8 задания: " + result;
    }

    /**
     * 9. Функция, вычисляющая среднее арифметическое элементов массива.
     * Написать функцию, которая вычисляет среднее арифметическое элементов массива,
     * переданного ей в качестве аргумента
     */
    @SuppressWarnings("unused")
    public static String ninthQuestion(String ignoredUnused) {
        return "Результат 9 задания: " + Arrays.stream(Solution.firstIntStream).average().orElseThrow();
    }

    /**
     * 10. Отсортировать массив по возрастанию суммы цифр
     * Дан одномерный массив, состоящий из натуральных чисел.
     * Выполнить сортировку данного массива по возрастанию суммы цифр чисел.
     * Например, дан массив чисел [14, 30, 103]. После сортировки он будет таким: [30, 103, 14],
     * так как сумма цифр числа 30 составляет 3, числа 103 равна 4, числа 14 равна 5.
     */
    @SuppressWarnings("unused")
    public static String tenthQuestion(String ignoredUnused) {
        IntStream stream = new Random().ints(50, 1, 10000);
        var result = stream
                .boxed()
                .sorted(Comparator.comparingInt(n -> {

                    int sumOfDigits = 0;
                    n = Math.abs(n);

                    while (n > 0) {
                        sumOfDigits += n % 10;
                        n /= 10;
                    }
                    return sumOfDigits;
                }))
                .toArray();

        return "Результат 10 задания: " + Arrays.toString(result);
    }

    /**
     * 11. Вывести на экран исходный массив, отсортированный массив,
     * а также для контроля сумму цифр каждого числа отсортированного массива.
     */
    @SuppressWarnings("unused")
    public static String eleventhQuestion(String ignoredUnused) {
        var res = "Результат 11 задания:\n";
        var array = new Random().ints(50, 1, 10000).toArray();
        res += "Исходный массив: " + Arrays.toString(array) + "\n";
        res += "Отсортированный массив: " + Arrays.stream(array).boxed().sorted().toList() + "\n";
        res += "Сумма цифр каждого числа: " + Arrays.stream(array).map(n -> {

            int sumOfDigits = 0;
            n = Math.abs(n);

            while (n > 0) {
                sumOfDigits += n % 10;
                n /= 10;
            }
            return sumOfDigits;
        }).boxed().toList();

        return res;
    }

    /**
     * 12. Определить количество разрядов числа.
     * Написать функцию, которая определяет количество разрядов введенного целого числа.
     */
    @SuppressWarnings("unused")
    public static String twelfthQuestion(String number) {
        int n = Math.abs(Integer.parseInt(number));
        // копия числа, так как я изменяю n
        var p = n;

        int count = 0;

        while (n > 0) {
            count += 1;
            n /= 10;
        }

        return String.format("Результат 12 задания:\nКоличество разрядов числа: %d равно: %d", p, count);
    }

    /**
     * 13. Сумма ряда с факториалом. Вычислить сумму ряда
     */
    @SuppressWarnings("unused")
    public static String thirteenthQuestion(String number) {

        int x = Integer.parseInt(number), result = 0;

        for (int i = 1; i < 6; i++) {
            result += (-1) * i * (x / BigIntegerMath.factorial(i).intValue());
        }

        return String.format("Результат 13 задания: %d", result);
    }

    /**
     * 14. Изменить порядок слов в строке на обратный.
     * Вводится строка, состоящая из слов, разделенных пробелами.
     * Следует заменить ее на строку, в которой слова идут в обратном порядке по сравнению с
     * исходной строкой. Вывести измененную строку на экран.
     */
    @SuppressWarnings("unused")
    public static String fourteenthQuestion(String words) {
        // List.of - переделывает в интерфейс List, потом приходится вручную кастовать к ArrayList
        // Collections.swap просит изменяемый объект, что вполне логично, поэтому переделал к ArrayList.
        var src = new ArrayList<>(List.of(words.split(" ")));
        var len = src.size();

        for (var i = 0; i <= (len / 2); i++)
            Collections.swap(src, len - i - 1, i);

        return String.format("Результат 14 задания: %s", String.join(" ", src));
    }

    /**
     * 15. Функция бинарного поиска в массиве
     * Пользователь вводит число. Сообщить, есть ли оно в массиве,
     * элементы которого расположены по возрастанию значений, а также, если есть,
     * в каком месте находится.
     * При решении задачи использовать бинарный (двоичный) поиск, который оформить в виде отдельной
     * функции.
     */
    @SuppressWarnings("unused")
    public static String fifteenthQuestion(String valueForSearch) {
        var sortedRandArr = new Random().ints(10, 0, 11).sorted().toArray();

        System.out.print("Введите ваше число, которое вы хотите найти: ");
        var value = Integer.parseInt(valueForSearch);

        // В Java есть встроенный бинарный поиск, зачем писать свой?
        int index = Arrays.binarySearch(sortedRandArr, value);


        return String.format(
                "15 задание: \n" + "Массив: " + Arrays.toString(sortedRandArr) + "\nЭлемент %d %s", value,
                index >= 0 ? " на позиции " + index : " не найден в массиве"
        );
    }

    /**
     * 16. Вычисление наибольших общих делителей.
     * Найти наибольшие общие делители (НОД) для множества пар чисел.
     */
    @SuppressWarnings("unused")
    public static String sixteenthQuestion(String stringWithTwoNumbers) {
        // Здесь будет использоваться алгоритм Штейна для нахождения НОД. Его сложность O(n^2/log(n)^2)
        // По сложности кажется, что он хуже Евклида O(log(min(a, b))), но он быстрее его за счет битовых сдвигов.
        var res = stringWithTwoNumbers.split(" ");
        int a = Integer.parseInt(res[0]), b = Integer.parseInt(res[1]);

        return String.format(
                "Результат 16 задания: %s",
                "НОД: " + HelpMethods.algorithm_stein(a, b)
        );
    }


    /**
     * 17. Найти площади разных фигур. В зависимости от выбора пользователя вычислить площадь круга, прямоугольника или
     * треугольника. Для вычисления площади каждой фигуры должна быть написана отдельная функция.
     */
    @SuppressWarnings("unused")
    public static String seventeenthQuestion(String param) {
        // Подумать над вводом в GUI
        return switch (Integer.parseInt(param)) {
            case 1 -> Circle.square();
            case 2 -> Rect.square();
            case 3 -> Triangle.square();
            default -> "Выбрали неверное задание";
        };
    }

    /**
     * 18. Найти массив с максимальной суммой элементов.
     * Сгенерировать десять массивов из случайных чисел.
     * Вывести их и сумму их элементов на экран.
     * Найти среди них один с максимальной суммой элементов.
     * Указать какой он по счету, повторно вывести этот массив и сумму его элементов.
     * Заполнение массива и подсчет суммы его элементов оформить в виде отдельной функции.
     */
    @SuppressWarnings("unused")
    public String eighteenthQuestion() {

        var matrix = HelpMethods.generateRandomMatrix(5, 5);
        HelpMethods.printMatrix(matrix);

        // Наш список с суммами.
        var sums = Arrays.stream(matrix).mapToInt(row -> Arrays.stream(row).sum()).boxed().toList();
        System.out.println(sums);

        // Странно, что в обычном массиве не реализован indexOf, только в списках есть данный метод.
        var index = sums.indexOf(sums.stream().max(Integer::compare).orElseThrow());

        return String.format("Результат 18 задания:\n" +
                        "Строка, где максимальная сумма %s, с индексом %d, сумма - %d",
                Arrays.toString(matrix[index]),
                index,
                Arrays.stream(matrix[index]).sum());
    }

    /**
     * 19. Вычислить сумму элементов главной или побочной диагонали матрицы.
     * Дана квадратная матрица. Вычислить сумму элементов главной или побочной диагонали в зависимости от
     * выбора пользователя. Сумма элементов любой диагонали должна вычисляться в одной и той же функции.
     */
    @SuppressWarnings("unused")
    public String nineteenthQuestion() {
        // Хотел на самом деле поискать аналог Numpy, но здесь так много библиотек, что вообще непонятно какую можно исп.
        // Пришлось вот так вручную через StreamApi делать, долго мучался, чтобы заработало.

        Scanner scanner = new Scanner(System.in);
        // Создаем генератор случайных чисел
        Random random = new Random();

        // Создаем матрицу с использованием Stream API и заполняем случайными числами
        var matrix = HelpMethods.generateRandomMatrix(5, 5);

        // Просто вывод матрицы в консоль
        HelpMethods.printMatrix(matrix);

        System.out.print("Введите что вы хотите сделать: " +
                "(1) вычислить сумму главной диагонали, " +
                "(2) вычислить сумму побочной диагонали: ");

        var userChoice = scanner.nextInt();

        var result = Arrays.stream(matrix)
                .mapToInt(row ->
                        row[userChoice == 1 ?
                                Arrays.asList(matrix).indexOf(row) :
                                matrix.length - 1 - Arrays.asList(matrix).indexOf(row)])
                .sum();

        return String.format("Результат 19 задания: %d", result);
    }

    /**
     * 20. Функция перевода десятичного числа в двоичное.
     * Переводить в двоичную систему счисления вводимые в десятичной системе счисления числа до тех пор,
     * пока не будет введен 0. Для перевода десятичного числа в двоичное написать функцию.
     */
    @SuppressWarnings("unused")
    public String twentiethQuestion() {
        Scanner scanner = new Scanner(System.in);
        var strBuilder = new StringBuilder();

        while (true) {
            System.out.print("Введите число (для завершения введите 0): ");
            var number = scanner.nextInt();

            if (number == 0)
                break;

            // Встроенная функция для перевода в различные системы исчисления.
            // Может переводить в СС от 2 до 36 включительно.
            var binaryNumber = Integer.toString(number, 2);
            strBuilder.append(String.format("Результат перевода двоичного числа %d - %s\n", number, binaryNumber));
        }
        scanner.close();

        return String.format("Результат 20 задания:\n%s", strBuilder);
    }

    /**
     * 21. Вычислить значения функции y=f(x) на заданном диапазоне.
     * Вычислить значения нижеприведенной функции в диапазоне значений x от -10 до 10
     * включительно с шагом, равным 1.
     * y = x2 при -5 <= x <= 5;
     * y = 2*|x|-1 при x < -5;
     * y = 2x при x > 5.
     * Вычисление значения функции оформить в виде программной функции, которая принимает значение x,
     * а возвращает полученное значение функции (y).
     */
    @SuppressWarnings("unused")
    public String twentyFirstQuestion() {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите x: ");
        int x = scanner.nextInt(), y;
        scanner.close();

        if (x <= 5)
            y = x >= -5 ? (int) Math.pow(x, 2) : 2 * Math.abs(x) - 1;
        else
            y = 2 * x;

        return String.format("Результат 21 задания: %d", y);
    }

    /**
     * 22. Функция заполнения массива случайными числами.
     * Написать функцию, которая заполняет массив случайными числами в диапазоне, указанном пользователем.
     * Функция должна принимать два аргумента - начало диапазона и его конец, при этом ничего не возвращать.
     * Вывод значений элементов массива должен происходить в основной ветке программы.
     */
    @SuppressWarnings("unused")
    public String twentySecondQuestion() {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите два числа через пробел: ");
        int start = scanner.nextInt(), end = scanner.nextInt();
        scanner.close();

        var randomArray = new Random().ints(10, start, end).toArray();

        return String.format("Результат 22 задания: %s", Arrays.toString(randomArray));
    }

    /**
     * 23. Написать функцию вычисления величины силы тока на участке электрической
     * цепи сопротивлением R Ом при напряжении U В.
     */
    @SuppressWarnings("unused")
    public String twentyThirdQuestion() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введите U, R через пробел:");
        double U = scanner.nextDouble(), R = scanner.nextDouble();

        scanner.close();
        return String.format("Результат 23 задания: %f", U / R);
    }

    /**
     * 24.	Написать функцию вычисления напряжения на каждом из последовательно
     * соединенных участков электрической цепи сопротивлением R1, R2, R3 Ом, если сила
     * тока при напряжении U В составляет I А.
     */
    @SuppressWarnings("unused")
    public String twentyFourthQuestion() {
        Scanner scanner = new Scanner(System.in);
        double[] R = new double[3], U = new double[3];

        System.out.print("Введите I: ");
        double I = scanner.nextDouble();

        for (int i = 0; i < 3; i++) {
            System.out.print("Введите R" + i + ": ");
            R[i] = scanner.nextDouble();
            U[i] = I * R[i];
        }
        scanner.close();
        // Создаем строки с соответствующими напряжениями. Через Decimal есть только округление, которое мне нужно
        // Очень странно, что разработчики не сделали в том же самом Math для этого нужный статический метод.
        var UString = Arrays.stream(U)
                .mapToObj(number -> BigDecimal.valueOf(number).setScale(6, RoundingMode.HALF_UP).toString())
                .collect(Collectors.joining(" "));

        return String.format("Результат 24 задания: %s", UString);
    }

    /**
     * 25. Составить программу для ввода на экран номера дня недели и вывода соответствующего
     * ему дня недели на русском языке.
     */
    @SuppressWarnings("unused")
    public String twentyFifthQuestion() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введите номер дня недели (от 1 до 7):");
        int dayNumber = scanner.nextInt();
        scanner.close();

        // Проверка, чтобы номер дня недели был в пределах от 1 до 7
        if (dayNumber >= 1 && dayNumber <= 7) {
            DayOfWeek dayOfWeek = DayOfWeek.of(dayNumber);
            String result = dayOfWeek.getDisplayName(TextStyle.FULL, Locale.forLanguageTag("ru"));
            return String.format("Результат 25 задания: День недели: %s", result);
        }
        return "Результат 25 задания: Некорректный номер дня недели.";
    }
}



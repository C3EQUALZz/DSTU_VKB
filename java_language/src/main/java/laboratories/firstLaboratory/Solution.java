/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package laboratories.firstLaboratory;


import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.time.DayOfWeek;
import java.time.format.TextStyle;
import java.util.*;
import java.util.stream.IntStream;
import java.util.stream.Collectors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.ibm.icu.text.RuleBasedNumberFormat;
import org.paukov.combinatorics3.Generator;

import com.google.common.math.BigIntegerMath;

public class Solution {
    static final IntStream firstIntStream = new Random().ints(20, -100, 21);
    static final IntStream secondIntStream = new Random().ints(15, -100, 16);
    static final IntStream thirdIntStream = new Random().ints(10, -100, 11);

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Перевод в англ слова, второе взял из stackoverflow.
        RuleBasedNumberFormat numberFormat = new RuleBasedNumberFormat(Locale.UK, RuleBasedNumberFormat.SPELLOUT);

        Object result;

        System.out.print("Введите какое задание вы хотите выполнить: ");
        try {
            // Получение значения метода из цифры, задавая ему правила.
            // Все вот эти штуки называются отражениями, здесь нет удобного аналога eval, как в Python.
            // Как бы говоря есть, но там под капотом JS, который не может работать с Java напрямую.
            var methodName = numberFormat.format(scanner.nextInt(), "%spellout-ordinal") + "Question";
            // В случае больше двадцати methodName может вернуть типа: twenty-first

            Pattern pattern = Pattern.compile("-(\\w)");
            Matcher matcher = pattern.matcher(methodName);

            StringBuilder str = new StringBuilder();

            // Находим и заменяем каждое вхождение
            while (matcher.find()) {
                matcher.appendReplacement(str, matcher.group(1).toUpperCase());
            }
            matcher.appendTail(str);

            Method method = Solution.class.getMethod(str.toString());
            result = method.invoke(new Solution());

        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            result = "Вы выбрали неверное задание";
        }

        System.out.println(result);
        scanner.close();
    }

    /**
     * 1. Вычислить z = Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt((Math.abs(max_x * max_y)))
     * где - наибольший элемент массива X(20); - наибольший элемент массива Y(15).
     * Для вычисления наибольшего элемента массива использовать функцию.
     *
     * @return значение после вычисления
     */
    @SuppressWarnings("unused")
    public String firstQuestion() {
        // orElseTrow возвращает значение, если оно существует, в ином случае будет возмущена ошибка
        var max_x = Solution.firstIntStream.max().orElseThrow();
        var max_y = Solution.secondIntStream.max().orElseThrow();
        var result = (Math.exp(Math.abs(max_x)) - Math.exp(Math.abs(max_y))) / Math.sqrt(Math.abs(max_x * max_y));

        return String.format("Результат 1 задания: %f", result);
    }

    /**
     * 2. Вычислить M = (S+T+K)/2, где S, T, K – суммы положительных элементов массивов А, В, С соответственно.
     * Для вычисления суммы положительных элементов использовать функцию.
     *
     * @return значение полученного выражения
     */
    @SuppressWarnings("unused")
    public String secondQuestion() {
        // -> - это лямбда выражение, как в .net
        var result = (Solution.firstIntStream.filter(n -> n > 0).sum() +
                Solution.secondIntStream.filter(n -> n > 0).sum() +
                Solution.thirdIntStream.filter(n -> n > 0).sum()) / 2.0;

        return String.format("Результат 2 задания: %f", result);
    }

    /**
     * 3. Даны целые числа m, n. Вычислить с = m!/(n! * (m-n)!).
     * Для вычисления факториала использовать функцию.
     *
     * @return Возвращает целое число, то есть результат сочетания.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion() {
        // когда мы определяем так самые базовые типы, то нельзя var писать.
        int m = 4, n = 2;
        // в Java, к сожалению, нет перегрузки операторов, поэтому тут математические действия делаются через методы
        // Взято с библиотеки
        var result = BigIntegerMath.factorial(m).divide(
                BigIntegerMath.factorial(n).multiply(BigIntegerMath.factorial(m - n)));
        return String.format("Результат 3 задания: %d", result);
    }

    /**
     * 4. Даны действительные х, у, z. Составить программу вычисления значения
     * Math.sqrt(pow_x + pow_y + Math.pow(Math.sin(x * y), 2)) + Math.sqrt(pow_x + pow_z + Math.pow(Math.sin(x * z), 2))
     * + Math.sqrt(pow_z + pow_y + Math.pow(Math.sin(z * y), 2))
     */
    @SuppressWarnings("unused")
    public String fourthQuestion() {
        // Здесь я нашел библиотеку, которая генерирует комбинации из (1, 2, 3) по 2 элемента.
        // map здесь делается то же самое, но есть небольшие разновидности, которые переделывают нам элементы к
        // нужному типу данных. По умолчанию generator возвращает итератор, где каждый элемент - это список с числами.
        var result = Generator.combination(1, 2, 3).simple(2).stream().mapToDouble(x ->
                Math.sqrt(Math.pow(x.getFirst(), 2) + Math.pow(x.getLast(), 2) +
                        Math.pow(Math.sin(x.getFirst() * x.getLast()), 2))).sum();
        return String.format("Результат 4 задания: %f", result);
    }

    /**
     * 5. Составить программу для вычисления среднего арифметического положительных элементов массивов Х(20), Y(15),
     * Z(10), используя в качестве подпрограммы функцию.
     *
     * @return Возвращает строку, где написаны средние значения в каждом массиве.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion() {
        // var не дает прописать, надо явно указать
        IntStream[] arrays = {firstIntStream, secondIntStream, thirdIntStream};
        // Нет аналога enumerate, поэтому воспользовался таким костылем.
        return "Результат 5 задания:\n" + IntStream.range(0, arrays.length)
                .mapToObj(index -> "Среднее значение массива " + (index + 1) + ": " +
                        String.format("%.3f", arrays[index].filter(x -> x > 0).average().orElseThrow()))
                .collect(Collectors.joining("\n"));
    }

    /**
     * 6. Даны массивы А(15), Y(15), C(12).
     * Вычислить l = min(b_i) + min(c_i) if abs(min(a_i)) > 10 else 1 + min(abs(c_i))
     */
    @SuppressWarnings("unused")
    public String sixthQuestion() {
        var result = Math.abs(firstIntStream.min().orElseThrow()) > 10 ?
                secondIntStream.min().orElseThrow() + thirdIntStream.min().orElseThrow() :
                1 + thirdIntStream.map(Math::abs).min().orElseThrow();
        return String.format("Результат 6 задания: %d", result);
    }

    /**
     * 7. Дан массив D(40) вещественных чисел. Найти среднее геометрическое его элементов,
     * которые удовлетворяют условию 0 < di <12. Для вычислений использовать функцию.
     */
    @SuppressWarnings("unused")
    public String seventhQuestion() {
        var D = new Random().doubles(40).toArray();
        var result = Math.pow(
                Arrays.stream(D).filter(x -> x > 0 && x < 12).reduce(1, (a, b) -> a * b),
                1.0 / D.length
        );

        return String.format("Результат 7 задания: %.3f", result);
    }

    /**
     * 8. Дан массив А(80) целых чисел.
     * Найти сумму и количество тех элементов массива, которые отрицательны и нечетны.
     * Использовать в качестве подпрограммы процедуру.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion() {
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
    public String ninthQuestion() {
        return "Результат 9 задания: " + Solution.firstIntStream.average().orElseThrow();
    }

    /**
     * 10. Отсортировать массив по возрастанию суммы цифр
     * Дан одномерный массив, состоящий из натуральных чисел.
     * Выполнить сортировку данного массива по возрастанию суммы цифр чисел.
     * Например, дан массив чисел [14, 30, 103]. После сортировки он будет таким: [30, 103, 14],
     * так как сумма цифр числа 30 составляет 3, числа 103 равна 4, числа 14 равна 5.
     */
    @SuppressWarnings("unused")
    public String tenthQuestion() {
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
    public String eleventhQuestion() {
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
    public String twelfthQuestion() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введите ваше число: ");
        var n = Math.abs(scanner.nextInt());
        // копия числа, так как я изменяю n
        var p = n;

        int count = 0;

        while (n > 0) {
            count += 1;
            n /= 10;
        }
        scanner.close();

        return String.format("Результат 12 задания:\nКоличество разрядов числа: %d равно: %d", p, count);
    }

    /**
     * 13. Сумма ряда с факториалом. Вычислить сумму ряда
     */
    @SuppressWarnings("unused")
    public String thirteenthQuestion() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введите число: ");
        int x = scanner.nextInt(), result = 0;

        for (int i = 1; i < 6; i++) {
            result += (-1) * i * (x / BigIntegerMath.factorial(i).intValue());
        }

        scanner.close();

        return String.format("Результат 13 задания: %d", result);
    }

    /**
     * 14. Изменить порядок слов в строке на обратный.
     * Вводится строка, состоящая из слов, разделенных пробелами.
     * Следует заменить ее на строку, в которой слова идут в обратном порядке по сравнению с
     * исходной строкой. Вывести измененную строку на экран.
     */
    @SuppressWarnings("unused")
    public String fourteenthQuestion() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Введите строку:");
        // List.of - переделывает в интерфейс List, потом приходится вручную кастовать к ArrayList
        // Collections.swap просит изменяемый объект, что вполне логично, поэтому переделал к ArrayList.
        var src = new ArrayList<>(List.of(scanner.nextLine().split(" ")));
        var len = src.size();

        for (var i = 0; i <= (len / 2); i++)
            Collections.swap(src, len - i - 1, i);

        scanner.close();

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
    public String fifteenthQuestion() {
        return "";
    }

    /**
     * 16. Вычисление наибольших общих делителей.
     * Найти наибольшие общие делители (НОД) для множества пар чисел.
     */
    @SuppressWarnings("unused")
    public String sixteenthQuestion() {
        // Здесь будет использоваться алгоритм Штейна для нахождения НОД. Его сложность O(n^2/log(n)^2)
        // По сложности кажется, что он хуже Евклида O(log(min(a, b))), но он быстрее его за счет битовых сдвигов.
        Scanner scanner = new Scanner(System.in);
        System.out.println("Введите два числа через пробел: ");
        int a = scanner.nextInt(), b = scanner.nextInt();
        scanner.close();

        return String.format("Результат 16 задания: %s",
                "НОД: " + HelpMethods.algorithm_stein(a, b)
        );
    }


    /**
     * 17. Найти площади разных фигур. В зависимости от выбора пользователя вычислить площадь круга,
     * прямоугольника или треугольника. Для вычисления площади каждой фигуры должна быть написана
     * отдельная функция.
     */
    @SuppressWarnings("unused")
    public String seventeenthQuestion() {
        return "";
    }

    /**
     * 18.	Найти массив с максимальной суммой элементов.
     * Сгенерировать десять массивов из случайных чисел.
     * Вывести их и сумму их элементов на экран.
     * Найти среди них один с максимальной суммой элементов.
     * Указать какой он по счету, повторно вывести этот массив и сумму его элементов.
     * Заполнение массива и подсчет суммы его элементов оформить в виде отдельной функции.
     */
    @SuppressWarnings("unused")
    public String eighteenthQuestion() {
        return "";
    }

    /**
     * 19. Вычислить сумму элементов главной или побочной диагонали матрицы.
     * Дана квадратная матрица. Вычислить сумму элементов главной или побочной диагонали в зависимости от выбора пользователя. Сумма элементов любой диагонали должна вычисляться в одной и той же функции.
     */
    @SuppressWarnings("unused")
    public String nineteenthQuestion() {
        return "";
    }

    /**
     * 20. Функция перевода десятичного числа в двоичное.
     * Переводить в двоичную систему счисления вводимые в десятичной системе счисления числа до тех пор,
     * пока не будет введен 0. Для перевода десятичного числа в двоичное написать функцию.
     */
    @SuppressWarnings("unused")
    public String twentiethQuestion() {
        return "";
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
        return "";
    }

    /**
     * 22.	Функция заполнения массива случайными числами.
     * Написать функцию, которая заполняет массив случайными числами в диапазоне,
     * указанном пользователем.
     * Функция должна принимать два аргумента - начало диапазона и его конец, при этом ничего не возвращать.
     * Вывод значений элементов массива должен происходить в основной ветке программы.
     */
    @SuppressWarnings("unused")
    public String twentySecondQuestion() {
        return "";
    }

    /**
     * 23. Написать функцию вычисления величины силы тока на участке электрической
     * цепи сопротивлением R Ом при напряжении U В.
     */
    @SuppressWarnings("unused")
    public String twentyThirdQuestion() {
        return "";
    }

    /**
     * 24.	Написать функцию вычисления напряжения на каждом из последовательно
     * соединенных участков электрической цепи сопротивлением R1, R2, R3 Ом, если сила
     * тока при напряжении U В составляет I А.
     */
    @SuppressWarnings("unused")
    public String twentyFourthQuestion() {
        return "";
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



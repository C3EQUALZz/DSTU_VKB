/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package laboratories.firstdotfirstLaboratory;
// данная библиотека позволяет переводить числа в английские слова

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;
import java.util.Comparator;
import java.util.Locale;
import java.util.stream.Collectors;

public class Solution {
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {

        // Перевод в англ слова, второе взял из stackoverflow.
        RuleBasedNumberFormat numberFormat = new RuleBasedNumberFormat(Locale.UK, RuleBasedNumberFormat.SPELLOUT);

        Object result;

        System.out.print("Введите какое задание вы хотите выполнить: ");
        try {
            // получение значения метода из цифры, задавая ему правила.
            // Все вот эти штуки называются отражениями, здесь нет удобного аналога eval, как в Python.
            // Как бы говоря есть, но там под капотом JS, который не может работать с Java напрямую.
            var methodName = numberFormat.format(Solution.scanner.nextInt(), "%spellout-ordinal") + "Question";
            Method method = Solution.class.getMethod(methodName);
            result = method.invoke(new Solution());

        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            result = "Вы выбрали неверное задание";
        }

        System.out.println(result);
        scanner.close();
    }


    /**
     * 1. Ввести n строк с консоли, найти самую короткую строку. Вывести эту строку и ее длину.
     */
    @SuppressWarnings("unused")
    public String firstQuestion() {

        var stringWithMinimalLength = getDataFromConsole()
                .stream()
                .min(Comparator.comparing(String::length))
                .orElse("Вы не ввели строки для нахождения! ");

        return String.format("Результат 1 задания:\nМинимальная строка - %s с длиной: %d",
                stringWithMinimalLength, stringWithMinimalLength.length());
    }

    /**
     * 2. Ввести n строк с консоли.
     * Упорядочить и вывести строки в порядке возрастания их длин, а также (второй приоритет) значений этих их длин.
     */
    @SuppressWarnings("unused")
    public String secondQuestion() {
        // я не совсем понял "значений этих длин", мы изначально сортируем по длине, уже сравнивая значения
        // это в плане лексикографически что ли? Здесь это сделано
        return getDataFromConsole()
                .stream()
                .sorted(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()))
                .collect(Collectors.joining("\n"));
    }

    /**
     * 3. Ввести n строк с консоли. Вывести на консоль те строки, длина которых меньше средней, также их длины.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion() {
        var averageLength = getDataFromConsole().stream().mapToInt(String::length).average().orElseThrow();
        return getDataFromConsole()
                .stream()
                .filter(row -> row.length() > averageLength)
                .collect(Collectors.joining("\n"));
    }

    /**
     * 4. В каждом слове текста k-ю букву заменить заданным символом.
     * Если k больше длины слова, корректировку не выполнять.
     */
    @SuppressWarnings("unused")
    public String fourthQuestion() {
        return "";
    }

    /**
     * 5. В русском тексте каждую букву заменить ее номером в алфавите.
     * В одной строке печатать текст с двумя пробелами между буквами,
     * в следующей строке внизу под каждой буквой печатать ее номер.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion() {
        return "";
    }

    /**
     * 6. Из небольшого текста удалить все символы, кроме пробелов, не являющиеся буквами.
     * Между последовательностями подряд идущих букв оставить хотя бы один пробел.
     */
    @SuppressWarnings("unused")
    public String sixthQuestion() {
        return "";
    }

    /**
     * 7. Из текста удалить все слова заданной длины, начинающиеся на согласную букву.
     */
    @SuppressWarnings("unused")
    public String seventhQuestion() {
        return "";
    }

    /**
     * 8. В тексте найти все пары слов, из которых одно является обращением другого.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion() {
        return "";
    }

    /**
     * 9. Найти и напечатать, сколько раз повторяется в тексте каждое слово.
     */
    @SuppressWarnings("unused")
    public String ninthQuestion() {
        return "";
    }

    /**
     * 10. Найти, каких букв, гласных или согласных, больше в каждом предложении текста.
     */
    @SuppressWarnings("unused")
    public String tenthQuestion() {
        return "";
    }

    /**
     * 11. Выбрать три разные точки заданного на плоскости множества точек,
     * составляющие треугольник наибольшего периметра.
     */
    @SuppressWarnings("unused")
    public String eleventhQuestion() {
        return "";
    }

    /**
     * 12. Найти такую точку заданного на плоскости множества точек,
     * сумма расстояний от которой до остальных минимальна.
     */
    @SuppressWarnings("unused")
    public String twelfthQuestion() {
        return "";
    }

    /**
     * 13. Выпуклый многоугольник задан на плоскости перечислением координат вершин в порядке обхода его границы.
     * Определить площадь многоугольника.
     */
    @SuppressWarnings("unused")
    public String thirteenthQuestion() {
        return "";
    }

    private static List<String> getDataFromConsole() {
        // Создание списка в Java. Использование List вместо ArrayList в объявлении переменной — это пример принципа
        // программирования на уровне интерфейсов
        List<String> rowsFromConsole = new ArrayList<>();

        System.out.println("Вводите сколько хотите строк. Конец - это строка 'exit'");
        String row = Solution.scanner.nextLine().strip();

        while (!row.equalsIgnoreCase("exit")) {

            // есть ошибка, что пустая строка добавляется в самое начало, а потом слово
            // не совсем понимаю почему
            if (!row.isEmpty())
                rowsFromConsole.add(row);

            row = Solution.scanner.nextLine().strip();
        }

        return rowsFromConsole;
    }

}


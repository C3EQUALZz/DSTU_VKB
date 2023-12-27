/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package laboratories.firstdotfirstLaboratory;
// данная библиотека позволяет переводить числа в английские слова

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

import java.util.*;
import java.util.stream.Collectors;

public class Solution {

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
        var result = getDataFromConsole()
                .stream()
                .sorted(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()))
                .collect(Collectors.joining("\n"));

        return String.format("Результат 2 задания: %s", result);
    }

    /**
     * 3. Ввести n строк с консоли. Вывести на консоль те строки, длина которых меньше средней, также их длины.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion() {
        // Получаем среднюю длину, проходя по всему списку
        var averageLength = getDataFromConsole().stream().mapToInt(String::length).average().orElseThrow();
        // Собираем те предложения, которые больше по длине
        var result = getDataFromConsole()
                .stream()
                .filter(row -> row.length() > averageLength)
                .collect(Collectors.joining("\n"));

        return String.format("Результат 3 задания: %s", result);
    }

    /**
     * 4. В каждом слове текста k-ю букву заменить заданным символом.
     * Если k больше длины слова, корректировку не выполнять.
     */
    @SuppressWarnings("unused")
    public String fourthQuestion() {
        Scanner scanner = new Scanner(System.in);

        var sentences = getDataFromConsole();

        System.out.print("Введите индекс буквы, которую вы хотите заменить: ");
        var index = scanner.nextInt();

        System.out.print("Введите букву, на которую вы хотите поменять: ");
        var letter = scanner.next();

        scanner.close();

        var result = sentences
                .stream()
                .map(word -> new StringBuilder(word).replace(index, index + 1, letter))
                .collect(Collectors.joining("\n"));

        return String.format("Результат 4 задания:\n,%s", result);
    }

    /**
     * 5. В русском тексте каждую букву заменить ее номером в алфавите.
     * В одной строке печатать текст с двумя пробелами между буквами,
     * в следующей строке внизу под каждой буквой печатать ее номер.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion() {
        // Здесь я получаю символы.
        // Метод chars переделывает в итератор с кодами ASCII символов
        // получается аналог map(int.ord, symbol)
        // map отличается от mapToObj тем, что один переделывает в новый тип данных, а другой нет
        var symbols = String.join("", getDataFromConsole())
                .chars()
                .mapToObj(c -> (char) c)
                .map(c -> centerString(String.valueOf(c)))
                .collect(Collectors.joining(""));

        var unicodeValuesOfChars = symbols
                .chars()
                .filter(n -> n != 32)
                .mapToObj(c -> centerString(String.valueOf(c)))
                .collect(Collectors.joining(""));

        return String.format("Результат 5 задания:\n%s\n%s", symbols, unicodeValuesOfChars);
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
        Scanner scanner = new Scanner(System.in);
        // Создание списка в Java. Использование List вместо ArrayList в объявлении переменной — это пример принципа
        // программирования на уровне интерфейсов
        List<String> rowsFromConsole = new ArrayList<>();

        System.out.println("Вводите сколько хотите строк. Конец - это строка 'exit'");
        String row = scanner.nextLine().strip();

        while (!row.equalsIgnoreCase("exit")) {

            // есть ошибка, что пустая строка добавляется в самое начало, а потом слово
            // не совсем понимаю почему
            if (!row.isEmpty())
                rowsFromConsole.add(row);

            row = scanner.nextLine().strip();
        }
        scanner.close();

        return rowsFromConsole;
    }

    /**
     * Вспомогательный метод для центрирования строки
     *
     * @param s - наша строка, которую мы хотим центрировать
     * @return новая строка, которую отцентрировали
     */
    private static String centerString (String s) {
        return String.format("%-" + 5 + "s", String.format("%" + (s.length() + (5 - s.length()) / 2) + "s", s));
    }

}


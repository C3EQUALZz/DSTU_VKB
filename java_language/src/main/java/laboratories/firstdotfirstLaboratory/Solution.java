/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package laboratories.firstdotfirstLaboratory;
// данная библиотека позволяет переводить числа в английские слова

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

import java.util.*;
import java.util.regex.Matcher;
import java.util.stream.Collectors;
import java.util.regex.Pattern;
import java.util.stream.Stream;

import java.awt.Point;

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
    // аннотация с собакой - просто указание IDE, что не надо ругаться, что данные методы не используются
    // Здесь IDEA явно не видит запуск методов, он в main происходит для неё неявно

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
        // Каждый раз делаю новый сканер из-за моего запуска методов из-под нового экземпляра класса
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

        return String.format("Результат 4 задания:\n%s", result);
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

        var result = String.join(" ", getDataFromConsole())
                .chars()
                .filter(Character::isLetter)
                .mapToObj(number -> String.valueOf((char) number))
                .collect(Collectors.joining(" "));

        return String.format("Результат 6 задания:\n%s", result);
    }

    /**
     * 7. Из текста удалить все слова заданной длины, начинающиеся на согласную букву.
     */
    @SuppressWarnings("unused")
    public String seventhQuestion() {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите длину слов, которые вы хотите удалить: ");
        var length = scanner.nextInt();

        var result = getDataFromConsole()
                .stream()
                .filter(word -> !(word.length() == length &&
                        Pattern.matches("^[^aeiouAEIOUЙйУуЕеОоЭэИиЯяЫыАаЮю].*", word)))
                .collect(Collectors.joining(" "));
        return String.format("Результат 7 задания:\n%s", result);
    }

    /**
     * 8. В тексте найти все пары слов, из которых одно является обращением другого.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion() {
        StringBuilder result = new StringBuilder();

        System.out.println("Введите ваше предложение, где вы хотите искать слова и их обращения: ");
        // В консоли в одной строке могут ввести целое предложение, поэтому мы все объединяем, а потом смотрим на слова
        var sentence = String.join(" ", getDataFromConsole());

        for (var word : sentence.split(" ")) {
            // Разворачиваем слово. Я так понимаю в Java для взаимодействия со строками используется StringBuilder
            // Обычный String просто, как литералы что ли?
            var reversedWord = new StringBuilder(word).reverse().toString();
            // Создаем паттерн для поиска слов
            var pattern = Pattern.compile(String.format("%s", reversedWord));
            var matcher = pattern.matcher(sentence);
            if (matcher.find())
                result.append(String.format("Результат для поиска слова %s: ", word)).append(matcher.group()).append("\n");
        }
        return String.format("Результат 8 задания:\n%s", result);
    }

    /**
     * 9. Найти и напечатать, сколько раз повторяется в тексте каждое слово.
     */
    @SuppressWarnings("unused")
    public String ninthQuestion() {
        // Здесь мы собираем отдельные слова.
        // Например, пользователь ввел так:
        // привет как
        // дела
        // -> ["привет", "как", "дела"]
        var words = getDataFromConsole()
                .stream()
                .flatMap(word -> Arrays.stream(word.split("\\s+")))
                .toList();

        var sentence = String.join(" ", words);
        // Создание множества
        Set<String> result = new HashSet<>();

        for (var word : words) {
            // Поиск слов с помощью регулярного выражения, я сразу буду добавлять слово и количество
            result.add(
                    String.format("Слово: '%s' появляется %d раза в тексте",
                            word, findAll(sentence, String.format("\\b%s\\b", word)).size())
            );
        }

        return String.format("Результат 9 задания: \n%s", String.join("\n", result));
    }

    /**
     * 10. Найти, каких букв, гласных или согласных, больше в каждом предложении текста.
     */
    @SuppressWarnings("unused")
    public String tenthQuestion() {
        var result = new StringBuilder();
        // Пользователь в одной строке может ввести предложение с точкой, поэтому такой костыль
        var sentences = String.join(".", getDataFromConsole()).split("\\. ");

        for (String sentence : sentences) {
            var vowelsCount = countVowels(sentence);
            var consonantsCount = countConsonants(sentence);

            result.append(String.format("В предложении '%s' %s букв: гласных - %d, согласных - %d%n",
                    sentence, (vowelsCount > consonantsCount) ? "гласных больше" : "согласных больше",
                    vowelsCount, consonantsCount));
        }

        return String.format("Результат 10 задания: %s", result);
    }

    /**
     * 11. Выбрать три разные точки заданного на плоскости множества точек,
     * составляющие треугольник наибольшего периметра.
     * FIXME
     */
    @SuppressWarnings("unused")
    public String eleventhQuestion() {

        // Я не совсем понимаю почему streamApi код возвращает Object[], тут приходится вручную кастовать к (Point[])
        var points = (Point[]) getDataFromConsole().stream().map(cord -> {

            var pattern = Pattern.compile("(\\d+)");
            var matcher = pattern.matcher(cord);

            if (matcher.find()) {
                var coordinates = matcher.group(1).split(",");
                return new Point(Integer.parseInt(coordinates[0].strip()), Integer.parseInt(coordinates[1].strip()));
            }
            // Если код не найдет цифры, то следует явно указать, что возвращает null.
            // Видимо, в Java нет неявного возвращения null (None), как в Python.
            return null;
        }).toArray();


        List<Triangle> triangles = new ArrayList<>();
        // Как сделать за O(n^2) я за весь день и не придумал, очень тяжелая для этого задача
        for (int i = 0; i < points.length - 2; i++) {
            for (int j = i + 1; j < points.length - 1; j++) {
                for (int k = j + 1; k < points.length; k++) {
                    Triangle triangle = new Triangle(points[i], points[j], points[k]);
                    triangles.add(triangle);
                }
            }
        }

        // Найдите треугольник с максимальным периметром
        Triangle maxPerimeterTriangle = triangles.stream()
                .max(Comparator.comparingDouble(Triangle::getPerimeter))
                .orElse(null);


        assert maxPerimeterTriangle != null;

        return String.format(
                "Результат 11 задания:\nМаксимальный периметр: %f\nТочки: %s, %s, %s",
                maxPerimeterTriangle.getPerimeter(),
                maxPerimeterTriangle.getX(),
                maxPerimeterTriangle.getY(),
                maxPerimeterTriangle.getZ()
        );
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

    /**
     * Метод, с помощью которого мы получаем ввод пользователя с клавиатуры.
     * Здесь пользователь вводит до того момента, пока не введет exit.
     * @return список с содержимым, который ввел пользователь.
     */

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
            if (!row.isBlank())
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
    private static String centerString(String s) {
        return String.format("%-" + 5 + "s", String.format("%" + (s.length() + (5 - s.length()) / 2) + "s", s));
    }

    /**
     * В Java нет аналога re.findall из Python, поэтому написал своё, так сказать.
     */
    private static List<String> findAll(String sentence, String regex) {
        List<String> matches = new ArrayList<>();
        // Здесь флаги немного по-другому называются относительно Python, тут добавляю поддержку UNICODE и игнорирую регистр
        Pattern pattern = Pattern.compile(regex, Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CHARACTER_CLASS);
        Matcher matcher = pattern.matcher(sentence);

        while (matcher.find()) {
            matches.add(matcher.group());
        }

        return matches;
    }

    /**
     * Вспомогательный метод для подсчета количества гласных букв
     *
     * @param str строка, которую передал пользователь
     * @return количество гласных символов
     */

    private static long countVowels(String str) {
        Set<Character> vowels = Stream.of('а', 'о', 'у', 'ы', 'э', 'е', 'ё', 'и', 'ю', 'я',
                'a', 'e', 'i', 'o', 'u').collect(Collectors.toSet());
        //Locale.ROOT представляет собой константу в классе Locale в Java, предназначенную для представления
        // нейтральной локали.
        // Нейтральная локаль означает отсутствие спецификации конкретного региона, языка или варианта.
        return str.toLowerCase(Locale.ROOT).chars()
                .mapToObj(c -> (char) c)
                .filter(vowels::contains)
                .count();
    }

    /**
     * Вспомогательный метод для нахождения количества согласных букв
     *
     * @param str Строка, которую передал наш пользователь.
     * @return Возвращает количество согласных букв.
     */
    private static long countConsonants(String str) {
        return str.toLowerCase(Locale.ROOT).chars()
                .mapToObj(c -> (char) c)
                .filter(c -> Character.isLetter(c) && countVowels(String.valueOf(c)) != 1)
                .count();
    }

}


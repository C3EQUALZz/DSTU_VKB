/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package programmingLanguagesJava.laboratories.firstdotfirstLaboratory;
// данная библиотека позволяет переводить числа в английские слова

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.awt.*;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.List;
import java.util.*;
import java.util.regex.Pattern;
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
    // аннотация с собакой - просто указание IDE, что не надо ругаться, что данные методы не используются
    // Здесь IDEA явно не видит запуск методов, он в main происходит для неё неявно

    /**
     * 1. Ввести n строк с консоли, найти самую короткую строку. Вывести эту строку и ее длину.
     */
    @SuppressWarnings("unused")
    public String firstQuestion() {

        var stringWithMinimalLength = HelpMethods.getDataFromConsole()
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
        var result = HelpMethods.getDataFromConsole()
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
        var averageLength = HelpMethods.getDataFromConsole().stream().mapToInt(String::length).average().orElseThrow();
        // Собираем те предложения, которые больше по длине
        var result = HelpMethods.getDataFromConsole()
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

        var sentences = HelpMethods.getDataFromConsole();

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
        var symbols = String.join("", HelpMethods.getDataFromConsole())
                .chars()
                .mapToObj(c -> (char) c)
                .map(c -> HelpMethods.centerString(String.valueOf(c)))
                .collect(Collectors.joining(""));

        var unicodeValuesOfChars = symbols
                .chars()
                .filter(n -> n != 32)
                .mapToObj(c -> HelpMethods.centerString(String.valueOf(c)))
                .collect(Collectors.joining(""));

        return String.format("Результат 5 задания:\n%s\n%s", symbols, unicodeValuesOfChars);
    }

    /**
     * 6. Из небольшого текста удалить все символы, кроме пробелов, не являющиеся буквами.
     * Между последовательностями подряд идущих букв оставить хотя бы один пробел.
     */
    @SuppressWarnings("unused")
    public String sixthQuestion() {

        var result = String.join(" ", HelpMethods.getDataFromConsole())
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

        var result = HelpMethods.getDataFromConsole()
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
        var sentence = String.join(" ", HelpMethods.getDataFromConsole());

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
        var words = HelpMethods.getDataFromConsole()
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
                            word, HelpMethods.findAll(sentence, String.format("\\b%s\\b", word)).size())
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
        var sentences = String.join(".", HelpMethods.getDataFromConsole()).split("\\. ");

        for (String sentence : sentences) {
            var vowelsCount = HelpMethods.countVowels(sentence);
            var consonantsCount = HelpMethods.countConsonants(sentence);

            result.append(String.format("В предложении '%s' %s букв: гласных - %d, согласных - %d%n",
                    sentence, (vowelsCount > consonantsCount) ? "гласных больше" : "согласных больше",
                    vowelsCount, consonantsCount));
        }

        return String.format("Результат 10 задания: %s", result);
    }

    /**
     * 11. Выбрать три разные точки заданного на плоскости множества точек,
     * составляющие треугольник наибольшего периметра.
     */
    @SuppressWarnings("unused")
    public String eleventhQuestion() {

        // Я не совсем понимаю почему streamApi код возвращает Object[], тут приходится вручную кастовать к (Point[])
        var points = HelpMethods.getDataFromConsole().stream().map(cord -> {

            var pattern = Pattern.compile("\\(?\\d+, \\d+\\)?");
            var matcher = pattern.matcher(cord);

            if (matcher.find()) {
                var coordinates = matcher
                        .group(0)
                        .replace("(", "")
                        .replace(")", "")
                        .split(",");

                return new Point(Integer.parseInt(coordinates[0].strip()), Integer.parseInt(coordinates[1].strip()));
            }
            // Если код не найдет цифры, то следует явно указать, что возвращает null.
            // Видимо, в Java нет неявного возвращения null (None), как в Python.
            return null;
        }).toArray();


        List<Triangle> triangles = HelpMethods.getTriangleList(points);

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
        var points = HelpMethods.getDataFromConsole().stream().map(cord -> {

            var pattern = Pattern.compile("\\(?\\d+, \\d+\\)?");
            var matcher = pattern.matcher(cord);

            if (matcher.find()) {
                var coordinates = matcher
                        .group(0)
                        .replace("(", "")
                        .replace(")", "")
                        .split(",");

                return new Point(Integer.parseInt(coordinates[0].strip()), Integer.parseInt(coordinates[1].strip()));
            }
            // Если код не найдет цифры, то следует явно указать, что возвращает null.
            // Видимо, в Java нет неявного возвращения null (None), как в Python.
            return null;
        }).toArray();


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
}


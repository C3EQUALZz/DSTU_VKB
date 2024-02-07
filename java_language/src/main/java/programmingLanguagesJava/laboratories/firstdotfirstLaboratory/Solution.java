/**
 * Автор: Данил Ковалев ВКБ22 Вариант -
 */
package programmingLanguagesJava.laboratories.firstdotfirstLaboratory;

import programmingLanguagesJava.laboratories.ConsoleReader;

import java.awt.*;
import java.util.List;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Solution {

    static String text = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et 
            dolore magna aliqua. Pellentesque adipiscing commodo elit at. Scelerisque purus semper eget duis. Purus
            sit amet volutpat consequat mauris nunc congue nisi vitae. Quis hendrerit dolor magna eget est lorem 
            ipsum. Molestie ac feugiat sed lectus vestibulum. Massa tincidunt dui ut ornare lectus sit. Sed 
            ullamcorper morbi tincidunt ornare massa eget egestas. In ornare quam viverra orci sagittis eu.
            Mauris rhoncus aenean vel elit. Sed arcu non odio euismod lacinia. Auctor augue mauris augue neque.
             Eleifend mi in nulla posuere sollicitudin aliquam
            """;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введите номер задания: ");
        var question = scanner.nextInt();

        System.out.printf("---------------------------------------------------\nРезультат %d задания:\n", question);

        Object result = switch (question) {
            case 1, 2, 3, 5, 6, 9 ->
                    ConsoleReader.executeTask(Solution.class, String.valueOf(question), HelpMethods.getDataFromConsole());

            case 4 -> {
                System.out.print("Введите индекс буквы, которую вы хотите заменить: ");
                var index = scanner.next();

                System.out.print("Введите букву, на которую вы хотите поменять: ");
                var letter = scanner.next();

                yield fourthQuestion(index + " " + letter);
            }

            case 7 -> {
                System.out.print("Введите длину слов, которые вы хотите убрать (одно число): ");
                yield seventhQuestion(scanner.next());
            }

            case 8, 10 -> {
                System.out.println("Введите ваше предложение (Пишите предложения с точками!) ");
                scanner.nextLine();
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.nextLine());
            }

            case 11, 12, 13 -> {
                System.out.println("Вводите координаты по такому шаблону (3, 5): ");
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), HelpMethods.getDataFromConsole());
            }

            default -> "Вы выбрали неверное задание";
        };

        scanner.close();
        System.out.println(result);

    }
    // аннотация с собакой - просто указание IDE, что не надо ругаться, что данные методы не используются
    // Здесь IDEA явно не видит запуск методов, он в main происходит для неё неявно

    /**
     * 1. Ввести n строк с консоли, найти самую короткую строку. Вывести эту строку и ее длину.
     */
    @SuppressWarnings("unused")
    public static String firstQuestion(String strings) {

        var stringWithMinimalLength = Arrays.stream(strings.split("\\s+"))
                .min(Comparator.comparing(String::length))
                .orElse("Вы не ввели строки для нахождения! ");

        return String.format("Минимальная строка - %s\nДлина самой короткой строки: %d",
                stringWithMinimalLength, stringWithMinimalLength.length());
    }

    /**
     * 2. Ввести n строк с консоли.
     * Упорядочить и вывести строки в порядке возрастания их длин, а также (второй приоритет) значений этих их длин.
     */
    @SuppressWarnings("unused")
    public static String secondQuestion(String strings) {
        // я не совсем понял "значений этих длин", мы изначально сортируем по длине, уже сравнивая значения
        // это в плане лексикографически что ли? Здесь это сделано
        var result = Arrays.stream(strings.split("\\s+"))
                .sorted(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()))
                .collect(Collectors.joining("\n"));

        return String.format("Отсортированные строки по длине:\n%s", result);
    }

    /**
     * 3. Ввести n строк с консоли. Вывести на консоль те строки, длина которых меньше средней, также их длины.
     */
    @SuppressWarnings("unused")
    public static String thirdQuestion(String strings) {
        var splitStrings = strings.split("\\s+");

        // Получаем среднюю длину, проходя по всему списку
        var averageLength = Arrays.stream(splitStrings).mapToInt(String::length).average().orElseThrow();

        // Собираем те предложения, которые больше по длине
        var result = Arrays.stream(splitStrings)
                .filter(row -> row.length() > averageLength)
                .collect(Collectors.joining("\n"));

        return String.format("Строки, длины которых меньше средней: %s", result);
    }

    /**
     * 4. В каждом слове текста k-ю букву заменить заданным символом.
     * Если k больше длины слова, корректировку не выполнять.
     */
    @SuppressWarnings("unused")
    public static String fourthQuestion(String strings) {

        var letterAndIndex = strings.split("\\s+");

        var index = Integer.parseInt(letterAndIndex[0]);
        var letter = letterAndIndex[1];

        // 2 split'а с той целью, чтобы сохранить паттерн текста и не выводит все в одну строку для удобства чтения.
        var result = Arrays.stream(Solution.text.split("\n"))
                .map(line -> Arrays.stream(line.split("\\s+"))
                        .map(word -> {

                            if (index >= 0 && index < word.length())
                                return new StringBuilder(word).replace(index, index + 1, letter).toString();
                            else
                                return word; // Возвращаем слово без изменений, если индекс вне диапазона


                        })
                        .collect(Collectors.joining(" ")))
                .collect(Collectors.joining("\n"));

        return String.format("Текст, в котором каждый %d поменяли на букву %s:\n%s", index + 1, letter, result);
    }

    /**
     * 5. В русском тексте каждую букву заменить ее номером в алфавите.
     * В одной строке печатать текст с двумя пробелами между буквами,
     * в следующей строке внизу под каждой буквой печатать ее номер.
     */
    @SuppressWarnings("unused")
    public static String fifthQuestion(String strings) {
        // Здесь я получаю символы.
        // Метод chars переделывает в итератор с кодами ASCII символов
        // получается аналог map(int.ord, symbol)
        // map отличается от mapToObj тем, что один переделывает в новый тип данных, а другой нет
        var symbols = String.join("", strings.split("\\s+")).chars()
                .mapToObj(c -> (char) c)
                .map(c -> HelpMethods.centerString(String.valueOf(c)))
                .collect(Collectors.joining(""));

        var unicodeValuesOfChars = symbols.chars()
                .filter(n -> n != 32)
                .mapToObj(c -> HelpMethods.centerString(String.valueOf(c)))
                .collect(Collectors.joining(""));

        return String.format("%s\n%s", symbols, unicodeValuesOfChars);
    }

    /**
     * 6. Из небольшого текста удалить все символы, кроме пробелов, не являющиеся буквами.
     * Между последовательностями подряд идущих букв оставить хотя бы один пробел.
     */
    @SuppressWarnings("unused")
    public static String sixthQuestion(String strings) {
        return String.format(
                "После удаления всех не нужных символов:\n%s",
                strings.replaceAll("[^A-Za-zа-яА-Я\\s]", "")
        );
    }

    /**
     * 7. Из текста удалить все слова заданной длины, начинающиеся на согласную букву.
     */
    @SuppressWarnings("unused")
    public static String seventhQuestion(String lengthStr) {

        var result = Arrays.stream(Solution.text.split("\n"))

                .map(line -> Arrays.stream(line.split("\\s+"))

                        .filter(word -> !(word.length() == Integer.parseInt(lengthStr) &&
                                Pattern.matches("^[^aeiouAEIOUЙйУуЕеОоЭэИиЯяЫыАаЮю].*", word)))

                        .collect(Collectors.joining(" ")))
                .collect(Collectors.joining("\n"));

        return String.format("Текст после удаления слов с длиной равной %s\n%s", lengthStr, result);
    }

    /**
     * 8. В тексте найти все пары слов, из которых одно является обращением другого.
     */
    @SuppressWarnings("unused")
    public static String eighthQuestion(String string) {

        var result = new StringBuilder();

        for (var word : string.split(" ")) {
            var reversedWord = new StringBuilder(word).reverse().toString();
            // Создаем паттерн для поиска слов
            var pattern = Pattern.compile(reversedWord);
            var matcher = pattern.matcher(string);
            if (matcher.find())
                result.append(String.format("Результат для поиска слова %s: ", word)).append(matcher.group()).append("\n");
        }

        return String.format("\n%s", result);
    }

    /**
     * 9. Найти и напечатать, сколько раз повторяется в тексте каждое слово.
     */
    @SuppressWarnings("unused")
    public String ninthQuestion(String strings) {
        // Здесь мы собираем отдельные слова.
        // Например, пользователь ввел так:
        // привет как
        // дела
        // -> ["привет", "как", "дела"]
        var words = Arrays.stream(strings.split("\\s+"))
                .flatMap(word -> Arrays.stream(word.split("\\s+")))
                .toList();

        var sentence = String.join(" ", words);

        var result = new HashSet<String>();

        words.forEach(word ->
                result.add(
                        String.format("Слово: '%s' появляется %d раза в тексте",
                                word,
                                HelpMethods.findAll(sentence, String.format("\\b%s\\b", word)).size())
                ));

        return String.format("Содержимое множества:\n%s", String.join("\n", result));
    }

    /**
     * 10. Найти, каких букв, гласных или согласных, больше в каждом предложении текста.
     */
    @SuppressWarnings("unused")
    public static String tenthQuestion(String strings) {
        var result = new StringBuilder();

        Arrays.stream(strings.split("[.?!]\\s+")).forEach(sentence -> {

            var vowelsCount = HelpMethods.countVowels(sentence);
            var consonantsCount = HelpMethods.countConsonants(sentence);

            result.append(String.format("В предложении '%s' %s букв: гласных - %d, согласных - %d%n",
                    sentence, (vowelsCount > consonantsCount) ? "гласных больше" : "согласных больше",
                    vowelsCount, consonantsCount));

        });

        return String.format("Мои подсчеты: %s", result);
    }

    /**
     * 11. Выбрать три разные точки заданного на плоскости множества точек,
     * составляющие треугольник наибольшего периметра.
     */
    @SuppressWarnings("unused")
    public static String eleventhQuestion(String strings) {

        // Я не совсем понимаю почему streamApi код возвращает Object[], тут приходится вручную кастовать к (Point[])
        var points = HelpMethods.cordsFromConsole(strings).toArray();

        List<Triangle> triangles = HelpMethods.getTriangleList(points);

        // Найдите треугольник с максимальным периметром
        Triangle maxPerimeterTriangle = triangles.stream()
                .max(Comparator.comparingDouble(Triangle::getPerimeter))
                .orElse(null);


        assert maxPerimeterTriangle != null;

        return String.format(
                "Максимальный периметр: %f\nТочки: %s, %s, %s",
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
    public static String twelfthQuestion(String strings) {
        var points = HelpMethods.cordsFromConsole(strings).toList();

        double minSum = Double.MAX_VALUE;
        Point minPoint = null;

        for (Point point : points) {
            double sum = 0;
            for (Point other : points) {
                if (!point.equals(other))
                    sum += Math.hypot(point.x - other.x, point.y - other.y);
            }

            if (sum < minSum) {
                minSum = sum;
                minPoint = point;
            }

        }

        assert minPoint != null;
        return String.format("Точка, где расстояние минимально: (%d, %d) ", minPoint.x, minPoint.y);
    }

    /**
     * 13. Выпуклый многоугольник задан на плоскости перечислением координат вершин в порядке обхода его границы.
     * Определить площадь многоугольника.
     */
    @SuppressWarnings("unused")
    public static String thirteenthQuestion(String strings) {
        var points = HelpMethods.cordsFromConsole(strings).toList();
        // https://www.mathopenref.com/coordpolygonarea.html
        int countPoints = points.size();
        double sum = 0;
        for (int i = 0; i < countPoints; i += 1)

            sum += points.get(i).x * points.get((i + 1) % countPoints).y -
                    points.get((i + 1) % countPoints).x * points.get(i).y;

        return String.format("Площадь многоугольника: %f", Math.abs(sum / 2.0));
    }
}
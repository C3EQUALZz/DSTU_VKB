package programmingLanguagesJava.laboratories.firstdotfirstLaboratory;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class HelpMethods {
    /**
     * Вспомогательный метод для центрирования строки
     *
     * @param s - наша строка, которую мы хотим центрировать
     * @return новая строка, которую отцентрировали
     */
    public static String centerString(String s) {
        return String.format("%-" + 5 + "s", String.format("%" + (s.length() + (5 - s.length()) / 2) + "s", s));
    }

    /**
     * Вспомогательный метод для нахождения количества согласных букв
     *
     * @param str Строка, которую передал наш пользователь.
     * @return Возвращает количество согласных букв.
     */
    public static long countConsonants(String str) {
        return str.toLowerCase(Locale.ROOT).chars()
                .mapToObj(c -> (char) c)
                .filter(c -> Character.isLetter(c) && countVowels(String.valueOf(c)) != 1)
                .count();
    }

    /**
     * Вспомогательный метод для подсчета количества гласных букв
     *
     * @param str строка, которую передал пользователь
     * @return количество гласных символов
     */

    public static long countVowels(String str) {
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
     * В Java нет аналога re.findall из Python, поэтому написал своё, так сказать.
     */
    public static List<String> findAll(String sentence, String regex) {
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
     * Метод, с помощью которого мы получаем ввод пользователя с клавиатуры.
     * Здесь пользователь вводит до того момента, пока не введет exit.
     * @return список с содержимым, который ввел пользователь.
     */

    public static List<String> getDataFromConsole() {
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
}

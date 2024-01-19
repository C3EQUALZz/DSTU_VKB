package programmingLanguagesJava.laboratories.thirdLaboratory;


import programmingLanguagesJava.laboratories.ConsoleReader;
import programmingLanguagesJava.laboratories.firstdotfirstLaboratory.HelpMethods;

import java.util.*;
import java.util.stream.Collectors;

public class Solution {
    public static void main(String[] args) {
        System.out.println(ConsoleReader.executeTask(Solution.class));
    }

    /**
     * 1. Ввести n строк с консоли, найти самую короткую и самую длинную строки. Вывести найденные строки и их длину.
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
     * 2. Ввести n строк с консоли. Упорядочить и вывести строки в порядке возрастания (убывания) значений их длины.
     */
    @SuppressWarnings("unused")
    public String secondQuestion() {
        var strings = HelpMethods.getDataFromConsole()
                .stream()
                .sorted(Comparator.comparing(String::length))
                .collect(Collectors.joining("\n"));
        return String.format("Результат 2 задания:\n%s", strings);
    }

    /**
     * 3. Ввести n строк с консоли. Вывести на консоль те строки, длина которых меньше (больше) средней, а также длину.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion() {
        // Наш список со строками, которые ввел пользователь
        var ListStrings = HelpMethods.getDataFromConsole();
        // Находим среднюю длину строк
        var averageLength = ListStrings.stream().mapToInt(String::length).average().orElseThrow();
        // Решил сделать так, а не через StreamApi, чтобы за один проход расположить элементы по контейнерам.
        // В одном случае сложность O(n), а в другом O(2*n), но 2 не учитывается как мы помним, но уже поступил так.
        var stringThatAreLonger = new StringBuilder(String.format("Строки, которые больше по длине, чем %f", averageLength));
        var stringWhereLengthLessAverage = new StringBuilder(String.format("Строки, которые меньше по длине, чем %f", averageLength));

        for (var row: ListStrings) {
            if (row.length() >= averageLength)
                stringThatAreLonger.append(String.format("\n%s", row));
            else
                stringWhereLengthLessAverage.append(String.format("\n%s", row));
        }
        return String.format("Результат 13 задания:\n%s\n%s", stringWhereLengthLessAverage, stringThatAreLonger);
    }

    /**
     * 4. Ввести n слов с консоли. Найти слово, в котором число различных символов минимально.
     * Если таких слов несколько, найти первое из них.
     */
    @SuppressWarnings("unused")
    public String fourthQuestion() {
        var ListWithRows = HelpMethods.getDataFromConsole();

        int minLenSymbols = Integer.MAX_VALUE;
        String wordWithMaxLength = "";

        for(var word: ListWithRows) {
            // c помощью StreamApi мы можем перевести в массив char-ов, тут встроенные методы, чтобы находить
            // вывести разные элементы, в конце подсчитываем их просто (почему нельзя было назвать size, как другие
            // коллекции? Java странный язык...)
            var wordLength = word.chars().mapToObj(i->(char)i).distinct().count();

            if (wordLength < minLenSymbols) {
                minLenSymbols = (int) wordLength;
                wordWithMaxLength = word;
            }

        }
        return String.format
                (
                        "Результат 4 задания: слово - %s, с количеством разных символов - %d",
                        wordWithMaxLength,
                        minLenSymbols
                );
    }

    /**
     * 5. Ввести n слов с консоли. Найти количество слов, содержащих только символы латинского алфавита,
     * а среди них – количество слов с равным числом гласных и согласных букв.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion() {
        var result = HelpMethods.getDataFromConsole()
                        .stream()
                        .filter(word -> word.matches("^[a-zA-Z0-9]+$"))
                        .filter(word -> {
                            var countConsonants = word.replaceAll("(?i)[^aeiouy]", "").length();
                            var countVowels = word.length() - countConsonants;
                            return countVowels == countConsonants;
                        })
                        .count();

        return String.format("Результат 5 задания: %d", result);
    }

    /**
     * 6. Ввести n слов с консоли. Найти слово, символы в котором идут в строгом порядке возрастания их кодов.
     * Если таких слов несколько, найти первое из них.
     */
    @SuppressWarnings("unused")
    public String sixthQuestion() {
        var result = HelpMethods.getDataFromConsole()
                .stream()
                .filter(word -> word.chars().sorted()
                        /*
                        Метод collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
                        используется для преобразования потока кодовых точек символов обратно в строку. Вот что делает
                        каждый из аргументов этого метода:
                        StringBuilder::new - это функция, которая создает новый экземпляр StringBuilder.
                         Это используется как начальное значение для аккумулятора.
                        StringBuilder::appendCodePoint - это функция, которая принимает текущее значение аккумулятора
                         (в данном случае, StringBuilder) и элемент потока (кодовую точку символа), и добавляет символ,
                          соответствующий кодовой точке, в StringBuilder.
                        StringBuilder::append - это функция, которая используется для объединения двух StringBuilder
                         в одну строку при параллельном выполнении потока. В данном случае, она используется для
                          объединения частей строки, созданных в разных потоках.
                         */
                        .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
                        .toString().equals(word))
                .findFirst()
                .orElse("Нет такой строки");

        return String.format("Результат 6 задания: %s", result);
    }

    /**
     * 7. Ввести n слов с консоли. Найти слово, состоящее только из различных символов.
     * Если таких слов несколько, найти первое из них.
     */
    @SuppressWarnings("unused")
    public String seventhQuestion() {
        var result = HelpMethods.getDataFromConsole();
        return "";
    }

    /**
     * 8. Ввести n слов с консоли. Среди слов, состоящих только из цифр, найти слово-палиндром.
     * Если таких слов больше одного, найти второе из них.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion() {
        return "";
    }

    /**
     * 9. Написать программы решения задач 1–8, осуществляя ввод строк как аргументов командной строки.
     */
    @SuppressWarnings("unused")
    public String ninthQuestion() {
        return "";
    }

    /**
     * 10. Введите одно из заданий, которые представлены ниже.
     * А) Напишите метод, который принимает в качестве параметра любую строку, например “I like Java!!!”.
     * Б) Распечатать последний символ строки. Используем метод String.charAt().
     * В) Проверить, заканчивается ли ваша строка подстрокой “!!!”. Используем метод String.endsWith().
     * Г) Проверить, начинается ли ваша строка подстрокой “I like”. Используем метод String.startsWith().
     * Д) Проверить, содержит ли ваша строка подстроку “Java”. Используем метод String.contains().
     * Е) Найти позицию подстроки “Java” в строке “I like Java!!!”.
     * Ж) Заменить все символы “а” на “о”.
     * З) Преобразуйте строку к верхнему регистру.
     * И) Преобразуйте строку к нижнему регистру.
     * К) Вырезать строку Java c помощью метода String.substring().
     */
    @SuppressWarnings("unused")
    public String tenthQuestion() {
        return "";
    }

    /**
     * 11.
     * А) Дано два числа, например 3 и 56, необходимо составить следующие строки:
     * 3 + 56 = 59
     * 3 – 56 = -53
     * 3 * 56 = 168.
     * Используем метод StringBuilder.append().
     * Б) Замените символ “=” на слово “равно”. Используйте методы StringBuilder.insert(), StringBuilder.deleteCharAt().
     * В) Замените символ “=” на слово “равно”. Используйте методы StringBuilder.replace().
     */
    @SuppressWarnings("unused")
    public String eleventhQuestion() {
        return "";
    }

    /**
     * 12. Напишите метод, заменяющий в строке каждое второе вхождение «object-oriented programming»
     * (не учитываем регистр символов) на «OOP». Например, строка "Object-oriented programming is a programming
     * language model organized around objects rather than "actions" and data rather than logic.
     * Object-oriented programming blabla. Object-oriented programming bla."должна быть преобразована в
     * "Object-oriented programming is a programming language model organized around objects rather than "actions" and
     * data rather than logic. OOP blabla.Object-oriented programming bla."
     */
    @SuppressWarnings("unused")
    public String twelfthQuestion() {
        return "";
    }

    /**
     * 13. Даны строки разной длины (длина - четное число), необходимо вернуть ее два средних знака: "string" → "ri",
     * "code" → "od", "Practice"→"ct".
     */
    @SuppressWarnings("unused")
    public String thirteenthQuestion() {
        return "";
    }

    /**
     * 14. Создать строку, используя форматирование: Студент [Фамилия] получил [оценка] по [предмету].
     * Форматирование и вывод строки на консоль написать в отдельном методе, который принимает фамилию,
     * оценку и название предмета в качестве параметров.
     * Выделить под фамилию 15 символов, под оценку 3 символа, предмет – 10.
     */
    @SuppressWarnings("unused")
    public String fourteenthQuestion() {
        return "";
    }

    /**
     * 15. Дана строка “Versions: Java 5, Java 6, Java 7, Java 8, Java 12.”.
     * Найти все подстроки "Java X" и распечатать их.
     */
    @SuppressWarnings("unused")
    public String fifteenthQuestion() {
        return "";
    }

    /**
     * 16. Найти слово, в котором число различных символов минимально.
     * Слово может содержать буквы и цифры. Если таких слов несколько, найти первое из них.
     * Например, в строке "fffff ab f 1234 jkjk" найденное слово должно быть "fffff".
     */
    @SuppressWarnings("unused")
    public String sixteenthQuestion() {
        return "";
    }

    /**
     * 17. Предложение состоит из нескольких слов, разделенных пробелами.
     * Например: "One two three раз два три one1 two2 123 ".
     * Найти количество слов, содержащих только символы латинского алфавита.
     */
    @SuppressWarnings("unused")
    public String seventeenthQuestion() {
        return "";
    }

    /**
     * 18. Предложение состоит из нескольких слов, например: "Если есть хвосты по дз, начните с 1 не сданного задания.
     * 123 324 111 4554". Среди слов, состоящих только из цифр, найти слово палиндром.
     */
    @SuppressWarnings("unused")
    public String eighteenthQuestion() {
        return "";
    }


}

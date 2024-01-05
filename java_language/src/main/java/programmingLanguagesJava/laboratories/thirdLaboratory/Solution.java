package programmingLanguagesJava.laboratories.thirdLaboratory;

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Locale;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
     * 1. Ввести n строк с консоли, найти самую короткую и самую длинную строки. Вывести найденные строки и их длину.
     */
    @SuppressWarnings("unused")
    public String firstQuestion() {return "";}

    /**
     * 2. Ввести n строк с консоли. Упорядочить и вывести строки в порядке возрастания (убывания) значений их длины.
     */
    @SuppressWarnings("unused")
    public String secondQuestion() {return "";}

    /**
     * 3. Ввести n строк с консоли. Вывести на консоль те строки, длина которых меньше (больше) средней, а также длину.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion() {return "";}

    /**
     * 4. Ввести n слов с консоли. Найти слово, в котором число различных символов минимально.
     * Если таких слов несколько, найти первое из них.
     */
    @SuppressWarnings("unused")
    public String fourthQuestion() {return "";}

    /**
     * 5. Ввести n слов с консоли. Найти количество слов, содержащих только символы латинского алфавита,
     * а среди них – количество слов с равным числом гласных и согласных букв.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion() {return "";}

    /**
     * 6. Ввести n слов с консоли. Найти слово, символы в котором идут в строгом порядке возрастания их кодов.
     * Если таких слов несколько, найти первое из них.
     */
    @SuppressWarnings("unused")
    public String sixthQuestion() {return "";}

    /**
     * 7. Ввести n слов с консоли. Найти слово, состоящее только из различных символов.
     * Если таких слов несколько, найти первое из них.
     */
    @SuppressWarnings("unused")
    public String seventhQuestion() {return "";}

    /**
     * 8. Ввести n слов с консоли. Среди слов, состоящих только из цифр, найти слово-палиндром.
     * Если таких слов больше одного, найти второе из них.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion() {return "";}

    /**
     * 9. Написать программы решения задач 1–8, осуществляя ввод строк как аргументов командной строки.
     */
    @SuppressWarnings("unused")
    public String ninthQuestion() {return "";}

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
    public String tenthQuestion() {return "";}

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
    public String eleventhQuestion() {return "";}

    /**
     * 12. Напишите метод, заменяющий в строке каждое второе вхождение «object-oriented programming»
     * (не учитываем регистр символов) на «OOP». Например, строка "Object-oriented programming is a programming
     * language model organized around objects rather than "actions" and data rather than logic.
     * Object-oriented programming blabla. Object-oriented programming bla."должна быть преобразована в
     * "Object-oriented programming is a programming language model organized around objects rather than "actions" and
     * data rather than logic. OOP blabla.Object-oriented programming bla."
     */
    @SuppressWarnings("unused")
    public String twelfthQuestion() {return "";}

    /**
     * 13. Даны строки разной длины (длина - четное число), необходимо вернуть ее два средних знака: "string" → "ri",
     * "code" → "od", "Practice"→"ct".
     */
    @SuppressWarnings("unused")
    public String thirteenthQuestion() {return "";}

    /**
     * 14. Создать строку, используя форматирование: Студент [Фамилия] получил [оценка] по [предмету].
     * Форматирование и вывод строки на консоль написать в отдельном методе, который принимает фамилию,
     * оценку и название предмета в качестве параметров.
     * Выделить под фамилию 15 символов, под оценку 3 символа, предмет – 10.
     */
    @SuppressWarnings("unused")
    public String fourteenthQuestion() {return "";}

    /**
     * 15. Дана строка “Versions: Java 5, Java 6, Java 7, Java 8, Java 12.”.
     * Найти все подстроки "Java X" и распечатать их.
     */
    @SuppressWarnings("unused")
    public String fifteenthQuestion() {return "";}

    /**
     * 16. Найти слово, в котором число различных символов минимально.
     * Слово может содержать буквы и цифры. Если таких слов несколько, найти первое из них.
     * Например, в строке "fffff ab f 1234 jkjk" найденное слово должно быть "fffff".
     */
    @SuppressWarnings("unused")
    public String sixteenthQuestion() {return "";}

    /**
     * 17. Предложение состоит из нескольких слов, разделенных пробелами.
     * Например: "One two three раз два три one1 two2 123 ".
     * Найти количество слов, содержащих только символы латинского алфавита.
     */
    @SuppressWarnings("unused")
    public String seventeenthQuestion() {return "";}

    /**
     * 18. Предложение состоит из нескольких слов, например: "Если есть хвосты по дз, начните с 1 не сданного задания.
     * 123 324 111 4554". Среди слов, состоящих только из цифр, найти слово палиндром.
     */
    @SuppressWarnings("unused")
    public String eighteenthQuestion() {return "";}


}

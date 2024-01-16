package programmingLanguagesJava.laboratories;

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Locale;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ConsoleReader {
    private static final Scanner scanner = new Scanner(System.in);
    // Перевод в англ слова, второе взял из stackoverflow.
    private static final RuleBasedNumberFormat numberFormat = new RuleBasedNumberFormat(Locale.UK, RuleBasedNumberFormat.SPELLOUT);

    public static Object executeTask(Class<?> solutionClass) {
        System.out.print("Введите какое задание хотите выполнить: ");
        try {
            // Получение значения метода из цифры, задавая ему правила.
            // Все вот эти штуки называются отражениями, здесь нет удобного аналога eval, как в Python.
            // Как бы говоря есть, но там под капотом JS, который не может работать с Java напрямую.
            var methodName = numberFormat.format(scanner.nextInt(), "%spellout-ordinal") + "Question";
            // В случае больше двадцати methodName может вернуть типа: twenty-first
            Pattern pattern = Pattern.compile("-(\\w)");
            Matcher matcher = pattern.matcher(methodName);

            StringBuilder str = new StringBuilder();

            while (matcher.find()) {
                matcher.appendReplacement(str, matcher.group(1).toUpperCase());
            }
            matcher.appendTail(str);

            Method method = solutionClass.getMethod(str.toString());
            return method.invoke(solutionClass.getDeclaredConstructor().newInstance());
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException | InstantiationException e) {
            return "Вы выбрали неверное задание";
        }
    }
}

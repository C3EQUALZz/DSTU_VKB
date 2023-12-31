package programmingLanguagesJava.laboratories.secondLaboratory;

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Locale;
import java.util.Scanner;

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
     * 2.1. Расставьте правильно операторы приведения типа, чтобы получился ответ: d = 3.765. Операторы — в условии.
     */
    @SuppressWarnings("unused")
    public String firstQuestion() {
        int a = 15;
        int b = 4;
        float c = (float) a / b;
        double d = a * 1e-3 + c;
        return String.format("Результат 1 задания: c - %f, d - %f", c, d);
    }

    /**
     * 2.2 Давайте тоже найдем решение задачи: у нас есть какие-то переменные,
     * преобразованные в другой тип, но их недостаточно.
     * Нужно добавить одну операцию по преобразованию типа, чтобы получался нужный нам ответ b = 0.
     */
    @SuppressWarnings("unused")
    public String secondQuestion() {
        float f = (float) 128.50;
        int i = (int) f;
        int b = (byte) ((int) (i + f));
        return String.format("Результат 2 задания: %d", b);
    }

    /**
     * 2.3 Даны short number = 9, char zero = ‘0’ и int nine = (zero + number).
     * Добавьте одну операцию по преобразованию типа, чтобы получился красивый правильный ответ: 9.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion() {
        short number = 9;
        char zero = '0';
        int nine = Character.digit(zero, 10) + number;
        return String.format("Результат 3 задания: %d", nine);
    }

    /**
     * 2.4 Уберите ненужные операторы приведения типа, чтобы получился ответ: result: 1000.0
     */
    @SuppressWarnings("unused")
    public String fourthQuestion() {
        double d = (short) 2.50256e2d;
        char c =  'd';
        short s = (short) 2.22;
        int i = 150000;
        float f = 0.50f;
        double result = f + ((double) i / c) - (d * s) - 500e-3;
        return String.format("Результат 4 задания: %f", result);
    }

    /**
     * 2.5 Уберите ненужные операторы приведения типа, чтобы получился ответ: 1234567.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion() {
        long l =  1234_564_890L;
        int x =  0b1000_1100_1010; //бинарность
        double m =  (byte) 110_987_654_6299.123_34;
        float f =  l++ + 10 + ++x - (float) m;
        l = (long) f / 1000;
        return String.format("Результат 5 задания: %d", l);
    }

    /**
     * 2.6 Нужно добавить одну операцию по преобразованию типа, чтобы получался ответ: d = 2.941.
     * Пример вывода: 2.9411764705882355
     */
    @SuppressWarnings("unused")
    public String sixthQuestion() {
        int a = 50;
        int b = 17;
        double d = (double)a / b;
        return String.format("Результат 6 задания: %f", d);
    }

    /**
     * 2.7 Нужно добавить одну операцию по преобразованию типа, чтобы получался ответ: d = 1.0
     */
    @SuppressWarnings("unused")
    public String seventhQuestion() {
        int a = 257;
        System.out.println((byte)a);
        int b = 4;
        int c = 3;
        int e = 2;
        double d = (byte)a + b / c / e;

        return String.format("Результат 7 задания: %f", d);
    }

    /**
     * 2.8 Вам надо добавить одну операцию по преобразованию типа, чтобы получался ответ: d = 5.5.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion() {
        int a = 5;
        int b = 4;
        int c = 3;
        int e = 2;
        double d = a + (float)(b / c) / e;
        return String.format("Результат 8 задания: %f", d);
    }
}

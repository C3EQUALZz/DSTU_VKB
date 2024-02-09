package programmingLanguagesJava.laboratories.secondLaboratory;

import programmingLanguagesJava.laboratories.ConsoleReader;

import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите номер задания: ");
        var question = scanner.nextInt();

        System.out.printf("---------------------------------------------------\nРезультат %d задания:\n", question);

        System.out.println(ConsoleReader.executeTask(Solution.class, String.valueOf(question), " "));
    }

    /**
     * 2.1. Расставьте правильно операторы приведения типа, чтобы получился ответ: d = 3.765. Операторы — в условии.
     */
    @SuppressWarnings("unused")
    public String firstQuestion(String ignoreUnused) {
        int a = 15;
        int b = 4;
        float c = (float) a / b;
        double d = a * 1e-3 + c;
        return String.format("Число d = %f", d);
    }

    /**
     * 2.2 Давайте тоже найдем решение задачи: у нас есть какие-то переменные,
     * преобразованные в другой тип, но их недостаточно.
     * Нужно добавить одну операцию по преобразованию типа, чтобы получался нужный нам ответ b = 0.
     */
    @SuppressWarnings("unused")
    public String secondQuestion(String ignoreUnused) {
        float f = (float) 128.50;
        int i = (int) f;
        int b = (byte) ((int) (i + f));
        return String.format("Число b = %d", b);
    }

    /**
     * 2.3 Даны short number = 9, char zero = ‘0’ и int nine = (zero + number).
     * Добавьте одну операцию по преобразованию типа, чтобы получился красивый правильный ответ: 9.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion(String ignoreUnused) {
        short number = 9;
        char zero = '0';
        int nine = Character.digit(zero, 10) + number;
        return String.format("Правильный ответ: %d", nine);
    }

    /**
     * 2.4 Уберите ненужные операторы приведения типа, чтобы получился ответ: result: 1000.0
     */
    @SuppressWarnings("unused")
    public String fourthQuestion(String ignoreUnused) {
        double d = (short) 2.50256e2d;
        char c = 'd';
        short s = (short) 2.22;
        int i = 150000;
        float f = 0.50f;
        double result = f + ((double) i / c) - (d * s) - 500e-3;
        return String.format("result = %.1f", result);
    }

    /**
     * 2.5 Уберите ненужные операторы приведения типа, чтобы получился ответ: 1234567.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion(String ignoreUnused) {
        long l = 1234_564_890L;
        int x = 0b1000_1100_1010; //бинарность
        double m = (byte) 110_987_654_6299.123_34;
        float f = 10 + ++x - (float) m;
        l = (long) f / 1000;
        return String.format("Ответ: %d", l);
    }

    /**
     * 2.6 Нужно добавить одну операцию по преобразованию типа, чтобы получался ответ: d = 2.941.
     * Пример вывода: 2.9411764705882355
     */
    @SuppressWarnings("unused")
    public String sixthQuestion(String ignoreUnused) {
        int a = 50;
        int b = 17;
        double d = (double) a / b;
        return String.format("d = %f", d);
    }

    /**
     * 2.7 Нужно добавить одну операцию по преобразованию типа, чтобы получался ответ: d = 1.0
     */
    @SuppressWarnings("unused")
    public String seventhQuestion(String ignoreUnused) {
        int a = 257;
        int b = 4;
        int c = 3;
        int e = 2;
        double d = (byte) a + b / c / e;

        return String.format("d = %.1f", d);
    }

    /**
     * 2.8 Вам надо добавить одну операцию по преобразованию типа, чтобы получался ответ: d = 5.5.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion(String ignoreUnused) {
        int a = 5;
        int b = 4;
        int c = 3;
        int e = 2;
        double d = a + (float) (b / c) / e;
        return String.format("d = %f", d);
    }
}

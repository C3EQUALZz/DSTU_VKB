/**
 * Ковалев Данил ВКБ22
 */
package programmingLanguagesJava.laboratories.zeroLaboratory;

import programmingLanguagesJava.laboratories.ConsoleReader;

import java.util.Scanner;

public class Solution {
    public static int a = 1, b = 3, c = 9, d = 27;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введите какое задание вы хотите выполнить (цифра): ");

        String numberOfQuestion = scanner.next();

        System.out.printf("Результат %s задания: ", numberOfQuestion);

        System.out.println(ConsoleReader.executeTask(Solution.class, numberOfQuestion, " "));
    }

    /**
     * Напишите программу, чтобы она выводила текст на экран:
     * "Mesa called Jar Jar Binks, mesa your humble servant!
     */
    @SuppressWarnings("unused")
    public static String firstQuestion(String ignoreUnused) {
        return "Mesa called Jar Jar Binks, mesa your humble servant!";
    }

    /**
     * Выведите на экран текст "We have to get out of here. We need transport".
     */
    @SuppressWarnings("unused")
    public static String secondQuestion(String ignoreUnused) {
        return "We have to get out of here\n" + "We need transport\n";
    }

    /**
     * Вывести на экран текст "Destroy Droidekas!" 5 раз
     */
    @SuppressWarnings("unused")
    public static String thirdQuestion(String ignoreUnused) {
        return "Destroy Droidekas!\n".repeat(5);
    }

    /**
     * Вывести разницу между цифрами.
     */
    @SuppressWarnings("unused")
    public static String fourthQuestion(String ignoreUnused) {
        int a = 4;
        int b = 3;
        return String.valueOf(a - b);
    }


    /**
     * Расставьте комментарии, чтобы получилось 12, 2
     */
    @SuppressWarnings("unused")
    public static String fifthQuestion(String ignoreUnused) {
        int x = 2;
        int y = 12;

        // y = x * y;
        y = x + y;

        x = y - x;
        y = y - x;

        return String.format("%d\n%d", x, y);
    }

    /**
     * Поставьте комментарий, чтобы вывести предложение.
     */
    @SuppressWarnings("unused")
    public static String sixthQuestion(String ignoreUnused) {
        String res = "The";
        // res += "Starship";
        // res += " car ";
        res += " car";
        res += " is ";
        // res += "ready ";
        res += "for";
        // res += " the";
        res += " the";
        res += " race";
        return res;
    }

    /**
     * Объявите переменную jedi типа String.
     * Сразу же в строке объявления присвойте ей какое-нибудь значение.
     * Выведите на экран переменную jedi
     */
    @SuppressWarnings("unused")
    public static String seventhQuestion(String ignoredUnused) {
        @SuppressWarnings("redunant")
        var jedi = "Привет";
        return jedi;
    }

    /**
     * Напишите программу, которая выводит на экран квадрат этой переменной (number * number)
     */
    @SuppressWarnings("unused")
    public static String eighthQuestion(String ignoredUnused) {
        var number = 5;
        return String.format("%d", number * number);
    }

    /**
     * Напишите программу, которая выводит на экран надпись:
     * "May the Force be with you" 10 раз.
     */
    @SuppressWarnings("unused")
    public static String ninthQuestion(String ignoredUnused) {
        return "May the Force be with you\n".repeat(10);
    }

    /**
     * Напишите программу, которая в методе main объявляет такие переменные:
     * name типа String, height типа int и planet типа String.
     */
    @SuppressWarnings("unused")
    public static String tenthQuestion(String ignoredUnused) {
        var s = "Anakin ";
/*
        s.append("how are you?");
        s.append("I am");
        s.append("glad");
        s.append("to see you");
        s.append("Your");
*/
        s += "is ";
        s += "a hero";
        s += "!";

        return s;
    }

    /**
     * Внесите изменения в программу, чтобы переменная mol имела значение Mol
     */
    @SuppressWarnings("unused")
    public static String eleventhQuestion(String ignoredUnused) {
        String mol = "Mol";
        return "Darth " + mol + "!";
    }

    /**
     * Расставить знаки плюс и минус так, чтобы значение переменной result равнялось 20.
     */
    @SuppressWarnings("unused")
    public static String twelfthQuestion(String ignoredUnused) {
        return String.format("%d", - a + b - c + d);
    }

    /**
     * Напишите программу, которая выводит на экран квадрат числа 5.
     */
    @SuppressWarnings("unused")
    public static String thirteenthQuestion(String ignoredUnused) {
        return String.format("%d", sqr());
    }

    private static int sqr() {
        return 5 * 5;
    }

    /**
     * Закомментируйте переменные, которые нигде не используются.
     * Программа должна компилироваться.
     */
    @SuppressWarnings("unused")
    public static String fourteenthQuestion(String ignoreUnused) {
//        int a = 1;
        double b = 1.5;
        double c = b + 1.5;
/*
        int d = a + 12;
        double e = 12.3;
        String s = "Luke, " + a;
*/
        String s1 = "Twice ";
//        String s2 = "a";
        String s3 = s1 + "the pride, ";
        String s4 = " the fall.";
        return s3 + c + s4;
    }

    /**
     * Вам предстоит написать метод print, который будет выводить на экран строку 4 раза.
     * Строка — аргумент метода, то есть подаётся на входе.
     */
    @SuppressWarnings("unused")
    public static String fifteenthQuestion(String ignoreUnused) {
        return print("The power is easy to use ") +
                print("The power opens many opportunities");
    }

    private static String print(String s) {
        return (s + "\n").repeat(4);
    }

    /**
     * Напишите метод public static void increaseSpeed(int a),
     * который будет принимать значение скорости n,  увеличивать ее  на 100
     * и выведите на экран надпись: "Your speed is: <n+100> km/h."
     */
    @SuppressWarnings("unused")
    public static String sixteenthQuestion(String ignoreUnused) {
        return increaseSpeed(700);
    }

    private static String increaseSpeed(int n) {
        return String.format("Your speed is: %d km/h", n + 100);
    }

    /**
     * В методе main создайте объект Zam, сохраните ссылку на него в переменную zam.
     * Создайте также объект Dron и сохраните ссылку на него в переменную dron.
     */
    @SuppressWarnings("unused")
    public static String seventeenthQuestion(String ignoreUnused) {

        var zam = new Zam();
        var dron = new Dron();

        zam.spy = dron;
        dron.hunter = zam;

        return "Сохранил в переменную";
    }

    @SuppressWarnings("unused")
    public static String eighteenthQuestion(String ignoreUnused) {
        Jedi jedi1 = new Jedi();
        jedi1.name = "Obi-Wan";

        Jedi jedi2 = new Jedi();
        jedi2.name = "Anakin";

        Jedi jedi3 = new Jedi();
        jedi3.name = "Joda";

        return "Готов";
    }

    /**
     * Создай 10 переменных типа Clone и 8 объектов типа Clone.
     */
    @SuppressWarnings("unused")
    public static String nineteenthQuestion(String ignoreUnused) {
        Clone clone1 = new Clone();
        Clone clone2 = new Clone();
        Clone clone3 = new Clone();
        Clone clone4 = new Clone();
        Clone clone5 = new Clone();
        Clone clone6 = new Clone();
        Clone clone7 = new Clone();
        Clone clone8 = new Clone();
        Clone clone9;
        Clone clone10;

        return "Все переменные созданы";
    }

    public static class Clone {}

    /**
     * Создайте объект типа Clone1, Clone2, Clone3 и объект типа Dias.
     * Присвой каждому клону владельца (owner).
     */
    @SuppressWarnings("unused")
    public static String twentiethQuestion(String ignoreUnused) {
        var clone1 = new Clone1();
        var clone2 = new Clone2();
        var clone3 = new Clone3();
        var dias = new Dias();

        clone1.owner = dias;
        clone2.owner = dias;
        clone3.owner = dias;

        return " ";
    }

    private static class Dias {}

    private static class Clone1 {
        protected Dias owner;
    }

    private static class Clone2 extends Clone1 {}

    private static class Clone3 extends Clone1 {}

    /**
     * Зная, что на планете Камино гравитация, как на Луне, реализуйте метод,
     * который переводит земной вес в лунный. Реализуй метод getWeight(int),
     * который принимает вес тела (в Ньютонах) на Земле, и возвращает, сколько это тело будет
     * весить на Луне (в Ньютонах).  Тип возвращаемого значения - double.
     */
    @SuppressWarnings("unused")
    public static String twentyFirstQuestion(String ignoreUnused) {
        return String.valueOf(getWeight(888));
    }

    private static double getWeight(int weight) {
        return weight / 6.0;
    }

    /**
     * Давайте перешлем сообщение астродроиду в понятном ему формате.
     * Для этого реализуем метод print3. Реализуйте метод print3.
     * Метод должен вывести переданную строку (слово) на экран три раза через пробел.
     */
    @SuppressWarnings("unused")
    public static String twentySecondQuestion(String ignoreUnused) {
        return print3("dump") + print3("cargo");
    }

    private static String print3(String str) {
        return (str + " ").repeat(5);
    }

    /**
     * Увидев, что ракета попала по цели, Фетт улетает на планету Дженозис, вы же,
     * успешно спрятавшись за астероидом затаились, чтобы выждать, когда наемник отлетит на
     * минимальное безопасное расстояние, чтобы проследовать за ним.
     * Напишите функцию, которая возвращает минимум из двух чисел.
     */
    @SuppressWarnings("unused")
    public static String twentyThirdQuestion(String ignoreUnused) {
        return String.format("%d\n%d\n%d", min(12, 33), min(-20, 0), min(-10, -20));
    }

    private static int min(int a, int b) {
        return a < b ? a : b;
    }
}

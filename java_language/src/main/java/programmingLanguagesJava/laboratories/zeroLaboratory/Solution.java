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
        System.out.println(ConsoleReader.executeTask(Solution.class, scanner.next(), " "));
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
     * Объявите переменную jedi типа String.
     * Сразу же в строке объявления присвойте ей какое-нибудь значение.
     * Выведите на экран переменную jedi
     */
    @SuppressWarnings("unused")
    public static String secondQuestion(String ignoredUnused) {
        var jedi = "Привет";
        return jedi;
    }

    /**
     * Напишите программу, которая выводит на экран квадрат этой переменной (number * number)
     */
    @SuppressWarnings("unused")
    public static String thirdQuestion(String ignoredUnused) {
        var number = 5;
        return String.format("%d", number * number);
    }

    /**
     * Напишите программу, которая выводит на экран надпись:
     * "May the Force be with you" 10 раз.
     */
    @SuppressWarnings("unused")
    public static String fourthQuestion(String ignoredUnused) {
        return "May the Force be with you".repeat(10);
    }

    /**
     * Напишите программу, которая в методе main объявляет такие переменные:
     * name типа String, height типа int и planet типа String.
     */
    @SuppressWarnings("unused")
    public static String fifthQuestion(String ignoredUnused) {
        var s = new StringBuilder("Anakin ");
//        s.append("how are you?");
//        s.append("I am");
//        s.append("glad");
//        s.append("to see you");
//        s.append("Your");
        s.append("is ");
        s.append("a hero");
        s.append("!");

        return s.toString();
    }

    /**
     * Внесите изменения в программу, чтобы переменная mol имела значение Mol
     */
    @SuppressWarnings("unused")
    public static String sixthQuestion(String ignoredUnused) {
        String mol = "Mol";
        return "Darth " + mol + "!";
    }

    /**
     * Расставить знаки плюс и минус так, чтобы значение переменной result равнялось 20.
     */
    @SuppressWarnings("unused")
    public static String seventhQuestion(String ignoredUnused) {
        return String.format("%d", - a + b - c + d);
    }

    /**
     * Напишите программу, которая выводит на экран квадрат числа 5.
     */
    @SuppressWarnings("unused")
    public static String eighthQuestion(String ignoredUnused) {
        return String.format("%d", sqr(5));
    }

    private static int sqr(int a) {
        return a * a;
    }
    @SuppressWarnings("unused")
    public static String ninthQuestion(String ignoreUnused) {
//        int a = 1;
        double b = 1.5;
        double c = b + 1.5;
//        int d = a + 12;
//        double e = 12.3;
//        String s = "Luke, " + a;
        String s1 = "Twice ";
//        String s2 = "a";
        String s3 = s1 + "the pride, ";
        String s4 = " the fall.";
        return s3 + c + s4;
    }
    @SuppressWarnings("unused")
    public static String tenthQuestion(String ignoreUnused) {
        return print("The power is easy to use ") +
                print("The power opens many opportunities");
    }

    private static String print(String s) {
        return (s + "\n").repeat(4);
    }

    @SuppressWarnings("unused")
    public static String eleventhQuestion(String ignoreUnused) {
        return increaseSpeed(700);
    }

    private static String increaseSpeed(int number) {
        return String.format("Your speed is: %d km/h", number + 100);
    }

    @SuppressWarnings("unused")
    public static String twelveQuestion(String ignoreUnused) {

        var zam = new Zam();
        var dron = new Dron();

        zam.spy = dron;
        dron.hunter = zam;

        return "Сохранил в переменную";
    }

    @SuppressWarnings("unused")
    public static String thirteenthQuestion(String ignoreUnused) {
        Jedi jedi1 = new Jedi();
        jedi1.name = "Obi-Wan";

        Jedi jedi2 = new Jedi();
        jedi2.name = "Anakin";

        Jedi jedi3 = new Jedi();
        jedi3.name = "Joda";

        return "Готов";
    }

}

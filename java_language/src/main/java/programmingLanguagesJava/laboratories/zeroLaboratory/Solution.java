/**
 * Ковалев Данил ВКБ22
 */
package programmingLanguagesJava.laboratories.zeroLaboratory;

import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите задание: ");
        Object result = switch (scanner.nextInt()) {
            case 1 -> firstQuestion();
            case 2 -> secondQuestion();
            case 3 -> thirdQuestion();
            case 4 -> fourthQuestion();
            case 5 -> fifthQuestion();
            case 6 -> sixthQuestion();
            case 7 -> seventhQuestion();
            default -> "Вы выбрали неверное задание";
        };

        scanner.close();

        System.out.println(result);
    }

    /**
     * Напишите программу, которая будет выводить несколько строчек:
     * «We have to get out of here»
     * «We need transport»
     */
    public static String firstQuestion() {
        return String.format("Результат 1 задания:\n%s", "We have to get out of here" + "\n" + "We need transport");
    }

    /**
     * Требуется написать программу, выводящую на экран надпись "Destroy Droidekas!" 5 раз.
     * Каждый раз - с новой строки.
     */
    public static String secondQuestion() {
        // В примере достаточно большие разрывы, поэтому есть ещё перенос строки
        return "Результат 2 задания:\n" + "Destroy Droidekas! \n".repeat(5);
    }

    /**
     * Напишите программу, которая посчитает и выведет сколько рабочих астродроидов осталось.
     */
    public static String thirdQuestion() {
        // Зачем перевод в строку, когда print - это делает неявно ?
        return "Результат 3 задания:\n" + Integer.toString(4 - 3);
    }

    /**
     * Напишите программу, которая в методе main объявляет такие переменные:
     * name типа String, height типа int и planet типа String.
     */
    public static String fourthQuestion() {
        final String name = "Anakin";
        final int height = 188;
        final String planet = "Tatooine";
        return "Результат 4 задания:\n%s" + name + "\n" + height + "\n" + planet;
    }

    /**
     * Напишите программу, которая выводит на экран надпись: "You should take our money".
     */
    public static String fifthQuestion() {
        return "Результат 5 задания:\n" + "You should take our money";
    }

    /**
     * Разкомментируйте одну или несколько строк, чтобы вывести сначала 12, а потом 2
     */
    public static String sixthQuestion() {
        int x = 2;
        int y = 12;
//        y = x * y;
        y = x + y;
        x = y - x;
        y = y - x;
        return String.format("Результат 6 задания:\n" + "x = %d, y = %d", x, y);
    }

    /**
     * Закомментируйте одну или несколько строк, чтобы программа выводила фразу : «The car is ready for the race»
     */
    public static String seventhQuestion() {
        // Я начал все оптимизировать под приложение, поэтому сразу переделываю некоторые лабораторные работы
        var a = "The";
//        var b = "Starship";
//        var c = " car ";
        var c = " car";
        var d = " is ";
        var e = "ready ";
//        var f = " ready ";
        var g = "for";
//        var h = " the";
        var i = " the";
        var j = " race";

        return String.format("Результат 7 задания:\n%s", a+c+d+e+g+i+j);
    }
}

package zeroLaboratory;

import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        interactUser();

    }

    public static void interactUser() {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите какое задание вы хотите сделать: ");

        switch (scanner.nextInt()) {
            case 1 -> firstQuestion();
            case 2 -> secondQuestion();
            case 3 -> thirdQuestion();
            case 4 -> fourthQuestion();
            case 5 -> fifthQuestion();
            case 6 -> sixthQuestion();
            case 7 -> seventhQuestion();
        }
    }

    /**
     * Напишите программу, которая будет выводить несколько строчек:
     * «We have to get out of here»
     * «We need transport»
     */
    public static void firstQuestion() {
        System.out.println("We have to get out of here" + "\n" + "We need transport");
    }

    /**
     * Требуется написать программу, выводящую на экран надпись "Destroy Droidekas!" 5 раз.
     * Каждый раз - с новой строки.
     */
    public static void secondQuestion() {
        // В примере достаточно большие разрывы, поэтому есть ещё перенос строки
        for (int i = 0; i < 5; i++)
            System.out.println("Destroy Droidekas! \n");
    }

    /**
     * Напишите программу, которая посчитает и выведет сколько рабочих астродроидов осталось.
     */
    public static void thirdQuestion() {
        // Зачем перевод в строку, когда print - это делает неявно ?
        System.out.println(Integer.toString(4 - 3));
    }

    /**
     * Напишите программу, которая в методе main объявляет такие переменные:
     * name типа String, height типа int и planet типа String.
     */
    public static void fourthQuestion() {
        final String name = "Anakin";
        final int height = 188;
        final String planet = "Tatooine";
    }

    /**
     * Напишите программу, которая выводит на экран надпись: "You should take our money".
     */
    public static void fifthQuestion() {
        System.out.println("You should take our money");
    }

    /**
     * Разкомментируйте одну или несколько строк чтобы вывести сначала 12, а потом 2
     */
    public static void sixthQuestion() {
        int x = 2;
        int y = 12;
//        y = x * y;
        y = x + y;
        x = y - x;
        y = y - x;
        System.out.println(x);
        System.out.println(y);
    }

    /**
     * Закомментируйте одну или несколько строк, чтобы программа выводила фразу : «The car is ready for the race»
     */
    public static void seventhQuestion() {
        System.out.print("The");
//        System.out.print("Starship");
//        System.out.println(" car ");
        System.out.print(" car");
        System.out.print(" is ");
        System.out.print("ready ");
//        System.out.print(" ready ");
        System.out.print("for");
//        System.out.println(" the");
        System.out.print(" the");
        System.out.println(" race");
    }
}

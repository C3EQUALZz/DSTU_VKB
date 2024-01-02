package programmingLanguagesJava.laboratories.firstLaboratory;

import java.util.Scanner;

public class Rect {

    public static String square() {
        Scanner keyboard = new Scanner(System.in);
        System.out.print("Введите длину: ");
        int a = keyboard.nextInt();
        System.out.print("Введите ширину: ");
        int b = keyboard.nextInt();
        return "Площадь прямоугольника: " + a * b;
    }
}

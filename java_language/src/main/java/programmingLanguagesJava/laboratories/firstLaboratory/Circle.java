package programmingLanguagesJava.laboratories.firstLaboratory;

import java.util.Scanner;

public class Circle {
    public static String square() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Введите радиус: ");
        double radius = sc.nextDouble();
        double S = radius * radius * Math.PI;
        return "Площадь круга: " + S;
    }
}

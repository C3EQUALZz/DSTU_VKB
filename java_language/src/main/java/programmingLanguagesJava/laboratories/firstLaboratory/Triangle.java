package programmingLanguagesJava.laboratories.firstLaboratory;

import java.util.Scanner;

public class Triangle {
    public static String square() {
        Scanner keyboard = new Scanner(System.in);

        System.out.print("Введите номер данных: (1) Высота и основание, (2) Три стороны: ");

        int params = keyboard.nextInt();
        return switch (params) {

            case 1 -> {
                System.out.println("Высота = ");
                int h = keyboard.nextInt();
                System.out.println("Основание = ");
                int b = keyboard.nextInt();
                yield String.format("Площадь треугольника - %f", ((h * b) / 2.0));
            }

            case 2 -> {

                System.out.println("Первая сторона = ");
                int a = keyboard.nextInt();
                System.out.println("Вторая сторона = ");
                int b = keyboard.nextInt();
                System.out.println("Третья сторона = ");
                int c = keyboard.nextInt();

                if (a < 0 || b < 0 || c < 0 || (a + b <= c) || a + c <= b || b + c <= a) {
                    yield "Не верные данные";
                }

                double P = (a + b + c) / 2.0;
                yield String.format("Площадь треугольника - %f", Math.sqrt(P * (P - a) * (P - b) * (P - c)));

            }
            default -> "Данный вариант не существует";

        };
    }
}
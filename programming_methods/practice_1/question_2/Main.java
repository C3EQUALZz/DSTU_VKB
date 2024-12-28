package practice_1.question_2;

import java.util.Arrays;

class Main {
    public static void main(String[] args) {
        Deque<Integer> deque = new Deque<>(10);

        int[] elementsToInsert1 = {10, 20, 30, 40, 50};
        System.out.println("Элементы для добавления в дек слева: " + Arrays.toString(elementsToInsert1));

        for (var element : elementsToInsert1) {
            deque.insertLeft(element);
        }
        System.out.println("Содержимое дека: " + deque);

        int[] elementsToInsert2 = {60, 70, 80};
        System.out.println("Элементы для добавления в дек справа: " + Arrays.toString(elementsToInsert2));

        for (var element : elementsToInsert2) {
            deque.insertRight(element);
        }
        System.out.println("Содержимое дека: " + deque);

        System.out.println("Удаляю один элемент справа: " + deque.removeRight());
        System.out.println("Содержимое дека: " + deque);

        System.out.print("Удаляю все элементы из дека: ");
        while (!deque.isEmpty()) {
            System.out.print(deque.removeLeft() + " ");
        }

        int[] elementsToFill = {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000};

        System.out.println("\nНаполняем дек: " + Arrays.toString(elementsToFill));

        for (var element : elementsToFill) {
            deque.insertRight(element);
        }

        System.out.println("Содержимое дека: " + deque);
        System.out.println("Полный ли дек?: " + deque.isFull());
    }
}

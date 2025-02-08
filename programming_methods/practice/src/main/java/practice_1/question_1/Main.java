package practice_1.question_1;

import java.util.Arrays;

class Main {
    public static void main(String[] args) {

        Queue<Integer> queue = new Queue<>(5);

        int[] elementsToInsert1 = {10, 20, 30, 40, 50, 4};

        System.out.println("Элементы для добавления в очередь: " + Arrays.toString(elementsToInsert1));

        for (var element : elementsToInsert1) {
            queue.insert(element);
        }

        System.out.println("Содержимое очереди: " + queue);

        System.out.print("Извлекаю элементы: ");
        for (int i = 0; i < 3; i++) {
            System.out.print(queue.remove() + " ");
        }
        System.out.println("\nСодержимое очереди: " + queue);

        System.out.println("Первый элемент очереди: " + queue.peekFront());

        int[] elementsToInsert2 = {50, 60, 70, 80};

        System.out.println("Элементы для добавления в очередь: " + Arrays.toString(elementsToInsert2));

        for (var element : elementsToInsert2) {
            queue.insert(element);
        }
        System.out.println("Содержимое очереди: " + queue);

        System.out.print("Извлечение и вывод всех элементов: ");
        while (!queue.isEmpty()) {
            var n = queue.remove();
            System.out.print(n + " ");
        }

        System.out.println("\n" + "Содержимое очереди: " + queue);

        int[] elementsToInsert3 = {44, 66, 77, 808};

        System.out.println("Элементы для добавления в очередь: " + Arrays.toString(elementsToInsert3));

        for (var element : elementsToInsert3) {
            queue.insert(element);
        }
        System.out.println("Содержимое очереди: " + queue);

        System.out.println("Удалили:" + Arrays.toString(queue.remove_n(2)));
        System.out.println(queue);
    }
}


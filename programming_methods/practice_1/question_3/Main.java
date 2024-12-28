package practice_1.question_3;

import java.util.Arrays;

class Main {
    public static void main(String[] args) {
        StackOperations<Integer> stack = new DequeStack<>(10);

        int[] elementsToInsert1 = {20, 40, 60, 80};
        System.out.println("Элементы для добавления в стек: " + Arrays.toString(elementsToInsert1));

        for (var element : elementsToInsert1) {
            stack.push(element);
        }

        System.out.println(stack);

        while (!stack.isEmpty()) {
            long value = stack.pop();
            System.out.print(value);
            System.out.print(" ");
        }
        System.out.println("Стек пуст после удаления всех элементов? " + stack.isEmpty());

        System.out.println("Попытка выполнить pop на пустом стеке:");
        try {
            stack.pop();  // Пытаемся выполнить pop на пустом стеке
        } catch (IllegalStateException e) {
            System.out.println("Ошибка: " + e.getMessage());
        }

        stack.push(100);
        stack.push(200);

        System.out.println("Верхний элемент стека (peek): " + stack.peek());

        System.out.println("Состояние стека после peek: " + stack);
    }
}

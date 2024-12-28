package practice_2.question_1;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {

        System.out.print("Введите цепочку символов для построения дерева (слитно): ");
        var input = System.console().readLine();

        if (input == null || input.isEmpty() || input.isBlank()) {
            System.out.println("Ошибка: пустая строка. Завершение программы.");
            return;
        }

        var elements = new ArrayList<Character>();
        for (var ch : input.toCharArray()) {
            elements.add(ch);
        }

        System.out.println(new Tree<>(elements));
    }
}


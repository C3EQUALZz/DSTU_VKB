package practice_2.question_1;

import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {

        System.out.print("Введите цепочку символов для построения дерева (слитно): ");
        String input = System.console().readLine();

        if (input == null || input.isEmpty()) {
            System.out.println("Ошибка: пустая строка. Завершение программы.");
            return;
        }

        List<Character> elements = new ArrayList<>();
        for (char ch : input.toCharArray()) {
            elements.add(ch);
        }

        System.out.println(new Tree<>(elements));
    }
}


package practice_2;

import practice_2.core.AbstractTree;
import practice_2.question_1.Tree;
import practice_2.question_2.BalancedTree;
import practice_2.question_3.FullBalancedTree;

import java.util.ArrayList;

class Main {
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

        System.out.print("Введите под каким заданием дерево вы хотите увидеть? (1, 2, 3): ");

        AbstractTree<Character> tree = switch (System.console().readLine()) {
            case "1" -> new Tree<>(elements);
            case "2" -> new BalancedTree<>(elements);
            case "3" -> new FullBalancedTree<>(elements);
            default -> throw new IllegalStateException("Неизвестное задание");
        };

        System.out.println(tree);
    }
}


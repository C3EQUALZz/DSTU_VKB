/**
 * Пример для ввода:
 * ----------------
 * A, B
 * A, D
 * B, C
 * B, E
 * C, F
 * D, G
 * E, F
 * G, H
 * H, I
 * I, F
 * F, D
 * E, H
 * ----------------
 * A, B
 * B, C
 * A, D
 * D, E
 * E, D
 */


package practice_3;

import practice_3.core.AbstractUnweightedGraph;
import practice_3.core.NonOrientedGraph;
import practice_3.core.OrientedGraph;
import practice_3.question_1.BreathFirstSearch;
import practice_3.question_2.DepthFirstSearch;

import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        AbstractUnweightedGraph<String> graph;

        while (true) {
            try {
                System.out.print("Какой граф вы хотите использовать? (1) - Ориентированный или (2) - неориентированный?: ");
                graph = switch (scanner.nextLine()) {
                    case "1" -> new OrientedGraph<>();
                    case "2" -> new NonOrientedGraph<>();
                    default -> throw new NumberFormatException();
                };
                break;
            } catch (NumberFormatException e) {
                System.out.println("Неправильный выбрали номер, перезапускаю ");
            }
        }

        while (true) {
            System.out.print("Введите пару (или `exit`): ");
            var input = scanner.nextLine().trim();

            if (input.equalsIgnoreCase("exit")) {
                break;
            }

            var vertices = input.split(",\\s*");
            if (vertices.length != 2) {
                System.out.println("Ошибка: введите ровно две вершины, разделённые запятой. Пример: A, B");
                continue;
            }

            var from = vertices[0];
            var to = vertices[1];

            graph.addEdge(from, to);
            System.out.println("Ребро добавлено: " + from + " -> " + to);
        }

        System.out.print("Введите стартовую вершину, которую вы хотите использовать: ");
        var startValue = scanner.nextLine();

        while (true) {
            try {
                System.out.print("Какой алгоритм вы хотите посмотреть? (1) - (мот) через bfs, (2) - dfs: ");
                switch (scanner.nextLine()) {
                    case "1" -> {
                        var result = BreathFirstSearch.execute(startValue, graph);
                        System.out.println("МОТ с помощью BFS:");
                        result.forEach(System.out::println);
                    }
                    case "2" -> {
                        var result = DepthFirstSearch.execute(startValue, graph);
                        System.out.println("Путь DFS: " + result);
                        System.out.println("Матрица смежности: ");
                        System.out.println(graph);
                    }
                    default -> throw new NumberFormatException();
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Выбрали неправильный номер, перезапускаю заново. ");
            }
        }

        scanner.close();
    }
}

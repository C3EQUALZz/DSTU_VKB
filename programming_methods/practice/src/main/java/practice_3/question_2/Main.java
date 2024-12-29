package practice_3.question_2;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        Graph<Character> graph = new Graph<>();

        // Добавление рёбер
        graph.addEdge('A', 'B');
        graph.addEdge('B', 'C');
        graph.addEdge('A', 'D');
        graph.addEdge('D', 'E');
        graph.addEdge('E', 'D');

        // Выполнение обхода в глубину
        List<Character> dfsPath = graph.dfs('A');
        System.out.println("DFS: " + dfsPath);

        // Вывод графа с помощью toString
        System.out.println("\nМатрица смежности:");
        System.out.println(graph);  // Использование метода toString
    }
}

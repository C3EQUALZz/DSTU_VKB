package practice_3.question_2;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        OrientedGraph<Character> orientedGraph = new OrientedGraph<>();

        // Добавление рёбер
        orientedGraph.addEdge('A', 'B');
        orientedGraph.addEdge('B', 'C');
        orientedGraph.addEdge('A', 'D');
        orientedGraph.addEdge('D', 'E');
        orientedGraph.addEdge('E', 'D');

        // Выполнение обхода в глубину
        List<Character> dfsPath = orientedGraph.dfs('A');
        System.out.println("DFS: " + dfsPath);

        // Вывод графа с помощью toString
        System.out.println("\nМатрица смежности:");
        System.out.println(orientedGraph);  // Использование метода toString
    }
}

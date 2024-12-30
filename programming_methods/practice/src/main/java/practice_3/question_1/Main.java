package practice_3.question_1;

import practice_3.core.Node;

import java.util.List;

class Main {
    public static void main(String[] args) {
        NonOrientedGraph<Character> theNonOrientedGraph = new NonOrientedGraph<>();

        // Добавление рёбер
        theNonOrientedGraph.addEdge('A', 'B');
        theNonOrientedGraph.addEdge('A', 'D');
        theNonOrientedGraph.addEdge('B', 'C');
        theNonOrientedGraph.addEdge('B', 'E');
        theNonOrientedGraph.addEdge('C', 'F');
        theNonOrientedGraph.addEdge('D', 'G');
        theNonOrientedGraph.addEdge('E', 'F');
        theNonOrientedGraph.addEdge('G', 'H');
        theNonOrientedGraph.addEdge('H', 'I');
        theNonOrientedGraph.addEdge('I', 'F');
        theNonOrientedGraph.addEdge('F', 'D'); // Для цикла
        theNonOrientedGraph.addEdge('E', 'H'); // Дополнительный путь

        List<List<Node<Character>>> bfsResult = theNonOrientedGraph.bfs('A');

        // Вывод рёбер, полученных после обхода
        System.out.println("Рёбра, построенные BFS:");
        for (List<Node<Character>> edge : bfsResult) {
            System.out.println(edge);
        }

        // AB AD BC BE DF DG EH FI
    }
}

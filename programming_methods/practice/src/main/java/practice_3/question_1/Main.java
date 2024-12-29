package practice_3.question_1;

import java.util.List;

class Main {
    public static void main(String[] args) {
        Graph<Character> theGraph = new Graph<>();

        // Добавление рёбер
        theGraph.addEdge('A', 'B');
        theGraph.addEdge('A', 'D');
        theGraph.addEdge('B', 'C');
        theGraph.addEdge('B', 'E');
        theGraph.addEdge('C', 'F');
        theGraph.addEdge('D', 'G');
        theGraph.addEdge('E', 'F');
        theGraph.addEdge('G', 'H');
        theGraph.addEdge('H', 'I');
        theGraph.addEdge('I', 'F');
        theGraph.addEdge('F', 'D'); // Для цикла
        theGraph.addEdge('E', 'H'); // Дополнительный путь

        List<List<Node<Character>>> bfsResult = theGraph.bfs('A');

        // Вывод рёбер, полученных после обхода
        System.out.println("Рёбра, построенные BFS:");
        for (List<Node<Character>> edge : bfsResult) {
            System.out.println(edge);
        }

        // AB AD BC BE DF DG EH FI
    }
}

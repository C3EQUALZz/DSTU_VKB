package practice_3.question_1.dummy;

class Main {
    public static void main(String[] args) {
        Graph theGraph = new Graph();

        // Добавляем 9 вершин (A-I)
        theGraph.addVertex('A'); // 0
        theGraph.addVertex('B'); // 1
        theGraph.addVertex('C'); // 2
        theGraph.addVertex('D'); // 3
        theGraph.addVertex('E'); // 4
        theGraph.addVertex('F'); // 5
        theGraph.addVertex('G'); // 6
        theGraph.addVertex('H'); // 7
        theGraph.addVertex('I'); // 8

        // Добавляем 12 рёбер
        theGraph.addEdge(0, 1); // AB
        theGraph.addEdge(0, 3); // AD
        theGraph.addEdge(1, 2); // BC
        theGraph.addEdge(1, 4); // BE
        theGraph.addEdge(2, 5); // CF
        theGraph.addEdge(3, 6); // DG
        theGraph.addEdge(4, 5); // EF
        theGraph.addEdge(6, 7); // GH
        theGraph.addEdge(7, 8); // HI
        theGraph.addEdge(8, 5); // IF
        theGraph.addEdge(5, 3); // FC (Добавляем для создания цикла)
        theGraph.addEdge(4, 7); // EH (Добавляем для создания дополнительного пути)

        System.out.print("МОД: ");
        theGraph.bfs(); // Построение МОД с использованием BFS
        System.out.println();
    }
}

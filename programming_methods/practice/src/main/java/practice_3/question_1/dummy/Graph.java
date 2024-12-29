package practice_3.question_1.dummy;


class Graph {
    private final Vertex[] vertexList; // Список вершин
    private final int[][] adjMat; // Матрица смежности
    private int nVertexes; // Текущее количество вершин
    private final Queue theQueue;

    public Graph() {
        int MAX_VERTEXES = 20;
        vertexList = new Vertex[MAX_VERTEXES];
        adjMat = new int[MAX_VERTEXES][MAX_VERTEXES];
        nVertexes = 0;
        for (int j = 0; j < MAX_VERTEXES; j++) // Матрица смежности
            for (int k = 0; k < MAX_VERTEXES; k++) // заполняется нулями
                adjMat[j][k] = 0;
        theQueue = new Queue();
    }

    /**
     * Метод для добавления вершины в граф.
     *
     * @param lab значение, которое мы хотим добавить.
     */
    public void addVertex(char lab) {
        vertexList[nVertexes++] = new Vertex(lab);
    }

    // -------------------------------------------------------------
    public void addEdge(int start, int end) {
        adjMat[start][end] = 1;
        adjMat[end][start] = 1;
    }

    // -------------------------------------------------------------
    public void displayVertex(int v) {
        System.out.print(vertexList[v].label);
    }

    // -------------------------------------------------------------
    public void bfs() {
        vertexList[0].wasVisited = true; // Пометка начальной вершины как посещённой
        theQueue.insert(0); // Вставка в очередь начальной вершины (обычно A)

        while (!theQueue.isEmpty()) {
            int parentVert = theQueue.remove(); // Удаление вершины в начале очереди

            // Пока существует не посещённая соседняя вершина
            int childVert;
            while ((childVert = getAdjUnvisitedVertex(parentVert)) != -1) {
                vertexList[childVert].wasVisited = true; // Пометка вершины как посещённой
                displayVertex(parentVert); // Выводим начальную вершину ребра
                displayVertex(childVert); // Выводим конечную вершину ребра
                System.out.print(" "); // Для разделения рёбер
                theQueue.insert(childVert); // Вставка вершины в очередь
            }
        }

        // Сброс состояний вершин после завершения обхода
        for (int j = 0; j < nVertexes; j++) {
            vertexList[j].wasVisited = false;
        }
    }

    /**
     * Метод возвращает не посещенную вершину, смежную по отношению к v
     *
     * @param v индекс строки матрицы, где мы хотим найти новую вершину.
     * @return вершина, которую ещё не проходили.
     */
    public int getAdjUnvisitedVertex(int v) {
        for (int j = 0; j < nVertexes; j++)
            if (adjMat[v][j] == 1 && !vertexList[j].wasVisited)
                return j; // Возвращает первую найденную вершину
        return -1; // Таких вершин нет
    }
}


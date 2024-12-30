/**
 * Измените программу bfs.java (см. листинг 13.2) так, чтобы для поиска минимального остовного дерева применялся
 * алгоритм обхода в ширину вместо обхода в глубину из программы mst.java (см. листинг 13.3).
 * Создайте в методе main() граф с 9 вершинами и 12 ребрами, постройте его минимальное остовное дерево.
 */


package practice_3.question_1;

import java.util.*;

class Graph<T extends Comparable<T>> {
    private final Map<T, Node<T>> vertices; // Словарь для хранения вершин по их значениям

    public Graph() {
        this.vertices = new HashMap<>();
    }

    /**
     * Добавляет ребро между двумя вершинами (без направления)
     *
     * @param start начальная вершина
     * @param end   конечная вершина
     */
    public void addEdge(T start, T end) {
        Node<T> startNode = vertices.computeIfAbsent(start, Node::new);
        Node<T> endNode = vertices.computeIfAbsent(end, Node::new);

        startNode.connect(endNode); // Связываем вершины через метод connect
    }

    /**
     * BFS для построения минимального остовного дерева
     *
     * @param startValue стартовое значение, от которого мы хотим начать поиск.
     * @return минимальное остовное дерево
     */
    public List<List<Node<T>>> bfs(T startValue) {
        Node<T> startNode = vertices.get(startValue);

        if (startNode == null) {
            throw new IllegalArgumentException("Start vertex not found: " + startValue);
        }

        List<List<Node<T>>> result = new LinkedList<>(); // Хранение рёбер
        Set<Node<T>> visited = new HashSet<>();
        Queue<Node<T>> queue = new LinkedList<>();

        visited.add(startNode);
        queue.add(startNode);

        while (!queue.isEmpty()) {
            Node<T> current = queue.poll();

            for (Node<T> neighbor : current.getNeighbors()) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);

                    // Сохраняем ребро как пару вершин
                    result.add(List.of(current, neighbor));

                    queue.add(neighbor);
                }
            }
        }

        return result;
    }
}


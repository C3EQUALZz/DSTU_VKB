/**
 * Задание №2.
 * Измените программу dfs.java (см. листинг 13.1), чтобы она выводила таблицу связности для направленного графа.
 */

package practice_3.question_2;

import practice_3.core.AbstractUnweightedGraph;
import practice_3.core.Node;

import java.util.*;


class OrientedGraph<T extends Comparable<T>> extends AbstractUnweightedGraph<T> {

    public OrientedGraph() {
        super();
    }

    /**
     * Добавление ребра между двумя вершинами (без направления)
     */
    @Override
    public void addEdge(T start, T end) {
        Node<T> startNode = vertices.computeIfAbsent(start, Node::new);
        Node<T> endNode = vertices.computeIfAbsent(end, Node::new);
        startNode.connect(endNode);
    }

    /**
     * DFS для обхода в глубину
     */
    public List<T> dfs(T startValue) {
        List<T> path = new ArrayList<>();
        Set<Node<T>> visited = new HashSet<>();
        Node<T> startNode = vertices.get(startValue);

        if (startNode == null) {
            throw new IllegalArgumentException("Start vertex not found: " + startValue);
        }

        dfsRecursive(startNode, visited, path);
        return path;
    }

    // Рекурсивный метод для обхода в глубину
    private void dfsRecursive(Node<T> current, Set<Node<T>> visited, List<T> path) {
        visited.add(current);
        path.add(current.getValue());

        for (Node<T> neighbor : current.getNeighbors()) {
            if (!visited.contains(neighbor)) {
                dfsRecursive(neighbor, visited, path);
            }
        }
    }


}

package practice_3.question_1;

import practice_3.core.AbstractUnweightedGraph;
import practice_3.core.UnweightedNode;

import java.util.*;

public class BreathFirstSearch {

    /**
     * BFS для построения минимального остовного дерева.
     *
     * @param startValue стартовая вершина.
     * @param graph      объект графа.
     * @param <T>        тип данных вершин.
     * @return минимальное остовное дерево как список рёбер.
     */
    public static <T extends Comparable<T>> List<List<UnweightedNode<T>>> execute(T startValue, AbstractUnweightedGraph<T> graph) {
        if (graph == null || graph.getVertex(startValue) == null) {
            throw new IllegalArgumentException("Graph is null or start vertex not found: " + startValue);
        }

        UnweightedNode<T> startNode = graph.getVertex(startValue);

        List<List<UnweightedNode<T>>> result = new LinkedList<>(); // Хранение рёбер
        Set<UnweightedNode<T>> visited = new HashSet<>();
        Queue<UnweightedNode<T>> queue = new LinkedList<>();

        visited.add(startNode);
        queue.add(startNode);

        while (!queue.isEmpty()) {
            UnweightedNode<T> current = queue.poll();

            for (UnweightedNode<T> neighbor : current.getNeighbors()) {
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

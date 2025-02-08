package practice_3.question_2;

import lombok.extern.slf4j.Slf4j;
import practice_3.core.AbstractUnweightedGraph;
import practice_3.core.UnweightedNode;

import java.util.*;

@Slf4j
public class DepthFirstSearch {

    /**
     * Выполняет обход в глубину (DFS) от заданной вершины.
     *
     * @param startValue стартовое значение вершины.
     * @param graph      объект графа.
     * @param <T>        тип значения вершины.
     * @return список, представляющий путь обхода.
     */
    public static <T extends Comparable<T>> List<T> execute(T startValue, AbstractUnweightedGraph<T> graph) {
        if (graph == null || graph.getVertex(startValue) == null) {
            throw new IllegalArgumentException("Graph is null or start vertex not found: " + startValue);
        }

        List<T> path = new ArrayList<>();
        Set<UnweightedNode<T>> visited = new HashSet<>();
        UnweightedNode<T> startNode = graph.getVertex(startValue);

        log.debug("Start node = {}", startNode);

        dfsRecursive(startNode, visited, path);

        return path;
    }

    /**
     * Рекурсивный метод для выполнения DFS.
     *
     * @param current текущая вершина.
     * @param visited множество посещённых вершин.
     * @param path    путь обхода.
     * @param <T>     тип значения вершины.
     */
    private static <T extends Comparable<T>> void dfsRecursive(UnweightedNode<T> current, Set<UnweightedNode<T>> visited, List<T> path) {
        visited.add(current);
        path.add(current.getValue());

        log.debug("Current node = {}, path = {}", current, path);

        for (UnweightedNode<T> neighbor : current.getNeighbors()) {
            if (!visited.contains(neighbor)) {
                dfsRecursive(neighbor, visited, path);
            }
        }
    }
}

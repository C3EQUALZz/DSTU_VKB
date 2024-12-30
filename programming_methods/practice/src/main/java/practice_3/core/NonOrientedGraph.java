/**
 * Измените программу bfs.java (см. листинг 13.2) так, чтобы для поиска минимального остовного дерева применялся
 * алгоритм обхода в ширину вместо обхода в глубину из программы mst.java (см. листинг 13.3).
 * Создайте в методе main() граф с 9 вершинами и 12 ребрами, постройте его минимальное остовное дерево.
 */


package practice_3.core;

public class NonOrientedGraph<T extends Comparable<T>> extends AbstractUnweightedGraph<T> {

    public NonOrientedGraph() {
        super();
    }

    /**
     * Добавляет ребро между двумя вершинами (без направления)
     *
     * @param start начальная вершина
     * @param end   конечная вершина
     */
    public void addEdge(T start, T end) {
        UnweightedNode<T> startNode = vertices.computeIfAbsent(start, UnweightedNode::new);
        UnweightedNode<T> endNode = vertices.computeIfAbsent(end, UnweightedNode::new);

        startNode.connect(endNode);
        endNode.connect(startNode);
    }
}


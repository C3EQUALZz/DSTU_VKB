/**
 * Задание №2.
 * Измените программу dfs.java (см. листинг 13.1), чтобы она выводила таблицу связности для направленного графа.
 */

package practice_3.core;


public class OrientedGraph<T extends Comparable<T>> extends AbstractUnweightedGraph<T> {

    public OrientedGraph() {
        super();
    }

    /**
     * Добавление ребра между двумя вершинами (без направления)
     */
    @Override
    public void addEdge(T start, T end) {
        UnweightedNode<T> startNode = vertices.computeIfAbsent(start, UnweightedNode::new);
        UnweightedNode<T> endNode = vertices.computeIfAbsent(end, UnweightedNode::new);
        startNode.connect(endNode);
    }



}

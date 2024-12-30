package practice_4.question_1;

import java.util.*;

class Graph<T extends Comparable<T>> {
    private final Map<T, Node<T>> nodes; // Словарь для хранения вершин

    public Graph() {
        this.nodes = new HashMap<>();
    }

    /**
     * Добавить ребро между вершинами
     *
     * @param from   начальная вершина
     * @param to     конечная вершина
     * @param weight вес ребра
     */
    public void addEdge(T from, T to, int weight) {
        nodes.putIfAbsent(from, new Node<>(from));
        nodes.putIfAbsent(to, new Node<>(to));
        nodes.get(from).connect(nodes.get(to), weight);
    }

    /**
     * Метод, который выполняет алгоритм Флойда-Уоршелла.
     * @return Возвращает матрицу кратчайших расстояний.
     */
    public Map<T, Map<T, Integer>> floydWarshall() {
        Map<T, Map<T, Integer>> distances = new HashMap<>();

        // Инициализация матрицы расстояний
        for (T from : nodes.keySet()) {
            distances.putIfAbsent(from, new HashMap<>());
            for (T to : nodes.keySet()) {
                if (from.equals(to)) {
                    distances.get(from).put(to, 0); // Расстояние до самой себя
                } else {
                    distances.get(from).put(to, Integer.MAX_VALUE); // Изначально пути нет
                }
            }

            // Установка весов для соседей
            for (Map.Entry<Node<T>, Integer> neighbor : nodes.get(from).getNeighbors().entrySet()) {
                distances.get(from).put(neighbor.getKey().getValue(), neighbor.getValue());
            }
        }

        // Основной алгоритм
        for (T k : nodes.keySet()) { // Промежуточная вершина
            for (T i : nodes.keySet()) { // Начальная вершина
                for (T j : nodes.keySet()) { // Конечная вершина
                    if (distances.get(i).get(k) != Integer.MAX_VALUE && distances.get(k).get(j) != Integer.MAX_VALUE) {
                        var newDist = distances.get(i).get(k) + distances.get(k).get(j);
                        if (newDist < distances.get(i).get(j)) {
                            distances.get(i).put(j, newDist);
                        }
                    }
                }
            }
        }

        return distances;
    }

}

/**
 * Задание №2.
 * Измените программу dfs.java (см. листинг 13.1), чтобы она выводила таблицу связности для направленного графа.
 */

package practice_3.question_2;

import utils.PrettyTable;

import java.util.*;

class Graph<T extends Comparable<T>> {
    private final Map<T, Node<T>> vertices; // Словарь для хранения вершин по их значениям

    public Graph() {
        this.vertices = new HashMap<>();
    }

    /**
     * Добавление ребра между двумя вершинами (без направления)
     */
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

    /**
     * Метод toString для вывода графа в виде списка смежности
     */
    @Override
    public String toString() {
        // Создаем список всех вершин графа
        List<T> verticesList = new ArrayList<>(vertices.keySet());

        // Создаем массив заголовков с первой пустой ячейкой
        String[] headers = new String[verticesList.size() + 1];  // +1 для пустой ячейки в левом верхнем углу
        headers[0] = "";  // Пустая ячейка в левом верхнем углу
        for (int i = 0; i < verticesList.size(); i++) {
            headers[i + 1] = verticesList.get(i).toString();  // Вставляем вершины в заголовки
        }

        // Передаем вершины в конструктор PrettyTable с добавленной пустой ячейкой
        PrettyTable table = new PrettyTable(headers);

        // Заполняем строки таблицы для каждой вершины
        for (T vertex : verticesList) {
            Node<T> node = vertices.get(vertex);
            List<String> row = new ArrayList<>();

            // Добавляем вершину в начало строки
            row.add(vertex.toString());

            // Для каждой вершины добавляем 1 или 0, если существует ребро
            for (T otherVertex : verticesList) {
                if (node.getNeighbors().stream().anyMatch(neighbor -> neighbor.getValue().equals(otherVertex))) {
                    row.add("1");  // Есть ребро между вершинами
                } else {
                    row.add("0");  // Нет ребра между вершинами
                }
            }

            // Добавляем строку в таблицу
            table.addRow(row.toArray(new String[0]));
        }

        return table.toString();
    }


}

package practice_3.core;

import lombok.AllArgsConstructor;
import utils.PrettyTable;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@AllArgsConstructor
public abstract class AbstractUnweightedGraph<T extends Comparable<T>> {
    protected final Map<T, Node<T>> vertices; // Словарь для хранения вершин по их значениям

    protected AbstractUnweightedGraph() {
        this.vertices = new HashMap<>();
    }

    public abstract void addEdge(T start, T end);


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

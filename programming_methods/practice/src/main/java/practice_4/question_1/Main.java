package practice_4.question_1;

import utils.PrettyTable;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

class Main {
    public static void main(String[] args) {
        Graph<String> graph = new Graph<>();
        graph.addEdge("A", "B", 50);
        graph.addEdge("A", "D", 80);
        graph.addEdge("B", "C", 60);
        graph.addEdge("B", "D", 90);
        graph.addEdge("C", "E", 40);
        graph.addEdge("D", "C", 20);
        graph.addEdge("D", "E", 70);
        graph.addEdge("E", "B", 50);

        Map<String, Map<String, Integer>> distances = graph.floydWarshall();

        var verticesList = new ArrayList<>(distances.keySet());

        String[] headers = new String[verticesList.size() + 1];
        headers[0] = "";
        for (int i = 0; i < verticesList.size(); i++) {
            headers[i + 1] = verticesList.get(i);
        }

        PrettyTable table = new PrettyTable(headers);

        // Заполняем строки таблицы
        for (var from : verticesList) {
            List<String> row = new ArrayList<>();
            row.add(from);

            for (var to : verticesList) {
                int distance = distances.get(from).get(to);
                row.add(distance == Integer.MAX_VALUE ? "INF" : String.valueOf(distance));
            }

            table.addRow(row.toArray(new String[0]));
        }

        // Печатаем таблицу
        System.out.println(table);

    }
}

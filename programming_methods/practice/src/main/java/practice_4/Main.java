package practice_4;

import practice_4.question_1.FloydWarshall;
import practice_4.question_1.OrientedGraph;
import utils.PrettyTable;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

class Main {
    public static void main(String[] args) {
        OrientedGraph<String> orientedGraph = new OrientedGraph<>();
        orientedGraph.addEdge("A", "B", 50);
        orientedGraph.addEdge("A", "D", 80);
        orientedGraph.addEdge("B", "C", 60);
        orientedGraph.addEdge("B", "D", 90);
        orientedGraph.addEdge("C", "E", 40);
        orientedGraph.addEdge("D", "C", 20);
        orientedGraph.addEdge("D", "E", 70);
        orientedGraph.addEdge("E", "B", 50);

        Map<String, Map<String, Integer>> distances = FloydWarshall.execute(orientedGraph);

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

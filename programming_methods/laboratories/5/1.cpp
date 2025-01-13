#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <deque>
#include <tuple>
#include <algorithm>

using namespace std;

class TravelingSalesmanGraph {
public:
    TravelingSalesmanGraph(const vector<pair<double, double>>& coordinates)
        : num_vertices(coordinates.size()), coordinates(coordinates) {
        distance_matrix.resize(1 << num_vertices, vector<double>(num_vertices, numeric_limits<double>::infinity()));
        distance_matrix[1][0] = 0.0; // Начальная вершина посещена, длина пути 0
        initialize_distance_matrix();
    }

    int get_num_vertices() const {
        return num_vertices;
    }

    pair<double, int> find_shortest_path_length() {
        int final_mask = (1 << num_vertices) - 1;
        double min_distance = numeric_limits<double>::infinity();
        int end_vertex = -1;
        for (int u = 1; u < num_vertices; ++u) {
            double distance = distance_matrix[final_mask][u] + calculate_distance(u, 0);
            if (distance < min_distance) {
                min_distance = distance;
                end_vertex = u;
            }
        }
        return {min_distance, end_vertex};
    }

    vector<int> reconstruct_path(int end_vertex, int final_mask) {
        deque<int> path;
        int mask = final_mask;
        int current_vertex = end_vertex;

        while (current_vertex != 0) {
            path.push_front(current_vertex);
            double current_distance = distance_matrix[mask][current_vertex];
            for (int prev_vertex = 0; prev_vertex < num_vertices; ++prev_vertex) {
                if ((mask & (1 << prev_vertex)) &&
                    abs(current_distance - (distance_matrix[mask ^ (1 << current_vertex)][prev_vertex] + calculate_distance(prev_vertex, current_vertex))) < 1e-9) {
                    current_vertex = prev_vertex;
                    mask ^= (1 << path.front());
                    break;
                }
            }
        }

        vector<int> result(path.begin(), path.end());
        return result;
    }

private:
    int num_vertices;
    vector<pair<double, double>> coordinates;
    vector<vector<double>> distance_matrix;

    void initialize_distance_matrix() {
        for (int mask = 0; mask < (1 << num_vertices); ++mask) {
            for (int u = 0; u < num_vertices; ++u) {
                if (!(mask & (1 << u))) continue;
                double current_distance = distance_matrix[mask][u];
                for (int v = 0; v < num_vertices; ++v) {
                    if (!(mask & (1 << v))) {
                        int next_mask = mask | (1 << v);
                        double new_distance = current_distance + calculate_distance(u, v);
                        distance_matrix[next_mask][v] = min(distance_matrix[next_mask][v], new_distance);
                    }
                }
            }
        }
    }

    double calculate_distance(int u, int v) {
        double dx = coordinates[u].first - coordinates[v].first;
        double dy = coordinates[u].second - coordinates[v].second;
        return sqrt(dx * dx + dy * dy);
    }
};

pair<double, vector<int>> find_optimal_tour(const vector<pair<double, double>>& coordinates) {
    TravelingSalesmanGraph graph(coordinates);
    auto [shortest_path_length, end_vertex] = graph.find_shortest_path_length();
    auto path = graph.reconstruct_path(end_vertex, (1 << graph.get_num_vertices()) - 1);
    for (int& vertex : path) {
        vertex += 1; // Преобразование индекса в 1-based
    }
    return {shortest_path_length, path};
}

int main() {
    int num_vertices;
    cin >> num_vertices;

    vector<pair<double, double>> coordinates(num_vertices);
    for (int i = 0; i < num_vertices; ++i) {
        cin >> coordinates[i].first >> coordinates[i].second;
    }

    auto [shortest_path_length, optimal_path] = find_optimal_tour(coordinates);

    cout.precision(14);
    cout << fixed << shortest_path_length << endl;
    for (size_t i = 0; i < optimal_path.size(); ++i) {
        if (i > 0) cout << " ";
        cout << optimal_path[i];
    }
    cout << endl;

    return 0;
}

#include <iostream>
#include <vector>
#include <queue>
#include <climits>

size_t n, m;
const long long INF = LONG_LONG_MAX;

struct Edge {
    int from, to;
    long long flow, cap;
    int reversed = -1;

    Edge(int from, int to, long long f, long long cap) : from(from), to(to), flow(f), cap(cap) {}
};

std::vector<std::vector<Edge>> edges;
std::vector<long long> d;
std::vector<int> id;
std::vector<Edge*> p;

void addEdge(int from, int to, long long flow, long long cap) {
    Edge edge = Edge(from, to, flow, cap);
    Edge rev = Edge(to, from, flow, 0);

    edges[from].push_back(edge);
    edges[to].push_back(rev);

    edges[from].back().reversed = edges[to].size() - 1;
    edges[to].back().reversed = edges[from].size() - 1;
}

long long dinicAlgorithm() {
    long long maxFlow = 0;
    while (true) {
        // Очереди для BFS
        std::queue<int> q1, q2;
        id.assign(n + 1, 0);
        d.assign(n + 1, INF);
        p.resize(n + 1);

        // Инициализация BFS
        d[1] = 0;
        q1.push(1);
        id[1] = 1;

        while (!q1.empty() || !q2.empty()) {
            // Обрабатываем первую очередь
            if (!q1.empty()) {
                int u = q1.front();
                q1.pop();
                id[u] = 2;

                for (Edge& edge : edges[u]) {
                    if (edge.flow < edge.cap && d[edge.to] > d[edge.from] + 1) {
                        d[edge.to] = d[edge.from] + 1;
                        if (id[edge.to] == 0) {
                            q2.push(edge.to); // Переводим в очередь q2 для дальнейшей обработки
                            id[edge.to] = 1;
                            p[edge.to] = &edge;
                        }
                    }
                }
            }

            // Обрабатываем вторую очередь
            if (!q2.empty()) {
                int u = q2.front();
                q2.pop();
                id[u] = 2;

                for (Edge& edge : edges[u]) {
                    if (edge.flow < edge.cap && d[edge.to] > d[edge.from] + 1) {
                        d[edge.to] = d[edge.from] + 1;
                        if (id[edge.to] == 0) {
                            q1.push(edge.to); // Переводим обратно в очередь q1
                            id[edge.to] = 1;
                            p[edge.to] = &edge;
                        }
                    }
                }
            }
        }

        long long del = INF;
        if (d[n] == INF) {
            break;
        } else {
            for (int u = n; u != 1; u = p[u]->from) {
                Edge* edge = p[u];
                del = std::min(del, edge->cap - edge->flow);
            }

            // Обновление потоков
            for (int u = n; u != 1; u = p[u]->from) {
                Edge* edge = p[u];
                Edge* reversed = &edges[edge->to][edge->reversed];

                edge->flow += del;
                reversed->flow -= del;
            }

            maxFlow += del;
        }
    }

    return maxFlow;
}

int main() {
    std::cin >> n >> m;
    edges.assign(n + 1, std::vector<Edge>());

    // Чтение рёбер
    for (int i = 0; i < m; ++i) {
        int from, to;
        long long cap;
        std::cin >> from >> to >> cap;

        addEdge(from, to, 0, cap);
    }

    // Вывод максимального потока
    std::cout << dinicAlgorithm() << std::endl;
    return 0;
}

#include <iostream>
#include <vector>

using namespace std;

bool isAvailable(const vector<int>& segments, int x, int y, int k) {
    // Проверяет, есть ли хотя бы одно свободное место на участке [x, y).
    for (int i = x; i < y; ++i) {
        if (segments[i] >= k) {
            return false;
        }
    }
    return true;
}

void processRequests(int n, int k, const vector<pair<int, int>>& requests) {
    vector<int> segments(n + 1, 0);  // Инициализируем массив мест

    for (const auto& req : requests) {
        int x = req.first;
        int y = req.second;

        if (isAvailable(segments, x, y, k)) {
            // Если есть свободное место, продаем билет и увеличиваем занятые места
            for (int i = x; i < y; ++i) {
                segments[i]++;
            }
            cout << 1 << endl;
        } else {
            cout << 0 << endl;
        }
    }
}

int main() {
    int n, k, m;
    cin >> n >> k >> m;  // Ввод данных

    vector<pair<int, int>> requests(m);
    for (int i = 0; i < m; ++i) {
        cin >> requests[i].first >> requests[i].second;  // Ввод запросов
    }

    processRequests(n, k, requests);  // Обработка запросов

    return 0;
}

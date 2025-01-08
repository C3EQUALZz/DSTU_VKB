#include <iostream>
#include <deque>
#include <vector>

int main() {
    int n, m;
    std::cin >> n >> m;

    std::deque<int> soldiers(n);
    for (int i = 0; i < n; ++i) {
        soldiers[i] = i + 1;
    }

    for (int i = 0; i < m; ++i) {
        int li, ri;
        std::cin >> li >> ri;
        --li; // Приводим к 0-индексации
        --ri; // Приводим к 0-индексации

        // Перемещаем солдат с li по ri в начало строя
        std::deque<int> segment(soldiers.begin() + li, soldiers.begin() + ri + 1);
        soldiers.erase(soldiers.begin() + li, soldiers.begin() + ri + 1);
        soldiers.insert(soldiers.begin(), segment.begin(), segment.end());
    }

    for (int soldier : soldiers) {
        std::cout << soldier << " ";
    }
    std::cout << std::endl;

    return 0;
}

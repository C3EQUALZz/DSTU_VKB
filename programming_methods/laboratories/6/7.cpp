#include <iostream>
#include <vector>
#include <string>

int main() {
    int n, m;
    std::cin >> n >> m;
    std::string particles;
    std::cin >> particles;

    std::vector<int> indexes(n);
    for (int i = 0; i < n; ++i) {
        indexes[i] = i;
    }

    for (int i = 0; i < m; ++i) {
        std::string action;
        std::cin >> action;

        if (action == "a") {
            int x, y;
            std::cin >> x >> y;
            --x; // Приводим к 0-индексации
            --y; // Приводим к 0-индексации

            // Перемещаем элемент x в позицию y
            if (x != y) {
                int temp = indexes[x];
                if (x < y) {
                    for (int j = x; j < y; ++j) {
                        indexes[j] = indexes[j + 1];
                    }
                } else {
                    for (int j = x; j > y; --j) {
                        indexes[j] = indexes[j - 1];
                    }
                }
                indexes[y] = temp;
            }
        } else {
            int k;
            std::cin >> k;
            --k; // Приводим к 0-индексации
            std::cout << particles[indexes[k]] << std::endl;
        }
    }

    return 0;
}

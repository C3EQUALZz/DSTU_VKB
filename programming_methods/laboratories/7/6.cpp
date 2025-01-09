#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// Проверяет, является ли прямоугольник симметричным относительно его центра
bool is_symmetric(const vector<string>& grid, int top, int bottom, int left, int right) {
    int rows = bottom - top + 1;
    int cols = right - left + 1;

    // Проверяем симметрию сверху вниз
    for (int i = 0; i <= rows / 2; ++i) {
        string topRow = grid[top + i].substr(left, cols);
        string bottomRow = grid[bottom - i].substr(left, cols);
        reverse(bottomRow.begin(), bottomRow.end());
        if (topRow != bottomRow) {
            return false;
        }
    }
    return true;
}

// Подсчитывает количество симпатичных прямоугольников
int count_pretty_rectangles(const vector<string>& grid, int n, int m) {
    int count = 0;

    // Перебор всех возможных прямоугольников
    for (int top = 0; top < n; ++top) {
        for (int bottom = top; bottom < n; ++bottom) {
            for (int left = 0; left < m; ++left) {
                for (int right = left; right < m; ++right) {
                    if (is_symmetric(grid, top, bottom, left, right)) {
                        ++count;
                    }
                }
            }
        }
    }

    return count;
}

int main() {
    // Ввод данных
    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
    }

    // Вычисление и вывод результата
    int result = count_pretty_rectangles(grid, n, m);
    cout << result << endl;

    return 0;
}
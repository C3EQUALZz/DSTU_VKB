#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main() {
    int k, n;
    cin >> k >> n;

    vector<int> cockroach(k);           // Перестановка тараканов
    vector<vector<int>> Rates(n, vector<int>(4)); // Ставки болельщиков

    // Считываем ставки
    for (int i = 0; i < n; i++) {
        cin >> Rates[i][0] >> Rates[i][1] >> Rates[i][2] >> Rates[i][3];
    }

    // Инициализация первой перестановки
    for (int i = 0; i < k; i++) {
        cockroach[i] = i + 1;
    }

    // Перебор всех перестановок
    do {
        bool valid = true; // Флаг для проверки условий ставок

        // Создаем массив позиций для быстрого доступа
        vector<int> positions(k + 1);
        for (int i = 0; i < k; i++) {
            positions[cockroach[i]] = i;
        }

        // Проверяем каждую ставку
        for (int i = 0; i < n; i++) {
            int a = Rates[i][0], b = Rates[i][1], c = Rates[i][2], d = Rates[i][3];

            // Индексы тараканов
            int index_a = positions[a];
            int index_b = positions[b];
            int index_c = positions[c];
            int index_d = positions[d];

            // Условия ставок
            bool condition1 = (index_a < index_b); // A до B
            bool condition2 = (index_c < index_d); // C до D

            // Проверяем, чтобы ровно одно из условий было выполнено
            if ((condition1 && condition2) || (!condition1 && !condition2)) {
                valid = false;
                break;
            }
        }

        // Если все ставки выполнены, выводим результат
        if (valid) {
            for (int i = 0; i < k; i++) {
                cout << cockroach[i] << " ";
            }
            cout << endl;
            return 0;
        }

    } while (next_permutation(cockroach.begin(), cockroach.end()));

    // Если не нашли подходящей перестановки
    cout << 0 << endl;
    return 0;
}

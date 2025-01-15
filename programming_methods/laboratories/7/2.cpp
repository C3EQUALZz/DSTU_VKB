#include <iostream>
#include <vector>
#include <cmath>
#include <sstream>

using namespace std;

class StringHash {
private:
    const long X = 257;
    const long P = 1000000007;
    vector<long> hDir;
    vector<long> hRev;
    vector<long> x;

public:
    StringHash(const vector<int>& digits) {
        int len = digits.size();
        hDir.resize(len + 1);
        hRev.resize(len + 1);
        x.resize(len + 1);
        x[0] = 1;

        // Вычисляем хеши и степени X
        for (int i = 1; i <= len; i++) {
            hDir[i] = (hDir[i - 1] * X + digits[i - 1]) % P;
            hRev[i] = (hRev[i - 1] * X + digits[len - i]) % P;
            x[i] = (x[i - 1] * X) % P;
        }
    }

    bool isEqualRev(int len, int from1, int from2) {
        // Сравниваем хеши зеркальных префиксов
        long one = (hDir[from1 + len] + hRev[hRev.size() - 1 - from2 - len] * x[len]) % P;
        long two = (hRev[hRev.size() - 1 - len] + hDir[from1] * x[len]) % P;
        return one == two;
    }
};

int main() {
    int n, m;
    cin >> n >> m;

    vector<int> digits(n);
    for (int i = 0; i < n; i++) {
        cin >> digits[i];
    }

    StringHash sH(digits);
    stringstream result;

    // Проверяем все возможные длины префиксов
    for (int i = n / 2; i > 0; i--) {
        if (sH.isEqualRev(i, 0, i)) {
            result << n - i << " ";
        }
    }
    result << n;

    // Выводим результат
    cout << result.str() << endl;

    return 0;
}

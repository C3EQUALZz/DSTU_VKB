#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1e5 + 5;
int a[MAXN], t[4*MAXN], lazy[4*MAXN];

//само построение дерева
void build(int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = a[tl];
    } else {
        int tm = (tl + tr) / 2;
        build(v*2, tl, tm);
        build(v*2+1, tm+1, tr);
        t[v] = min(t[v*2], t[v*2+1]);
    }
}

//применение отложенных операций
void push(int v, int tl, int tr) {
    if (lazy[v]) {
        int tm = (tl + tr) / 2;
        reverse(a + tl, a + tm + 1);
        reverse(a + tm + 1, a + tr + 1);
        lazy[v*2] ^= 1;
        lazy[v*2+1] ^= 1;
        lazy[v] = 0;
    }
}

//переворачивание отрезка
void reverse(int v, int tl, int tr, int l, int r) {
    if (l > r)
        return;
    if (l == tl && r == tr) {
        lazy[v] ^= 1;
    } else {
        push(v, tl, tr);
        int tm = (tl + tr) / 2;
        reverse(v*2, tl, tm, l, min(r, tm));
        reverse(v*2+1, tm+1, tr, max(l, tm+1), r);
        t[v] = min(t[v*2], t[v*2+1]);
    }
}

//нахождение минимума на отрезке
int minimum(int v, int tl, int tr, int l, int r) {
    if (l > r)
        return INT_MAX;
    if (l <= tl && tr <= r)
        return t[v];
    push(v, tl, tr);
    int tm = (tl + tr) / 2;
    return min(minimum(v*2, tl, tm, l, min(r, tm)),
               minimum(v*2+1, tm+1, tr, max(l, tm+1), r));
}

int main() {
    ifstream fin("input.txt");
    int n, m;
    fin >> n >> m;
    for (int i = 0; i < n; ++i) {
        fin >> a[i];
    }
    build(1, 0, n-1);
    while (m--) {
        int type, l, r;
        fin >> type >> l >> r;
        --l; --r;
        if (type == 1) {
            reverse(1, 0, n-1, l, r);
        } else {
            cout << minimum(1, 0, n-1, l, r) << "\n";
        }
    }
    fin.close();
    return 0;
}
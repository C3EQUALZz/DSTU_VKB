#include <bits/stdc++.h>
using namespace std;
//#define int int64_t
void solve() {
    string s;
    cin >> s;
    int n = int(s.size());
    vector<int> x(n);
    for (int i = 0; i < n; i++) {
        x[i] = int(s[i] - '0');
    }
    vector<vector<int>> blocks;
    int cur_block = 0;
    blocks.push_back({});
    vector<bool> cnt(10, false);
    for (int i = n - 1; i >= 0; i--) {
        cnt[x[i]] = true;
        blocks[cur_block].push_back(x[i]);
        bool check_all = true;
        for (int j = 0; j < 10; j++) {
            if (cnt[j] == false) {
                check_all = false;
                break;
            }
        }
        if (check_all) {
            cur_block++;
            blocks.push_back({});
            for (int j = 0; j < 10; j++) {
                cnt[j] = false;
            }
        }
    }
    for (int i = 0; i <= cur_block; i++) {
        reverse(blocks[i].begin(), blocks[i].end());
    }
    /*for (auto to : blocks) {
        for (auto to2 : to) {
            cout << to2;
        }
        cout << '\n';
    }*/
    for (int j = 0; j < 10; j++) {
        cnt[j] = false;
    }
    for (auto num : blocks[cur_block]) {
        cnt[num] = true;
    }
    int first_digit = 0;
    for (int j = 1; j < 10; j++) {
        if (cnt[j] == false) {
            first_digit = j;
            break;
        }
    }
    if (first_digit == 0) {
        cout << 10;
    }
    else {
        cout << first_digit;
    }
    int cur_digit = first_digit;
    for (int i = cur_block - 1; i >= 0; i--) {
        for (int j = 0; j < 10; j++) {
            cnt[j] = false;
        }
        bool ff = true;
        for (auto digit : blocks[i]) {
            if (ff == false) {
                cnt[digit] = true;
            }
            if (digit == cur_digit && ff == true) {
                ff = false;
            }
        }
        for (int j = 0; j < 10; j++) {
            if (cnt[j] == false) {
                cout << j;
                cur_digit = j;
                break;
            }
        }
    }
}
int32_t main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    //freopen("inputik.txt", "r", stdin);
    //freopen("outputik.txt", "w", stdout);
    int t = 1;
    //cin >> t;
    while (t--) {
        solve();
    }
}

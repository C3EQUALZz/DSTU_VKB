#include <bits/stdc++.h>
using namespace std;
#define int int64_t
mt19937 rnd(int(3131));
struct Node {
    int val;
    int prior;
    int l, r;
    int sz;
};
vector<Node> a(0);
int new_(int u) {
    int gg=a.size();
    a.push_back({});
    a[gg].val=u;
    a[gg].sz=1;
    a[gg].prior=rnd();
    a[gg].l=-1, a[gg].r=-1;
    return gg;
}
int size_(int u) {
    if(u==-1) {
        return 0;
    }
    return a[u].sz;
}
void upd(int u) {
    if(u==-1) {
        return;
    }
    a[u].sz=size_(a[u].l)+size_(a[u].r)+1;
}
int root=-1;
int merge_(int l, int r) {
    upd(l);
    upd(r);
    if(l==-1) {
        return r;
    }
    if(r==-1) {
        return l;
    }
    if(a[l].prior>a[r].prior) {
        a[l].r=merge_(a[l].r, r);
        upd(l);
        return l;
    }
    else {
        a[r].l=merge_(l, a[r].l);
        upd(r);
        return r;
    }
}
pair<int, int> split(int u, int k) {
    if(u==-1) {
        return {-1, -1};
    }
    upd(u);
    if(size_(a[u].l)+1<=k) {
        pair<int, int> w=split(a[u].r, k-size_(a[u].l)-1);
        a[u].r=w.first;
        upd(u);
        return {u, w.second};
    }
    else {
        pair<int, int> w=split(a[u].l, k);
        a[u].l=w.second;
        upd(u);
        return {w.first, u};
    }
}
void get(int u) {
    if(u==-1) {
        return;
    }
    get(a[u].l);
    cout << a[u].val << ' ';
    get(a[u].r);
}
void sol() {
    int n,m;
    cin >> n >> m;
    for(int i=1;i<=n;i++) {
        root=merge_(root, new_(i));
    }
    for(int q=1;q<=m;q++) {
        int l,r;
        cin >> l >> r;
        pair<int, int> w=split(root, r);
        pair<int, int> g=split(w.first, l-1);
        root=merge_(merge_(g.second, g.first), w.second);
    }
    get(root);
}
int32_t main() {
    /*ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);*/
    //freopen("movetofront.in", "r", stdin);
    //freopen("movetofront.out", "w", stdout);
    int t=1;
    //cin >> t;
    while (t--) {
        sol();
    }
}

/* 1960 */
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <map>
using namespace std;

#define MAXN 100005

_int64 a[MAXN];

int main() {
    int t;
    int n, m;
    int i, j, k;
    __int64 x, ans;
    
    #ifndef ONLINE_JUDGE
        freopen("data.in", "r", stdin);
        freopen("data.out", "w", stdout);
    #endif
    
    scanf("%d", &t);
    while (t--) {
        scanf("%d %d", &n, &k);
        map<int, int> tb;
        m = 0;
        for (i=0; i<n; ++i) {
            scanf("%I64d", &x);
            if (tb[x] == 0) {
                tb[x] = 1;
                a[m++] = x;
            }
        }
        
        ans = 0;
        for (i=0; i<m; ++i) {
            if (a[i]<=k && tb[k-a[i]]==1) {
                ++ans;
            }
        }
        printf("%I64d\n", ans);
    }
    
    return 0;
}
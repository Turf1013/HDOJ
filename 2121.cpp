/* 2121 */
#include <cstdio>
#include <cstring>

#define MAXN 1005

int pre[MAXN], ans;

int find(int x) {
    return x==pre[x] ? x:find(pre[x]);
}

void merge(int a, int b, int c) {
    a = find(a);
    b = find(b);
    if (a != b) {
        if (a > b)
            pre[a] = b;
        else
            pre[b] = a;
        ans += c;
    }
}

int main() {
    int n, m;
    int i, j, k;

    while (scanf("%d %d",&n,&m) != EOF) {
        ans = 0;
        for (i=0; i<n; ++i)
            pre[i] = i;
        while (m--) {
            scanf("%d %d %d", &i, &j, &k);
            merge(i, j, k);
        }
        k = find(0);
        j = 1;
        for (i=1; i<n; ++i)
            if (find(i) != k) {
                j = 0;
                break;
            }
        if (j)
            printf("%d %d\n\n", ans, k);
        else
            printf("impossible\n\n");
    }

    return 0;
}


/* 5020 */
#include <cstdio>
#include <cstring>
#include <cstdlib>

#define MAXN 1005

typedef struct {
    __int64 x, y;
} Point_t;

Point_t Ps[MAXN];
Point_t D[500005];
__int64 delta[500005];

__int64 chaji(Point_t p1, Point_t p2) {
    return p1.x*p2.y - p2.x*p1.y;
}

int main() {
    int t, n;
    int i, j, m, p, q;
    __int64 ans, k=0;

    for (i=1; i<1000; ++i)
        for (j=0; j<i; ++j,++k)
            delta[k+j] = k+j+i;

    scanf("%d", &t);
    while (t--) {
        scanf("%d", &n);
        m = 0;
        for (i=0; i<n; ++i) {
            scanf("%I64d %I64d", &Ps[i].x, &Ps[i].y);
            for (j=0; j<i; ++j) {
                D[m].x = Ps[i].x - Ps[j].x;
                D[m].y = Ps[i].y - Ps[j].y;
                ++m;
            }
        }
        ans = 0;
        for (i=0; i<m; i=delta[i]) {
            for (j=delta[i]; j<m; j=delta[j])
                if (chaji(D[i], D[j]) == 0)
                    ++ans;
        }
        printf("%I64d\n", ans);
    }

    return 0;
}
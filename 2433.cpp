/* 2433 */
#include <cstdio>
#include <cstring>

#define MAXN 105
#define MAXM 3005
#define INF  0x3fffffff

int buf[MAXM][2];
int map[MAXN][MAXN], m, n;
bool visit[MAXN];
int set[MAXN];

int dijkstra(int x) {
    int i, j, min, v, ans=0;

    memset(visit, false, sizeof(visit));
    visit[x] = true;
    for (i=1; i<=n; ++i)
        if (map[x][i] == 0)
            set[i] = INF;
        else
            set[i] = 1;
    set[x] = 0;

    for (i=1; i<n; ++i) {
        min = INF;
        for (j=1; j<=n; ++j) {
            if (!visit[j] && set[j]<min) {
                v = j;
                min = set[j];
            }
        }
        if (min == INF)
            return INF;
        visit[v] = true;
        for (j=1; j<=n; ++j) {
            if (!visit[j] && map[v][j] && set[j]>min+1)
                set[j] = min + 1;
        }
    }
    for (i=1; i<=n; ++i)
        ans += set[i];
    return ans;
}

int SUM() {
    int i, tmp, ret = 0;

    for (i=1; i<=n; ++i) {
        tmp = dijkstra(i);
        if (tmp == INF) {
           return tmp;
        } else
            ret += tmp;
    }
    return ret;
}

int main() {
    int i, j, k, ans, nsum;

    while (scanf("%d %d", &n, &m) != EOF) {
        memset(map, 0, sizeof(map));
        for (k=0; k<m; ++k) {
            scanf("%d %d", &i, &j);
            ++map[i][j];
            ++map[j][i];
            buf[k][0] = i;
            buf[k][1] = j;
        }
        ans = SUM();
        for (k=0; k<m; ++k) {
            i = buf[k][0];
            j = buf[k][1];
            if (ans == INF)
                nsum = ans;
            else if (map[i][j]-1 > 0)
                nsum = ans;
            else {
                --map[i][j];
                nsum = SUM();
                ++map[i][j];
            }
            if (nsum == INF)
                printf("INF\n");
            else
                printf("%d\n", nsum);
        }
    }

    return 0;
}
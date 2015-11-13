/* 3498 */
#include <iostream>
#include <string>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <vector>
#include <deque>
#include <algorithm>
#include <cstdio>
#include <cmath>
#include <ctime>
#include <cstring>
#include <climits>
#include <cctype>
#include <cassert>
#include <functional>
using namespace std;
//#pragma comment(linker,"/STACK:102400000,1024000")

#define mpii			map<int,int>
#define vi				vector<int>
#define pii				pair<int,int>
#define vpii			vector<pair<int,int> >
#define rep(i, a, n) 	for (int i=a;i<n;++i)
#define per(i, a, n) 	for (int i=n-1;i>=a;--i)
#define pb 				push_back
#define mp 				make_pair
#define fir				first
#define sec				second
#define all(x) 			(x).begin(),(x).end()
#define SZ(x) 			((int)(x).size())
#define lson			l, mid, rt<<1
#define rson			mid+1, r, rt<<1|1

const int maxn = 60;
bool M[maxn][maxn];
set<pii, greater<pii> > Q;
int deg[maxn];
bool visit[maxn];
int a[maxn];

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif
	
	int n, m;
	int u, v;
	int ans = 0;
	
	while (scanf("%d %d", &n, &m)!=EOF) {
		memset(M, false, sizeof(M));
		memset(deg, 0, sizeof(deg));
		memset(visit, false, sizeof(visit));
		while (m--) {
			scanf("%d %d", &u, &v);
			M[u][v] = M[v][u] = true;
		}
		rep(i, 1, n+1) {
			M[i][i] = true;
			rep(j, 1, n+1)
				deg[i] += M[i][j];
			Q.insert(mp(deg[i], i));
		}
		ans = 0;
		while (!Q.empty()) {
			// int d = Q.begin()->fir;
			u = Q.begin()->sec;
			visit[u] = true;
			Q.erase(Q.begin());
			++ans;
			#ifndef ONLINE_JUDGE
				printf("%d: %d\n", ans, u);
			#endif
			m = 0;
			rep(j, 1, n+1) {
				if (!visit[j] && M[u][j]) {
					visit[j] = true;
					a[m++] = j;
					Q.erase(mp(deg[j], j));
				}
			}
			
			rep(i, 0, m) {
				v = a[i];
				rep(j, 1, n+1) {
					if (!visit[j] && M[v][j]) {
						Q.erase(mp(deg[j], j));
						--deg[j];
						Q.insert(mp(deg[j], j));
					}
				}
			}
		}
		printf("%d\n", ans);
	}
	
	#ifndef ONLINE_JUDGE
		printf("time = %d.\n", (int)clock());
	#endif
	
	return 0;
}

// from random import randint
// import string

// with open("data.in", "w") as fout:
	// t = 105
	// for t_ in xrange(t):
		// n = randint(2, 55)
		// m = randint(0, n*n)
		// fout.write("%d %d\n" % (n, m))
		// while m>0:
			// u = randint(1, n)
			// v = randint(1, n)
			// fout.write("%d %d\n" % (u, v))
			// m -= 1
		
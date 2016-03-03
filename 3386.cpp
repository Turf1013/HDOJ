/* 3386 */
// 3385's name is just one word, and need to filter ' '
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
using namespace std;

#define MAXL 205
#define MAXN 205

bool m[MAXN][MAXN];
map<string, int> tb;
map<int, string> rtb;
int rorder[MAXN], order[MAXN];
bool valid[MAXN];
map<string, int>::iterator iter;
char s[MAXL];

int main() {
	int n = 1, t=0, tt;
	int i, j, k, u, v;
	string ss, src;
	
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif
	
	while (gets(s) != NULL) {
		if (strcmp(s, "GRAPH BEGIN") == 0) {
			// init
			if (t++)
				printf("\n");
			memset(m, false, sizeof(m));
			tb.clear();
			rtb.clear();
			n = 1;
			tt = 0;
			while (1) {
				gets(s);
				if (strcmp(s, "GRAPH END") == 0)
					break;
				i = k = u = 0;
				while (1) {
					if (s[i]==' ' || s[i]=='\0') {
						ss = string(s+k, i-k);
						if (tb.find(ss) == tb.end()) {
							rtb[n] = ss;
							tb[ss] = n;
							v = n++;
						} else {
							v = tb[ss];
						}
						if (u == 0) {
							u = v;
						} else {
							m[u][v] = m[v][u] = true;
						}
						k = i+1;
					}
					if (s[i] == '\0')
						break;
					++i;
				}
			}
			// get dict order
			i = 1;
			for (iter=tb.begin(); iter!=tb.end(); ++iter) {
				rorder[iter->second] = i;
				order[i] = iter->second;
				++i;
			}
		} else {
			// output
			u = tb[string(s)];
			memset(valid, false, sizeof(valid));
			for (v=1; v<n; ++v) {
				if (m[u][v]) {
					for (i=1; i<n; ++i) {
						if (m[v][i] && !m[u][i])
							valid[rorder[i]] = true;
					}
				}
			}
			i = 1;
			valid[rorder[u]] = false;
			while (i<n && valid[i] == false)
				++i;
			if (i < n) {
				if (tt)
					printf(" %s", rtb[order[i]].c_str());
				else
					printf("%s", rtb[order[i]].c_str());
				tt = 1;
			}
			while (++i < n) {
				if (valid[i])
					printf(" %s", rtb[order[i]].c_str());
			}
		}
	}
	printf("\n");
	
	return 0;
}
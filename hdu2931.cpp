/*  */
#include <iostream>
#include <sstream>
#include <string>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <vector>
#include <deque>
#include <bitset>
#include <algorithm>
#include <cstdio>
#include <cmath>
#include <ctime>
#include <cstring>
#include <climits>
#include <cctype>
#include <cassert>
#include <functional>
#include <iterator>
#include <iomanip>
using namespace std;
//#pragma comment(linker,"/STACK:102400000,1024000")

#define sti				set<int>
#define stpii			set<pair<int, int> >
#define mpii			map<int,int>
#define vi				vector<int>
#define pii				pair<int,int>
#define vpii			vector<pair<int,int> >
#define rep(i, a, n) 	for (int i=a;i<n;++i)
#define per(i, a, n) 	for (int i=n-1;i>=a;--i)
#define clr				clear
#define pb 				push_back
#define mp 				make_pair
#define fir				first
#define sec				second`
#define all(x) 			(x).begin(),(x).end()
#define SZ(x) 			((int)(x).size())
#define lson			l, mid, rt<<1
#define rson			mid+1, r, rt<<1|1
#define INF				0x3f3f3f3f
#define mset(a, val)	memset(a, (val), sizeof(a))

const int maxn = 10005;
const int maxm = maxn * 4;
const int maxl = 20;
char s[maxl], ss[maxl], sc[maxl], cc[maxl], ccc[maxl];
char sa[3][8];
char srca[8], srcc[8];
char srcax[8], srccx[8];
char sb[3][8];
int bits[3], slen;
vi can1[11];
vi can2[11][11];
int ans, ansx, ansd, ll, clen;
int ln, mxrn;

typedef struct {
	#define RT 1
	int nxt[maxm][11];
	int c[maxm];
	int l;

	inline int newNode() {
		memset(nxt[l], 0, sizeof(nxt[l]));
		c[l] = 0;
		return l++;
	}

	void init() {
		l = 1;
		newNode();
	}

	void clrc() {
		memset(c, 0, sizeof(c));
	}

	void NearSearch(char *s, int d, char *p, int r=RT) {
		if (d < 0)	return ;

		++c[r];
		if (*s < 0)	return ;
		int id = *s;
		if (nxt[r][id]) NearSearch(s+1, *p==id?d:d-1, p+1, nxt[r][id]);
		if (nxt[r][0])	NearSearch(s+1, *p==0?d:d-1, p+1, nxt[r][0]);
	}

	void hard_Insert(char *s, int p=RT) {
		if (*s < 0)	return ;
		int id = *s;
		if (!nxt[p][id]) nxt[p][id] = newNode();
		hard_Insert(s+1, nxt[p][id]);
		if (!nxt[p][0]) nxt[p][0] = newNode();
		hard_Insert(s+1, nxt[p][0]);
	}

	inline bool scmp() {
		rep(j, 0, bits[2]) if (cc[j] < ccc[j])	return true;
		return false;
	}

	void check(int dep, int d, char *p, int r=RT) {
		if (c[r]==0 || d+ln>=ansd)	return ;
		if (*p < 0) {
			if (c[r] == 1) {
				// if (d+ln<ansd || scmp()) {
					ansd = d + ln;
					rep(j, 0, bits[2]) ccc[j] = cc[j];
				// }
			}
			return ;
		}

		rep(i, 0, 11) if (nxt[r][i]) {
			cc[dep] = i;
			check(dep+1, *p==i?d:d+1, p+1, nxt[r][i]);
		}
	}

} trie;

trie tr;

void sprintI(int x) {
	clen = 0;
	while (x) {
		cc[clen++] = x % 10 + 1;
		x /= 10;
	}
	cc[clen] = -1;
	reverse(cc, cc+clen);
}

void Init() {

	tr.init();
	rep(i, 1, 100) {
		rep(j, i, 100) {
			sprintI(i * j);
			tr.hard_Insert(cc);
		}
	}

	rep(i, 1, 10) {
		can1[i+1].pb(i);
		can1[0].pb(i);
	}

	int num = 0;

	rep(i, 0, 10) {
		rep(j, 0, 10) {
			if (i) {
				can2[i+1][j+1].pb(num);
				can2[0][j+1].pb(num);
				can2[i+1][0].pb(num);
				can2[0][0].pb(num);
			}
			++num;
		}
	}
}

inline void getBits() {
	int i, j, k, l;

	i = j = k = l = 0;
	while (i <= slen) {
		if (s[i]==' ' || s[i]=='\0') {
			if (l) {
				s[i] = '\0';
				strcpy(sa[k], s+j);
				bits[k++] = l;
			}
			l = 0;
			j = i + 1;
		} else {
			++l;
		}
		if (i == slen)
			break;

		++i;
	}
}

void nearsearch() {
	mxrn = ans - ln;
	vi &src0 = (bits[0]==1) ? can1[s[0]]:can2[s[0]][s[1]];
	const int& l = bits[0];
	vi &src1 = (bits[1]==1) ? can1[s[l]]:can2[s[l]][s[l+1]];
	int sz[2];

	sz[0] = SZ(src0);
	sz[1] = SZ(src1);

	tr.clrc();
	rep(i, 0, sz[0]) {
		rep(j, 0, sz[1]) {
			sprintI(src0[i] * src1[j]);
			if (clen == bits[2]) {
				tr.NearSearch(cc, mxrn, sc);
			}
		}
	}

	ansd = INF;
	tr.check(0, 0, sc);
}

bool judge1() {
	rep(j, 0, ll) if (s[j] != srca[j])	return s[j]<srca[j];
	rep(j, 0, bits[2]) if (ccc[j] != srcc[j])	return ccc[j]<srcc[j];
	return false;
}

bool judge() {
	rep(j, 0, ll) if (srcax[j] != srca[j])	return srcax[j]<srca[j];
	rep(j, 0, bits[2]) if (srccx[j] != srcc[j])	return srccx[j]<srcc[j];
	return false;
}

void dfs(int dep, int ln) {
	if (ln<0 || ln>ll-dep)	return ;

	if (dep == ll) {
		if (ln == 0) {
			nearsearch();
			// if (ansd < ans || (ansd==ans&&judge1())) {
			// if (ansd < ans) {
			if (ansd < ansx) {
				ansx = ansd;
				rep(j, 0, ll) srcax[j] = s[j];
				rep(j, 0, bits[2]) srccx[j] = ccc[j];
			}
		}
		return ;
	}

	rep(i, 0, 11) {
		s[dep] = i;
		dfs(dep+1, i==ss[dep]?ln:ln-1);
	}
}

void solve() {
	slen = strlen(s);
	getBits();

	int lbits = bits[0] + bits[1];
	ans = INF;

	ll = 0;
	rep(i, 0, 2) {
		rep(j, 0, bits[i])
			ss[ll++] = (sa[i][j]=='*') ? 0:sa[i][j]-'0'+1;
	}
	rep(j, 0, bits[2])
		sc[j] = (sa[2][j]=='*') ? 0:sa[2][j]-'0'+1;
	ss[ll] = s[ll] = sc[bits[2]] = -1;

	for (ln=0; ln<=ans&&ln<=lbits; ++ln) {
		ansx = ans + 1;
		dfs(0, ln);
		if (ansx<ans || (ansx==ans&&judge())) {
			ans = ansx;
			rep(j, 0, ll) srca[j] = srcax[j];
			rep(j, 0, bits[2]) srcc[j] = srccx[j];
		}
	}

	{
		int l = 0;
		rep(i, 0, 2) {
			rep(j, 0, bits[i]) {
				sb[i][j] = srca[l]==0 ? '*':srca[l]+'0'-1;
				++l;
			}
			sb[i][bits[i]] = '\0';
		}

		rep(j, 0, bits[2]) {
			sb[2][j] = srcc[j]==0 ? '*' : srcc[j]+'0'-1;
		}
		sb[2][bits[2]] = '\0';
	}
	printf("%s %s %s\n", sb[0], sb[1], sb[2]);
}

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif

	int tt = 0;

	Init();
	while (gets(s) != NULL) {
		if (s[0]=='0' && s[1]=='\0')
			break;
		printf("Case %d: ", ++tt);
		solve();
	}

	#ifndef ONLINE_JUDGE
		printf("time = %ldms.\n", clock());
	#endif

	return 0;
}
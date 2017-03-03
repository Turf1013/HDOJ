/* 2609 */
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
#pragma comment(linker,"/STACK:102400000,1024000")

#define sti                set<int>
#define stpii            set<pair<int, int> >
#define mpii            map<int,int>
#define vi                vector<int>
#define pii                pair<int,int>
#define vpii            vector<pair<int,int> >
#define rep(i, a, n)     for (int i=a;i<n;++i)
#define per(i, a, n)     for (int i=n-1;i>=a;--i)
#define clr                clear
#define pb                 push_back
#define mp                 make_pair
#define fir                first
#define sec                second
#define all(x)             (x).begin(),(x).end()
#define SZ(x)             ((int)(x).size())
#define lson            l, mid, rt<<1
#define rson            mid+1, r, rt<<1|1

typedef long long LL;
typedef unsigned long long ULL;

typedef struct {
    char a[24];
	short pre;
	short deep;
	
	void print() {
		static char s[] = "*WYROGB";
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		rep(i, 0, 2)	putchar(a[i]), putchar(' ');
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		putchar('\n');

		rep(i, 0, 2)	putchar(' '), putchar(' ');
		rep(i, 2, 4)	putchar(a[i]), putchar(' ');
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		putchar('\n');

		rep(i, 4, 10) 	putchar(a[i]), putchar(' ');
		putchar('\n');
		rep(i, 10, 16) 	putchar(a[i]), putchar(' ');
		putchar('\n');

		rep(i, 0, 2)	putchar(' '), putchar(' ');
		rep(i, 16, 18)	putchar(a[i]), putchar(' ');
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		putchar('\n');

		rep(i, 0, 2)	putchar(' '), putchar(' ');
		rep(i, 18, 20)	putchar(a[i]), putchar(' ');
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		putchar('\n');

		rep(i, 0, 2)	putchar(' '), putchar(' ');
		rep(i, 20, 22)	putchar(a[i]), putchar(' ');
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		putchar('\n');

		rep(i, 0, 2)	putchar(' '), putchar(' ');
		rep(i, 22, 24)	putchar(a[i]), putchar(' ');
		rep(i, 0, 2)	putchar(' '), putchar(' ');
		putchar('\n');

		putchar('\n');
	}
} node_t;

int a[24], b[24];
int n;
int face[6][4] = {
    {0, 1, 2, 3},
    {4, 5, 10, 11},
    {6, 7, 12, 13},
    {8, 9, 14, 15},
    {16, 17, 18, 19},
    {20, 21, 22, 23}
};

int movf[3][12] = {
    {0,1,3,2,         22,23,9,8,7,6,5,4},
    {4,5,11,10,        0,2,6,12,16,18,20,22},
    {6,7,13,12,        2,3,8,14,17,16,11,5}
};
int movp[6][24];
int nxt[4];
int unxt[4];
int ans;
vector<node_t> vc[8];



struct Hash {
	static const int mod = 23456;
	map<string,int> tb[mod];
	
    void clear() {
		rep(i, 0, mod)
			tb[i].clr();
    }

    static int HashCode(const char *s) {
        int ret = 0;

        rep(i, 0, 24)
            ret = (ret * 31 + s[i]) % mod;

        return ret;
    }
	
	static LL toLL(const char *s) {
		int ret = 0;
		rep(i, 0, 24)	ret = 10*ret + s[i];
		return ret;
	}

    bool find(const char* s) {
        int h = HashCode(s);
        return tb[h].count(string(s, 24)) > 0;
    }

	bool find(int h, const char *s) {
		return tb[h].count(string(s, 24)) > 0;
	}
	
	int get(const char *s) {
		int h = HashCode(s);
		return tb[h][string(s, 24)];
	}

	int get(int h, const char *s) {
		return tb[h][string(s, 24)];
	}

	void update(const char *s, int step) {
		int h = HashCode(s);
		map<string,int>& tb_ = tb[h];
		string ss(s, 24);
		if (tb_.find(ss) == tb_.end())
			tb_[ss] = step;
	}

	void update(const char *s, int h, int step) {
		map<string,int>& tb_ = tb[h];
		string ss(s, 24);
		if (tb_.find(ss) == tb_.end())
			tb_[ss] = step;
	}

};

Hash H[2];
void init_pos();

void init() {
    rep(i, 0, 4) {
        nxt[i] = (i+1) % 4;
        unxt[i] = (i-1+4)%4;
    }

    int i, j, k;
    for (k=0,j=0; k<3; ++k,j+=2) {
        int *mf = movf[k];
        int *c = movp[j];
        for (i=0; i<24; ++i)    c[i] = i;
        for (i=0; i<4; ++i)
            c[mf[nxt[i]]] = mf[i];
        for (i=0; i<4; ++i) {
            c[mf[(nxt[i]<<1)+4]] = mf[(i<<1)+4];
            c[mf[(nxt[i]<<1|1)+4]] = mf[(i<<1|1)+4];
        }

        c = movp[j+1];
        for (i=0; i<24; ++i)    c[i] = i;
        for (i=0; i<4; ++i)
            c[mf[unxt[i]]] = mf[i];
        for (i=0; i<4; ++i) {
            c[mf[(unxt[i]<<1)+4]] = mf[(i<<1)+4];
            c[mf[(unxt[i]<<1|1)+4]] = mf[(i<<1|1)+4];
        }
    }

	init_pos();
}

vector<vi> vpos;

vi flip(const vi& vtmp) {
	vi ret;

	per(i, 16, 20) 	ret.pb(vtmp[i]);
	per(i, 10, 16) 	ret.pb(vtmp[i]);
	per(i, 4, 10)  	ret.pb(vtmp[i]);
	per(i, 0, 4) 	ret.pb(vtmp[i]);
	per(i, 20, 24) 	ret.pb(vtmp[i]);
	return ret;
}

#define push_vtmp2(a, b) {vtmp.pb(a); vtmp.pb(b);}
#define push_vtmp4(a, b, c, d) {vtmp.pb(a); vtmp.pb(b); vtmp.pb(c); vtmp.pb(d);}
#define push_vtmp6(a, b, c, d, e, f) {vtmp.pb(a); vtmp.pb(b); vtmp.pb(c); vtmp.pb(d); vtmp.pb(e); vtmp.pb(f);}
void init_pos() {
	vi vtmp;

	// 1
	vtmp.clr();
	push_vtmp4(0, 1, 2, 3);
	push_vtmp6(4, 5, 6, 7, 8, 9);
	push_vtmp6(10, 11, 12, 13, 14, 15);
	push_vtmp4(16, 17, 18, 19);
	push_vtmp4(20, 21, 22, 23);
	vpos.pb(vtmp);
	vpos.pb(flip(vtmp));


	// 2
	vtmp.clr();
	push_vtmp4(1, 3, 0, 2);
	push_vtmp6(23, 22, 4, 5, 6, 7);
	push_vtmp6(21, 20, 10, 11, 12, 13);
	push_vtmp4(18, 16, 19, 17);
	push_vtmp4(15, 14, 9, 8);
	vpos.pb(vtmp);
	vpos.pb(flip(vtmp));

	// 3
	vtmp.clr();
	push_vtmp4(2, 0, 3, 1);
	push_vtmp6(6, 7, 8, 9, 23, 22);
	push_vtmp6(12, 13, 14, 15, 21, 20);
	push_vtmp4(17, 19, 16, 18);
	push_vtmp4(11, 10, 5, 4);
	vpos.pb(vtmp);
	vpos.pb(flip(vtmp));

	// 4
	vtmp.clr();
	push_vtmp4(3, 2, 1, 0);
	push_vtmp6(8, 9, 23, 22, 4, 5);
	push_vtmp6(14, 15, 21, 20, 10, 11);
	push_vtmp4(19, 18, 17, 16);
	push_vtmp4(13, 12, 7, 6);
	vpos.pb(vtmp);
	vpos.pb(flip(vtmp));

	// 5
	vtmp.clr();
	push_vtmp4(20, 21, 22, 23);
	push_vtmp6(10, 4, 0, 1, 9, 15);
	push_vtmp6(11, 5, 2, 3, 8, 14);
	push_vtmp4(6, 7, 12, 13);
	push_vtmp4(16, 17, 18, 19);
	vpos.pb(vtmp);
	vpos.pb(flip(vtmp));

	// 6
	vtmp.clr();
	push_vtmp4(6, 7, 12, 13);
	push_vtmp6(5, 11, 16, 17, 14, 8);
	push_vtmp6(4, 10, 18, 19, 15, 9);
	push_vtmp4(20, 21, 22, 23);
	push_vtmp4(0, 1, 2, 3);
	vpos.pb(vtmp);
	vpos.pb(flip(vtmp));
	
	#ifndef ONLINE_JUDGE
	rep(i, 0, SZ(vpos)) {
		rep(j, 0, 24)
			printf("%d ", vpos[i][j]);
		putchar('\n');
	}
	#endif
}

node_t bnode, enode;
queue<node_t> Q[2];

void Init() {
	rep(i, 0, 2) {
		while (!Q[i].empty()) Q[i].pop();
		H[i].clr();
    }
}

int update(node_t& nd, int idx, int step) {
	static char s[26];

	Hash& h = H[idx];
	Hash& hh = H[idx^1];
	const int sz = SZ(vpos);

	rep(i, 0, sz) {
		rep(j, 0, 24)
			s[j] = nd.a[vpos[i][j]];
		#ifndef ONLINE_JUDGE
		printf("%d: %s\n", idx, string(s, 24).c_str());
		#endif
		int hval = Hash::HashCode(s);
		if (hh.find(hval, nd.a))
			return step + hh.get(hval, nd.a);
		h.update(nd.a, hval, step);
	}

	return -1;
}

int bfs(int idx, int step) {
	queue<node_t>& Q = ::Q[idx];
	int sz = SZ(Q);
	node_t nd, d;
	int tmp;

	while (sz--) {
		nd = Q.front();
		Q.pop();
		rep(i, 0, 6) {
			if ((i^1) == nd.pre)
				continue;
			if (i != nd.pre) {
				rep(j, 0, 24)    d.a[j] = nd.a[movp[i][j]];
				d.pre = i;
				d.deep = 1;

			} else if (nd.deep < 2) {
				rep(j, 0, 24)    d.a[j] = nd.a[movp[i][j]];
				d.pre = i;
				d.deep = 2;
			} else {
				continue;
			}
			#ifndef ONLINE_JUDGE
			// if (idx == 0)
				d.print();
			#endif
			tmp = update(d, idx, step);
			if (tmp >= 0) {
				return tmp;
			} else {
				Q.push(d);
			}
		}
	}

	return -1;
}

void solve() {
	Init();
	update(bnode, 0, 0);
	if (update(enode, 1, 0) >= 0) {
		puts("0");
		return ;
	}
	Q[0].push(bnode);
	Q[1].push(enode);
	int ans = -1, tmp;
	
	// #ifndef ONLINE_JUDGE
	// bnode.print();
	// enode.print();
	// #endif

	for (int i=1; i<6;++i) {
		tmp = bfs(0, i);
		if (tmp >= 0) {
			ans = tmp;
			break;
		}
		tmp = bfs(1, i);
		if (tmp >= 0) {
			ans = tmp;
			break;
		}
		#ifndef ONLINE_JUDGE
		if (Q[0].empty() && Q[1].empty()) {
			break;
		}
		#endif
	}

    printf("%d\n", ans);
}

inline char getVal(char c) {
	return c;
	if (c == 'W')	return 1;
	if (c == 'Y')	return 2;
	if (c == 'R')	return 3;
	if (c == 'O')	return 4;
	if (c == 'G')	return 5;
	if (c == 'B')	return 6;
	#ifndef ONLINE_JUDGE
	assert(false);
	#endif
	return -1;
}

int main() {
    ios::sync_with_stdio(false);
    #ifndef ONLINE_JUDGE
        freopen("data.in", "r", stdin);
        freopen("data.out", "w", stdout);
    #endif

	int t;
	char s[24];
	int p[24];
	
	{
		int l = 0;
		rep(i, 0, 4) p[l++] = i;
		rep(i, 4, 10) p[l++] = i;
		p[l++] = 23; p[l++] = 22;
		rep(i, 10, 16) p[l++] = i;
		p[l++] = 21; p[l++] = 20;
		rep(i, 16, 20) p[l++] = i;
	}

    init();
	scanf("%d", &t);
	gets(s);
    while (t--) {
		int l = 0;
		rep(j, 0, 6) {
			gets(s);
			int len = strlen(s);
			rep(i, 0, len) {
				if (s[i] == ' ')	continue;
				bnode.a[p[l++]] = getVal(s[i]);
			}
		}
		#ifndef ONLINE_JUDGE
		printf("l = %d\n", l);
		#endif
		l = 0;
		rep(j, 0, 6) {
			gets(s);
			int len = strlen(s);
			rep(i, 0, len) {
				if (s[i] == ' ')	continue;
				enode.a[p[l++]] = getVal(s[i]);
			}
		}
		#ifndef ONLINE_JUDGE
		printf("l = %d\n", l);
		#endif
		bnode.pre = -1;
		enode.pre = -1;
        solve();
    }

    #ifndef ONLINE_JUDGE
        printf("time = %d.\n", (int)clock());
    #endif

    return 0;
}

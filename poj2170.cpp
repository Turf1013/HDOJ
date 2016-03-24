/* 2170 */
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
#define sec				second
#define all(x) 			(x).begin(),(x).end()
#define SZ(x) 			((int)(x).size())
#define lson			l, mid, rt<<1
#define rson			mid+1, r, rt<<1|1
#define INF				0x3f3f3f3f
#define mset(a, val)	memset(a, (val), sizeof(a))

#define LL unsigned long long

typedef struct node_t {
	vpii vp;

	void sorted() {
		sort(all(vp));
	}

	void push_back(pii p) {
		vp.pb(p);
	}

	void clear() {
		vp.clr();
	}

	int size() const {
		return vp.size();
	}
	
	void regular() {
		int mnx = INT_MAX, mny = INT_MAX;
		
		int sz = SZ(vp);
		
		rep(i, 0, sz) {
			mnx = min(vp[i].fir, mnx);
			mny = min(vp[i].sec, mny);
		}
		
		rep(i, 0, sz) {
			vp[i].fir -= mnx;
			vp[i].sec -= mny;
		}
	}

	pair<pii,pii> calBound() const {
		int mnx, mny, mxx, mxy;
		int sz = SZ(vp);

		if (sz == 0)
			return mp(mp(0, 0), mp(0,0));

		mnx = mny = INT_MAX;
		mxx = mxy = INT_MIN;
		rep(i, 0, sz) {
			mnx = min(mnx, vp[i].fir);
			mxx = max(mxx, vp[i].fir);
			mny = min(mny, vp[i].sec);
			mxy = max(mxy, vp[i].sec);
		}

		return mp(mp(mnx, mxx), mp(mny, mxy));
	}
	
	pii calL() const {
		pair<pii,pii> ppii = calBound();
		return mp(ppii.fir.sec-ppii.fir.fir+1, ppii.sec.sec-ppii.sec.fir+1);
	}
} node_t;

const int maxn = 11;
vector<node_t> E[maxn][maxn];
set<pair<LL,LL> > has;
int ans[maxn][maxn][maxn];
int dir[4][2] = {
	-1, 0, 1,0, 0,-1, 0,1
};
int n, m, cn;
bool printInfo = false;
	
pair<LL,LL> zip(const node_t& d, int sz) {
	node_t nd = d;
	LL x = 0, y = 0;
	
	nd.regular();
	nd.sorted();
	
	rep(i, 0, sz)  {
		x = 10 * x + nd.vp[i].fir;
		y = 10 * y + nd.vp[i].sec;
	}
	
	return mp(x, y);
}

void unzip(pair<LL,LL> p, node_t& nd, int sz) {
	LL &x = p.fir, &y = p.sec;
	
	per(i, 0, sz) {
		nd.vp[i].fir = x % 10;
		nd.vp[i].sec = y % 10;
		x /= 10;
		y /= 10;
	}
}

bool check(const node_t& b) {
	pair<LL,LL> p = zip(b, cn);

	return has.find(p) != has.end();
}

void rotate(node_t& d) {
	// int sz = SZ(d);

	rep(i, 0, cn) {
		swap(d.vp[i].fir, d.vp[i].sec);
		d.vp[i].sec = -d.vp[i].sec;
	}
}

void mirror(node_t& d) {
	// int sz = SZ(d);

	rep(i, 0, cn)
		d.vp[i].fir = -d.vp[i].fir;
}

bool judge(node_t& d) {
	rep(i, 0, cn) {
		rep(j, i+1, cn) {
			if (d.vp[i] == d.vp[j])
				return false;
		}
	}
	
	node_t dd;
	
	dd = d;
	
	rep(i, 0, 2) {
		rep(j, 0, 4) {
			if (check(dd))
				return false;
			rotate(dd);
		}
		mirror(dd);
	}

	return true;
}

int calc() {
	if (n>=cn && m>=cn)
		return SZ(E[cn][cn]);

	const vector<node_t>& vc = E[cn][cn];
	int sz = SZ(vc);
	int ret = 0;

	rep(i, 0, sz) {
		pair<pii,pii> ppii = vc[i].calBound();
		int lx = ppii.fir.sec - ppii.fir.fir + 1;
		int ly = ppii.sec.sec - ppii.sec.fir + 1;
		if ((lx<=n && ly<=m) || (lx<=m && ly<=n))
			++ret;
	}

	return ret;
}

void printAns() {
	puts("int ans[10][100] = {");
	rep(i, 1, 11) {
		putchar('\t');
		putchar('{');
		rep(j, 1, 11) {
			rep(k, 1, 11) {
				if (j==1 && k==1)
					printf("%d", ans[i][j][k]);
				else
					printf(",%d", ans[i][j][k]);
			}
		}
		putchar('}');
		if (i != 10)
			putchar(',');
		putchar('\n');
	}
	puts("};");
}

void solve() {
	vector<node_t>& vc = E[n][cn];
	const vector<node_t>& ovc = E[n][cn-1];

	has.clr();
	int osz = SZ(ovc);

	rep(i, 0, osz) {
		const node_t& nd = ovc[i];
		pair<pii,pii> ppii = nd.calBound();
		int mxx, mxy, mnx, mny;
		
		node_t d;

		rep(j, 0, cn-1) d.pb(nd.vp[j]);
		d.pb(mp(0, 0));
		
		rep(j, 0, cn-1) {
			const int& x = nd.vp[j].fir;
			const int& y = nd.vp[j].sec;
			int xx, yy;

			rep(k, 0, 4) {
				xx = x + dir[k][0];
				yy = y + dir[k][1];
				d.vp[cn-1].fir = xx;
				d.vp[cn-1].sec = yy;
				
				mnx = min(ppii.fir.fir, xx);
				mxx = max(ppii.fir.sec, xx);
				mny = min(ppii.sec.fir, yy);
				mxy = max(ppii.sec.sec, yy);
				
				if (mxx-mnx+1>n || mxy-mny+1>n)
					continue;
				
				#ifndef ONLINE_JUDGE
				// rep(ii, 0, cn)
					// printf("(%d,%d)\n", d.vp[ii].fir, d.vp[ii].sec);
				// putchar('\n');
				#endif
				
				if (judge(d)) {
					vc.pb(d);
					pair<LL, LL> p = zip(d, cn);
					has.insert(p);
				}
			}
		}
	}
}

void init() {
	for (n=1; n<maxn; ++n) {
		for (cn=1; cn<maxn; ++cn) {
			if (cn == 1) {
				node_t nd;
				nd.pb(mp(0, 0));
				E[n][cn].pb(nd);
			} else if (cn < n) {
				int sz = SZ(E[cn][cn]);
				rep(i, 0, sz)
					E[n][cn].pb(E[cn][cn][i]);
			} else {
				solve();
			}
			
			printf("E[%d][%d] = %d\n", n, cn, SZ(E[n][cn]));
			fflush(stdout);
		}
	}

	for (cn=1; cn<=10; ++cn) {
		for (n=1; n<=cn; ++n) {
			for (m=n; m<=cn; ++m) {
				ans[cn][n][m] = ans[cn][m][n] = calc();
			}
		}
	}

	printAns();
}

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif

	init();

	#ifndef ONLINE_JUDGE
		printf("time = %d.\n", (int)clock());
	#endif

	return 0;
}

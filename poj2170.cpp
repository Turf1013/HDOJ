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

//////// AC final Program
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

int ans[10][100] = {
	{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,1,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,1,0,0,0,0,0,0,0,1,4,5,0,0,0,0,0,0,0,4,4,5,0,0,0,0,0,0,1,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,1,0,0,0,0,0,0,0,2,5,6,0,0,0,0,0,0,2,8,11,12,0,0,0,0,0,0,5,11,11,12,0,0,0,0,0,1,6,12,12,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,1,0,0,0,0,0,0,1,7,12,13,0,0,0,0,0,1,8,29,34,35,0,0,0,0,0,7,29,29,34,35,0,0,0,0,0,12,34,34,34,35,0,0,0,0,1,13,35,35,35,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,1,0,0,0,0,0,0,2,13,18,19,0,0,0,0,0,7,48,84,89,90,0,0,0,0,2,48,66,102,107,108,0,0,0,0,13,84,102,102,107,108,0,0,0,0,18,89,107,107,107,108,0,0,0,1,19,90,108,108,108,108,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,1,0,0,0,0,0,1,11,30,37,38,0,0,0,0,3,63,169,223,230,231,0,0,0,1,63,140,307,361,368,369,0,0,0,11,169,307,307,361,368,369,0,0,0,30,223,361,361,361,368,369,0,0,0,37,230,368,368,368,368,369,0,0,1,38,231,369,369,369,369,369,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,1,0,0,0,0,0,3,25,53,60,61,0,0,0,1,43,256,466,543,550,551,0,0,0,43,224,820,1127,1204,1211,1212,0,0,3,256,820,893,1200,1277,1284,1285,0,0,25,466,1127,1200,1200,1277,1284,1285,0,0,53,543,1204,1277,1277,1277,1284,1285,0,0,60,550,1211,1284,1284,1284,1284,1285,0,1,61,551,1212,1285,1285,1285,1285,1285,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,16,68,108,117,118,0,0,0,21,277,842,1226,1329,1338,1339,0,0,21,287,1847,3234,3773,3876,3885,3886,0,1,277,1847,2376,4003,4542,4645,4654,4655,0,16,842,3234,4003,4003,4542,4645,4654,4655,0,68,1226,3773,4542,4542,4542,4645,4654,4655,0,108,1329,3876,4645,4645,4645,4645,4654,4655,0,117,1338,3885,4654,4654,4654,4654,4654,4655,1,118,1339,3886,4655,4655,4655,4655,4655,4655}
};

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif

	int n, w, h;

	while (scanf("%d%d%d",&n,&w,&h)!=EOF) {
		--n;
		--w;
		--h;
		cout << ans[n][w*10+h] << endl;
	}

	#ifndef ONLINE_JUDGE
		printf("time = %d.\n", (int)clock());
	#endif

	return 0;
}


//////// Data Generator
import sys
import string
from random import randint, shuffle

    
def GenData(fileName):
	with open(fileName, "w") as fout:
		t = 1
		for tt in xrange(t):
			for j in xrange(1, 11):
				for i in xrange(1, j+1):
					for k in xrange(1, j+1):
						fout.write("%d %d %d\n" % (j, i, k))
			
			
def MovData(srcFileName, desFileName):
    with open(srcFileName, "r") as fin:
        lines = fin.readlines()
    with open(desFileName, "w") as fout:
        fout.write("".join(lines))

        
def CompData():
    print "comp"
    srcFileName = "F:\Qt_prj\hdoj\data.out"
    desFileName = "F:\workspace\cpp_hdoj\data.out"
    srcLines = []
    desLines = []
    with open(srcFileName, "r") as fin:
        srcLines = fin.readlines()
    with open(desFileName, "r") as fin:
        desLines = fin.readlines()
    n = min(len(srcLines), len(desLines))-1
    for i in xrange(n):
        ans2 = int(desLines[i])
        ans1 = int(srcLines[i])
        if ans1 > ans2:
            print "%d: wrong" % i

            
if __name__ == "__main__":
    srcFileName = "F:\Qt_prj\hdoj\data.in"
    desFileName = "F:\workspace\cpp_hdoj\data.in"
    GenData(srcFileName)
    MovData(srcFileName, desFileName)
	
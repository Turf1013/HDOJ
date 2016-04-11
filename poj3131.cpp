/* 3131 */
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

#define WR	0
#define WB	1
#define RW	2
#define RB	3
#define	BR	4
#define	BW	5
#define EMPTY	6
#define TOP 	0
#define DOWN 	1
#define LEFT	2
#define RIGHT	3

typedef struct node_t {
	int st, ept;

	node_t() {}
	node_t(int st, int ept):
		st(st), ept(ept) {}

} node_t;

int des[9], bn[9];
int Move[6][4];
int dir[4][2] = {
	1,0, -1,0, 0,1, 0,-1
};
int mdir[4] = {
	DOWN, TOP, LEFT, RIGHT
};				 
const int maxm = 1680000;
char visit[2][maxm][9];
pii link[9][4];
int lsz[9];
int ID[3][3];
queue<node_t> Q[2];
int tStep[2];
int Base6[9];
int iEpt;

int getVal(char ch) {
	if (ch == 'E')	return 3;
	if (ch == 'W')	return 0;
	if (ch == 'R')	return 1;
	if (ch == 'B')	return 2;
	return -1;
}

void init() {
	// No.0
	// Top: 	white
	// Front:	red
	// right: 	blue
	Move[WR][TOP] 	= RW;
	Move[WR][DOWN] 	= RW;
	Move[WR][LEFT]	= BR;
	Move[WR][RIGHT]	= BR;

	// No.1
	// Top: 	white
	// Front:	blue
	// right: 	red
	Move[WB][TOP] 	= BW;
	Move[WB][DOWN] 	= BW;
	Move[WB][LEFT]	= RB;
	Move[WB][RIGHT]	= RB;

	// No.2
	// Top: 	red
	// Front:	white
	// right: 	blue
	Move[RW][TOP] 	= WR;
	Move[RW][DOWN] 	= WR;
	Move[RW][LEFT]	= BW;
	Move[RW][RIGHT]	= BW;

	// No.3
	// Top: 	red
	// Front:	blue
	// right: 	white
	Move[RB][TOP] 	= BR;
	Move[RB][DOWN] 	= BR;
	Move[RB][LEFT]	= WB;
	Move[RB][RIGHT]	= WB;

	// No.4
	// Top: 	blue
	// Front:	red
	// right: 	white
	Move[BR][TOP] 	= RB;
	Move[BR][DOWN] 	= RB;
	Move[BR][LEFT] 	= WR;
	Move[BR][RIGHT] = WR;

	// No.5
	// Top: 	blue
	// Front:	white
	// right: 	red
	Move[BW][TOP] 	= WB;
	Move[BW][DOWN] 	= WB;
	Move[BW][LEFT] 	= RW;
	Move[BW][RIGHT] = RW;

	{
		int cnt = 0;
		rep(i, 0, 3)
			rep(j, 0, 3)
				ID[i][j] = cnt++;
	}

	rep(i, 0, 3) {
		rep(j, 0, 3) {
			int uid = ID[i][j];
			int& sz = lsz[uid];
			sz = 0;
			rep(k, 0, 4) {
				int x = i + dir[k][0];
				int y = j + dir[k][1];
				if (x>=0 && x<3 && y>=0 && y<3) {
					int vid = ID[x][y];
					link[uid][sz].fir = vid;
					link[uid][sz].sec = mdir[k];
					++sz;
				}
			}
		}
	}

	Base6[0] = 1;
	rep(i, 1, 9)
		Base6[i] = Base6[i-1] * 6;
}

inline int zip(int *a) {
	int ret = 0, bn = 0;

	rep(i, 0, 9) {
		if (a[i] == EMPTY)
			continue;
		ret += a[i] * Base6[bn++];
	}

	return ret;
}

inline void unzip(int st, int *a, int ept) {
	rep(i, 0, 9) {
		if (i == ept) {
			a[i] = EMPTY;
		} else {
			a[i] = st % 6;
			st /= 6;
		}
	}
}

int Ept;
void dfs_EndSt(int idx, int cst) {
	if (idx == 9) {
		// #ifndef ONLINE_JUDGE
		// printf("eval = %d, ept = %d\n", cst, Ept);
		// fflush(stdout);
		// assert(cst>=0 && cst<maxm && Ept>=0 && Ept<9);
		// #endif
		visit[1][cst][Ept] = 0;
		Q[1].push(node_t(cst, Ept));
		return ;
	}

	if (des[idx] == 3) {
		dfs_EndSt(idx+1, cst);
	} else {
		dfs_EndSt(idx+1, cst+(des[idx]<<1)*Base6[bn[idx]]);
		dfs_EndSt(idx+1, cst+(des[idx]<<1|1)*Base6[bn[idx]]);
	}
}

int bfs(int id) {
	queue<node_t>& q = Q[id];
	node_t nd;
	int sz = SZ(q);
	int nst, nept;
	int a[9];

	++tStep[id];

	while (sz--) {
		nd = q.front();
		q.pop();
		const int& st = nd.st;
		const int& ept = nd.ept;
		const int& sz = lsz[ept];
		const int step = visit[id][st][ept] + 1;

		unzip(st, a, ept);
		rep(i, 0, sz) {
			nept = link[ept][i].fir;
			swap(a[nept], a[ept]);
			int tmp = a[ept];
			a[ept] = Move[a[ept]][link[ept][i].sec];

			nst = zip(a);
			if (visit[id^1][nst][nept] >= 0) {
				return step + visit[id^1][nst][nept];
			}
			if (visit[id][nst][nept] == -1) {
				visit[id][nst][nept] = step;
				q.push(node_t(nst, nept));
			}

			// #ifndef ONLINE_JUDGE
			// if (0 == 0) {
				// printf("Q[%d]: value = %d, ept = %d\n", id, nst, nept);
			// }
			// fflush(stdout);
			// #endif
			a[ept] = tmp;
			swap(a[nept], a[ept]);
		}
	}

	return -1;
}

int bibfs() {
	int tmp;

	while (!Q[0].empty() || !Q[1].empty()) {
		// #ifndef ONLINE_JUDGE
			// rep(i, 0, 1)
				// printf("Q[%d].size() = %d\n", 0, SZ(Q[0]));
			// fflush(stdout);
		// #endif
		if (tStep[0] + tStep[1] >= 30)	break;
		tmp = bfs(0);
		if (tmp >= 0)	return tmp;
		if (tStep[1] <= 9) {
			// #ifndef ONLINE_JUDGE
				// rep(i, 1, 2)
					// printf("Q[%d].size() = %d\n", 1, SZ(Q[1]));
				// fflush(stdout);
			// #endif
			tmp = bfs(1);
			if (tmp >= 0)	return tmp;
		}
	}

	return -1;
}

void solve() {
	memset(visit, -1, sizeof(visit));
	
	if (des[0] == 3) {
		bn[0] = -1;
		Ept = 0;
	} else {
		bn[0] = 0;
	}
	rep(i, 1, 9) {
		if (des[i] == 3) {
			Ept = i;
			bn[i] = bn[i-1];
		} else {
			bn[i] = bn[i-1] + 1;
		}
	}

	rep(i, 0, 2)
		while (!Q[i].empty())	Q[i].pop();
	dfs_EndSt(0, 0);

	int a[9];

	memset(a, 0, sizeof(a));
	a[iEpt] = EMPTY;
	int st1 = zip(a);

	if (visit[1][st1][iEpt] != -1) {
		puts("0");
		return ;
	}

	Q[0].push(node_t(st1, iEpt));
	visit[0][st1][iEpt] = 0;
	tStep[0] = tStep[1] = 0;

	int ans = bibfs();

	printf("%d\n", ans);
	// #ifndef ONLINE_JUDGE
	// fflush(stdout);
	// #endif
}

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif

	int x, y;
	char cmd[4];

	init();
	while (scanf("%d%d",&x,&y)!=EOF && (x||y)) {
		rep(i, 0, 9) {
			scanf("%s", cmd);
			des[i] = getVal(cmd[0]);
		}
		iEpt = ID[y-1][x-1];
		solve();
	}

	#ifndef ONLINE_JUDGE
		printf("time = %ldms.\n", clock());
	#endif

	return 0;
}

import sys
import string
from random import randint, shuffle

    
def GenData(fileName):
	with open(fileName, "w") as fout:
		t = 20
		op = "WRB"
		# fout.write("%d\n" % (t))
		for tt in xrange(t):
			x = randint(1, 3)
			y = randint(1, 3)
			fout.write("%d %d\n" % (x, y))
			x = randint(0, 2)
			y = randint(0, 2)
			for i in xrange(3):
				L = []
				for j in xrange(3):
					if i==x and j==y:
						L.append('E')
					else:
						idx = randint(0, 2)
						L.append(op[idx])
				fout.write(" ".join(L) + "\n")
		fout.write("0 0\n")
		
			
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
	
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
#define sec				second
#define all(x) 			(x).begin(),(x).end()
#define SZ(x) 			((int)(x).size())
#define lson			l, mid, rt<<1
#define rson			mid+1, r, rt<<1|1
#define INF				0x3f3f3f3f
#define mset(a, val)	memset(a, (val), sizeof(a))

const int maxl = 20;
const int maxn = 100;
char s[maxl];
char sa[3][8];
char sb[3][8];
char str[maxn][maxn][4];
int L[maxn][maxn];
int bits[3], slen;
vi can1[11];
vi can2[11][11];

void init_can() {
	rep(i, 0, 10)	{
		can1[i].pb(i);
		can1[10].pb(i);
	}
	
	int num = 0;
	
	rep(i, 0, 10) {
		rep(j, 0, 10) {
			can2[i][j].pb(num);
			can2[10][j].pb(num);
			can2[i][10].pb(num);
			can2[10][10].pb(num);
			++num;
		}
	}
}

void init_exp(int a, int b) {
	int &l = L[a][b], res = a * b;
	char *s = str[a][b];
	
	if (res == 0) {
		s[l++] = 0;
	} else {
		while (res) {
			s[l++] = res%10;
			res /= 10;
		}
		reverse(s, s+l);
	}
}

void init() {
	rep(i, 0, maxn) {
		rep(j, i, maxn) {
			init_exp(i, j);
			if (i != j) {
				L[j][i] = L[i][j];
				rep(k, 0, 4)	str[j][i][k] = str[i][j][k];
			}
		}
	}
	
	init_can();
}

inline void getBits() {
	int i, j, k, l;
	
	i = j = k = l = 0;
	while (i <= slen) {
		if (s[i]==' ' || s[i]=='\0') {
			if (l) {
				s[i] = '\0';
				strcpy(sa[k], s[i]+j);
				bits[k++] = l;
			}
			l = 0;
			j = i + 1;
		}
		if (i == slen)
			break;
		
		++i;
	}
}

void solve() {
	slen = strlen(s);
	
	getBits();
	
	int l = 
}

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif
	
	while (gets(s) != NULL) {
		if (s[0]=='0' && s[1]=='\0')
			break;
		solve();
	}
	
	#ifndef ONLINE_JUDGE
		printf("time = %ldms.\n", clock());
	#endif
	
	return 0;
}

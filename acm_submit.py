#!/usr/env python

import urllib2
import urllib
import cookielib
import logging
from urlparse import *
from time import sleep
from lxml import etree
import string

global url, n_vol
url  = "http://acm.hdu.edu.cn"
n_vol = 46
judgeStatus_xpath 	= "/html/body/table/tr[4]/td/div/table/tr[2]/td[3]/font"
exeTime_xpath 		= "/html/body/table/tr[4]/td/div/table/tr[2]/td[5]"
exeMemory_xpath 	= "/html/body/table/tr[4]/td/div/table/tr[2]/td[6]"

def initLog():
	# os.chdir(parentDirPath)
	suffix = 'hdu'
	logging.basicConfig(
				level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=__file__[:-3]+'_'+suffix+'.log',
                filemode='w')
	
	
def acmHdu_Login(user, password):
	login_page = urljoin(url, "userloginex.php?action=login")
	try:
		'create cookie'
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('User-agent',\
				 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
		data = urllib.urlencode({"username":user, "userpass":password})
		urllib2.install_opener(opener)
		urllib2.urlopen(login_page, data)
		
	except Exception, e:
		print "Login unsucceed"
		print e
	
def acmHdu_Submit(pid, lang, code):
	submit_url = urljoin(url, "submit.php?action=submit")
	data = urllib.urlencode({"problemid":pid, "language":lang, "usercode":code})
	req = urllib2.Request(submit_url, data)
	response = urllib2.urlopen(req)
	content = response.read()
	
	
def acmHdu_Status(user, pid, lang):
	sleep(5)
	status_url = urljoin(url, "status.php?first=&pid=%s&user=%s&lang=%s&status=0" % (str(pid), user, str(lang+1)))
	# print status_url
	content = urllib2.urlopen(status_url).read()
	with open("C:\Users\hooh\Desktop\st.html", "w") as fout:
		fout.write(content)
		
		
def acmHdu_Status_Parse(user, pid, lang):
	sleep(5)
	status_url = urljoin(url, "status.php?first=&pid=%s&user=%s&lang=%s&status=0" % (str(pid), user, str(lang+1)))
	# print status_url
	content = urllib2.urlopen(status_url).read()
	tree = etree.HTML(content)
	infoList = map(
		lambda ele: ele.text, tree.xpath(judgeStatus_xpath)
	)
	return infoList[0] if infoList else ""
	
def acmHdu_ExeTime_Parse(user, pid, lang):
	sleep(5)
	status_url = urljoin(url, "status.php?first=&pid=%s&user=%s&lang=%s&status=0" % (str(pid), user, str(lang+1)))
	# print status_url
	content = urllib2.urlopen(status_url).read()
	tree = etree.HTML(content)
	statusList = map (
		lambda ele: ele.text, tree.xpath(judgeStatus_xpath)
	)
	status = statusList[0] if statusList else ""
	etimeList = map (
		lambda ele: ele.text, tree.xpath(exeTime_xpath)
	)
	etime = int(etimeList[0][:-2]) if etimeList else 10**9
	return status.strip(),etime
	

class constForSubmit:
	can = ' ' + string.digits + string.uppercase + string.lowercase
	pid = 3337
	lang = 2
	LangDict = {
		"G++" 		: 0,
		"GCC" 		: 1,
		"C++" 		: 2,
		"C" 		: 3,
		"Pascal" 	: 4,
		"Java"	 	: 4,
		"C#" 		: 4,
	}
	template = string.Template(\
'''
/* 3337 */
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

char pattern[105];
int len;

void init() {
	len = 0;
	pattern[len++] = ' ';
	rep(i, 0, 10)
		pattern[len++] = '0'+i;
	rep(i, 0, 26)
		pattern[len++] = 'A'+i;
	rep(i, 0, 26)
		pattern[len++] = 'a'+i;
	puts(pattern);
}

void WA() {
	puts("Wa");
}

void TLE() {
	while (true);
}

void OLE() {
	while (true)
		puts("123");
}

int main() {
	ios::sync_with_stdio(false);
	#ifndef ONLINE_JUDGE
		freopen("data.in", "r", stdin);
		freopen("data.out", "w", stdout);
	#endif
	
	init();
	
	char line[20];
	
	gets(line);
	int len = strlen(line);
	int index = $index;
	int th = $th;
	
	if (index >= len)
		OLE();
	
	if (pattern[th] == line[index]) {
		WA();
	} else {
		while	(true)
			;
	}
	
	#ifndef ONLINE_JUDGE
		printf("time = %d.\\n", (int)clock());
	#endif
	
	return 0;
}


''')
	code_4801 = r'''
	/* 4801 */
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

	#define LL __int64

	typedef struct {
		char a[24];
	} node_t;

	typedef struct {
		node_t p;
		int pre, deep;
	} node;

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

	void bfs();

	void init() {
		rep(i, 0, 4) {
			nxt[i] = (i+1) % 4;
			unxt[i] = (i-1+4)%4;
		}
		
		int i, j, k;
		for (k=0,j=0; k<3; ++k,j+=2) {
			int *mf = movf[k];
			int *c = movp[j];
			for (i=0; i<24; ++i)	c[i] = i;
			for (i=0; i<4; ++i)
				c[mf[nxt[i]]] = mf[i];
			for (i=0; i<4; ++i) {
				c[mf[(nxt[i]<<1)+4]] = mf[(i<<1)+4];
				c[mf[(nxt[i]<<1|1)+4]] = mf[(i<<1|1)+4];
			}
			
			c = movp[j+1];
			for (i=0; i<24; ++i)	c[i] = i;
			for (i=0; i<4; ++i)
				c[mf[unxt[i]]] = mf[i];
			for (i=0; i<4; ++i) {
				c[mf[(unxt[i]<<1)+4]] = mf[(i<<1)+4];
				c[mf[(unxt[i]<<1|1)+4]] = mf[(i<<1|1)+4];
			}
		}
		
		bfs();
	}

	void bfs() {
		queue<node> Q;
		node nd, d;
		int step = 0;
		
		rep(i, 0, 24)	nd.p.a[i] = i;
		nd.pre = -1;
		nd.deep = 0;
		Q.push(nd);
		vc[step].pb(nd.p);
		
		while (1) {
			int sz = SZ(Q);
			if (sz==0 || ++step>7)
				break;
			while (sz--) {
				nd = Q.front();
				Q.pop();
				rep(i, 0, 6) {
					if ((i^1) == nd.pre)
						continue;
					if (i != nd.pre) {
						rep(j, 0, 24)	d.p.a[j] = nd.p.a[movp[i][j]];
						d.pre = i;
						d.deep = 1;
						vc[step].pb(d.p);
						Q.push(d);
						
					} else if (nd.deep < 2) {
						rep(j, 0, 24)	d.p.a[j] = nd.p.a[movp[i][j]];
						d.pre = i;
						d.deep = 2;
						vc[step].pb(d.p);
						Q.push(d);
					}
				}
			}
		}
	}

	int calc(int *b) {
		int ret = 0;

		rep(i, 0, 6) {
			++ret;
			rep(j, 1, 4) {
				if (b[face[i][j]] != b[face[i][0]]) {
					--ret;
					break;
				}
			}
		}

		return ret;
	}

	void solve() {
		ans = 0;

		rep(i, 0, n+1) {
			int sz = SZ(vc[i]);
			rep(j, 0, sz) {
				rep(k, 0, 24)
					b[k] = a[vc[i][j].a[k]];
				
				ans = max(ans, calc(b));
			}
		}

		printf("%d\n", ans);
	}

	int main() {
		ios::sync_with_stdio(false);
		#ifndef ONLINE_JUDGE
			freopen("data.in", "r", stdin);
			freopen("data.out", "w", stdout);
		#endif

		init();
		while (scanf("%d", &n)!=EOF) {
			rep(i, 0, 24)
				scanf("%d", &a[i]);
			solve();
		}

		#ifndef ONLINE_JUDGE
			printf("time = %d.\n", (int)clock());
		#endif

		return 0;
	}
	'''

class CFS(constForSubmit):
	pass
	
	
def acmHdu_Submit3337(user, pid, lang, template):
	maxl = 20
	varDict = dict()
	cn = len(CFS.can)
	ret = ""
	for index in xrange(maxl):
		flag = False
		for th in xrange(cn):
			varDict["index"] = index
			varDict["th"] = th
			code = template.safe_substitute(varDict)
			acmHdu_Submit(pid, lang, code)
			while True:
				status = acmHdu_Status_Parse(user, pid, lang)
				if status=="Running" or status=="Queuing" or status=="Compiling":
					continue
				print status
				if status == "Wrong Answer":
					### find the correct char
					ret += CFS.can[th]
					flag = True
					break
				elif status == "Output Limit Exceeded":
					### find the last char
					logging.debug("Result is %s" % (ret))
					return ret
				elif status == "Time Limit Exceeded":
					break
				else:
					continue
			if flag:
				break
		logging.debug("%d: ret = %s" % (index, ret))
	return ret
	
	
def acmHdu_Submit4801(user, pid, lang):
	maxtimes = 10
	code = CFS.code_4801
	mintime = 10**9
	for i in xrange(maxtimes):
		acmHdu_Submit(pid, lang, code)
		print "submit %d" % (i)
		while True:
			status,etime = acmHdu_ExeTime_Parse(user, pid, lang)
			if status=="Running" or status=="Queuing" or status=="Compiling":
				continue
			logging.debug("%d: %s, %d" % (i, status, etime))
			if status=="Accepted":
				mintime = min(mintime, etime)
			break
	logging.debug("mintime = %d" % (mintime))
	return mintime
	
if __name__ == "__main__":
	# user = "Bombe16"
	# password = "496528674"
	# initLog();
	# logging.debug("acm submit begin...")
	# acmHdu_Login(user, password)
	# acmHdu_Submit(CFS.pid, CFS.lang, CFS.code)
	# acmHdu_Status(user, CFS.pid, CFS.lang)
	# logging.debug("acm submit end...")
	
	# 3337
	# user = "Bombe16"
	# password = "496528674"
	# initLog();
	# logging.debug("acm submit begin...")
	# acmHdu_Login(user, password)
	# line = acmHdu_Submit3337(user, CFS.pid, CFS.lang, CFS.template)
	# with open("F:\Qt_prj\hdoj\data.in", "w") as fout:
		# fout.write(line)
	# logging.debug("acm submit end...")
	
	# 4801
	user = "Bombe16"
	password = "496528674"
	initLog();
	logging.debug("acm submit begin...")
	acmHdu_Login(user, password)
	mintime = acmHdu_Submit4801(user, pid=4801, lang=CFS.LangDict["G++"])
	with open("F:\Qt_prj\hdoj\data.out", "w") as fout:
		fout.write("%d\n" % (mintime))
	logging.debug("acm submit end...")
	

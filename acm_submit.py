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
judgeStatus_xpath = "/html/body/table/tr[4]/td/div/table/tr[2]/td[3]/font"

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
	

class constForSubmit:
	can = ' ' + string.digits + string.uppercase + string.lowercase
	pid = 3337
	lang = 2
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
				status = acmHdu_Status_Parse(user, pid, lang).strip()
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
	
	
if __name__ == "__main__":
	# user = "Bombe16"
	# password = "496528674"
	# initLog();
	# logging.debug("acm submit begin...")
	# acmHdu_Login(user, password)
	# acmHdu_Submit(CFS.pid, CFS.lang, CFS.code)
	# acmHdu_Status(user, CFS.pid, CFS.lang)
	# logging.debug("acm submit end...")
	
	user = "Bombe16"
	password = "496528674"
	initLog();
	logging.debug("acm submit begin...")
	acmHdu_Login(user, password)
	line = acmHdu_Submit3337(user, CFS.pid, CFS.lang, CFS.template)
	with open("F:\Qt_prj\hdoj\data.in", "w") as fout:
		fout.write(line)
	logging.debug("acm submit end...")
	

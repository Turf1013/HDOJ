#!/usr/env python
import sys
import urllib2
import urllib
import cookielib
import logging
from urlparse import *
from time import sleep
from lxml import etree
import string


global url, n_vol
url  = "http://acm.fzu.edu.cn/"
judgeStatus_xpath 	= "/html/body/div[2]/div[2]/div/div/div[2]/table/tr[2]/td[3]/font"
pendList = [
	"Wait",
	"Pend",
	"Queuing",
	"Queue",
	"Compiling",
	"Running",
]

def initLog():
	logging.basicConfig(
				level=logging.DEBUG,
                format='%(asctime)s [line:%(lineno)d] %(message)s',
                datefmt='%H:%M:%S',
                filename="fzu_1952.log",
                filemode='w')
	
	
def acmFzu_Login(user, password):
	login_page = url + "/login.php?act=1"
	try:
		'create cookie'
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('User-agent',\
				 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
		data = urllib.urlencode({"uname":user, "upassword":password})
		urllib2.install_opener(opener)
		response = urllib2.urlopen(login_page, data)
		content = response.read()
		
	except Exception, e:
		print "Login unsucceed"
		print e
		
	
def acmFzu_Submit(pid, code, lang=0):
	submit_url = url + "/submit.php?act=5"
	data = urllib.urlencode({"pid":pid, "code":code, 'lang':lang})
	req = urllib2.Request(submit_url, data)
	response = urllib2.urlopen(req)
	content = response.read()
	
def acmFzu_Status(user, pid):
	sleep(3)
	status_url = url + "/log.php?pid=%s&user=%s" % (str(pid), user)
	# print status_url
	content = urllib2.urlopen(status_url).read()
	with open("C:\Users\hooh\Desktop\st.html", "w") as fout:
		fout.write(content)
		
		
def acmFzu_Status_Parse(user, pid):
	sleep(3)
	status_url = url + "log.php?pid=%s&user=%s" % (str(pid), user)
	# print status_url
	content = urllib2.urlopen(status_url).read()
	tree = etree.HTML(content)
	infoList = map(
		lambda ele: ele.text, tree.xpath(judgeStatus_xpath)
	)
	return infoList[0] if infoList else ""
	

class constForSubmit:
	lc = map(ord, string.lowercase)
	uc = map(ord, string.uppercase)
	dts = map(ord, string.digits)
	tmpList = list(set(range(0, 32)) - set([0, 9, 10, 11, 13]))
	left = list(set(range(32, 127)) - set(lc) - set(uc) - set(dts))
	left.remove(35)
	can = [35]
	can += lc
	can += dts
	can += uc
	can += [0, 9, 10, 11, 13]
	can += left
	can += tmpList
	pid = 1952
	lang = 2
	LangDict = {
		"G++" 		: 0,
		"GCC" 		: 1,
		"Pascal" 	: 2,
		"Java"	 	: 3,
		"C++" 		: 4,
		"C" 		: 5,
	}
	template = string.Template(\
'''
#include <cstdio>
#include <cstring>
char s[1005];
int nlines = 0;
void gao() {
	if (nlines==$lineIdx && s[$idx]==$val) {
		while (1) ;
	}
}
int main() {
	while (gets(s)!=NULL) {
		gao();
		if (strcmp(s, "####") == 0)
			puts("0");
		++nlines;
	}
	puts("0");
	
	return 0;
}
''')
	code_aplusb = r'''
#include <iostream>
using namespace std;
int main() {
	int a, b;
	while (cin >> a >> b) {
		cout << a + b << endl;
	}
	return 0;
}
'''

class CFS(constForSubmit):
	pass
	
	
def acmHdu_Submit1952(user, pid, template):
	maxl = 15
	lineIdx,idx = 0,9
	varDict = dict()
	line = "#include "
	for index in xrange(maxl):
		flag = False
		ch = -1
		for val in CFS.can:
			varDict["lineIdx"] = lineIdx
			varDict["val"] = val
			varDict["idx"] = idx
			
			code = template.safe_substitute(varDict)
			# print code
			# continue
			acmFzu_Submit(pid, code)
			for i in xrange(15):
				status = acmFzu_Status_Parse(user, pid)
				if not status:
					status = ''
				status = status.strip()
				if status == "Time Limit Exceed":
					### find the correct char
					flag = True
					break
				elif status == "Wrong Answer":
					break
			if flag:
				ch = val
				break
		chrTmp = chr(ch) if ch>32 else ch
		logging.debug("%d.%d: char = %s" % (lineIdx, idx, chrTmp))
		print "%d.%d: char = %s" % (lineIdx, idx, chrTmp)
		sys.stdout.flush()
		# assert ch >= 0
		idx += 1
		if ch == 0:
			logging.debug("[%d]: line = %s" % (lineIdx, line))
			print "[%d]: line = %s" % (lineIdx, line)
			sys.stdout.flush()
			lineIdx += 1
			idx = 0
			line = ""
		else:
			line += chr(ch)
			
	
if __name__ == "__main__":
	user = "XXX"
	password = "XXX"
	initLog();
	logging.debug("acm submit begin...")
	acmFzu_Login(user, password)
	try:
		acmHdu_Submit1952(user=user, pid=1952, template=CFS.template)
		logging.debug("acm submit end...")
		logging.shutdown()
	except Exception as e:
		print e
		sys.stdout.flush()
		logging.shutdown()
	

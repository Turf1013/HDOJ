#!/usr/env python

import os
from datetime import date
import httplib
import urllib2
import urllib
import cookielib
import logging
from urlparse import *
from time import sleep
from lxml import etree
import string

class constForHdu:
	mainPage  = "http://acm.hdu.edu.cn"
	judgeStatus_xpath 	= "/html/body/table/tr[4]/td/div/table/tr[2]/td[3]/font"
	exeTime_xpath 		= "/html/body/table/tr[4]/td/div/table/tr[2]/td[5]"
	exeMemory_xpath 	= "/html/body/table/tr[4]/td/div/table/tr[2]/td[6]"
	searchTitle_xpath   = "/html/body/table/tr[4]/td/table/tr[2]/td/table/"
	solved_xpath = "/html/body/table/tr[4]/td/table/tr/td/p[3]/script"
	probTitle_xpath = "/html/body/table/tr[4]/td/h1"
	probTitle_xpath = "/html/body/table/tr[4]/td/h1"
	describe_xpath = "/html/body/table/tr[4]/td/div[2]"
	runId_xpath = "/html/body/table/tr[4]/td/div/table/tr[2]/td[1]"
	lang_xpath = "/html/body/table/tr[4]/td/div/table/tr[2]/td[8]"
	code_xpath = "/html/body/table/tr[4]/td/div/textarea"
	
	langDict = {
		"G++" 		: 0,
		"GCC" 		: 1,
		"C++" 		: 2,
		"C" 		: 3,
		"Pascal" 	: 4,
		"Java"	 	: 5,
		"C#" 		: 6,
	}
	
class CFH(constForHdu):
	pass
	
class constForPku:
	mainPage = "http://poj.org"
	judgeStatus_xpath = "/html/body/table[2]/tr[2]/td[4]/font"
	exeTime_xpath = "/html/body/table[2]/tr[2]/td[6]"
	exeMemory_xpath = "/html/body/table[2]/tr[2]/td[5]"
	searchTitle_xpath = "/html/body/center[2]/table/tr"
	probTitle_xpath = "/html/body/table[2]/tr/td/div[2]"
	describe_xpath = "/html/body/table[2]/tr/td/div[4]"
	solved_xpath = "/html/body/center/table/tr[3]/td[3]/script"
	langDict = {
		"G++"		: 0,
		"GCC"		: 1,
		"Java"		: 2,
		"Pascal"	: 3,
		"C++" 		: 4,
		"C" 		: 5,
		"Fortran"	: 6,
	}
	a_plus_b = '''
	#include <iostream>
	using namespace std;

	int main() {
		int a, b;
		
		cin >> a >> b;
		
		cout << a + b << endl;
		
		return 0;
	}

	'''
class CFP(constForPku):
	pass
	

def initLog():
	# os.chdir(parentDirPath)
	suffix = 'v%02d%02d' % (date.today().month, date.today().day)
	logging.basicConfig(
				level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=__file__[:__file__.rindex('.')]+'_'+suffix+'.log',
                filemode='w')
	
def acmHdu_Login(user, password):
	login_page = urljoin(CFH.mainPage, "userloginex.php?action=login")
	try:
		'create cookie'
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('User-agent',\
				 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
		data = urllib.urlencode({"username":user, "userpass":password})
		urllib2.install_opener(opener)
		urllib2.urlopen(login_page, data)
		return opener
		
	except Exception, e:
		print "Login unsucceed"
		print e
		
		
def acmHdu_getUserInfo(user, opener=None):
	info_url = urljoin(CFH.mainPage, "userstatus.php?user="+user)
	print info_url
	if opener:
		content = opener.open(info_url).read()
	else:
		content = urllib2.urlopen(info_url).read()
	return content
	
	
def acmHdu_getProblem(pid, opener=None):
	problem_url = CFH.mainPage + "/showproblem.php?pid=" + str(pid)
	if opener:
		content = opener.open(problem_url).read()
	else:
		content = urllib2.urlopen(problem_url).read()
	return content
	
	
def acmHdu_parseProblemInfo(content):
	tree = etree.HTML(content)
	eleList = tree.xpath(CFH.probTitle_xpath)
	title = eleList[0].text if eleList else ""
	desList = tree.xpath(CFH.describe_xpath)
	des = desList[0].text if desList else ""
	return (title, des)
	

def acmHdu_getAcList(user,pid, opener=None):	
	ac_url = CFH.mainPage + "/status.php?first=&pid=%s&user=%s&lang=0&status=5" % (str(pid), user)
	if opener:
		content = opener.open(ac_url).read()
	else:
		content = urllib2.urlopen(ac_url).read()
	return content
	
	
def acmHdu_getAcCodeInfo(content):
	tree = etree.HTML(content)
	eleList = tree.xpath(CFH.runId_xpath)
	runId = eleList[0].text if eleList else ""
	desList = tree.xpath(CFH.lang_xpath)
	lang = desList[0].text if desList else ""
	return (runId, lang)
	
	
def acmHdu_getAcCode(runId, opener=None):
	code_url = CFH.mainPage + "/viewcode.php?rid=" + str(runId)
	if opener:
		content = opener.open(code_url).read()
	else:
		content = urllib2.urlopen(code_url).read()
	# print content
	tree = etree.HTML(content)
	eleList = tree.xpath(CFH.code_xpath)
	code = eleList[0].text if eleList else ""
	codeList = filter(lambda s:s.strip(), code.split("\r\n"))
	return "\n".join(codeList)
		
	
def acmHdu_Submit(pid, lang, code, opener=None):
	submit_url = urljoin(CFH.mainPage + "/submit.php?action=submit")
	data = urllib.urlencode({"problemid":pid, "language":lang, "usercode":code})
	req = urllib2.Request(submit_url, data)
	if opener:
		response = opener.open(req)
	else:
		response = urllib2.urlopen(req)
	
	
def acmHdu_Search(keyword, opener=None):
	search_url = urljoin(CFH.mainPage, "search.php?action=listproblem")
	data = urllib.urlencode({"content":keyword.strip(), "searchmode":"title"})
	try:
		req = urllib2.Request(search_url, data)
		if opener:
			response = opener.open(req)
		else:
			response = urllib2.urlopen(req)
		content = response.read()
		return  content
		
	except:
		raise ValueError, "search [%s] failed" % (keyword)

		
def acmHdu_parseSolved(content):
	tree = etree.HTML(content)
	js_code = tree.xpath(CFH.solved_xpath)[0].text
	tmpList = js_code.split(';')[:-1]
	solvedList = map(lambda p:p[2:6], tmpList)
	return solvedList	

	
def acmHdu_Status_Parse(user, pid, lang, opener=None):
	sleep(5)
	status_url = urljoin(CFH.mainPage, "status.php?first=&pid=%s&user=%s&lang=%s&status=0" % (str(pid), user, str(lang+1)))
	if opener:
		content = opener.open(status_url).read()
	else:
		content = urllib2.urlopen(status_url).read()
	tree = etree.HTML(content)
	infoList = map(
		lambda ele: ele.text, tree.xpath(CFH.judgeStatus_xpath)
	)
	return infoList[0] if infoList else ""
	
	
def acmHdu_ExeTime_Parse(user, pid, lang, opener=None):
	sleep(5)
	status_url = urljoin(CFH.mainPage, "status.php?first=&pid=%s&user=%s&lang=%s&status=0" % (str(pid), user, str(lang+1)))
	if opener:
		content = opener.open(status_url).read()
	else:
		content = urllib2.urlopen(status_url).read()
	tree = etree.HTML(content)
	statusList = map (
		lambda ele: ele.text, tree.xpath(CFH.judgeStatus_xpath)
	)
	status = statusList[0] if statusList else ""
	etimeList = map (
		lambda ele: ele.text, tree.xpath(CFH.exeTime_xpath)
	)
	etime = int(etimeList[0][:-2]) if etimeList else 10**9
	return status.strip(),etime
	

def acmPku_Login(user, password):
	login_page = urljoin(CFP.mainPage, "login?")
	try:
		'create cookie'
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('User-agent',\
				 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
		data = urllib.urlencode({"B1":"login", "password1":password, "user_id1":user, "url":"."})
		urllib2.install_opener(opener)
		loginSt = urllib2.urlopen(login_page, data).read()
		return opener
		
	except Exception, e:
		print "Login unsucceed"
		print e
		

def acmPku_Submit(pid, lang, code):
	if isinstance(lang, str):
		langId = CFP.langDict[lang]
	else:
		langId = lang
	submit_url = urljoin(CFP.mainPage, "submit?")
	data = urllib.urlencode({"language":langId, "problem_id":pid, "source":code, "submit":"Submit", "encoded":0})
	try:
		req = urllib2.Request(submit_url, data)
		response = urllib2.urlopen(req)
		content = response.read()
		# print content
		
	except:
		print "submit unsucessful"
		

def acmPku_Search(keyword):
	search_url = urljoin(CFP.mainPage, "searchproblem")
	try:
		data = urllib.urlencode({"B1":"GO", "field":"title", "key":keyword.strip()})
	except:
		logging.debug("[keyword-Error]: %s" % (keyword))
		return ""
	try:
		req = urllib2.Request(search_url, data)
		response = urllib2.urlopen(req)
		content = response.read()
		return  content
		
	except:
		raise ValueError, "search [%s] failed" % (keyword)

		
def acmPku_getProblem(pid):
	problem_url = CFP.mainPage + "/problem?id=" + str(pid)
	content = urllib2.urlopen(problem_url).read()
	return content
	
def acmPku_getUserInfo(user, opener=None):
	status_url = CFP.mainPage + "/userstatus?user_id=" + str(user)
	if opener:
		content = opener.open(status_url).read()
	else:
		content = urllib2.urlopen(status_url).read()
	return content
	
def acmPku_parseSolved(content):
	tree = etree.HTML(content)
	eleList = tree.xpath(CFP.solved_xpath)
	js_code = eleList[0].text
	lines = js_code.split("\n")
	retList = []
	for line in lines:
		if line.startswith('p('):
			retList.append(line[2:-1])
	return retList
	
def acmPku_parseProblemInfo(content):
	tree = etree.HTML(content)
	eleList = tree.xpath(CFP.probTitle_xpath)
	title = eleList[0].text if eleList else ""
	desList = tree.xpath(CFP.describe_xpath)
	des = desList[0].text if desList else ""
	return (title, des)
	
	
def acmPku_getProblemList(content):
	tree = etree.HTML(content)
	eleList = tree.xpath(CFP.searchTitle_xpath)
	retList = []
	for i,ele in enumerate(eleList[1:]):
		pid,pname = ele[1].text, ""
		for subele in ele.iter():
			if subele.tag == "a":
				pname = subele.text
				break
		retList.append((pid, pname))
			
	return retList

	
def acmPku_Status_Parse(user, pid):
	sleep(3)
	status_url = CFP.mainPage + "/status?problem_id=%s&user_id=%s" % (pid, user)
	content = urllib2.urlopen(status_url).read()
	tree = etree.HTML(content)
	statusList = map(
		lambda ele: ele.text, tree.xpath(CFP.judgeStatus_xpath)
	)
	return statusList[0] if statusList else ""
	
		
def acmPku_ExeTime_Parse(user, pid):
	sleep(3)
	status_url = CFP.mainPage + "/status?problem_id=%s&user_id=%s" % (pid, user)
	content = urllib2.urlopen(status_url).read()
	with open("F:\code_today\data.in", "w") as fout:
		fout.write(content)
	tree = etree.HTML(content)
	statusList = map(
		lambda ele: ele.text, tree.xpath(CFP.judgeStatus_xpath)
	)
	status = statusList[0] if statusList else ""
	etimeList = map (
		lambda ele: ele.text, tree.xpath(CFP.exeTime_xpath)
	)
	etime = int(etimeList[0][:-2]) if etimeList else 10**9
	return status.strip(), etime
	
	
def acmPku_SubmitOnce(user, pid, lang, code):
	acmPku_Submit(pid, lang, code)
	# print "submit %d" % (pid)
	while True:
		status = acmPku_Status_Parse(user, pid)
		status = status.strip()
		print status
		if status=="Waiting" or status=="Compiling" or status.startswith("Running"):
			continue
		logging.debug("%s: %s" % (pid, status))
		break
	return status
	
	
if __name__ == "__main__":
	initLog()
	
	hdu_user = "Bombe16"
	pku_user = "Bombe1013"
	password = "496528674"
	# logging.debug("hdu login begin...")
	# hdu_opener = acmHdu_Login(hdu_user, password)
	
	logging.debug("pku login begin...")
	acmPku_Login(pku_user, password)
	# logging.debug("pku submit begin...")
	# acmPku_Submit(1000, "C++", CFP.a_plus_b)
	# content = acmPku_Search("Problem")
	# with open("F:\code_today\data.in", "w") as fout:
		# fout.write(content)
	# logging.debug("pku submit end...")
	# parse_status()
	# hduAcCont = acmHdu_getAcList(hdu_user, 1000)
	# runId, lang = acmHdu_getAcCodeInfo(hduAcCont)
	# codeCont = acmHdu_getAcCode(runId)
	# codeCont = acmHdu_getAcCode(16611787, hdu_opener)
	# with open("F:\code_today\data.in", "w") as fout:
		# fout.write(codeCont)
	status = acmPku_SubmitOnce(pku_user, 1000, "C++", CFP.a_plus_b)
	print status
	
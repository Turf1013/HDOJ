#!/usr/env python

import urllib2
import urllib
import cookielib
import logging
from urlparse import *


global url, n_vol
url  = "http://acm.hdu.edu.cn"
n_vol = 46

def initLog():
	# os.chdir(parentDirPath)
	suffix = 'hdu'
	logging.basicConfig(
				level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=__file__[:-3]+'_'+suffix+'.log',
                filemode='w')
				

def acmHdu_handle_status(opener, user):
	user_status = urljoin(url, "userstatus.php?user="+user)
	op = opener.open(user_status)
	status_data = op.read()
	if status_data is None:
		logging.debug("status fetch unsuccessful")
		return False
	else:	
		with open("status.html", "w") as fout:
			fout.write(status_data)
		logging.debug("status fetch successful")
		return True
		

def acmHdu_handle_aList(opener, i_vol):
	list_page = urljoin(url, 'listproblem.php?vol=%d' % (i_vol))
	op = opener.open(list_page)
	list_data = op.read()
	if list_data is None:
		logging.debug("list_%d fetch unsuccessful" % (i_vol))
		return False
	else:
		with open("list_%d.html" % (i_vol), 'w') as fout:
			fout.write(list_data)
		logging.debug("list_%d fetch successful" % (i_vol))
		return True
			

def acmHdu_handle_AllList(opener):
	for i_vol in range(1, n_vol+1):
		st = acmHdu_handle_aList(opener, i_vol)
		if st == False:
			raise Exception, "fetch list error"
	pass
	
	
def acmHdu_Login(user, password):
	login_page = urljoin(url, "userloginex.php?action=login")
	try:
		'create cookie'
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('User-agent',\
				 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
		data = urllib.urlencode({"username":user, "userpass":password})
		opener.open(login_page, data)
		
		'get the status page'
		st = acmHdu_handle_status(opener, user)
		if st == False:
			return 
		'get the problem list'
		acmHdu_handle_AllList(opener)
		
	except Exception, e:
		print e
	
		
		
if __name__ == "__main__":
	user = "XXXXX"
	password = "XXXXXX"
	initLog();
	logging.debug("acm fetch begin...")
	acmHdu_Login(user, password)
	logging.debug("acm fetch end...")
	

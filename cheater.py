import urllib2
from random import choice, randint
from time import sleep

class proxyIp:
	ipList = [
		# ("221.7.153.141", "80"),
		# ("182.90.22.31", "80"),
		# ("124.127.126.9", "808"),
		# ("182.90.23.239", "80"),
		# ("182.90.79.124", "80"),
		# ("182.90.37.95", "80"),
		# ("182.90.39.59", "80"),
		# ("182.90.38.228", "80"),
		# ("110.73.15.56", "8123"),
		# ("103.1.51.10", "8088"),
		# ("182.90.9.58", "80"),
		# ("114.91.43.164", "8888"),
		# ("118.255.121.139", "3128"),
		# ("119.188.94.145", "80"),
		# ("61.158.163.225", "80"),
		# ("61.178.19.117", "808"),
		# ("182.123.10.131", "3128"),
		# ("182.90.23.230", "80"),
		# ("182.90.63.25", "80"),
		# ("110.72.4.42", "8123"),
		# ("221.7.153.141", "80"),
		# ("103.1.50.124", 	"3128"),
		("42.96.196.231", 	"3128"),
	]

	
	
class blogs:
	urlList = [
		# "http://www.cnblogs.com/qwerty1013/p/5386573.html",
		# "http://www.cnblogs.com/bombe1013/p/3294301.html",
		# "http://www.cnblogs.com/bombe1013/p/3294303.html",
		# "http://www.cnblogs.com/bombe1013/p/3945987.html",
		# "http://www.cnblogs.com/bombe1013/p/4909700.html",
		# "http://www.cnblogs.com/bombe1013/p/3621568.html",
		# "http://www.cnblogs.com/qwerty1013/p/5386573.html",
		# "http://www.baidu.com",
		"http://acm.hdu.edu.cn"
	]
	

global user_agents
user_agents = [
	# 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    # 'Opera/9.25 (Windows NT 5.1; U; en)',
    # 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    # 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    # 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    # 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
	# 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
	# 'Mozilla/5.0 (Windows NT 6.2; rv:45.0) Gecko/20100101 Firefox/45.0',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
]




def choices(L):
	n = min(5, randint(1, len(L)))
	ret = [choice(L) for i in xrange(n)]
	return ret

	
def cheat():
	proxy_ip = choice(proxyIp.ipList)
	agent = choice(user_agents)
	proxy_dict = dict(http = "http://%s:%s" % (proxy_ip))
	proxy_handler = urllib2.ProxyHandler(proxy_dict)
	opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
	opener.addheaders = [('User-agent', agent)]
	
	urllib2.install_opener(opener)
	urls = choices(blogs.urlList)
	
	print proxy_dict
	for url in urls:
		print url
		data = ""
		mxcnt = 10
		while mxcnt>0:
			try:
				response = urllib2.urlopen(url)
				data = response.read()
				break
			except urllib2.URLError:
				mxcnt -= 1
		with open("I:\\response.html", "w") as fout:
			fout.write(data)
		# try:
			# response = urllib2.urlopen(url)
			# with open("I:\\response.html", "w") as fout:
				# fout.write(response.read())
			# sleep(randint(3, 5))
		# except urllib2.URLError as e:
			# raise e, "URL Error"
	
	
if __name__ == "__main__":
	cheat()
	
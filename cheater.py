import urllib2
from random import choice, randint
from time import sleep

class proxyIp:
	ipList = [
		("182.88.30.8", "8123"),
		("116.21.43.238", "8118"),
		("112.64.28.248", "8090"),
		("119.188.94.145", "80"), 	
		("182.90.2.142", "80"), 	
		("202.205.22.155", "80"), 	
		("14.111.220.6", "8888"),
		("27.159.34.113", "8888"),
		("110.72.43.93", "8123"),
		("182.90.21.7", "80"), 	
		("182.90.22.105", "80"), 	
		("121.31.77.42", "80"), 	
		("183.140.163.222", "3128"),	
		("182.90.40.206", "80"), 	
		("220.185.103.54", "3128"),
		("222.79.73.187", "8090"),
		("60.169.78.218", "808"), 
		("112.94.224.229", "808"), 
		("182.90.60.189", "80"), 	
		("182.90.20.24", "80"), 	
		("218.62.90.208", "8080"),
	]
	
	
class blogs:
	urlList = [
		# "http://www.cnblogs.com/qwerty1013/p/5386573.html",
		# "http://www.cnblogs.com/bombe1013/p/3294301.html",
		# "http://www.cnblogs.com/bombe1013/p/3294303.html",
		# "http://www.cnblogs.com/bombe1013/p/3945987.html",
		# "http://www.cnblogs.com/bombe1013/p/4909700.html",
		"http://www.cnblogs.com/bombe1013/p/3621568.html",
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
	'Mozilla/5.0 (Windows NT 6.2; rv:45.0) Gecko/20100101 Firefox/45.0',
]




def choices(L):
	n = min(5, randint(1, len(L)))
	ret = [choice(L) for i in xrange(n)]
	return ret

	
def cheat():
	proxy_ip = choice(proxyIp.ipList)
	agent = choice(user_agents)
	proxy_dict = dict(http = "http://%s:%s" % (proxy_ip))
	proxy_dict = dict()
	proxy_handler = urllib2.ProxyHandler(proxy_dict)
	opener = urllib2.build_opener(proxy_handler)
	opener.addheaders = [('User-agent', agent)]
	
	urllib2.install_opener(opener)
	urls = choices(blogs.urlList)
	
	for url in urls:
		print url
		try:
			response = urllib2.urlopen(url)
			with open("I:\\response.html", "w") as fout:
				fout.write(response.read())
			sleep(randint(3, 5))
		except urllib2.URLError:
			print "URL Error"
	
	
if __name__ == "__main__":
	cheat()
	
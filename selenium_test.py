from selenium import webdriver
import time
from random import randint
import codecs

excutable_path = r"E:\Software\phantomjs\bin\phantomjs.exe"
service_args = [
	'--proxy=42.96.196.231:3128',
	'--proxy-type=http', 
]

url = "http://acm.hdu.edu.cn"

driver = webdriver.PhantomJS(executable_path=excutable_path, service_args=service_args)

# status = driver.get(url)
status = driver.execute("get", {'url': url})

for item in status.iteritems():
	print item
# time.sleep(1)

# source = driver.page_source

driver.close()
source = ""
fout = codecs.open("I:\\response.html", "w", "utf-8")
fout.write(source)
fout.close()


# coding: utf-8

import urllib2
from time import sleep
from lxml import etree
from selenium import webdriver
import string
import os
import sys
import getopt
import codecs
from random import shuffle, randint, choice


class constForBlog:
	blog_prefix = "http://www.cnblogs.com/bombe1013/p/"
	cate_prefix = "http://www.cnblogs.com/bombe1013/category/"
	tag_prefix = "http://www.cnblogs.com/bombe1013/tag/"
	tag_suffix = "default.html?page="
	categoryList = [
		# ACM
		"555776",
		# algorithm
		"558746",
		# FPGA
		"513738",
		# latex
		"797837",
		# linux
		"598899",
		# MIPS
		"513743",
		# Translate
		"513741",
		# Codeforces
		"792606",
		# Python
		"554828",
		# ZYNQ
		"792604",
	]
	tagList = [
		"acm",
		"algorithm",
		"codeforces",
		"linux",
		"FPGA",
		"Qemu",
		"MIPS",
	]
	blogLinkInCate_xpath = "/html/body/div[2]/div/h5/a"
	tagPageNum_xpath = "/html/body/div[2]/div/div[1]/div/a"
	blogLinkInTag_xpath = "/html/body/div[2]/div/div/div[1]/a"
	HREF = "href"
	HTML = "html"
	phatomJS_path = r"E:\Software\phantomjs\bin\phantomjs.exe"
	
class CFB(constForBlog):
	pass


class blog(object):

	def __init__(self):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [
			('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
		]
		self.driver = driver = webdriver.PhantomJS(executable_path=CFB.phatomJS_path)
	
	
	def fetchByTag(self, tagList=[]):
		if not tagList:
			tagList = CFB.tagList
		ret = []
		for tag in tagList:
			tagUrl = "%s%s/" % (CFB.tag_prefix, tag, CFB.tag_suffix)
			ret += self.fetchBlogByTag(tagUrl)
		return ret
		
		
	def __handlePid(self, pidList):
		pidList = filter(lambda pid: isinstance(pid, str), pidList)
		return max(map(int, pidList)) if pidList else 1
	
		
	def fetchBlogByTag(self, url):
		# permit use only code to fetch blog
		if not url.endswith("page="):
			if not url.endswith("/"):
				url = url + "/" + CFB.tag_suffix
			else:
				url = url + CFB.tag_suffix
		if not url.startswith("http:"):
			url = CFB.tag_prefix + url
		ret = []
		pageN = pageId = 1
		while pageId <= pageN:
			pageUrl = url + str(pageId)
			content = self.opener.open(pageUrl).read()
			tree = etree.HTML(content)
			pidList = map(
				lambda ele: ele.text, tree.xpath(CFB.tagPageNum_xpath)
			)
			pageN = max(pageN, self.__handlePid(pidList))
			attribList = map (
				lambda ele: ele.attrib, tree.xpath(CFB.blogLinkInTag_xpath)
			)
			for attribDict in attribList:
				if CFB.HREF in attribDict:
					blogUrl = attribDict[CFB.HREF]
					if blogUrl.endswith(CFB.HTML):
						ret.append(blogUrl)
			pageId += 1
		return ret
		
	
	def fetchByCategory(self, cateList=[]):
		if not cateList:
			cateList = CFB.categoryList
		ret = []
		for cateCode in cateList:
			cateUrl = "%s%s.html" % (CFB.cate_prefix, cateCode)
			ret += self.fetchBlogByCate(cateUrl)
		return ret
		
	
	def fetchBlogByCate(self, url):
		# permit use only code to fetch blog
		if not url.endswith(".html"):
			url = url + ".html"
		if not url.startswith("http:"):
			url = CFB.cate_prefix + url
		ret = []
		content = self.opener.open(url).read()
		tree = etree.HTML(content)
		attribList = map(
			lambda ele: ele.attrib, tree.xpath(CFB.blogLinkInCate_xpath)
		)
		for attribDict in attribList:
			if CFB.HREF in attribDict:
				ret.append(attribDict[CFB.HREF])
		return ret
		
		
	@staticmethod	
	def split(url):
		return url[url.rindex('/')+1:url.rindex('.')]
		
		
	@staticmethod	
	def restore(url):
		return CFB.blog_prefix + url + ".html"
	
		
	def dump(self, filename, urls):
		with open(filename, "w") as fout:
			# here we split the complete url, only fetch different part
			for url in urls:
				url = self.split(url)
				fout.write(url + "\n")
		
		
	def fetch(self, filename):
		ret = []
		with open(filename, "r") as fin:
			for line in fin:
				line = line.strip()
				if line:
					ret.append(line)
		return ret
		
		
	def cheat(self, urls):
		for url in urls:
			self.incView( self.restore(url) )
			sleep(randint(5, 10))
		
		
	def incView(self, url):
		self.driver.get(url)
		sleep(1)
		
		
	def search(self, tag):
		tag = tag.lower()
		for item in CFB.tagList:
			if item.lower() == tag:
				return item
		return None
	

	def cheatByFile(self, filename="algorithm"):
		if not filename.endswith(".out"):
			tagname = self.search(filename)
			if not tagname:
				raise ValueError, "%s not exists" % (filename)
			filename = "blog_%s.out" % (tagname)
		if not os.path.isfile(filename):
			raise ValueError, "%s is not a file" % (filename)
		urls = self.fetch(filename)
		shuffle(urls)
		n = min(50, len(urls))
		self.cheat(urls[:n])
		
		
def usage():
	print "-t xxx"
	print "--tag=xxx"
		
		
if __name__ == "__main__":
	desFilePath = "F:\\HDOJ"
	bg = blog()
	# urls = bg.fetchByCategory()
	# for tag in CFB.tagList:
		# if tag == "acm":
			# continue
		# desFileName = os.path.join(desFilePath, "blog_%s.out" % (tag))
		# urls = bg.fetchBlogByTag(tag)
		# bg.dump(desFileName, urls)
	# bg.cheatByFile("algorithm")
	tag = "algorithm"
	if len(sys.argv) > 1:
		options, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "tag="])
		for name, value in options:
			if name in ("-h", "--help"):
				usage()
			elif name in ("-t", "--tag"):
				tag = value
	# print tag
	bg.cheatByFile(tag)
	
		
# encoding: utf-8
#!/usr/env python
from lxml import etree
import os.path
from acm_database import *
import fnmatch

fpath = 'F:/HDOJ'
info_xpath = "/html/body/table/tr[4]/td/table/tr/td/table[1]/tr/td"
name_xpath = "/html/body/table/tr[4]/td/table/tr/td/h1[1]"
solved_xpath = "/html/body/table/tr[4]/td/table/tr/td/p[3]/script"
unsolved_xpath = "/html/body/table/tr[4]/td/table/tr/td/p[4]/script"
problem_xpath = "/html/body/table/tr[5]/td/table/script"


def parse_prob_aP(p_str):
	ele_List = p_str[2:-1].split(',')
	if len(ele_List) > 6:
		ele_List = ele_List[:3] + [','.join(ele_List[3:-2])] + ele_List[-2:]
	_, id, _, title, ac, sub = ele_List
	return (int(id), title[1:-1], float(ac)*100./(float(sub)+0.001), int(ac), int(sub), 0)


def parse_prob_js_code(js_code):
	p_List = js_code.split(';')[:-1]
	return map(parse_prob_aP, p_List)


def parse_problem(prob_filename='list_1.html'):
	prob_path = os.path.join(fpath, prob_filename)
	with open(prob_path, 'rt') as fin:
		tree = etree.HTML(fin.read())
		
		js_code = tree.xpath(problem_xpath)[0].text
		problem_List = parse_prob_js_code(js_code)
		
	return problem_List

	
def print_myInfo(user, infoDict, unsolved_List):
	print '%20s' % (user)
	for key, value in infoDict.iteritems():
		print '%20s: %s'	% (key, value)
	print
	print '%30s' % ("Unsolved Problems")
	print ', '.join(unsolved_List)
	

def parse_status_js_code(js_code):
	p_List = js_code.split(';')[:-1]
	return map(lambda p: p[2:6], p_List)
	
	
def parse_status(st_filename='status.html', check=False):	
	status_path = os.path.join(fpath, st_filename)
	with open(status_path, 'rt') as fin:
		tree = etree.HTML(fin.read())
	
		infoList = map(
			lambda ele: ele.text, tree.xpath(info_xpath)[2:]
		)
		infoDict = dict(zip(infoList[0::2], infoList[1::2]))
		username = tree.xpath(name_xpath)[0].text
		js_code = tree.xpath(unsolved_xpath)[0].text
		unsolved_List = parse_status_js_code(js_code)
		# for node in tree.xpath(unsolved_xpath):
			# print node.text
		print_myInfo(username, infoDict, unsolved_List)
		
		if check:
			js_code = tree.xpath(solved_xpath)[0].text
			solved_List = map(lambda x:(x,), parse_status_js_code(js_code))
			update(solved_List)
		

def parse_all_problem():
	format = 'list_%d.html'
	filter_format = 'list_*.html'
	for filename in fnmatch.filter(os.listdir(fpath), filter_format):
		# print filename
		try:
			prob_List = parse_problem(filename)
			
		except Exception as e:
			print 'parse %s error: %s' % (filename, e)
			
		else:
			insert(prob_List)
		
	
def test_stauts(check):
	parse_status(check=check)
	
	
def test_problem():
	parse_problem('list_11.html')
	
	
def test_insert():
	prob_List = parse_problem('list_1.html')
	print prob_List[0]
	insert(prob_List)
	query_test()
	
	
if __name__ == '__main__':
	# test_stauts(True)
	# test_problem()
	# test_insert()
	# query_test()
	# parse_all_problem()
	parse_status(check=True)
	# query_test()
	
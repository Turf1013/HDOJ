import sys
import string
from random import randint
	
def GenLine(bound, op=string.lowercase):
	length = randint(1, bound)
	ret = ""
	uc = list(op)
	eid = len(uc) - 1
	for i in xrange(length):
		idx = randint(0, eid)
		ret += uc[idx]
	return ret

	
def GenVector(bound, rng):
	n = randint(1, bound)
	ret = []
	for i in xrange(n):
		x = randint(*rng)
		ret.append(x)
	return ret
	

def	GenArray(bn, bm, rng):
	n = randint(1, bn)
	m = randint(1, bm)
	ret = []
	for i in xrange(n):
		dataList = []
		for j in xrange(m):
			x = randint(*rng)
			dataList.append(x)
		ret.append( dataList )
	return ret
	
	
def VectorToStr(L):
	ret = ""
	n = len(L)
	ret += "%d\n" % (n)
	ret += " ".join(map(str, L)) + "\n"
	return ret
	
	
def ArrayToStr(L):
	ret = ""
	n = len(L)
	m = len(L[0])
	ret += "%d %d\n" % (n, m)
	for l in L:
		ret += " ".join(map(str, l)) + "\n"
	return ret

	
def GenData(fileName):
	with open(fileName, "w") as fout:
		t = 20
		fout.write("%d\n" % t)
		for tt in xrange(t):
			L = GenArray(10, 5, (-10, 10))
			line = ArrayToStr(L)
			fout.write("%s" % line)	
				
		
def MovData(srcFileName, desFileName):
	with open(srcFileName, "r") as fin:
		lines = fin.readlines()
	with open(desFileName, "w") as fout:
		fout.write("".join(lines))

		
def CompData():
	print "comp"
	srcFileName = "F:\Qt_prj\hdoj\data.out"
	desFileName = "F:\workspace\cpp_hdoj\data.out"
	srcLines = []
	desLines = []
	with open(srcFileName, "r") as fin:
		srcLines = fin.readlines()
	with open(desFileName, "r") as fin:
		desLines = fin.readlines()
	n = min(len(srcLines), len(desLines))-1
	for i in xrange(n):
		ans2 = int(desLines[i])
		ans1 = int(srcLines[i])
		if ans1 > ans2:
			print "%d: wrong" % i

			
if __name__ == "__main__":
	srcFileName = "F:\Qt_prj\hdoj\data.in"
	desFileName = "F:\workspace\cpp_hdoj\data.in"
	GenData(srcFileName)
	MovData(srcFileName, desFileName)
	
	
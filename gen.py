import sys
import string
from random import randint


def GenData(fileName):
	lc = string.lowercase
	with open(fileName, "w") as fout:
		t = 20
		bound = 10**5
		fout.write("%d\n" % (t))
		for tt in xrange(t):
			# n = randint(100, 500)
			n = 300
			k = randint(1, n)
			fout.write("%d %d\n" % (n, k))
			tot = bound / n
			for i in xrange(n):
				length = randint(1, tot)
				line = ""
				for j in xrange(length):
					idx = randint(0, 25)
					line += lc[idx]
				fout.write("%s\n" % line)
		 
		
		
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
	
	
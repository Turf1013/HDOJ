import sys
import string
from random import randint, shuffle

    
def GenData(fileName):
	with open(fileName, "w") as fout:
		t = 1
		# fout.write("%d\n" % (t))
		# bound = (2**32) - 1
		for tt in xrange(t):
			for j in xrange(1, 11):
				for i in xrange(1, j+1):
					for k in xrange(1, j+1):
						fout.write("%d %d %d\n" % (j, i, k))
			
			
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
    desFileName_ = "F:\code_today\data.in"
    GenData(srcFileName)
    MovData(srcFileName, desFileName)
    MovData(srcFileName, desFileName_)
	
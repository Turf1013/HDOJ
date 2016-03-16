import sys
import string
from random import randint, shuffle

    
def GenData(fileName):
	with open(fileName, "w") as fout:
		t = 20
		fout.write(t)
		# for tt in xrange(t):
			# n = randint(1, 1000)
			# fout.write("%d\n" % (n))
			# for i in xrange(n):
				# op = randint(0, 1)
				# if op:
					# length = randint(1, 100)
				# else:
					# length = randint(1, 10)
				# L = [randint(0, 1) for j in xrange(length)]
				# if op:
					# fout.write("?" + "".join(map(str, L)) + "\n")
				# else:
					# fout.write("+" + "".join(map(str, L)) + "\n")
			
			
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
    
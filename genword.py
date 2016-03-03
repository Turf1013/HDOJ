import sys
import string
from random import randint

def GenWords(n = 20):
	ret = []
	lc = list(string.lowercase)
	llc = len(lc) - 1
	for i in xrange(n):
		length = randint(2, 5)
		word = ""
		for j in xrange(length):
			idx = randint(0, llc)
			word += lc[idx]
		ret.append( word )
	return ret

	
def GenWord(word):
	op = "!#$%^&*()023+-"
	lop = len(op) - 1
	ret = ""
	for i in xrange(len(word)):
		k = randint(0, 100)
		if k%4 == 0:
			idx = randint(0, lop)
			ret += op[idx]
		if k%4 == 1:
			ret += word[i].upper()
		else:
			ret += word[i]
	return ret
	
	
def GenSpace():
	op = " \t"
	length = randint(1, 3)
	ret = ""
	for i in xrange(length):
		k = randint(0, 1)
		ret += op[k]
	return ret
	
	
def GenTile(wordList):
	lw = len(wordList) - 1
	ret = "T: "
	nline = randint(1, 5)
	lines = []
	for i in xrange(nline):
		nword = randint(2, 10)
		line = ""
		for i in xrange(nword):
			line += GenSpace()
			idx = randint(0, lw)
			line += GenWord(wordList[idx])
		lines.append(line)
	ret = ret + "\n".join(lines) + "|"
	return ret

	
def GenPile(wordList):
	lw = len(wordList) - 1
	ret = "P: "
	k = randint(0, 10)
	ret += " %d" % k
	nword = randint(2, 10)
	for i in xrange(nword):
		ret += GenSpace()
		idx = randint(0, lw)
		ret += wordList[idx]
	return ret
	

def GenData(fileName):
	wordList = GenWords()
	lw = len(wordList) - 1
	with open(fileName, "w") as fout:
		pn = randint(10, 20)
		tn = randint(10, 30)
		for i in xrange(pn):
			line = GenPile(wordList)
			fout.write("%s\n" % line)
		for i in xrange(tn):
			line = GenTile(wordList)
			fout.write("%s\n" % line)	
		fout.write("#\n")
		
		
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
	
	
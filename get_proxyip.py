

def get_proxyList(filename):
	ret = []
	with open(filename, "r") as fin:
		for line in fin:
			L = map(lambda s:s.strip(), line.split())
			ret.append(L)
	return ret
	
	
def dump_proxyList(filename, L):
	with open(filename, "w") as fout:
		fout.write("\tipList = [\n")
		for l in L:
			fout.write('\t\t("%s", "%s"),\n' % (l[0], l[1]))
		fout.write("\t]\n")
	
	
if __name__ == "__main__":
	srcFileName = "F:\Qt_prj\hdoj\data.in"
	desFileName = "F:\Qt_prj\hdoj\data.out"
	dump_proxyList(desFileName, get_proxyList(srcFileName))
	
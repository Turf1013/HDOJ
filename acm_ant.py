#!/usr/env python

import re
import logging
from acm_exchange import *

def judge2OJ(pkuId, hduDes):
	pkuCont = acmPku_getProblem(pkuId)
	__, pkuDes = acmPku_parseProblemInfo(pkuCont)
	hduDes = re.split('\s+', hduDes)
	pkuDes = re.split('\s+', pkuDes)
	mn = min(len(pkuDes), len(hduDes), 5)
	for i in xrange(mn):
		if pkuDes[i] != hduDes[i]:
			return False
	return True
	
	
def fuzzySubmit(pid):
	probCont = acmHdu_getProblem(pid)
	probTitle, probDes = acmHdu_parseProblemInfo(probCont)
	probTitle = probTitle.strip()
	logging.debug("[HDU] %s %s" % (pid, probTitle))
	# search in pku
	pkuSearchCont = acmPku_Search(probTitle)
	probList = acmPku_getProblemList(pkuSearchCont)
	retList = []
	for (pkuId, pkuTitle) in probList:
		pkuTitle = pkuTitle.strip()
		if pkuTitle != probTitle:
			break
		if judge2OJ(pkuId, probDes):
			retList.append(pkuId)
	return retList
		

def fuzzyMatch(hduUser, solved):
	maxTime = 3
	for pid in solved:
		candList = fuzzySubmit(pid)
		hduAcCont = acmHdu_getAcList(hduUser, pid)
		runId, lang = acmHdu_getAcCodeInfo(hduAcCont)
		logging.debug("%s: %s" % (pid, str(candList)))
		if candList:
			code = acmHdu_getAcCode(runId)
			print code
			for pkuId in candList:
				logging.debug("[submit] %s %s %s" % (pid, lang, code))
				acmPku_Submit(pkuId, lang, code)
			maxTime -= 1
			if maxTime <= 0:
				break
		

if __name__ == "__main__":
	desFileName = "F:\Qt_prj\hdoj\data.out"
				
	hdu_user = "Trasier"
	pku_user = "Bombe1013"
	password = "496528674"
	initLog()
	logging.debug("hdu login...")
	acmHdu_Login(hdu_user, password)
	logging.debug("pku login...")
	acmPku_Login(pku_user, password)
	acmPku_Submit(1000, "C++", CFP.a_plus_b)
	
	logging.debug("hdu get user info...")
	userInfo = acmHdu_getUserInfo(hdu_user)
	with open(desFileName, "w") as fout:
		fout.write(userInfo)
		
	logging.debug("hdu get solved...")
	solvedList = acmHdu_parseSolved(userInfo)
	print "solved =", len(solvedList)
	
	logging.debug("matching in pku...")
	fuzzyMatch(hdu_user, solvedList)
	
	logging.debug("ending all...")
	
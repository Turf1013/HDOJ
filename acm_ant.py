#!/usr/env python

import re
import logging
from acm_exchange import *

def judge2OJ(pkuId, hduDes):
	pkuCont = acmPku_getProblem(pkuId)
	__, pkuDes = acmPku_parseProblemInfo(pkuCont)
	
	if not isinstance(pkuDes, str) or not isinstance(hduDes, str):
		return False
	hduDes = re.split('\s+', hduDes)
	pkuDes = re.split('\s+', pkuDes)
	mn = min(len(pkuDes), len(hduDes), 5)
	for i in xrange(mn):
		if pkuDes[i] != hduDes[i]:
			return False
	return True
	
	
def fuzzySubmit(pid, hdu_opener):
	retList = []
	probCont = acmHdu_getProblem(pid, hdu_opener)
	probTitle, probDes = acmHdu_parseProblemInfo(probCont)
	probTitle = probTitle.strip()
	logging.debug("[HDU] %s %s" % (pid, probTitle))
	# search in pku
	pkuSearchCont = acmPku_Search(probTitle)
	# if not pkuSearchCont:
		# return retList
	probList = acmPku_getProblemList(pkuSearchCont)
	for (pkuId, pkuTitle) in probList:
		pkuTitle = pkuTitle.strip()
		if pkuTitle != probTitle:
			break
		if judge2OJ(pkuId, probDes):
			retList.append(pkuId)
	return retList
		

def fuzzyMatch(hduUser, hdu_solved, pku_solved, hdu_opener):
	# maxTime = 10
	for pid in hdu_solved:
		candList = fuzzySubmit(pid, hdu_opener)
		hduAcCont = acmHdu_getAcList(hduUser, pid, hdu_opener)
		runId, lang = acmHdu_getAcCodeInfo(hduAcCont)
		logging.debug("%s: %s" % (pid, str(candList)))
		if candList:
			code = acmHdu_getAcCode(runId, hdu_opener)
			for pkuId in candList:
				if int(pkuId) in pku_solved:
					break
				logging.debug("[submit] %s %s %s" % (pid, lang, len(code)))
				# sleep(2)
				# acmPku_Submit(pkuId, lang, code)
				pku_solved.add(int(pkuId))
			# maxTime -= 1
			# if maxTime <= 0:
				# break
		

if __name__ == "__main__":
	desFileName = "F:\code_today\data.in"
				
	hdu_user = "Bombe16"
	pku_user = "Bombe1013"
	password = "496528674"
	initLog()
	logging.debug("hdu login...")
	hdu_opener = acmHdu_Login(hdu_user, password)
	logging.debug("pku login...")
	pku_opener = acmPku_Login(pku_user, password)
	
	logging.debug("hdu get user info...")
	hdu_userInfoCont = acmHdu_getUserInfo(hdu_user, hdu_opener)
	
	logging.debug("pku get user info...")
	pku_userInfoCont = acmPku_getUserInfo(pku_user)
		
	logging.debug("hdu get solved...")
	hdu_solvedList = acmHdu_parseSolved(hdu_userInfoCont)
	print "|hdu_solved| =", len(hdu_solvedList)
	
	logging.debug("pku get solved...")
	pku_solvedList = acmPku_parseSolved(pku_userInfoCont)
	pku_solvedSet = set(map(int, pku_solvedList))
	print "|pku_solved| =", len(pku_solvedList)
	
	logging.debug("matching in pku...")
	fuzzyMatch(hdu_user, hdu_solvedList, pku_solvedSet, hdu_opener)
	
	logging.debug("ending all...")
	
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tianyanfei
# @Mail    : tyfdream@163.com
# @Data    : 2016-11-24 15:17:52
# @Version : python 2.7

import os
import pynlpir
import cPickle as p
from testCharacter import *

testChar = u'\u3010' # this character is '[' in Chinese (gbk to unicode)

def getStopwords():
	'''
		return the list of stopwords
	'''
	#checked ok
	isFile = os.path.isfile(r'stopwords.data')
	ret = []
	if isFile :
		f1 = file(r'stopwords.data', 'r')
		ret = p.load(f1)
		f1.close()
		return ret 
	else:
		f2 = file(r'../data/stopwords.txt', 'r')
		line = f2.readline()
		while line:
			line = line.strip()
			if line == '':
				line = f2.readline()
				continue
			ret.append(line.decode('gbk'))
			line = f2.readline()
		f2.close()
		f3 = file(r'stopwords.data', 'w')
		p.dump(ret, f3)
		f3.close()
		return ret
def splitFile(docName, encodingType):
	'''
		default code style of docName : encodingType
		function : segmente the chinese text of docName and return 
	'''
	# all is wrote in cache -- ok ? maybe wrote in files
	f = file(docName, 'r')
	pynlpir.open(encoding = 'utf-8')
	contest = []
	line = f.readline()
	cou = 0
	while line:
		line = line.strip()
		cou += 1
		
		try:
			line = line.decode(encodingType)
			if line.find(testChar) != -1:#delete the file header
				line = f.readline()
				continue
			temp = pynlpir.segment(line, pos_tagging = False)
			contest += temp 
			line = f.readline()
		except:
			line = f.readline()
			# print '.'
			# print "err %s, %d"%(docName, cou)
	f.close()
	pynlpir.close()
	return contest

def removeNegativeWords(wordsList):
	'''
		type of wordsList : list
		function : filter the characters not in stopwords,alpha, digital, chinese
		type of return : list
	'''
	stopwords = getStopwords() 
	#delete stopwords
	wordsList = filter(lambda item: item not in stopwords, wordsList)
	#delete not alpha chinese or digital
	wordsList = filter(is_other, wordsList)
	return wordsList
def getDocWordsList(docName, encodingType):
	'''
		docName : the path of file
		function : return the target content of docName
	'''
	tempWords = splitFile(docName, encodingType)
	tempWords = removeNegativeWords(tempWords)
	return tempWords
if __name__ == "__main__":
	# temp = getStopwords()
	# g = splitFile(r'../data/train/C3-Art/C3-Art0001.txt')
	g = getDocWordsList(r'../data/train/Car/26.txt', 'utf-8')
	f = file(r'a.txt', 'w')
	for i in g:
		f.write(i.encode('gbk') + ' ')
	f.close()

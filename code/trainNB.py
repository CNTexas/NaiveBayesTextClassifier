#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tianyanfei
# @Mail    : tyfdream@163.com
# @Data    : 2016-11-24 18:37:15
# @Version : python 2.7

import os
import time
import numpy as np 
import cPickle as p
from init import getDocWordsList
import re

vocabulary = []
ratio = 0.8 #80%作为训练集
logHandle = None
encodingType = 'utf-8'#训练集文本的字符编码

def getVocabulary(rootDir):
	# the vocabulary is not sorted
	print 'get Vocabulary'
	logHandle.write('get Vocabulary \n')
	isFile = os.path.isfile('vocabulary.data')
	if isFile:
		f = file('vocabulary.data', 'r')
		ret = []
		ret = p.load(f)
		f.close()
		return ret 
	voca = {}
	words = []
	fileList = []
	cou = 0
	for parent, dirNames, fileNames in os.walk(rootDir):
		L = len(fileNames)
		for i in range(0, int(L*ratio)):
			fileName = fileNames[i]
			file_ = os.path.join(parent, fileName)
			words = getDocWordsList(file_, encodingType)
			cou += 1
			for word in words:
				if not voca.has_key(word):
					voca[word] = 1
				else :
					voca[word] += 1
			print cou,
			logHandle.write(str(cou) + " ")
		logHandle.flush()
	print '\nall is :', len(voca)
	logHandle.write('\n length of voc(total) : ' + str(len(voca)))
	#-----------------------
	ff = file('fullVocabulary.data', 'w')
	p.dump(voca.keys(), ff)
	ff.close()
	#-----------------------
	for word, count in voca.items():
		if count < 3:
			del voca[word]
	ret = voca.keys()
	vocaFile = 'vocabulary.data'
	f = file(vocaFile, 'w')
	p.dump(ret, f)
	f.close()
	print 'vocabulary length: ', len(ret)
	logHandle.write('\nvocabulary length: ' + str(len(ret)))
	return ret 

def getClassNames(rootDir):
	classNames = os.listdir(rootDir)
	# RE = re.compile('[\w]*')
	# ret = []
	# for cla in classNames:
	# 	ret.append(re.findall(RE, cla))
	classNames.sort()
	return classNames


def classPriorProbility(rootDir):
	print '\n\nget class Prio Probility \n'
	logHandle.write('\n\nget class Prio Probility \n')
	isFile = os.path.isfile('classPriorProbility.data')
	if isFile:
		f = file('classPriorProbility.data', 'r')
		ret = {}
		ret = p.load(f) 
		f.close()
		print 'load classPriorProbility ok...'
		return ret 
	allSum = 0
	global vocabulary
	print 'vocabulary length: ', len(vocabulary)
	#----------convert list to dict---
	voca = {}
	for word in vocabulary :
		voca[word] = 1
	#---------------------------------
	classNames = getClassNames(rootDir)
	clsPriPro = {}
	cou = 0
	tempCount = 0
	for parent, dirNames, fileNames in os.walk(rootDir):
		if len(fileNames) == 0:
			continue
		cou += 1
		print 'sloving class: ', classNames[cou-1]
		logHandle.write('sloving class: ' + classNames[cou-1])
		#----------c------------
		print parent
		#----------------------
		clsPriPro[classNames[cou - 1]] = 0.0
		wordSum = 0
		L = len(fileNames)
		for i in range(0, int(L * ratio)):
			fileName = fileNames[i]
			filePath = os.path.join(parent, fileName)
			words = getDocWordsList(filePath, encodingType)
			words = filter(lambda item: voca.has_key(item), words) # filter low frequent words
			wordSum += len(words)
			#------just counting ----
			tempCount += 1
			print tempCount,
			logHandle.write(str(tempCount) + ' ')
			#-----------------------
		allSum += wordSum
		print 'words num: ', wordSum
		logHandle.write('words num: '+ str(wordSum) + '\n')
		clsPriPro[classNames[cou-1]] = wordSum
		logHandle.flush()
	for className in classNames:
		clsPriPro[className] = clsPriPro[className] *1.0 / allSum
		logHandle.write(className + str(clsPriPro[className]))
	# logHandle.write(clsPriPro)
	f = file('classPriorProbility.data', 'w')
	p.dump(clsPriPro,f)
	f.close()
	return clsPriPro

def wordProOnClass(rootDir) :
	print 'get word pro on class'
	logHandle.write('\n\nget word pro on class\n')
	isFile = os.path.isfile('wordProOnClass.data')
	if isFile :
		f = file('wordProOnClass.data', 'r')
		ret = {}
		ret = p.load(f)
		f.close()
		print 'load wordProOnClass ok'
		return ret
	#----- not find .data---
	global vocabulary
	ret = {}
	voca = {}
	classWordsNum = {}
	vocaSize = len(vocabulary)
	for word in vocabulary:
		voca[word] = 1
	vocabulary.sort()
	cou = 0
	tempCou = 0
	classNames = getClassNames(rootDir)
	for parent, dirNames, fileNames in os.walk(rootDir):
		if len(fileNames) == 0:
			continue
		tempVoca = {}
		classWordsSum = 0
		cou += 1
		className = classNames[cou-1]
		L = len(fileNames)
		for i in range(0, int(L * ratio)):
			fileName = fileNames[i]
			#----just count -- 
			tempCou += 1
			print tempCou,
			logHandle.write(str(tempCou) + " ")
			#-----------------
			filePath = os.path.join(parent, fileName)
			words = getDocWordsList(filePath, encodingType)
			words = filter(lambda item: voca.has_key(item), words)
			classWordsSum += len(words)
			for word in words :
				if not tempVoca.has_key(word):
					tempVoca[word] = 1
				else:
					tempVoca[word] += 1
		classWordsNum[className] = classWordsSum
		wordProOnClassList = []
		for word in vocabulary:
			tempC = 0
			if tempVoca.has_key(word):
				tempC = tempVoca[word]
			wordProOnClassList.append(tempC)
		ret[className] = wordProOnClassList
		logHandle.flush()

	for className in classNames:
		for i in range(vocaSize):
			ret[className][i] = (ret[className][i] + 1)*1.0 / (classWordsNum[className] + vocaSize)

	f = file('wordProOnClass.data', 'w')
	p.dump(ret, f)
	f.close()
	return ret

if __name__ == '__main__':
	startTime = time.time()

	logHandle = file('trainLog.txt', 'w')
	rootDir = r'../data/train'
	vocabulary = getVocabulary(rootDir)
	print 'load vocabulary ok'

	print classPriorProbility(rootDir)
	wordProOnClass(rootDir)

	endTime = time.time()
	print 'consumu time : ', endTime - startTime
	logHandle.write('\nconsumu time : '+ str(endTime - startTime))
	logHandle.close()
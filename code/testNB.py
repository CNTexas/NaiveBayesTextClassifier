#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tianyanfei
# @Mail    : tyfdream@163.com
# @Data    : 2016-11-25 20:31:28
# @Version : python 2.7

import os
import time
import math
import numpy as np 
import cPickle as p
from init import getDocWordsList
import re

vocabulary = []
clsPriPro = {}
wordProOnClass = {}
classNames = {}
ratio = 0.8 # 80%作为训练集，其余为测试集
logHandle = None
encodingType = 'utf-8'#训练文本的字符编码

def getTextFeature(textPath):
	global vocabulary
	wordsList = []
	wordsList = getDocWordsList(textPath, encodingType)
	voca = {}
	for word in vocabulary:
		voca[word] = 1
	wordsList = filter(lambda item: voca.has_key(item), wordsList)#delete low frequent words
	textVoca = {}
	for word in wordsList:
		if textVoca.has_key(word):
			textVoca[word] += 1
		else :
			textVoca[word] = 1
	textFeature = []
	for word in vocabulary:
		temp = 0
		if textVoca.has_key(word):
			temp = textVoca[word]
		textFeature.append(temp)
	return textFeature

def TextClassifier(textPath):
	global clsPriPro, wordProOnClass
	classConfidence = {}
	textFeature = [1,] + getTextFeature(textPath)
	textFeatureVec = np.array(textFeature)

	weight = {}
	for class_ in clsPriPro.keys():
		weight[class_] = [clsPriPro[class_]] + wordProOnClass[class_]

	for class_, weight_ in weight.items():
		# get log value for weight
		weight_ = [np.float(math.log(item)) for item in weight_]
		weightVec = np.array(weight_)
		classConfidence[class_] = np.dot(weightVec, textFeatureVec)

	# for class_, pro in classConfidence.items():
	# 	print class_, pro
	ans = max(classConfidence.iterkeys(), key = lambda i : classConfidence[i])
	return ans

def getClassNames(rootDir):
	global classNames 
	isFile = os.path.isfile('classNames.data')
	if isFile:
		f = file('classNames.data', 'r')
		classNames = p.load(f)
		f.close()
		# print classNames
		return classNames
	classNames = os.listdir(rootDir)
	classNames.sort()
	f = file('classNames.data', 'w')
	p.dump(classNames, f)
	f.close()
	return classNames

def testNB(rootDir):
	testNum = 0
	acNum = 0
	wrongNum = 0
	classNames = getClassNames(rootDir)
	cou = 0
	ANS = {}
	for parent, dirNames, fileNames in os.walk(rootDir):
		if len(fileNames) == 0:
			continue
		fileNum = len(fileNames)
		cou += 1
		className = classNames[cou - 1]
		
		print cou, className, parent
		logHandle.write('\n' + className + '\n') 
		an = 0
		wn = 0
		for i in range(int(fileNum*ratio), fileNum):
			fileName = fileNames[i]
			filePath = os.path.join(parent, fileName)
			testNum += 1
			ans = TextClassifier(filePath)
			if ans == className:
				an += 1
				print 'Y', 
				logHandle.write('Y ')
			else :
				wn += 1
				print ans, 
				print 'N',
				logHandle.write(ans + ' ')
		acNum += an 
		wrongNum += wn 
		ANS[className] = [an, wn]
		print an, '/', wn+an
		logHandle.write(str(an) + '/' + str(wn+an))
		logHandle.flush()
	print 'right answer: ', acNum, 'wrong answei :', wrongNum
	print 'test answer: ', 1.0*acNum / testNum
	logHandle.write('\nright answer: '+ str(acNum) + '  wrong answer: '+ str(wrongNum))
	logHandle.write('\ntest answer: '+ str(1.0*acNum / testNum))
	f = file('testAnswer.data', 'w')
	p.dump(ANS,f)
	f.close()

if __name__ == '__main__':

	logHandle = file("testLog.txt", "w")
	#load vocabulary.data
	f1 = file('vocabulary.data', 'r')
	vocabulary = p.load(f1)
	vocabulary.sort()
	f1.close()

	#load classPriorPro
	f2 = file('classPriorProbility.data', 'r')
	clsPriPro = p.load(f2)
	f2.close()

	#load wordProOnClass
	f3 = file('wordProOnClass.data', 'r')
	wordProOnClass = p.load(f3)
	f3.close()
	print TextClassifier('../data/testText.txt')
	testNB('../data/train')
	logHandle.close()
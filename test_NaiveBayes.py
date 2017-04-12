import os
from code.trainNB import train
from code.testNB import runTest
def test_train():
	dir = os.getcwd()
	os.chdir(dir + r'\code')
	train()
	runTest()


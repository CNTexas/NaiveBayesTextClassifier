import os
from code.trainNB import train
from code.testNB import runTest
def test_train():
	dir = os.getcwd()
	os.chdir(os.path.join(dir, "code"))
	train()
	runTest()


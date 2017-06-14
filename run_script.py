import os
for i in range(100):
	os.system("rm -rf ../149*")
	os.system("python test.py")

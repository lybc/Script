import os
import time
import shutil
def is_date(str):
	try:
		time.strptime(str, "%Y-%m-%d")
		return True
	except:
		return False


filepath = "D:\workspace\upupw\htdocs\LenovoCrm\uploads"
for filename in os.listdir(filepath):
	if is_date(filename):
		shutil.rmtree(filepath + "\\" + filename)
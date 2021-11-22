
def fileExist(path):
	try:
		open(path, "r")
	except:
		return False
	else:
		return True
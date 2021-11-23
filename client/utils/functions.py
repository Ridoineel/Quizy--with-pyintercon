import sys
import os
import pickle
import getpass

# do this to can import  utils.Class
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.Class import Color
from utils.variables import *

def login(cl, pseudo, password):
	req = {
		"name": "login",
		"body": {
			"pseudo": pseudo,
			"password": password
		}
	}

	res = cl.send(req)

	return res

def signup(cl, pseudo, password):
	req = {
		"name": "signup",
		"body": {
			"pseudo": pseudo,
			"password": password
		}
	}

	res = cl.send(req)

	return res

def userConnection(cl):
	haveAcct = input("Already have account ? (yes): ") or "yes" # set 'yes' as default

	pseudo = input("Pseudo: ")
	password = getpass.getpass("Password: ")

	if haveAcct in ["yes", "y", "oui"]:
		res = login(cl, pseudo, password)
	else:
		res = signup(cl, pseudo, password)

	if res["status"] == 0:
		print(Color.danger(res["message"]))
		print()

		# redo
		return userConnection(cl)
	else:
		best_score = res["best_score"]
		total_score = res["total_score"]

		return pseudo.capitalize(), password, best_score, total_score

def sendPlayLog(cl, pseudo, password, ip, quiz_id, score):
	req = {
		"name": "add_play_log",
		"body": {
			"pseudo": pseudo,
			"password": password,
			"ip": ip,
			"quiz_id": quiz_id,
			"score": score,
		}
	}


	res = cl.send(req)

	return res

def getQuestions(cl, nb):
	""" return question id and question label

	"""

	req = {
		"name": "quiz_questions",
		"body": {
			"nb": nb
		}
	}

	res = cl.send(req)

	return res["quiz_id"], res["questions"]

def submit(cl, quiz_id, q_id, answer):

	req = {
		"name": "submission",
		"body": {
			"quiz_id": quiz_id,
			"question_id": q_id,
			"answer": answer
		}
	}

	res = cl.send(req)

	success = bool(res["success"])

	return success


def saveLocal(pseudo):
	obj = {
		"pseudo": pseudo
	}

	with open(storage_file_path, "wb") as file:
		registration = pickle.Pickler(file)

		registration.dump(obj)

def getStateDatas():
	datas = {}
	storage_filename = "local_storage.data"

	if fileExist(storage_file_path):
		with open(storage_file_path, "rb") as file:
			registration = pickle.Unpickler(file)

			datas = registration.load()

	return datas

def fileExist(path):
	try:
		open(path, "r")
	except:
		return False
	else:
		return True

# def createFile(path):
# 	os.system(f"touch {path}")

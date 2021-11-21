import sys
import os

# do this to can import  utils.Class
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.Class import Color

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
	
	pseudo = input("Your pseudo: ")
	password = input("Password: ")

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
		return res["pseudo"], password, res["best_score"]

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
import os
import sys
import json
import random
import datetime

# do this to can import databases.requests and utils.variables
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import databases.requests as sqlRequests
from utils.variables import *  # nb_quiz and quizs_path



def getQuizDatas(quiz_id):
	quiz_path = quizs_path[quiz_id]
	quiz_datas = json.load(open(quiz_path))

	return quiz_datas

def getQuizQuestions(body):
	nb_questions = body.get("nb")

	if nb_questions != None:
		# Get random Quiz path
		random_quiz_id = random.randint(0, nb_quiz - 1)

		# Get quiz datas and questions list
		quiz_datas = getQuizDatas(random_quiz_id)
		quiz_questions = list(quiz_datas.keys())
		total_questions = len(quiz_questions)

		# (id, question)
		questions = list(enumerate(quiz_questions))
		sample_questions = random.sample(questions, min(nb_questions, total_questions))

		res = {
			"status": 1,
			"questions": sample_questions,
			"quiz_id": random_quiz_id
		}

	else:
		res = {
			"status": 0,
			"message": "missing nb: number of questions"
		}

	return res

def result(body):
	quiz_id = body.get("quiz_id")
	question_id = body.get("question_id")
	answer = body.get("answer")

	if quiz_id != None and question_id != None and answer != None:
		answer = str(answer).strip()

		# Get quiz datas and questions list
		quiz_datas = getQuizDatas(quiz_id)
		quiz_questions = list(quiz_datas.keys())

		question = quiz_questions[question_id]
		right_answers = quiz_datas[question] 

		# convert all right answers in lower case
		right_answers = [i.lower() for i in right_answers]

		is_right = answer.lower() in right_answers

		res = {"status": 1, "success": is_right}
	else:
		msg = "Missing question id or answer."

		res = {"status": 0, "message": msg}

	return res

def checkAuth(body):
	""" Refer to user login:
		return pseudo and best_score if user is registered
	
	"""

	pseudo = body.get("pseudo").lower()
	password = body.get("password")

	if pseudo != None and password != None:
		if sqlRequests.isUser(pseudo, password):
			best_score = sqlRequests.getUserInfo(pseudo, "best_score")
			total_score = sqlRequests.getUserInfo(pseudo, "total_score")

			res = {
				"status": 1,
				"pseudo": pseudo,
				"best_score": best_score,
				"total_score": total_score
			}
		else:
			res = {
				"status": 0,
				"message": "Incorrect pseudo or password"
			}
	else:
		res = {
			"status": 0,
			"message": "Missing pseudo or password"
		}

	return res

def createUser(body):
	""" Create new user with pseudo and password,
		and return response ("status", ...)
	
	"""

	pseudo = body.get("pseudo").lower()
	password = body.get("password")

	if pseudo != None and password != None:
		date = datetime.datetime.now()
		date = date.strftime("%m-%d-%Y %H:%M:%S")

		if sqlRequests.isUser(pseudo, password):
			res = {
				"status": 0,
				"message": "This pseudo exist"
			}
		else:
			sqlRequests.createUser(pseudo, password, date)

			res = {
				"status": 1,
				"pseudo": pseudo,
				"best_score": 0,
				"total_score": 0
			}
	else:
		res = {
			"status": 0,
			"message": "Missing pseudo or password"
		}

	return res

def addPlayLog(body):
	pseudo = body.get("pseudo").lower()
	password = body.get("password")
	ip = body.get("ip")
	quiz_id = body.get("quiz_id")
	score = body.get("score")

	if pseudo != None and quiz_id != None and password != None:
		date = datetime.datetime.now()
		date = date.strftime("%m-%d-%Y %H:%M:%S")

		best_score = sqlRequests.getUserInfo(pseudo, "best_score") 
		total_score = sqlRequests.getUserInfo(pseudo, "total_score")

		quiz_name = filename(quizs_path[quiz_id])

		if sqlRequests.isUser(pseudo, password):
			total_score += score

			# create Log
			sqlRequests.createLog(pseudo, ip, quiz_name, score, date)
			# update user total score and user last_view date
			sqlRequests.updateUserInfo(pseudo, "total_score", total_score)
			sqlRequests.updateUserInfo(pseudo, "last_view", date)

			# Update user score if score > best_score
			if score > best_score:
				sqlRequests.updateUserInfo(pseudo, "best_score", score)

			res = {"status": 1}
		else:
			res = {"status": 0}
	else:
		res = {
			"status": 0,
			"message": "Missing pseudo or quiz_id"
		}

	return res

def filename(path):
	path_rev = path[::-1]

	# fisrt slash index in reverse mode
	if "/" in path_rev:
		slash_index = path_rev.index("/")
	else:
		slash_index = -1

	name_rev = path_rev[:slash_index]
	name = name_rev[::-1]

	return name

def fileExist(path):
	try:
		open(path, "r")
	except:
		return False
	else:
		return True
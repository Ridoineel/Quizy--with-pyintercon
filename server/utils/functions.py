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
		right_answer = quiz_datas[question]

		is_right = right_answer.lower() == answer.lower()

		res = {"status": 1, "success": is_right}
	else:
		msg = "Missing question id or answer."

		res = {"status": 0, "message": msg}

	return res

def checkAuth(body):
	""" Refer to user login:
		return pseudo and best_score if user is registered
	
	"""

	pseudo = body.get("pseudo")
	password = body.get("password")

	if pseudo != None and password != None:
		if sqlRequests.isUser(pseudo, password):
			best_score = sqlRequests.getUserScore(pseudo)
			total_score = sqlRequests.getUserTotalScore(pseudo)

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
		and return response
	
	"""

	pseudo = body.get("pseudo")
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
	pseudo = body.get("pseudo")
	password = body.get("password")
	ip = body.get("ip")
	quiz_id = body.get("quiz_id")
	score = body.get("score")

	if pseudo != None and quiz_id != None and password != None:
		date = datetime.datetime.now()
		date = date.strftime("%m-%d-%Y %H:%M:%S")

		best_score = sqlRequests.getUserScore(pseudo) 
		quiz_name = quizs_path[quiz_id]

		if sqlRequests.isUser(pseudo, password):
			sqlRequests.createLog(pseudo, ip, quiz_name, score, date)

			# Update user score if score > best_score
			if score > best_score:
				sqlRequests.updateScore(pseudo, score)

			res = {"status": 1}
		else:
			res = {"status": 0}
	else:
		res = {
			"status": 0,
			"message": "Missing pseudo or quiz_id"
		}

	return res
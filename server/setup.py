#! /usr/bin/env python3

from pyintercon import Server
# get functions result, getQuizQuestions, createUser, checkAuth and addPlayLog
from utils.functions import *

host = "localhost"
port = 8081

funcs = {
	"submission": result,
	"quiz_questions": getQuizQuestions,
	"signup": createUser,
	"login": checkAuth,
	"add_play_log": addPlayLog
}

def responseManager(request):
	name = request.get("name") # would be "submision" or "quiz_questions"
	# default response
	res = {
		"status": 0,
		"message": "missing body"
	}

	body = request.get("body")

	if body:
		if name in funcs:
			res = funcs[name](body)
		else:
			res = {"status": 0, "message": "invalid request name"}

	return res

def main():
	sv = Server(1)
	sv.treatment = responseManager

	sv.activate(host, port)

if __name__ == "__main__":
	main()

#! /usr/bin/env python3

import json
import os
import random
from pyintercon import Server

host = "localhost"
port = 8080

# quizs paths
quizs_path = os.popen("ls datas/*.json").read().split()

if not quizs_path:
    print("Empty or missing datas directory")
    exit()

nb_quiz = len(quizs_path)

# Get random Quiz datas & questions list
quiz_path = random.choice(quizs_path)
quiz_datas = json.load(open(quiz_path))
quiz_questions = list(quiz_datas.keys())

total_questions = len(quiz_questions)

# save user
# login user
# get quiz question
# get the result of submission

def getQuizQuestions(nb_questions):
    if type(nb_questions) != int or nb_questions <= 0:
        return []

    # (id, question)
    questions = list(enumerate(quiz_questions))

    # return random {nb_questions} questions (id, question)
    return random.sample(questions, min(nb_questions, total_questions))

def result(question_id, answer):
    if type(question_id) != int or not (0 <= question_id < total_questions):
        return False

    answer = str(answer).strip()

    question = quiz_questions[question_id]
    right_answer = quiz_datas[question]

    return right_answer.lower() == answer.lower()

def responseManager(request):
    name = request.get("name") # would be "submision" or "quiz_questions"
    # default response
    res = {
        "response": "invalid request",
        "message": "Invalid request name"
    }

    body = request.get("body")

    if name == "submission":
        if body:
            question_id = body.get("question_id")
            answer = body.get("answer")

            if question_id != None and answer != None:
                res_status = int(result(question_id, answer))
                res = {"success": res_status}
            else:
                res["message"] = "Missing question id or answer."
    elif name == "quiz_questions":
        nb = body.get("nb")

        if nb:
            questions = getQuizQuestions(nb)
            res = {"questions": questions}

    return res

def main():
    sv = Server(1)
    sv.treatment = responseManager

    sv.activate(host, port)

if __name__ == "__main__":
    main()

#! /usr/bin/env python3

from os import system
from random import shuffle
from pyintercon import Client

host = "localhost"
port  = 8080

class Color:
	success = lambda _str: '\033[92m' + _str + '\033[0m'
	danger = lambda _str: '\033[91m' + _str + '\033[0m'

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

    return res["questions"]

def submit(cl, q_id, answer):

    req = {
        "name": "submission",
        "body": {
            "question_id": q_id,
            "answer": answer
        }
    }

    res = cl.send(req)

    success = bool(res["success"])

    return success

def main():
    cl = Client()
    cl.connect(host, port)

    nb_random_questions = 10
    
    print("QUIZY".center(40))
    print()

    questions = getQuestions(cl, nb_random_questions)

    quiz_results = []

    i = 1
    for id, question in questions:
        print(f"Q{i}: {question}")

        answer = input(">>> ")

        success = submit(cl, id, answer)

        if success:
            success_msg = Color.success("Right answer")
        else:
            success_msg = Color.danger("Wrong answer")

        print(success_msg)

        quiz_results.append(["Wrong", "Right"][success])

        # system("clear")
        print()

        i += 1

    print(quiz_results)

if __name__ == "__main__":
    main()

#! /usr/bin/env python3

from os import system
from random import shuffle
from pyintercon import Client

host = "localhost"
port  = 8081

def getQuestions(cl):
    """ return question id and question label

    """

    req = {
        "name": "quiz_questions"
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

    print("QUIZYYYYY".center(40))
    print()

    questions = getQuestions(cl)

    # change questions order
    shuffle(questions)

    quiz_results = []

    i = 1
    for id, question in questions:
        print(f"{i}: {question}")

        answer = input("Your answer: ")

        success = submit(cl, id, answer)

        quiz_results.append(success)

        system("clear")
        i += 1

    print(quiz_results)

if __name__ == "__main__":
    main()

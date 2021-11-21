#! /usr/bin/env python3

from random import shuffle
from pyintercon import Client

# get functions login, signup, submit, sendPlayLog and getQuestions, userConnection
from utils.functions import *
# get class Color and Style
from utils.Class import *

host = "localhost"
port  = 8080

def main():
	cl = Client()
	cl.connect(host, port)

	title = "Welcome in QUIZY"
	title = Style.bold(Style.underline(title))
	print(title.center(100))
	print()

	pseudo, password, best_score = userConnection(cl)

	nb_random_questions = 10
	continuous = True

	while continuous:
		print()
		print("Answer the questions:\n")

		print("Best score: " + Color.success(str(best_score)) + "\n")

		quiz_id, questions = getQuestions(cl, nb_random_questions)

		score = int()
		quiz_results = []
		
		i = 1
		for id, question in questions:
			print(f"Q{i}: {question}")

			answer = input(">>> ")

			success = submit(cl, quiz_id, id, answer)

			if success:
				success_msg = Style.bold(Color.success("Right answer"))
				score += 10
			else:
				success_msg = Style.bold(Color.danger("Wrong answer"))
				score -= 5

			print(success_msg)
			print()

			quiz_results.append(["Wrong", "Right"][success])

			i += 1
		
		# set score to 0 if he is negative
		score = max(score, 0)
		
		print(f"Score: {score}")

		if score > best_score:
			print("Congratulation: new score (best score)")
			best_score = score
		
		# add logs
		res = sendPlayLog(cl, pseudo, password, host, quiz_id, score)

		print(quiz_results)

		redo = input("Redo ? (yes): ") or "yes" # set 'yes' as default

		continuous = redo in ["yes", "y", "oui"]

if __name__ == "__main__":
	main()

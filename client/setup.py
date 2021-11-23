#! /usr/bin/env python3

import os
import getpass
from random import shuffle
from pyintercon import Client

# get functions login, signup, submit, sendPlayLog and getQuestions, userConnection, 
from utils.functions import *
# get class Color and Style
from utils.Class import *
# get local storage file path
from utils.variables import storage_file_path, nb_random_questions

host = "localhost"
port  = 8081

def main():
	cl = Client()
	cl.connect(host, port)

	title = "Welcome in QUIZY"
	title = Style.bold(Style.underline(title))

	print(title.center(100))
	print()

	# get state datas
	stateDatas = getStateDatas()

	if stateDatas:
		pseudo = stateDatas["pseudo"]

		cont = input(f"Continous with pseudo {Style.bold(pseudo)} ? (yes): ") or "yes" # set 'yes' as default

		if cont in ["yes", "y", "oui", "o"]:
			password = getpass.getpass("Password: ")

			res = login(cl, pseudo, password)

			if res["status"] == 0:
				# del storage file
				os.remove(storage_file_path)

				print(Color.danger(res["message"]))
				exit()


			best_score = res["best_score"]
			total_score = res["total_score"]
		else:
			pseudo, password, best_score, total_score = userConnection(cl)
	else:
		# if user state datas not exist
		pseudo, password, best_score, total_score = userConnection(cl)

	# local save
	saveLocal(pseudo)

	continuous = True

	while continuous:
		# clear console
		os.system("cls||clear")

		print()
		print("Answer the questions:\n")

		print("Total score: " + Color.success(str(total_score)))
		print("Best score: " + Color.success(str(best_score)))
		print()

		quiz_id, questions = getQuestions(cl, nb_random_questions)

		score = int()
		quiz_results = []
		
		i = 1
		for id, question in questions:
			print(f"Q{i}: {question}")

			answer = input(">>> ")

			success = submit(cl, quiz_id, id, answer)

			if success:
				success_msg = Style.bold(Color.success("Right answer (+10)"))
				score += 10
			else:
				success_msg = Style.bold(Color.danger("Wrong answer (-5)"))
				score -= 5

			print(success_msg)
			print()

			quiz_results.append(["Wrong", "Right"][success])

			i += 1
		
		print(f"Score: {score}")

		if score > best_score:
			print(Style.blink(Color.primary(
					f"Congratulation. New score: {Style.bold(str(score))}"
					))
			)

			best_score = score

		# add score to total_score
		total_score += score
		
		# add logs
		res = sendPlayLog(cl, pseudo, password, host, quiz_id, score)

		# print(quiz_results)

		redo = input("\nRedo ? (yes): ") or "yes" # set 'yes' as default

		continuous = redo in ["yes", "y", "oui"]

if __name__ == "__main__":
	main()

import os

# quizs paths
quizs_path = os.popen("ls datas/*.json").read().split()

if not quizs_path:
	print("Empty or missing datas directory")
	exit()

nb_quiz = len(quizs_path)
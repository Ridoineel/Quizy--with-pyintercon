import re
from os import listdir
from os.path import isfile, join, dirname

_parentdir = dirname(dirname(__file__))
# quizs paths
quizs_path = list()

for file in listdir(join(_parentdir, "datas")):
	file_path = join(_parentdir, "datas", file)

	# filter the json files
	if isfile(file_path) and re.match(r"^.*\.json$", file) is not None:
		quizs_path.append(file_path)

if not quizs_path:
	print("Empty or missing datas directory")
	exit()

nb_quiz = len(quizs_path)
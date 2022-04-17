# QUIZY. Simple quiz application using my Pyintercon module

Do following commands to get project or download it using the button with labeled as "Code":

```bash
git clone https://github.com/Ridoineel/Quizy--with-pyintercon.git
cd Quizy--with-pyintercon

```

This project contains two directories:
* client
* server

client for client configuration and server for server configurations

So copy client directory once for player( client)

> By default, number of players (client) set as 1 in server/setup.py main function
> So, change it to change number of players
___

Quiz datas is in server/datas directory, json file.
Add new quiz with json file in this form.

```json
{
	"question1":
		["answer1", "answer2", "answerM"],
	"question2":
		["answer1", "answer2", "answerM"],
	"questionnM":
		["answer1", "answer2", "answerM"],
}
```

> The players get random questions, random numbers of questions from random quiz.
the random number of questions is in client/utils/variables.py 10 by default **(edit it)**

So you can put more than questions in one quiz (json file).

___

> To refresh database, go to server/databases and run **refresh.py**
___

___
> #### If user quit game, you must be restart server before he can restart. Sorry, It will be resolved
___

### For server:

In localhost, you can set ip as "localhost".
But in network (local) set ip as true host ip (exemple: 10.22.22.22), don't set as 127.0.0.1 (for example) for this.

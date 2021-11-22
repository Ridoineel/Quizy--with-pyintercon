import sqlite3
import os

dirname = os.path.dirname(__file__)

con = sqlite3.connect(f"{dirname}/User.db")
cur = con.cursor()

def no_interference(value):
    """ to avoir sql injection """

    value = str(value)
    return "'" not in value and '"' not in value

def isUser(pseudo, password):
    comb = pseudo + password

    assert no_interference(comb)

    res = cur.execute(f"""
        SELECT *
        FROM User
        WHERE pseudo='{pseudo}' and password='{password}'
    """)

    if list(res):
        return True
    else:
        return False

    con.commit()

def getUserScore(pseudo):
    assert no_interference(pseudo)

    res = cur.execute(f"""
        SELECT best_score
        FROM User
        WHERE pseudo='{pseudo}'
    """)

    con.commit()

    score = list(res)[0][0]

    return score

def getUserTotalScore(pseudo):
    assert no_interference(pseudo)

    res = cur.execute(f"""
        SELECT SUM(score) 
        FROM PlayLog 
        WHERE player='{pseudo}'
    """)

    total_score = list(res)[0][0]

    return total_score

def updateScore(pseudo, new_score):

    assert no_interference(pseudo) and no_interference(new_score)

    cur.execute(f"""
        UPDATE User
        SET best_score={new_score}
        WHERE pseudo='{pseudo}'
    """)

    con.commit()

def createUser(pseudo, password, date):
    assert sum(map(no_interference, [pseudo, password, date])) == 3

    cur.execute(f"""
        INSERT INTO User
        VALUES(
            '{pseudo}',
            '{password}',
            '{date}',
            '{date}',
            0
        )
    """)
    con.commit()
    print(f"New user {pseudo}")

def createLog(pseudo, ip, quiz_name, score, date):
    assert sum(map(no_interference, [pseudo, ip, quiz_name, score, date])) == 5


    cur.execute(f"""
        INSERT INTO PlayLog
        VALUES(
            '{pseudo}',
            '{ip}',
            '{quiz_name}',
            '{score}',
            '{date}'
        )
    """)
    con.commit()
    
    print(f"User: {pseudo}, ip: {ip}, quiz: {quiz_name}, score: {score}, date: {date}")
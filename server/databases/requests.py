import sqlite3
import os
import refresh

from functions import fileExist

dirname = os.path.dirname(__file__)

# refresh (create) database if not exist
if not fileExist(f"{dirname}/quizy.db"):
    refresh.main()

# connect to database
con = sqlite3.connect(f"{dirname}/quizy.db")
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

def getUserInfo(pseudo, column):
    assert no_interference(pseudo)

    res = cur.execute(f"""
        SELECT {column}
        FROM User
        WHERE pseudo='{pseudo}'
    """)

    con.commit()

    value = list(res)[0][0]

    return value

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

def updateUserInfo(pseudo, column, value):

    assert sum(map(no_interference, [pseudo, column, value])) == 3

    cur.execute(f"""
        UPDATE User
        SET {column}='{value}'
        WHERE pseudo='{pseudo}'
    """)

    con.commit()

def createUser(pseudo, password, date):
    assert sum(map(no_interference, [pseudo, password, date])) == 3

    try:
        cur.execute(f"""
            INSERT INTO User
            VALUES(
                '{pseudo}',
                '{password}',
                '{date}',
                '{date}',
                0,
                0
            )
        """)
    except sqlite3.IntegrityError as e:
        print("Warning: ", e)
        exit()

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

def getUsers(sorted_by="pseudo", desc=True):
    assert no_interference(sorted_by)

    res = cur.execute(f"""
        SELECT * 
        FROM User
        ORDER BY {sorted_by}
        {'desc' if desc else ''}
    """)

    return res
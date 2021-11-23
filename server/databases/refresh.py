#!/usr/bin/env python3

import sqlite3
import os
from functions import fileExist

dirname = os.path.dirname(__file__)

def main():
    db_path = os.path.join(dirname, "quizy.db")
    
    # delete database
    if fileExist(db_path):
        os.remove(db_path)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE 
            User(
                    pseudo varchar unique,
                    password varchar(256),
                    date varchar(256),
                    last_view varchar(256),
                    best_score integer,
                    total_score integer
                )
    """)

    cur.execute("""
        CREATE TABLE 
            PlayLog(
                    player varchar,
                    ip varchar(20),
                    quiz_name varchar(256),
                    score integer,
                    date varchar(20)
                )
    """)

    con.commit()

    con.close()

if __name__ == "__main__":
    refresh = input("Are you sure to refresh databases ? (yes|no): ")

    if refresh in ["yes", "oui", "y"]:
        main()

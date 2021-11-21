#!/usr/bin/env python3

import sqlite3
import sys
import os

dirname = os.path.dirname(__file__)

refresh = input("You want sure to refresh databases ? (yes|no): ")

if refresh in ["yes", "oui", "y"]:
    # delete User.db
    os.system(f"rm {dirname}/User.db")


    con = sqlite3.connect(f"{dirname}/User.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE User(
                        pseudo varchar unique,
                        password varchar(256),
                        date varchar(256),
                        last_view varchar(256),
                        best_score integer
                    )
    """)

    cur.execute("""
        CREATE TABLE PlayLog(
                        player varchar,
                        ip varchar(20),
                        quiz_name varchar(256),
                        score integer,
                        date varchar(20)
                    )
    """)

    con.commit()

con.close()

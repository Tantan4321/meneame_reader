#!/usr/bin/env python3
import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def db_connect(db_path: str = DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def create_article(connection, title, username, sub, timestamp):
    sql = """
        INSERT INTO articles (title, votes, user, sub, timestamp) 
        VALUES (?,?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (title, 0, username, sub, timestamp))
    return cur.lastrowid


def update_votes(connection, title, votes):
    sql = """
            UPDATE articles SET votes = ? WHERE title = ?"""

    cur = connection.cursor()
    cur.execute(sql, (votes, title))
    return cur.lastrowid

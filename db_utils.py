#!/usr/bin/env python3
import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def db_connect(db_path: str = DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def create_database(connection):
    cur = connection.cursor()

    articles_sql = """
    CREATE TABLE articles (
        id integer PRIMARY KEY,
        title text NOT NULL,
        votes integer NOT NULL,
        comments integer NOT NULL,
        posting_user text NOT NULL,
        sub text NOT NULL,
        timestamp text NOT NULL)"""
    cur.execute(articles_sql)

    votes_sql = """
    CREATE TABLE votes (
        id integer PRIMARY KEY,
        user text NOT NULL,
        status text NOT NULL,
        timestamp text NOT NULL,
        article_id integer NOT NULL,
        FOREIGN KEY (article_id) REFERENCES articles (id))"""
    cur.execute(votes_sql)

    comments_sql = """
    CREATE TABLE comments (
        id integer PRIMARY KEY,
        user text NOT NULL,
        status text NOT NULL,
        timestamp text NOT NULL,
        article_id integer NOT NULL,
        FOREIGN KEY (article_id) REFERENCES articles (id))"""
    cur.execute(comments_sql)

    edits_sql = """
    CREATE TABLE edits (
        id integer PRIMARY KEY,
        user text NOT NULL,
        status text NOT NULL,
        timestamp text NOT NULL,
        article_id integer NOT NULL,
        FOREIGN KEY (article_id) REFERENCES articles (id))"""
    cur.execute(edits_sql)

    published_sql = """
    CREATE TABLE published (
        id integer PRIMARY KEY,
        user text NOT NULL,
        status text NOT NULL,
        timestamp text NOT NULL,
        article_id integer NOT NULL,
        FOREIGN KEY (article_id) REFERENCES articles (id))"""
    cur.execute(published_sql)

    problems_sql = """
    CREATE TABLE problems (
        id integer PRIMARY KEY,
        title text NOT NULL,
        user text NOT NULL,
        status text NOT NULL,
        timestamp text NOT NULL)"""
    cur.execute(problems_sql)

    post_sql = """
    CREATE TABLE posts (
        id integer PRIMARY KEY,
        title text NOT NULL,
        user text NOT NULL,
        status text NOT NULL,
        timestamp text NOT NULL)"""
    cur.execute(post_sql)


def create_article(connection, title, username, sub, timestamp):
    sql = """
        INSERT INTO articles (title, votes, user, sub, timestamp) 
        VALUES (?,?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (title, 0, username, sub, timestamp))
    return cur.lastrowid


def handle_exit(connection):
    print('committing and closing DB...')
    connection.commit()
    connection.close()
    print('Success!')


def update_votes(connection, title, votes):
    sql = """
            UPDATE articles SET votes = ? WHERE title = ?"""

    cur = connection.cursor()
    cur.execute(sql, (votes, title))
    return cur.lastrowid


def print_table(connection):
    """
    For debugging purposes.
    Prints all rows in the SQLite articles table in the format:
    (id, title, votes)
    """
    cur = connection.cursor()
    cur.execute("SELECT * FROM articles")
    results = cur.fetchall()

    for row in results:
        print(row)

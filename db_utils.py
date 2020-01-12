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

    connection.commit()


def create_article(connection, title, username, sub, timestamp):
    sql = """
        INSERT INTO articles (title, votes, comments, posting_user, sub, timestamp) 
        VALUES (?,?,?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (title, 0, 0, username, sub, timestamp))


def find_article(connection, title) -> int:
    """
        Finds the id of the of the article in the articles table (if it exists)
        :return: -1 if the article doesn't exist, otherwise returns the table id
    """
    sql = """
                SELECT id FROM articles WHERE title = ?"""

    cur = connection.cursor()
    cur.execute(sql, (title,))
    result = cur.fetchone()
    if result is None:
        article_id = -1  # the article does not exist in the db
    else:
        article_id = result[0]  # article exists, get id
    return article_id


def add_vote(connection, article_id, username, status, timestamp):
    sql = """
        INSERT INTO votes (user, status, timestamp, article_id) 
        VALUES (?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (username, status, timestamp, article_id))


def add_comment(connection, article_id, username, status, timestamp):
    sql = """
        INSERT INTO comments (user, status, timestamp, article_id) 
        VALUES (?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (username, status, timestamp, article_id))


def add_edit(connection, article_id, username, status, timestamp):
    sql = """
        INSERT INTO edits (user, status, timestamp, article_id) 
        VALUES (?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (username, status, timestamp, article_id))


def add_published(connection, article_id, username, status, timestamp):
    sql = """
        INSERT INTO published (user, status, timestamp, article_id) 
        VALUES (?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (username, status, timestamp, article_id))


def add_problem(connection, title, username, status, timestamp):
    sql = """
        INSERT INTO problems (title, user, status, timestamp) 
        VALUES (?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (title, username, status, timestamp))


def add_post(connection, title, username, status, timestamp):
    sql = """
        INSERT INTO posts (title, user, status, timestamp) 
        VALUES (?,?,?,?)"""

    cur = connection.cursor()
    cur.execute(sql, (title, username, status, timestamp))


def update_votes(connection, article_id, votes):
    sql = """
            UPDATE articles SET votes = ? WHERE id = ?"""

    cur = connection.cursor()
    cur.execute(sql, (votes, article_id))


def update_comments(connection, article_id, comments):
    sql = """
            UPDATE articles SET comments = ? WHERE id = ?"""

    cur = connection.cursor()
    cur.execute(sql, (comments, article_id))


def handle_exit(connection):
    print('committing and closing DB...')
    connection.commit()
    connection.close()
    print('Success!')


def print_table(connection):
    """
    For debugging purposes.
    Prints all rows in the SQLite articles table.
    """
    cur = connection.cursor()
    cur.execute("SELECT * FROM articles")
    results = cur.fetchall()

    for row in results:
        print(row)

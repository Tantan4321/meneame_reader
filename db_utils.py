#!/usr/bin/env python3
import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def db_connect(db_path: str = DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

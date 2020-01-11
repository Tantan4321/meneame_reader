#!/usr/bin/env python3

from datetime import datetime
import db_utils

import atexit
import requests
from bs4 import BeautifulSoup


def exit_handler(connection):
    db_utils.handle_exit(connection)


def run_reader():
    last_timestamp = 0
    is_first_run = True
    last_events = []

    try:
        requests.get("https://www.google.com/")
    except Exception:
        print("HTTPS error, check connection")
        exit(0)

    con = db_utils.db_connect()  # connect to sqlite database
    atexit.register(exit_handler, con)

    latest_events = []
    try:
        while True:
            r = requests.get("https://www.meneame.net/backend/sneaker2")
            data = r.json()  # parse response into json

            events_list = data["events"]  # parse events item into list
            reversed_events = events_list[::-1]  # reverse the list to be chronologically correct

            latest_events.clear()  # clear the local latest events tracker

            if is_first_run:
                last_timestamp = int(events_list[0]["ts"])  # first element of reversed list will be latest event
                for event in reversed_events:
                    if int(event["ts"]) == int(last_timestamp):
                        latest_events.append(event)
                    log_entry(con, event)

                last_events = latest_events.copy()  # copy local latest events into last events
                is_first_run = False
            else:
                new_timestamp = int(events_list[0]["ts"])  # first element of reversed list will be the most recent
                for event in reversed_events:
                    if int(event["ts"]) == int(new_timestamp):  # keep track of latest events for next run
                        latest_events.append(event)
                    if int(event["ts"]) < int(last_timestamp):  # entry is before latest timestamp, already logged
                        continue
                    if int(event["ts"]) == int(last_timestamp):  # new entries with latest timestamp could have arrived
                        if event in last_events:
                            continue  # this event was reported last run, continue
                    log_entry(con, event)

                last_events = latest_events.copy()  # copy local latest events into last events
                last_timestamp = new_timestamp  # track last timestamp for next run

    except KeyboardInterrupt:
        print('Keyboard interrupt...')


def print_entry(time, sub_name, action, votes: str, comments: str, title, user, status):
    vote_comments = str(votes) + "/" + str(comments)

    print(str(BeautifulSoup("{} | {:<12} | {:<10} | {:<8} | {} | {} | {}"
                            .format(time, sub_name, action, vote_comments, title, user, status), 'html.parser')))


def log_entry(connection, event):
    time = str(datetime.utcfromtimestamp(int(event["ts"])).strftime('%Y-%m-%d %H:%M:%S'))
    sub_name = event["sub_name"]
    action = str(event["type"]).strip()
    votes = event["votes"]
    comments = str(event["com"]).strip()
    title = event["title"]
    user = event["who"]
    status = event["status"]

    # if action == 'new':
    #     db_utils.create_article(connection, title, user, sub_name, time)
    #
    # if action == 'vote':
    #     db_utils.update_votes(connection, title, int(votes))
    #
    # if action == 'comment':
    #     db_utils.update_comments(connection, title, int(comments))

    print_entry(time, sub_name, action, votes, comments, title, user, status)  # print the entry in CL


if __name__ == "__main__":
    run_reader()

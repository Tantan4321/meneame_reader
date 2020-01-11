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
    atexit.register(exit_handler, con)  # register exit_handler to run on script stop

    try:
        while True:
            r = requests.get("https://www.meneame.net/backend/sneaker2")
            data = r.json()  # parse response into json

            events_list = data["events"]  # parse events item into list
            reversed_events = events_list[::-1]  # reverse the list to be chronologically correct

            latest_events = []  # create empty local latest events tracker

            if is_first_run:
                last_timestamp = int(events_list[0]["ts"])  # first element of reversed list will be latest event
                for event in reversed_events:
                    ret = build_entry(event).strip()
                    if int(event["ts"]) == last_timestamp:
                        last_events.append(ret)
                    print(ret)  # print the entry in CL
                    # log_entry(con, event)
                is_first_run = False
            else:
                latest_events.clear()
                new_timestamp = int(events_list[0]["ts"])  # first element of reversed list will be the most recent
                for event in reversed_events:
                    ret = build_entry(event).strip()  # build the formatted string
                    if int(event["ts"]) == new_timestamp:  # keep track of latest events for next run
                        latest_events.append(ret)
                    if int(event["ts"]) < last_timestamp:  # entry is before last timestamp, already logged
                        continue
                    if int(event["ts"]) == last_timestamp:  # new entries with last timestamp could have arrived
                        skip = False
                        for old_event in last_events:
                            old = ":".join("{:02x}".format(ord(c)) for c in old_event)
                            new = ":".join("{:02x}".format(ord(c)) for c in ret)
                            if old == new:
                                skip = True
                                break
                        if skip:
                            continue  # this event was reported last run, continue
                    print(ret)
                    # log_entry(con, event)

                last_events.clear()  # clear out last events list
                last_events = latest_events.copy()  # copy local latest events into last events
                last_timestamp = new_timestamp  # track last timestamp for next run

    except KeyboardInterrupt:
        print('Keyboard interrupt...')


def build_entry(event) -> str:
    time = convert_to_datatime(int(event["ts"]))
    sub_name = event["sub_name"]
    action = event["type"]
    title = event["title"]
    user = event["who"]
    status = event["status"]
    vote_comments = str(event["votes"]) + "/" + str(event["com"])

    return str(BeautifulSoup("{} | {:<12} | {:<10} | {:<8} | {} | {} | {}"
                             .format(time, sub_name, action, vote_comments, title, user, status), 'html.parser'))


def convert_to_datatime(timestamp: int) -> str:
    return str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))


def convert_to_epoch(timestamp: str) -> int:
    dt_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return int(dt_obj.timestamp())


def log_entry(connection, event):
    time = convert_to_datatime(int(event["ts"]))
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


if __name__ == "__main__":
    run_reader()

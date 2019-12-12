import requests
from bs4 import BeautifulSoup

from project import firehose_url
from datetime import datetime


def run_reader():
    last_timestamp = 0
    same_ts_count = 0  # keep track of number of events with last_timestamp

    while True:
        try:
            r = requests.get(firehose_url)
        except Exception:
            print("No HTTPS connection")
            exit(0)
        data = r.json()  # parse response into json

        events_list = data["events"]  # parse events item into list
        reversed_events = events_list[::-1]  # reverse the list to be chronologically correct
        ts_duplicate_counter = 0  # unique events with same ts can show up next query

        for event in reversed_events:
            if int(event["ts"]) < int(last_timestamp):
                continue
            if int(event["ts"]) == int(last_timestamp):
                ts_duplicate_counter += 1
                if ts_duplicate_counter <= same_ts_count:
                    continue  # this would be a duplicate event, continue

            print_entry(event)
            last_timestamp = event["ts"]  # track last timestamp for next run

        same_ts_count = ts_duplicate_counter


def print_entry(event):
    time = str(datetime.utcfromtimestamp(int(event["ts"])).strftime('%Y-%m-%d %H:%M:%S'))
    sub_name = event["sub_name"]
    action = event["type"]
    vote_comments = str(event["votes"]) + "/" + str(event["com"])
    title = event["title"]
    user = event["who"]
    status = event["status"]

    print(BeautifulSoup("{} | {:<12} | {:<8} | {:<8} | {} | {} | {}"
                        .format(time, sub_name, action, vote_comments, title, user, status), "html.parser"))

import requests
from bs4 import BeautifulSoup

from datetime import datetime


def run_reader():
    last_timestamp = 0
    same_ts_count = 0  # keep track of number of events with last_timestamp
    ts_duplicate_counter = 1  # unique events with same ts can show up next query, init with 1
    try:
        requests.get("https://www.google.com/")
    except Exception:
        print("HTTPS error, check connection")
        exit(0)
    while True:
        r = requests.get("https://www.meneame.net/backend/sneaker2")
        data = r.json()  # parse response into json

        events_list = data["events"]  # parse events item into list
        reversed_events = events_list[::-1]  # reverse the list to be chronologically correct

        for event in reversed_events:
            if int(event["ts"]) < int(last_timestamp):  # entry is before latest timestamp, already logged
                continue
            if int(event["ts"]) == int(last_timestamp):  # new entries with latest timestamp could have arrived
                ts_duplicate_counter += 1
                if ts_duplicate_counter <= same_ts_count:
                    continue  # this would be a duplicate event, continue

            print_entry(event)
            last_timestamp = event["ts"]  # track last timestamp for next run

        same_ts_count = ts_duplicate_counter  # track number of entries with latest timestamp for next run
        ts_duplicate_counter = 0  # reset ts counter for next loop


def print_entry(event):
    time = str(datetime.utcfromtimestamp(int(event["ts"])).strftime('%Y-%m-%d %H:%M:%S'))
    sub_name = event["sub_name"]
    action = event["type"]
    vote_comments = str(event["votes"]) + "/" + str(event["com"])
    title = event["title"]
    user = event["who"]
    status = event["status"]

    print(BeautifulSoup("{} | {:<12} | {:<10} | {:<8} | {} | {} | {}"
                        .format(time, sub_name, action, vote_comments, title, user, status), "html.parser"))


if __name__ == "__main__":
    run_reader()

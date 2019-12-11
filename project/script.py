import requests

from project import firehose_url


def run_reader():
    last_timestamp = 0
    same_ts_count = 0  # keep track of number of events with last_timestamp
    while True:
        r = requests.get(firehose_url)
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

            print(event["ts"])
            last_timestamp = event["ts"]  # track last timestamp for next run

        same_ts_count = ts_duplicate_counter


def print_entry(timestamp, sub, action):
    print("test")

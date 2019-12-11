import requests

from project import firehose_url


def run_reader():
    last_timestamp = 0
    while True:
        r = requests.get(firehose_url)
        data = r.json()  # parse response into json

        events_list = data["events"]  # parse events item into list
        reversed_events = events_list[::-1]  # reverse the list to be chronologically correct

        for event in reversed_events:
            if int(event["ts"]) <= int(last_timestamp):
                continue
            print(event["ts"])

        last_timestamp = data["ts"]  # track last timestamp for next run


def print_entry(timestamp, sub, action):
    print("test")

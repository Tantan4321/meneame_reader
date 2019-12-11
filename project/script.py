import requests

from project import firehose_url


def run_reader():
    last_timestamp = 0
    while True:
        r = requests.get(firehose_url)
        data = r.json()  # TODO: filter json input for only new timestamps (reduce loop time)
        print(data)



def print_entry(timestamp, sub, action):
    print("test")

import requests;

from project import firehose_url


def print_output():
    r = requests.get(firehose_url)
    data = r.json()
    print(data)

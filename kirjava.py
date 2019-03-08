__version__ = "0.1.0"
__author__ = "Sam Ireland"

import requests
import json

def execute(url, message, method="POST", headers=None):
    head = {"Accept": "application/json", "Content-Type": "application/json"}
    if headers: head = {**head, **headers}
    data = {"query": message}
    resp = requests.request(method, url, headers=head, data=json.dumps(data))
    return resp.json()

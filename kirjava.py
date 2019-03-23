__version__ = "0.1.0"
__author__ = "Sam Ireland"

import requests
import json

class Client:

    def __init__(self, url):
        self._url = url
        self._headers = {
         "Accept": "application/json", "Content-Type": "application/json"
        }


    @property
    def url(self):
        return self._url


    @property
    def headers(self):
        return self._headers


    def execute(self, message, method="POST"):
        data = {"query": message}
        resp = requests.request(
         method, self._url, headers=self._headers, data=json.dumps(data)
        )
        return resp.json()

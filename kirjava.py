"""The kirjava library."""

__version__ = "0.1.0"
__author__ = "Sam Ireland"

import requests
import json

class Client:
    """A GraphQL client. This is the object which sends requests to the GraphQL
    server.

    The URL that serves the GraphQL content is given on creating the Client.

    :param str url: The URL of the GraphQL server to interact with."""

    def __init__(self, url):
        self._url = url
        self._headers = {
         "Accept": "application/json", "Content-Type": "application/json"
        }


    def __repr__(self):
        return f"<Client (URL: {self._url})>"


    @property
    def url(self):
        """The URL of the GraphQL server to interact with.

        :rtype: ``str``"""

        return self._url


    @property
    def headers(self):
        """The HTTP headers that will be sent with every request.

        :rtype: ``dict``"""

        return self._headers


    def execute(self, message, method="POST", variables=None):
        """Sends a request to the GraphQL server.

        :param str message: The query to make.
        :param str method: By default, POST requests are sent, but this can be\
        overriden here.
        :param dict variables: Any GraphQL variables can be passed here.
        :rtype: ``dict``"""

        data = {"query": message}
        if variables: data["variables"] = variables
        resp = requests.request(
         method, self._url, headers=self._headers, data=json.dumps(data)
        )
        return resp.json()

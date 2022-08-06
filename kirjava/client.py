"""Contains the Client class itself."""

import requests
import json

from .utilities import files_to_map, get_files_from_variables, create_response_error_message, pack_files

class Client:
    """A GraphQL client. This is the object which sends requests to the GraphQL
    server.

    The URL that serves the GraphQL content is given on creating the Client.

    :param str url: The URL of the GraphQL server to interact with.
    :param dict headers: Any additional HTTP headers."""

    def __init__(self, url):
        self._url = url
        self._headers = {
            "Accept": "application/json", "Content-Type": "application/json"
        }
        self._history = []
        self.session = requests.Session() 


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


    @property
    def history(self):
        """The queries sent, most recent first.

        :rtype: ``tuple``"""

        return tuple(self._history)


    def execute(self, message, method="POST", variables=None):
        """Sends a request to the GraphQL server.

        :param str message: The query to make.
        :param str method: By default, POST requests are sent, but this can be\
        overriden here.
        :param dict variables: Any GraphQL variables can be passed here.
        :rtype: ``dict``"""

        headers = {key: value for key, value in self._headers.items()}
        variables, files = get_files_from_variables(variables)
        operation = json.dumps({"variables": variables, "query": message})
        if files:
            del headers["Content-Type"]
            data = {"operations": operation, "map": json.dumps(files_to_map(files))}
            files = pack_files(files)
            response = self.session.request(
                method, self._url, files=files, data=data, headers=headers
            )
        else:
            response = self.session.request(
                method, self._url, headers=headers, data=operation
            )
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            raise ValueError(create_response_error_message(response))
        self._history.insert(0, (
            {"query": message, "variables": variables or {}}, result
        ))
        return result

       


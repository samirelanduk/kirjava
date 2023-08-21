"""Contains the Client class itself."""

import json
import requests
import time
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


    def execute(self, message, method="POST", variables=None, retries=0, retry_statuses=None):
        """Sends a request to the GraphQL server.

        :param str message: The query to make.
        :param str method: By default, POST requests are sent, but this can be\
        overriden here.
        :param dict variables: Any GraphQL variables can be passed here.
        :param int retries: The number of times to retry on failure.
        :param list retry_statuses: The HTTP statuses to retry on.
        :rtype: ``dict``"""

        headers = {key: value for key, value in self._headers.items()}
        variables, files = get_files_from_variables(variables)
        operation = json.dumps({"variables": variables, "query": message})
        if files:
            del headers["Content-Type"]
            data = {"operations": operation, "map": json.dumps(files_to_map(files))}
            files = pack_files(files)
            response = self.request_with_retries(
                operation=data, headers=headers, method=method,
                retries=retries, retry_statuses=retry_statuses, files=files
            )
        else:
            response = self.request_with_retries(
                operation=operation, headers=headers, method=method,
                retries=retries, retry_statuses=retry_statuses
            )
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            raise ValueError(create_response_error_message(response))
        self._history.insert(0, (
            {"query": message, "variables": variables or {}}, result
        ))
        return result


    def request_with_retries(self, operation, headers, files=None, method="POST", retries=0, retry_statuses=None):
        """Sends a GraphQL request, retrying if necessary the specified number
        of times.
        
        :param str operation: The GraphQL operation to send.
        :param dict headers: The HTTP headers to send.
        :param dict files: The files to send.
        :param str method: The HTTP method to use.
        :param int retries: The number of times to retry.
        :param list retry_statuses: The HTTP statuses to retry on.
        :rtype: ``requests.Response``"""

        attempts = 0
        while True:
            try:
                response = self.session.request(
                    method, self._url, headers=headers, data=operation, files=files
                )
                if retry_statuses and response.status_code in retry_statuses:
                    raise Exception(f"Status code {response.status_code}")
                return response
            except Exception as e:
                attempts += 1
                if attempts > retries: raise e
                time.sleep(2**attempts)
                continue
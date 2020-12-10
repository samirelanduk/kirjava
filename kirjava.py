"""The kirjava library."""

__version__ = "0.1.3"
__author__ = "Sam Ireland"

import requests
import json
import io
import mimetypes

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

        # What will the headers be?
        headers = {key: value for key, value in self._headers.items()}

        # Are any files being sent?
        files = {
            key: value for key, value in variables.items()
            if isinstance(value, io.IOBase)
        } if variables else {}

        # If so, process variables
        if variables and files:
            variables = {
                k: None if k in files else v for
                k, v in variables.items()
            }
        
        # Create operations string
        operation = json.dumps({"variables": variables, "query": message})

        if files:
            del headers["Content-Type"]
            data = {
                "operations": operation,
                "map": json.dumps({
                    str(i): [f"variables.{key}"] for i, key in enumerate(files.keys())
                })
            }
            files = {
                str(i): (f.name, f.read(), mimetypes.MimeTypes().guess_type(f.name)[0]) for i, f in enumerate(files.values())
            }
            
            response = self.session.request(
                method, self._url,
                files=files,
                data=data,
                headers=headers
            )
        else:
            response = self.session.request(
                method, self._url, headers=headers, data=operation
            )
        
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            content_type = response.headers["Content-type"]
            try:
                content = response.content.decode()
            except: content = None
            message = f"Server did not return JSON, it returned {content_type}"
            if content and len(content) < 256:
                message += ":\n" + content
            raise ValueError(message)
        self._history.insert(0, (
            {"string": message, "variables": variables or {}}, result
        ))
        return result

       


def execute(url, *args, headers=None, **kwargs):
    """Sends a GraphQL request without the user haveing to make a dedicated
    :py:class:`.Client` object.

    :param str url: the URL to send to.
    :param str message: The query to make.
    :param str method: By default, POST requests are sent, but this can be\
    overriden here.
    :param dict headers: Any additional HTTP headers.
    :param dict variables: Any GraphQL variables can be passed here.
    :rtype: ``dict``"""

    client = Client(url)
    if headers: client.headers.update(headers)
    return client.execute(*args, **kwargs)


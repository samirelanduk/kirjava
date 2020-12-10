"""Useful functions."""

import io

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

    from .client import Client
    client = Client(url)
    if headers: client.headers.update(headers)
    return client.execute(*args, **kwargs)


def get_files_from_variables(variables):
    """Takes a variables objects and looks to see if any of the values are file
    objects which need to be sent separately.

    :param dict variables: the variables to inspect, or ``None``.
    :returns: ``(variables, files)``"""

    if not variables: return variables, None
    files = {k: v for k, v in variables.items() if isinstance(v, io.IOBase)}
    variables = {k: None if k in files else v for k, v in variables.items()}
    return variables, files


def create_response_error_message(response):
    """Works out what to say about a response that isn't JSON.

    :param response: The HTTP response object.
    :rtype: ``str``"""

    content_type = response.headers["Content-type"]
    try:
        content = response.content.decode()
    except: content = None
    message = f"Server did not return JSON, it returned {content_type}"
    if content and len(content) < 256:
        message += ":\n" + content
    return message
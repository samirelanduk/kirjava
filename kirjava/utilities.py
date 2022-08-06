"""Useful functions."""

import io
import mimetypes

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
    files, new_variables = {}, {}
    for k, v in variables.items():
        if isinstance(v, io.IOBase):
            files[k] = v
            new_variables[k] = None
        elif isinstance(v, list) and len(v) and isinstance(v[0], io.IOBase):
            files[k] = v
            new_variables[k] = [None] * len(v)
        else:
            new_variables[k] = v
    return new_variables, files


def files_to_map(files):
    """Takes a files dict and creates the map dict needed by the GraphQL file
    upload spec.
    
    :param dict files: the files dict.
    :rtype: ``dict``"""

    map = {}
    for k, v in files.items():
        is_list = isinstance(v, list)
        l = v if is_list else [v]
        for i in range(len(l)):
            map[str(len(map))] = [f"variables.{k}.{i}" if is_list else f"variables.{k}"]
    return map


def pack_files(files):
    """Takes a files dict and packs them into a HTTP sendable form.
    
    :param dict files: the files dict.
    :rtype: ``dict``"""

    packed_files = {}
    for file in files.values():
        l = file if isinstance(file, list) else [file]
        for f in l:
            packed_files[str(len(packed_files))] = (
                f.name, f.read(), mimetypes.MimeTypes().guess_type(f.name)[0]
            )
    return packed_files


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
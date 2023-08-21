Overview
--------

kirjava is a lightweight Python GraphQL client.


Making Queries with a Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GraphQL services are interacted with using a :py:class:`.Client` object:

    >>> import kirjava
    >>> client = kirjava.Client("https://api.coolsite.com/")

The client is associated with a particular URL upon creation.

Queries are then made using the ``execute`` method.

    >>> client.execute("{ me { name email }}")
    {'data': {'me': {'name': 'Jon Snow', 'email': 'jon@winterfell.gov.ws'}}}

If authentication tokens need to be added, they can be inserted into the
headers:

    >>> client.headers["Authorization"] = "dani123"

Variables can be passed along with the query:

    >>> client.execute("{ me { name email }}", variables={"var1": 123})

You can instruct the client to retry failed requests:

    >>> client.execute("{ me { name email }}", retries=3, retry_statuses=[500, 502, 503, 504])

You can see all previous queries made by a client:

    >>> client.history
    (({'string': { me { name email }}, 'variables': {'var1': 123}, {'data': {'me
    ': {'name': 'Jon Snow', 'email': 'jon@winterfell.gov.ws'}}}), ({'string': {
    me { name email }}, 'variables': {}}, {'data': {'me': {'name': 'Jon Snow', '
    email': 'jon@winterfell.gov.ws'}}}))

Clients use `requests <http://docs.python-requests.org/>`_ sessions internally,
and you can access any cookies set by the server via ``client.session.cookies``.

Uploading Files
~~~~~~~~~~~~~~~

If you want to upload files as part of your request, kirjava can do this. Just
add them as a variable:

    >>> mutation = "mutation sendFile($file: Upload) {sendFile(file: $file) { success }}"
    >>> f = open("local_file.txt", "rb"):
    >>> response = client.execute(mutation, variables={"file": f})
    >>> f.close()

kirjava does this by implementing the
`GraphQL multipart request specification <https://github.com/jaydenseric/graphql-multipart-request-spec>`_
under the hood, and using this if any of the variables supplied are Python file
objects.

Note that the GraphQL server on the other end must be set up to process
multipart requests.


Making Queries without a Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, if creating a dedicated :py:class:`.Client` object is somehow
beneath you, and you just want to fire off a quick request without any of that
overhead, there is a module level :py:func:`.execute` function:

    >>> kirjava.execute("https://api.coolsite.com/", "{ me { name email }}", headers={"Authorization": "dani123"}, variables={"var1": 123})

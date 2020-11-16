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

You can see all previous queries made by a client:

    >>> client.history
    (({'string': { me { name email }}, 'variables': {'var1': 123}, {'data': {'me
    ': {'name': 'Jon Snow', 'email': 'jon@winterfell.gov.ws'}}}), ({'string': {
    me { name email }}, 'variables': {}}, {'data': {'me': {'name': 'Jon Snow', '
    email': 'jon@winterfell.gov.ws'}}}))

Clients use `requests <http://docs.python-requests.org/>`_ sessions internally,
and you can access any cookies set by the server via ``client.session.cookies``.


Making Queries without a Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, if creating a dedicated :py:class:`.Client` object is somehow
beneath you, and you just want to fire off a quick request without any of that
overhead, there is a module level :py:func:`.execute` function:

    >>> kirjava.execute("https://api.coolsite.com/", "{ me { name email }}", headers={"Authorization": "dani123"}, variables={"var1": 123})

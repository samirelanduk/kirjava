Overview
--------

kirjava is a lightweight Python GraphQL client.


Making Queries
~~~~~~~~~~~~~~

GraphQL services are interacted with using a :py:class:`.Client` object:

    >>> import kirjava
    >>> client = kirjava.Client("https://api.coolsite.com/")

The client is associated with a particular URL upon creation.

Queries are then made using the ``execute`` method.

    >>> client.execute("""{ me { name email }}""")
    {'data': {'me': {'name': 'Jon Snow', 'email': 'jon@winterfell.gov.ws'}}}

If authentication tokens need to be added, they can be inserted into the
headers:

    >>> client.headers["Authorization"] = "dani123"

Variables can be passed along with the query:

  >>> client.execute("""{ me { name email }}""", variables={"var1": 123})

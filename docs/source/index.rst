kirjava
========

kirjava is a Python GraphQL client.

Example
-------

    >>> import kirjava
    >>> client = kirjava.Client("https://api.coolsite.com/")
    >>> client.execute("""{ me { name email }}""")
    {'data': {'me': {'name': 'Jon Snow', 'email': 'jon@winterfell.gov.ws'}}}

Table of Contents
-----------------

.. toctree ::
  installing
  overview
  api
  contributing
  changelog

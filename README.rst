kirjava
========

|travis| |coveralls| |pypi| |version| |commit|

.. |travis| image:: https://api.travis-ci.org/samirelanduk/kirjava.svg?branch=master
  :target: https://travis-ci.org/samirelanduk/kirjava/

.. |coveralls| image:: https://coveralls.io/repos/github/samirelanduk/kirjava/badge.svg?branch=master
  :target: https://coveralls.io/github/samirelanduk/kirjava/

.. |pypi| image:: https://img.shields.io/pypi/pyversions/kirjava.svg
  :target: https://pypi.org/project/kirjava/

.. |version| image:: https://img.shields.io/pypi/v/kirjava.svg
  :target: https://pypi.org/project/kirjava/

.. |commit| image:: https://img.shields.io/github/last-commit/samirelanduk/kirjava/master.svg
  :target: https://github.com/samirelanduk/kirjava/tree/master/

kirjava is a Python GraphQL client.

Example
-------

    >>> import kirjava
    >>> client = kirjava.Client("https://api.coolsite.com/")
    >>> client.execute("""{ me { name email }}""")
    {'data': {'me': {'name': 'Jon Snow', 'email': 'jon@winterfell.gov.ws'}}}


Installing
----------

pip
~~~

kirjava can be installed using pip:

``$ pip3 install kirjava``

If you get permission errors, try using ``sudo``:

``$ sudo pip3 install kirjava``

Or alternatively, consider using a virtual environment.


Development
~~~~~~~~~~~

The repository for kirjava, containing the most recent iteration, can be
found `here <http://github.com/samirelanduk/kirjava/>`_. To clone the
kirjava repository directly from there, use:

``$ git clone git://github.com/samirelanduk/kirjava.git``


Requirements
~~~~~~~~~~~~

kirjava requires `requests <http://docs.python-requests.org/>`_.


Overview
--------

kirjava is a lightweight Python GraphQL client.


Making Queries with a Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GraphQL services are interacted with using a ``Client`` object:

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

Alternatively, if creating a dedicated ``Client`` object is somehow
beneath you, and you just want to fire off a quick request without any of that
overhead, there is a module level ``execute`` function:

    >>> kirjava.execute("https://api.coolsite.com/", "{ me { name email }}", headers={"Authorization": "dani123"}, variables={"var1": 123})


Changelog
---------

Release 0.4.0
~~~~~~~~~~~~~

`21 August 2023`

* You can retry failed requests.


Release 0.3.0
~~~~~~~~~~~~~

`6 August 2022`

* File upload array type now supported.


Release 0.2.0
~~~~~~~~~~~~~

`11 December 2020`

* Implements GraphQL multipart request specification to allow file upload.
* Refactored kirjava.py into full package.


Release 0.1.3
~~~~~~~~~~~~~

`16 November 2020`

* Provides access to requests cookie jar.
* Better handling of non-JSON responses.


Release 0.1.2
~~~~~~~~~~~~~

`1 April 2019`

* Added module-level execute function.


Release 0.1.1
~~~~~~~~~~~~~

`30 March 2019`

* Added tests.
* Clients now store history of their queries.


Release 0.1.0
~~~~~~~~~~~~~

`23 March 2019`

* Created basic Client.

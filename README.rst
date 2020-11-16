kirjava
=======

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

kirjava is written for Python 3, and does not support Python 2.

If you get permission errors, try using ``sudo``:

``$ sudo pip3 install kirjava``


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

Alternatively, if creating a dedicated ``Client`` object is somehow
beneath you, and you just want to fire off a quick request without any of that
overhead, there is a module level ``execute`` function:

    >>> kirjava.execute("https://api.coolsite.com/", "{ me { name email }}", headers={"Authorization": "dani123"}, variables={"var1": 123})


Changelog
---------

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

|travis| |coveralls| |pypi|

.. |travis| image:: https://api.travis-ci.org/samirelanduk/kirjava.svg?branch=master
  :target: https://travis-ci.org/samirelanduk/kirjava/

.. |coveralls| image:: https://coveralls.io/repos/github/samirelanduk/kirjava/badge.svg?branch=master
  :target: https://coveralls.io/github/samirelanduk/kirjava/

.. |pypi| image:: https://img.shields.io/pypi/pyversions/kirjava.svg
  :target: https://pypi.org/project/kirjava/

atomium
========

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


Making Queries
~~~~~~~~~~~~~~

GraphQL services are interacted with using a ``Client`` object:

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


Changelog
---------

Release 0.1.0
~~~~~~~~~~~~~

`23 March 2019`

* Created basic Client.
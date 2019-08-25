Heartbeat module for oarepo invenio
===================================

A heartbeat module for oarepo invenio. It provides 3 endpoints:

* ``.well-known/heartbeat/readiness``

* ``.well-known/heartbeat/liveliness``

* ``.well-known/heartbeat/environ``



``.well-known/heartbeat/readiness``
------------------------------------

This endpoint returns HTTP status 200 if the server is ready for user requests or 500
if the server is not yet ready.

At the same time, it returns a payload explaining what is not yet ready/what went wrong:

.. code:: json

    {
        "status": false,
        "messages": {
            "Database default": "Error accessing database"
        }
    }

This endpoint should be called as Kubernetes readiness probe

*Note:* the result is extensible, ignore unknown keys

**Signals:**

A ``oarepo_heartbeat.readiness_probe`` signal (with name ``oarepo.probe.readiness``)
is called during the readiness processing. Signal handler should return a response
in the form of a tuple ``(status, messages)``. The ``status`` is the ``logical and`` of returned statuses
and messages is the union of all messages.


``.well-known/heartbeat/liveliness``
------------------------------------

This endpoint returns HTTP status 200 if the server is functioning correctly or 500
if the server has a problem.

At the same time, it returns a payload explaining what went wrong in the same format as in
readiness probe:

.. code:: json

    {
        "status": false,
        "messages": {
            "Database default": "Error accessing database"
        }
    }

This endpoint should be called as Kubernetes liveliness probe

*Note:* the result is extensible, ignore unknown keys

**Signals:**

A ``oarepo_heartbeat.liveliness_probe`` signal (with name ``oarepo.probe.liveliness``)
is called during the readiness processing. Signal handler should return a response
in the form of a tuple ``(status, messages)``. The ``status`` is the ``logical and`` of returned statuses
and messages is the union of all messages.


``.well-known/heartbeat/environ``
------------------------------------

Endpoint returning the runtime environment of the server. The result contains at least
a set of libraries present in the virtualenv and their versions.

.. code:: json

    {
        "status": true,
        "libraries": {
            "oarepo": {
                "conflicts": null,
                "version": "3.1.1"
            }
        },
        "python": [3, 6, 1]
    }

*Note:* the result is extensible, ignore unknown keys

**Signals:**

A ``oarepo_heartbeat.environ_probe`` signal (with name ``oarepo.probe.environ``)
is called during the readiness processing. Signal handler should return a response
as a tuple ``(status, {data})``. The ``status`` is the ``logical and`` of returned statuses
and the data are merged into one dictionary.


Invenio usage:
==============

To use this library on invenio, do not forget to add it to setup's blueprints
and define your own readiness & liveliness signal handlers as needed (for example,
checking database, ES connectivity):

.. code:: python

    'invenio_base.blueprints': [
        'oarepo-heartbeat = oarepo_heartbeat.views:blueprint',
    ],


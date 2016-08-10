Unclegabe - Unclebob testing style for Django 1.8+
=========================================================================

Unclegabe is a library to emulate the properties of ``Unclebob`` when testing
in Django 1.8+

Installation
------------

.. code:: bash

    $ pip install unclegabe

Or just add it to your ``development.txt``.

Usage
-----

In your ``settings.py``:

.. code:: python

    TEST_RUNNER = 'unclegabe.runners.NoseRunner'

==============
Installation
==============

Install via PIP
================

Install this package by pip:

.. code-block:: bash

    pip install multirunnable


Dependencies
==============

* Gevent

*MultiRunnable* is dependence on another Python package *gevent* which is a framework of green thread of Python.
Python has a native library to implement Green Thread feature is *greenlet*.
However, it's a very featherweight library. It event doesn't have Lock or something else features.
That's the reason why *multirunnable* uses *gevent*.

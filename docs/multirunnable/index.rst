.. multirunnable documentation master file, created by
   sphinx-quickstart on Mon Dec 27 18:03:24 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MultiRunnable's documentation!
=========================================

|python-versions| |release-version| |pypi-version| |license| |codacy-level|

:Date: |today|


Building Status
-----------------

+------------------+-----------------------------------+----------------------+
|        OS        |           Building Status         |    Coverage Status   |
+==================+===================================+======================+
|    Linux/MacOS   |   |github-actions build-status|   |  |codecov-coverage|  |
+------------------+-----------------------------------+----------------------+
|      Windows     |      |circle-ci build-status|     | |coveralls-coverage| |
+------------------+-----------------------------------+----------------------+


Overview
----------

A Python library integrates the APIs of 3 strategies (Parallel, Concurrent, Coroutine) and
4 libraries (multiprocessing, threading, gevent, asyncio) to help developers build parallelism humanly.
It targets to help developers build parallelism feature easily and clearly. You just only focus
on the business logic implementations or others.

Let's demonstrate an example to show how easy and clear it is!

.. code-block:: python

   from multirunnable import SimpleExecutor, RunningMode

   _executor = SimpleExecutor(mode=RunningMode.Parallel, executors=10)
   _executor.run(function=lambda *args: print("This is target function args: ", args), args=("index_1", "index_2.2"))
   _result = _executor.get_result()


General documentation
----------------------

This part of documentation, which introduces the package and has some step-by-step instructions for using or building parallelism features.

.. toctree::
   :maxdepth: 3

   introduction
   installation
   quickly_start
   advanced_usage
   examples


API Reference
--------------

Information about some function, class or method.

.. toctree::
   :maxdepth: 2

   Mode </api_references/mode.rst>
   Executors </api_references/executors.rst>
   Pools </api_references/pools.rst>
   Parallel Modules </api_references/strategy_parallel.rst>
   Concurrent Modules </api_references/strategy_concurrent.rst>
   Coroutine Modules </api_references/strategy_coroutine.rst>
   Synchronizations </api_references/synchronizations.rst>
   Decorators Modules </api_references/decorators.rst>
   Context </api_references/context.rst>
   Persistence with File </api_references/persistence_file.rst>
   Persistence with Database </api_references/persistence_database.rst>


Development documentation
--------------------------

If you're curious about the detail of implementation of this package includes workflow, software architecture, system design or development, this section is for you.

.. toctree::
   :maxdepth: 2

   flow
   architecture
   test
   ci_cd



.. |python-versions| image:: https://img.shields.io/pypi/pyversions/multirunnable.svg?logo=python&logoColor=FBE072
    :alt: Travis-CI build status
    :target: https://pypi.org/project/multirunnable


.. |release-version| image:: https://img.shields.io/github/release/Chisanan232/multirunnable.svg?label=Release&amp;logo=github
    :alt: Package release version in GitHub
    :target: https://github.com/Chisanan232/multirunnable/releases


.. |pypi-version| image:: https://img.shields.io/pypi/v/MultiRunnable?color=%23099cec&amp;label=PyPI&amp;logo=pypi&amp;logoColor=white
    :alt: Package version in PyPi
    :target: https://pypi.org/project/MultiRunnable/


.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :target: https://opensource.org/licenses/Apache-2.0


.. |codacy-level| image:: https://app.codacy.com/project/badge/Grade/6733a68742a64b3dbcfa57b1309de4ce
    :alt: Code Quality by Codacy
    :target: https://www.codacy.com/gh/Chisanan232/multirunnable/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Chisanan232/multirunnable&amp;utm_campaign=Badge_Grade


.. |circle-ci build-status| image:: https://circleci.com/gh/Chisanan232/multirunnable.svg?style=svg
    :alt: Circle-CI building status
    :target: https://app.circleci.com/pipelines/github/Chisanan232/multirunnable


.. |github-actions build-status| image:: https://github.com/Chisanan232/multirunnable/actions/workflows/ci-cd-master.yml/badge.svg
    :alt: GitHub-Actions building status
    :target: https://github.com/Chisanan232/multirunnable/actions/workflows/ci-cd-master.yml


.. |appveyor build-status| image:: https://ci.appveyor.com/api/projects/status/v0nq38jtof6vcm23?svg=true
    :alt: AppVeyor building status
    :target: https://ci.appveyor.com/project/Chisanan232/multirunnable


.. |codecov-coverage| image:: https://codecov.io/gh/Chisanan232/multirunnable/branch/master/graph/badge.svg?token=E2AGK1ZIDH
    :alt: Test coverage with 'codecov'
    :target: https://codecov.io/gh/Chisanan232/multirunnable


.. |coveralls-coverage| image:: https://coveralls.io/repos/github/Chisanan232/multirunnable/badge.svg?branch=master
    :alt: Test coverage with 'coveralls'
    :target: https://coveralls.io/github/Chisanan232/multirunnable?branch=master


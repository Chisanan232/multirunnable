.. multirunnable documentation master file, created by
   sphinx-quickstart on Mon Dec 27 18:03:24 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MultiRunnable's documentation!
=========================================

|python-versions| |release-version| |pypi-version| |license|


:GitHub Release: |version|
:PyPi Release: |release|
:Date: |today|


Building Status
-----------------

+------------+---------------------------------+----------------------+
|     OS     |          Building Status        |    Coverage Status   |
+============+=================================+======================+
|    Linux   |    |travis-ci build-status|     |    (Deprecated CI)   |
+------------+---------------------------------+----------------------+
|    Linux   |     |circle-ci build-status|    |                      |
+------------+---------------------------------+   |codecov-coverage| |
|    Linux   |  |github-actions build-status|  |                      |
+------------+---------------------------------+----------------------+
|   Windows  |     |appveyor build-status|     | |coveralls-coverage| |
+------------+---------------------------------+----------------------+


Overview
----------

A Python framework integrates running multiple tasks simultaneously with different strategy.
It target to help developers build parallelism feature easily and clearly. You just only focus
on the business logic implementations or others.

Let's demonstrate an example to show how easy and clear it is!

.. code-block:: python

   from multirunnable import SimpleExecutor, RunningMode

   _executor = SimpleExecutor(mode=RunningMode.Parallel, executors=10)
   _executor.run(function=target_function, args=("index_1", "index_2.2"))


.. toctree::
   :caption: General documentation
   :maxdepth: 3

   introduction
   installation
   usage
   examples


.. toctree::
   :caption: Development documentation
   :maxdepth: 2

   flow
   architecture
   test


.. toctree::
   :caption: API Reference
   :maxdepth: 2

   Mode </api_references/mode.rst>
   Executors </api_references/executors.rst>
   Pools </api_references/pools.rst>
   Parallel Modules </api_references/strategy_parallel.rst>
   Concurrent Modules </api_references/strategy_concurrent.rst>
   Coroutine Modules </api_references/strategy_coroutine.rst>
   Synchronizations </api_references/synchronizations.rst>
   Decorators Modules </api_references/decorators.rst>
   Persistence with File </api_references/persistence_file.rst>
   Persistence with Database </api_references/persistence_database.rst>



.. |python-versions| image:: https://img.shields.io/pypi/pyversions/multirunnable.svg?logo=python&logoColor=FBE072
    :alt: Travis-CI build status
    :target: https://pypi.org/project/multirunnable


.. |release-version| image:: https://img.shields.io/github/release/Chisanan232/multirunnable.svg?label=Release&sort=semver
    :alt: Package release version in GitHub
    :target: https://github.com/Chisanan232/multirunnable/releases


.. |pypi-version| image:: https://badge.fury.io/py/multirunnable.svg
    :alt: Package version in PyPi
    :target: https://badge.fury.io/py/multirunnable


.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :target: https://opensource.org/licenses/Apache-2.0


.. |travis-ci build-status| image:: https://app.travis-ci.com/Chisanan232/multirunnable.svg?branch=master
    :alt: Travis-CI building status
    :target: https://app.travis-ci.com/Chisanan232/multirunnable


.. |circle-ci build-status| image:: https://circleci.com/gh/Chisanan232/multirunnable.svg?style=svg
    :alt: Circle-CI building status
    :target: https://app.circleci.com/pipelines/github/Chisanan232/multirunnable


.. |github-actions build-status| image:: https://github.com/Chisanan232/multirunnable/actions/workflows/ci.yml/badge.svg
    :alt: GitHub-Actions building status
    :target: https://github.com/Chisanan232/multirunnable/actions/workflows/ci.yml


.. |appveyor build-status| image:: https://ci.appveyor.com/api/projects/status/v0nq38jtof6vcm23?svg=true
    :alt: AppVeyor building status
    :target: https://ci.appveyor.com/project/Chisanan232/multirunnable


.. |codecov-coverage| image:: https://codecov.io/gh/Chisanan232/multirunnable/branch/master/graph/badge.svg?token=E2AGK1ZIDH
    :alt: Test coverage with 'codecov'
    :target: https://codecov.io/gh/Chisanan232/multirunnable


.. |coveralls-coverage| image:: https://coveralls.io/repos/github/Chisanan232/multirunnable/badge.svg?branch=master
    :alt: Test coverage with 'coveralls'
    :target: https://coveralls.io/github/Chisanan232/multirunnable?branch=master


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

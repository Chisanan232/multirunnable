=======
Tests
=======

.. _Building Status:

Building Status
=================

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


.. _Testing Concerns:

Testing Concerns
=================

A great testing tool is a very important to developers for testing in development.
In *MultiRunnable*, it could consider about 3 points for testing:

* Testing in localhost conveniently and clearly.
    It only cares testing but doesn't care about testing in different version or different OS, etc.
    Focus on the feature testing of APIs.

* Testing for different version of language.
    It cares about testing with different language version (ex: Python 3.8, 3.10, etc).
    Feature testing should already be passing at this step.

* Testing automatically by third party platform.
    In addition to passing feature testing in different Python version, it also could test
    with different OS (ex: MacOS, Linux, Windows). It event could run these automatically
    by CI tool (of course it does about deployment, too).


.. _PyTest - Python Testing Framework:

PyTest - Python Testing Framework
=================================

A powerful testing framework for Python. It could help developer test code and verify the testing result.
*MultiRunnable* has a configuration of **pytest**, *pytest.ini*, to do it.

It only run below command line at the root path of the project:

>>> pytest

It would test all items to verify the feature of *MultiRunnable* APIs.
Finally, it has a testing result to inform developers some important things like
the code coverage, which cases are fail, etc.

* Note:
    Remember that it needs to install some plugins to use some feature.
    For example, it should install *pytest-cov* by *pip* if needs code coverage result by option *--cov=*.
    *pytest-html* be needed for exporting testing report by option *--html*.
    *pytest-rerunfailures* be needed for rerun the testing failed items by option *--reruns*.

If it just only tests one or more new test case(s) or debugs someone, it could run with the testing item name by option *-k*.
For example, run the below command line:

>>> pytest -q --cache-clear --reruns 0 --cov=./multirunnable tests/concurrent/strategy.py -k 'test_apply_with_'

It would run all the testing items which naming 'test_apply_with_XXXXXXXXX'.

If it needs more information about **pytest**, please refer to the official documentation `PyTest <https://docs.pytest.org/en/latest/contents.html>`_.

About tool **pytest**, it achieves the goal about testing feature of APIs in localhost.
It could guarantee that APIs feature work finely.
However, it only  makes sure that with one specific Python version.
So it needs a tool which could help us to test with different Python version and they doesn't be effected by each others.


.. _Tox - Testing in SandBox:

Tox - Testing in SandBox
========================

From the final of section :ref:`PyTest - Python Testing Framework`, we need a testing tool to test with different Python version
and they doesn't effected each others. So **Tox** is the one which could achieve that.
**Tox** is a tool which could run Python code with different Python version.
It could set Python version with option *envlist*. It would initial and create a
sandbox which the runtime environment independently to each target Python version.

*MultiRunnable* has a configuration of **Tox**, *tox.ini*. It could test the code
with **PyTest** via **Tox** in different Python version.

* Note:
    It should install *tox* by *pip* before use it.

It only modify the value of option *envlist* if it needs and run the command below at the root path of the project:

>>> tox

It would run *pytest* with the target Python versions.

If it needs more information about *tox*, please refer to the official documentation `Tox <https://tox.wiki/en/latest/>`_.


.. _Docker - Testing with Container:

Docker - Testing with Container
===============================

*MultiRunnable* has a subpackage *persistence.database*  to define how to extends yourself own classes
*ConnectionStrategy*, *DatabaseOperator* and *DAO* to do something with database.
No one want to build multiple databases in localhost for testing different database driver.
And it's so hard to ensure they're NOT effected each others.
That's the reason why testing features of *persistence.database* with Docker.
It could be convenient and fast to build a database. Furthermore, it guarantees the environment is cleaning.

For example, I want to test it with RDB MySQL. Let's ready Docker image first:

>>> docker pull mysql:8.0.23

Check the image:

>>> docker images | grep -P "mysql"
mysql                          8.0.23              xxxx12349d81        12 months ago       546MB

In MacOS, the option should be *-E*

>>> docker images | grep -E "mysql"
mysql                          8.0.23              xxxx12349d81        12 months ago       546MB

And start to setup database service MySQL:

>>> docker run --name test_mysql --restart always -p 3306:3306 --env="MYSQL_ROOT_PASSWORD=password" -d mysql:8.0.23

Verify the running state:

>>> docker ps -a
xxxx123466c5        mysql:8.0.23                          "docker-entrypoint.s…"   10 months ago       Up 2 weeks                   0.0.0.0:3306->3306/tcp, 33060/tcp                                                                          mysql_stock

Let's build some testing data to testing:

>>> docker exec -it test_mysql mysql -u root -ppassword  --execute="CREATE DATABASE tw_stock;"
>>> docker exec -it test_mysql mysql -u root -ppassword  --execute="CREATE TABLE IF NOT EXISTS tw_stock.stock_data_1234 (   stock_date DATETIME NOT NULL,   trade_volume DECIMAL(12,4) NOT NULL,   turnover_price DECIMAL(16,4) NOT NULL,   opening_price DECIMAL(8,4) NOT NULL,   highest_price DECIMAL(8,4) NOT NULL,   lowest_price DECIMAL(8,4) NOT NULL,   closing_price DECIMAL(8,4) NOT NULL,   gross_spread DECIMAL(8,4) NOT NULL,   turnover_volume DECIMAL(12,4) NOT NULL,   PRIMARY KEY(stock_date)) DEFAULT CHARSET=utf8;"
>>> docker exec -it test_mysql mysql -u root -ppassword  --execute="INSERT INTO tw_stock.stock_data_1234 (stock_date, trade_volume, turnover_price, opening_price, highest_price, lowest_price, closing_price, gross_spread, turnover_volume) VALUES ('0108-01-02 00:00:00' , 32900482 , 7276419230 ,226.5000 ,226.5000 , 219.0000, 219.5000 ,-6.00 , 12329);"
>>> docker exec -it test_mysql mysql -u root -ppassword  --execute="INSERT INTO tw_stock.stock_data_1234 (stock_date, trade_volume, turnover_price, opening_price, highest_price, lowest_price, closing_price, gross_spread, turnover_volume) VALUES ('0108-01-31 00:00:00' , 32900482 , 7276419230 ,226.5000 ,226.5000 , 219.0000, 219.5000 ,-6.00 , 12329);"

Above 4 command lines create a new database and a table in it, and it inserts 2 data rows into the table.

Show data rows:

>>> docker exec -it test_mysql mysql -u root -ppassword  --execute="SELECT * FROM tw_stock.stock_data_1234;"
+---------------------+---------------+-----------------+---------------+---------------+--------------+---------------+--------------+-----------------+
| stock_date          | trade_volume  | turnover_price  | opening_price | highest_price | lowest_price | closing_price | gross_spread | turnover_volume |
+---------------------+---------------+-----------------+---------------+---------------+--------------+---------------+--------------+-----------------+
| 0108-01-02 00:00:00 | 32900482.0000 | 7276419230.0000 |      226.5000 |      226.5000 |     219.0000 |      219.5000 |      -6.0000 |      12329.0000 |
| 0108-01-31 00:00:00 | 32900482.0000 | 7276419230.0000 |      226.5000 |      226.5000 |     219.0000 |      219.5000 |      -6.0000 |      12329.0000 |
+---------------------+---------------+-----------------+---------------+---------------+--------------+---------------+--------------+-----------------+

Docker create a virtual environment and setup MySQL. It could setup others with different database driver conveniently, too.
And then we could test code with it.


.. _Combine with CI tool:

Combine with CI tool
=====================

Above all, it could test with different Python version in different OS.
However, it's necessary that there is a platform which could run these tasks
and record testing result in every scenarios when it be triggered by some movements
like *git push*, *git merge* or something else. Therefore, it needs CI tools.

In :ref:`Building Status`, these all are the building state which including testing.
It also could be triggered by the *git* movements. It means that it could make sure that
the latest code is correct and it could run finely without issue (depend on the code coverage).

Currently, *MultiRunnable* uses **Circle-CI**, **GitHub Actions** and **AppVeyor**.
**Circle-CI** and **GitHub Actions** for Linux OS or MacOS.
**AppVeyor** for Windows. It had run with **Travis-CI** before, but credits is fulled so it deprecated it now.



.. |python-versions| image:: https://img.shields.io/pypi/pyversions/multirunnable.svg?logo=python&logoColor=FBE072
    :alt: travis-ci build status
    :target: https://pypi.org/project/multirunnable


.. |release-version| image:: https://img.shields.io/github/release/Chisanan232/multirunnable.svg?label=Release&sort=semver
    :alt: travis-ci build status
    :target: https://github.com/Chisanan232/multirunnable/releases


.. |pypi-version| image:: https://badge.fury.io/py/MultiRunnable.svg
    :alt: travis-ci build status
    :target: https://badge.fury.io/py/MultiRunnable


.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: travis-ci build status
    :target: https://opensource.org/licenses/Apache-2.0


.. |travis-ci build-status| image:: https://app.travis-ci.com/Chisanan232/multirunnable.svg?branch=master
    :alt: travis-ci build status
    :target: https://app.travis-ci.com/Chisanan232/multirunnable


.. |circle-ci build-status| image:: https://circleci.com/gh/Chisanan232/multirunnable.svg?style=svg
    :alt: circle-ci build status
    :target: https://app.circleci.com/pipelines/github/Chisanan232/multirunnable


.. |github-actions build-status| image:: https://github.com/Chisanan232/multirunnable/actions/workflows/ci.yml/badge.svg
    :alt: github-actions build status
    :target: https://github.com/Chisanan232/multirunnable/actions/workflows/ci.yml


.. |appveyor build-status| image:: https://ci.appveyor.com/api/projects/status/v0nq38jtof6vcm23?svg=true
    :alt: github-actions build status
    :target: https://ci.appveyor.com/project/Chisanan232/multirunnable


.. |codecov-coverage| image:: https://codecov.io/gh/Chisanan232/multirunnable/branch/master/graph/badge.svg?token=E2AGK1ZIDH
    :alt: Test coverage with 'codecov'
    :target: https://codecov.io/gh/Chisanan232/multirunnable


.. |coveralls-coverage| image:: https://coveralls.io/repos/github/Chisanan232/multirunnable/badge.svg?branch=master
    :alt: Test coverage with 'coveralls'
    :target: https://coveralls.io/github/Chisanan232/multirunnable?branch=master


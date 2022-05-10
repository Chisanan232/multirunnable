================
Advanced Usages
================

This page for the people who have some requirements which doesn't be satisfied or resolved by :doc:`Quickly Start <quickly_start>`.


.. _Synchronization with Python decorator:

Synchronization with Python decorator
======================================

You could learn about how to use synchronization features in :ref:`Running with Synchronizations <Running with Synchronizations>` in Quickly Start.
Actually, you also could use it with a easier way --- Python decorator.

No matter for *Lock*, *RLock*, *Semaphore* or *Bounded Semaphore*, they all could work with
Python keyword *with*. The code in the same indentation would be run synchronously. For the
same reason, *RunWith* implements some decorators so that function would run synchronously
under the decorator.

The synchronization features of *MultiRunnable* which support usage with Python decorator are:

* Lock
* RLock
* Semaphore
* Bounded Semaphore

You could enjoy this feature via **RunWith**. Let's import module before demonstrate:

.. code-block:: python

    from multirunnable.api import RunWith


Let's start to use synchronization features.

*Lock*
-------

Following code is a demonstration with *RunWith*:

.. code-block:: python

    from multirunnable import sleep

    @RunWith.Lock
    def lock_function():
        print("Running process in lock and will sleep 2 seconds.")
        sleep(2)
        print("Wake up process and release lock.")


The function *lock_function* would work synchronously. Below code working is the same as above:

.. code-block:: python

    lock_opt = LockOperator()

    def lock_function():
        with lock_opt:
            print("Running process in Lock and it will sleep 2 seconds.")
            sleep(2)
            print(f"Wake up process and release Lock.")


In the other words, code would works synchronously which in the same indentation for Python keyword *with*;
code would be blocking to run in the function with decorator *RunWith*.

For other features, the usage is completely the same. So it only demonstrates the usage without introduction for others.


*RLock*
--------

.. code-block:: python

    from multirunnable import sleep

    @RunWith.RLock
    def rlock_function():
        print("Running process in RLock and it will sleep 2 seconds.")
        sleep(2)
        print("Wake up process and release RLock.")



*Semaphore*
-------------

.. code-block:: python

    from multirunnable import sleep

    @RunWith.Semaphore
    def smp_function():
        print("Running process with Semaphore and it will sleep 2 seconds.")
        sleep(2)
        print("Wake up process and release Semaphore.")



*Bounded Semaphore*
---------------------

.. code-block:: python

    from multirunnable import sleep

    @RunWith.BoundedSemaphore
    def bsmp_function():
        print("Running process with Bounded Semaphore and it will sleep 2 seconds.")
        sleep(2)
        print("Wake up process and release Bounded Semaphore.")


Why Lock with decorator?
~~~~~~~~~~~~~~~~~~~~~~~~~

Lock, Semaphore or something else features would deeply affect the performance of parallelism.
*MultiRunnable* require developers do as much as you can about ONLY lock the necessary section to
let parallelism stay at high performance. It also could remind others this function would run with
lock.


.. _Retry to run target function if it raises exception:

Retry to run target function if it raises any exception
=========================================================

*retry* - Retry to do it
------------------------

It's possible that occurs unexpected something when running. Sometimes, it needs 
to catch that exceptions or errors to do some handling or it needs to do something
finally and keep going run. That's the reason why this feature exists.

It could use the feature via Python decorator **retry** (It's **async_retry** with Asynchronous).

.. code-block:: python

    from multirunnable import sleep
    from multirunnable.api import retry

    @retry
    def target_fail_function(*args, **kwargs):
        print("It will raise exception after 3 seconds ...")
        sleep(3)
        raise Exception("Test for error")


Absolutely, it could configure how many times it would timeout (Default value is 1).

.. code-block:: python

    from multirunnable import sleep
    from multirunnable.api import retry

    @retry(timeout=3)
    def target_fail_function(*args, **kwargs):
        print("It will raise exception after 3 seconds ...")
        sleep(3)
        raise Exception("Test for error")


It would be decorated as a 'retry' object after adds decorator on it. 
So we could add some features if you need:

* :ref:`<retry function object>.initialization - Do it before run target retry function <initialization>`
* :ref:`<retry function object>.done_handling - Do it after run target retry function successfully <done_handling>`
* :ref:`<retry function object>.final_handling - No matter what it happens after it runs target retry function, it must to do it finally <final_handling>`
* :ref:`<retry function object>.error_handling - Do it after run target retry function if it get fail <error_handling>`

.. _initialization:

*initialization* - Do it before retry
--------------------------------------

The function which should be run first before run target retry function. It doesn't receive any
argument and it doesn't return value, too.

.. code-block:: python

    @target_fail_function.initialization
    def initial():
        print("This is testing initialization")


.. _done_handling:

*done_handling* - Do it after retry and run successfully
---------------------------------------------------------

It runs *done_handling* function after it runs target retry function successfully without
raising any exception. It has an argument *result* which is the return value of target retry
function. It also can return value which is the truly return value for outside caller.

.. code-block:: python

    @target_fail_function.done_handling
    def done(result):
        print("This is testing done process")
        print("Get something result: ", result)
        return result


.. _final_handling:

*final_handling* - Must to do it after retry
---------------------------------------------

No matter what it happens in target retry function, it MUST to run this finally.
For example, close IO stream.

It doesn't receive any argument and it doesn't return any value.

.. code-block:: python

    @target_fail_function.final_handling
    def final():
        print("This is final process")


.. _error_handling:

*error_handling* - Do it if it get fail in retry
------------------------------------------------

Target to handle every exceptions or errors. It only receive one argument *error* which is
what exception or error it got when it run the target retry function. It doesn't have any
return value.

.. code-block:: python

    @target_fail_function.error_handling
    def error(error):
        print("This is error process")
        print("Get something error: ", error)


Persistence in parallelism
===========================

For a parallelism development, persistence may be the most difficult problem.
*MultiRunnable* provides some APIs or rules to let you use it or implement it if it needs.


Operate with file
------------------

About persistence as file, it could use FAO (File Access Object) with object *BaseFao* directly:

.. code-block:: python

    fao = BaseFao(strategy=SavingStrategy.ALL_THREADS_ONE_FILE)
    fao.save_as_csv(mode="a+", file="testing.csv", data=_data)
    fao.save_as_excel(mode="a+", file="testing.xlsx", data=_data)
    fao.save_as_json(mode="a+", file="testing.json", data=_data)


Consider about remove the template implementations to let subclass to implement it like database subpackage.
It will deprecate this at version 0.18.0 and remove this at version 0.19.0 if it ensures the decision.


Operate with database
----------------------

It has 3 sections in subpackage *multirunnable.persistence.database*.

* Connection Factory
    module: *multirunnable.persistence.database.strategy*

    * Single Connection
    * Connection Pool

* Database Operators
    module: *multirunnable.persistence.database.operator*

For connection factory section, literally, its responsibility is generating connection or connection pool instance(s).
For another one --- operator, it responses of doing any operators with database via the connection instance which be generated from connection factory.


About implementing customized persistence objects with database, it should inherit some classes if it needs:

* Connection Factory
    * Single Connection:
        object: *BaseSingleConnection*
    * Connection Pool:
        object: *BaseConnectionPool*

* Database Operators:
    object: *DatabaseOperator*

It could only select one of them of Connection Factory. Below are some demonstrations of how to implement them (demonstrating with MySQL).


Connection Strategy
~~~~~~~~~~~~~~~~~~~~~

For *BaseSingleConnection* object, it should implement 4 functions:

* **_connect_database**: connect to database to create session.
* **_is_connected**: it should return *True* if session is connected.
* **commit**: commit the execution in session to database.
* **_close_connection**: close the session resource of database.

.. code-block:: python

    from mysql.connector.connection import MySQLConnection
    from mysql.connector.cursor import MySQLCursor
    import mysql.connector


    class MySQLSingleConnection(BaseSingleConnection):

        def _connect_database(self, **kwargs) -> MySQLConnection:
            _connection = mysql.connector.connect(**kwargs)
            return _connection


        def _is_connected(self) -> bool:
            return self.current_connection.is_connected()


        def commit(self) -> None:
            self.current_connection.commit()


        def _close_connection(self) -> None:
            if self.current_connection is not None and self.current_connection.is_connected():
                self.current_connection.close()


For *BaseConnectionPool* object, it should implement 6 functions:

* **connect_database**: connect to database to build a connection pool.
* **_get_one_connection**: get one connection instance from the connection pool.
* **_is_connected**: it should return *True* if session is connected.
* **_commit**: commit the execution in session to database.
* **_close_connection**: close the connection resource of database.
* **close_pool**: close the pool resource of database.

.. code-block:: python

    from mysql.connector.connection import MySQLConnection
    from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
    from mysql.connector.errors import PoolError
    from mysql.connector.cursor import MySQLCursor
    import mysql.connector


    class MySQLDriverConnectionPool(BaseConnectionPool):

        def connect_database(self, **kwargs) -> MySQLConnectionPool:
            connection_pool = MySQLConnectionPool(**kwargs)
            return connection_pool


        def _get_one_connection(self, pool_name: str = "", **kwargs) -> PooledMySQLConnection:
            while True:
                try:
                    __connection = get_connection_pool(pool_name=pool_name).get_connection()
                    logging.info(f"Get a valid connection: {__connection}")
                    return __connection
                except PoolError as e:
                    logging.error(f"Connection Pool: {get_connection_pool(pool_name=pool_name)} ")
                    logging.error(f"Will sleep for 5 seconds to wait for connection is available.")
                    time.sleep(5)
                except AttributeError as ae:
                    raise ConnectionError(f"Cannot get the one connection instance from connection pool because it doesn't exist the connection pool with the name '{pool_name}'.")


        def _is_connected(self, conn: PooledMySQLConnection) -> bool:
            return conn.is_connected()


        def _commit(self, conn: PooledMySQLConnection) -> None:
            conn.commit()


        def _close_connection(self, conn: PooledMySQLConnection) -> None:
            if self.connection is not None and self.connection.is_connected():
                self.connection.close()


        def close_pool(self, pool_name: str) -> None:
            get_connection_pool(pool_name=pool_name).close()


Operator
~~~~~~~~~~

For *DatabaseOperator* object, it could implement some functions:

* **initial_cursor**: initial a cursor instance for all functions to do some operators with database.
* **execute**: execute the SQL query.
* **execute_many**: batch execute the SQL query.
* **fetch_one**: get one data row.
* **fetch_many**: get a specific count of data rows.
* **fetch_all**: get all data rows.

.. code-block:: python

    class MySQLOperator(DatabaseOperator):

        def __init__(self, conn_strategy: BaseDatabaseConnection, db_config: Dict = {}):
            super().__init__(conn_strategy=conn_strategy, db_config=db_config)


        def initial_cursor(self, connection: Union[MySQLConnection, PooledMySQLConnection]) -> MySQLCursor:
            return connection.cursor(buffered=True)


        def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> MySQLCursor:
            return self._cursor.execute(operation=operator, params=params, multi=multi)


        def execute_many(self, operator: Any, seq_params=None) -> MySQLCursor:
            return self._cursor.executemany(operation=operator, seq_params=seq_params)


        def fetch_one(self) -> MySQLCursor:
            return self._cursor.fetchone()


        def fetch_many(self, size: int = None) -> MySQLCursor:
            return self._cursor.fetchmany(size=size)


        def fetch_all(self) -> MySQLCursor:
            return self._cursor.fetchall()


Dao
~~~~~

Finally, let's implement your customized DAO which extends *BaseDao*:

* **_instantiate_strategy**: initial strategy.
* **_instantiate_database_opts**: initial database operator.

.. code-block:: python

    class TestingDao(BaseDao):

        def __init__(self, db_driver=None, use_pool=False):
            self.db_driver = db_driver
            self.use_pool = use_pool

            # Initial and connect to database and get connection, cursor (or session) instance
            self._database_config = {
                "host": "127.0.0.1",
                # "host": "172.17.0.6",
                "port": "3306",
                "user": "root",
                "password": "password",
                "database": "tw_stock"
            }

            super().__init__()
            self._logger = logging.getLogger(self.__class__.__name__)


        def _instantiate_strategy(self) -> BaseDatabaseConnection:
            if self.db_driver == "mysql":
                # from db_mysql import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator
                if self.use_pool is True:
                    db_conn_strategy = MySQLDriverConnectionPool(**self._database_config)
                else:
                    db_conn_strategy = MySQLSingleConnection(**self._database_config)
                return db_conn_strategy
            else:
                raise ValueError


        def _instantiate_database_opts(self, strategy: BaseDatabaseConnection) -> DatabaseOperator:
            _database_opts = MySQLOperator(conn_strategy=strategy)
            return _database_opts


        def get_test_data(self):
            self.execute('SELECT col_1, col_2 FROM test.test_table LIMIT 10')
            data = self.fetch_all()
            return data


Okay, we done all tasks we need to implement! Let's try to use it via *DAO*:

.. code-block:: python

    _dao = TestingDao(db_driver="mysql")    # Use single connection strategy
    # _dao = TestingDao(db_driver="mysql", use_pool=True)    # Use connections pool
    _data = _dao.get_test_data()
    print(f"Data: {_data}")


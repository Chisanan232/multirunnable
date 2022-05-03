==========
Examples
==========

Some demonstrations of how to use some general modules and its APIs. It demonstrates 4 points and 2 features:

* 4 Points
    * *multirunnable.SimpleExecutor*
    * *multirunnable.SimplePool*
    * Executor or Pool with *multirunnable.persistence.file*
    * Executor or Pool with *multirunnable.persistence.database*

* 2 Features
    * Lock with Python decorators
    * Retry mechanism


4 Points
=========

Demonstrating the core module and APIs of *multirunnable*.

.. _Simple Executor:

Simple Executor
----------------

An example shows how to use *multirunnable.SimpleExecutor*:

.. code-block:: python

    from multirunnable import RunningMode, SimpleExecutor, sleep

    def target_function(self, *args, **kwargs) -> str:
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        return "Hello, Return"

    _executor_number = 3
    # # # # Initial Executor object
    _executor = SimpleExecutor(mode=RunningMode.Parallel, executors=_executor_number)
    # _executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=_executor_number)
    # _executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=_executor_number)

    # # # # Running the Executor
    _executor.run(function=target_function, args=("index_1", "index_2.2"))

    # # # # Get result
    _result = p.get_result()
    print("Result: ", _result)



.. _Simple Pool:

Simple Pool
------------

Using *multirunnable.SimplePool*:

.. code-block:: python

    from multirunnable import RunningMode, SimplePool, sleep
    import random

    def target_function(self, *args, **kwargs) -> str:
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        return "Hello, Return"

    _pool_size = 5
    # # # # Initial Pool object
    _pool = SimplePool(mode=RunningMode.Parallel, pool_size=_pool_size)
    # _pool = SimplePool(mode=RunningMode.Concurrent, pool_size=_pool_size)
    # _pool = SimplePool(mode=RunningMode.GreenThread, pool_size=_pool_size)

    with _pool as p:
        # # # # Running Pool
        # p.apply(function=target_function, tasks_size=_pool_size, kwargs={"index": f"test_{random.randrange(10,20)}"})
        p.async_apply(function=target_function, tasks_size=_pool_size, kwargs={"index": f"test_{random.randrange(10,20)}"})
        # p.map(function=target_function, args_iter=("index_1", "index_2.2", "index_3"))
        # p.map_by_args(function=target_function, args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Get result
        # # # # You will get the result of 'map' only.
        _result = p.get_result()
        print("Result: ", _result)



.. _Persistence - File:

Persistence - File
-------------------

About persistence as file, it could use FAO (File Access Object) with object *BaseFao* directly:

.. code-block:: python

    fao = BaseFao(strategy=SavingStrategy.ALL_THREADS_ONE_FILE)
    fao.save_as_csv(mode="a+", file="testing.csv", data=_data)
    fao.save_as_excel(mode="a+", file="testing.xlsx", data=_data)
    fao.save_as_json(mode="a+", file="testing.json", data=_data)


Consider about remove the template implementations to let subclass to implement it like database subpackage.
It will deprecate this at version 0.18.0 and remove this at version 0.19.0 if it ensures the decision.


.. _Persistence - Database:

Persistence - Database
-----------------------

It has 3 sections in subpackage *.multirunnable.persistence.database*.

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

It only select one of them of Connection Factory. Below are some demonstrations of how to implement them (demonstrating with MySQL).


For *BaseSingleConnection* object:

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


For *BaseConnectionPool* object:

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
            self.connection.commit()


        def _close_connection(self, conn: PooledMySQLConnection) -> None:
            if self.connection is not None and self.connection.is_connected():
                self.connection.close()


        def close_pool(self, pool_name: str) -> None:
            get_connection_pool(pool_name=pool_name).close()


For *DatabaseOperator* object:

.. code-block:: python

    class MySQLOperator(DatabaseOperator):

        def __init__(self, conn_strategy: BaseDatabaseConnection, db_config: Dict = {}):
            super().__init__(conn_strategy=conn_strategy, db_config=db_config)


        def initial_cursor(self, connection: Union[MySQLConnection, PooledMySQLConnection]) -> MySQLCursor:
            return connection.cursor(buffered=True)


        @property
        def column_names(self) -> MySQLCursor:
            return self._cursor.column_names


        @property
        def row_count(self) -> MySQLCursor:
            return self._cursor.rowcount


        def next(self) -> MySQLCursor:
            return self._cursor.next()


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


        def reset(self) -> None:
            self._cursor.reset()


Here is an example how to use them:

.. code-block:: python

    _database_config = {
        "host": "127.0.0.1",
        "port": "3306",
        "user": "root",
        "password": "password",
        "database": "test"
    }

    # # Using single connection strategy
    _db_opts = MySQLOperator(MySQLSingleConnection(**_database_config))
    # # Using connection pool strategy
    # _db_opts = MySQLOperator(MySQLDriverConnectionPool(**_database_config))

    _db_opts.execute('SELECT col_1, col_2 FROM test.test_table LIMIT 10')
    _data = _db_opts.fetch_all()


2 Features
===========

Demonstrating some features with Python syntactic sugar of *multirunnable*.

Lock with Python decorators
----------------------------

An example show how to decorate Lock feature to a function.

.. code-block:: python

    from multirunnable.api import RunWith

    @RunWith.Lock
    def lock_function(self):
        print("This is testing process with Lock and sleep for 3 seconds.")
        sleep(3)
        return "Return_Value"



.. _Retry mechanism:

Retry mechanism
-----------------

An example show how to use feature 'retry'.

.. code-block:: python

    from multirunnable.api import retry
    import multirunnable

    class ExampleTargetFunction:

        def target_function(self, *args, **kwargs) -> str:
            multirunnable.sleep(3)
            return "Return_Value."


        @retry
        def target_fail_function(self, *args, **kwargs) -> None:
            print("It will raise exception after 3 seconds ...")
            multirunnable.sleep(3)
            raise Exception("Test for error")


        @target_fail_function.initialization
        def initial(self):
            print("This is testing initialization")


        @target_fail_function.done_handling
        def done(self, result):
            print("This is testing done process")
            print("Get something result: ", result)


        @target_fail_function.final_handling
        def final(self):
            print("This is final process")


        @target_fail_function.error_handling
        def error(self, error):
            print("This is error process")
            print("Get something error: ", error)


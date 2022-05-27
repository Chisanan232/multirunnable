=======================
Persistence - Database
=======================


*module* multirunnable.persistence.database

The subpackage for database features of persistence of *MultiRunnable*.
It could connect to database and instantiate a connection instance with database like general usage.
It also could implement that in multiple runnable objects to operate with database.
However, it would be a problem in high performance scenario. Connection Pool would
be developer's good choice as that time. It's a pool of connection instances so
that it doesn't need to do initial process like connect to database to instantiate
every time it needs to use in every runnable objects.

In parallelism, it needs to initial the connection pool first to ready to do any
operator with database for runnable objects. In the other words, it should
initial connection pool before it initials and runs multiple runnable objects.
So *MultiRunnable* divides the database-persistence features to 3 sections:

* Connection Factory
    module: *multirunnable.persistence.database.strategy*

    Objects:

    * Single Connection
    * Connection Pool

* Database Operators
    module: *multirunnable.persistence.database.operator*

* Persistence Layer
    module: *multirunnable.persistence.database.layer*


For **Connection Factory** section, literally, its responsibility is generating connection or connection pool instance(s).
For **Database Operator**, it responses of doing any operators with database via the connection instance which be generated from connection factory.
And for another one --- **Persistence Layer**, it responses of being a DAO (Database Access Object) role for client site.

All of them are abstracted class. They're template classes annotate some template methods already to use.
So subclass only need to implement all abstract methods which could let some template methods work finely.

All the modules in *multirunnable.persistence.database* has be refactored in new version 0.17.0.


Strategy Objects
===================

*module* multirunnable.persistence.database.strategy

About strategy module, it has 2 objects *BaseSingleConnection* and *BaseConnectionPool*.
Literally, one for using single database connection instance which would be
initialed, instantiated, executed and closed every using time. Another one
would initial pool once and get the connection instance from the pool every time.


**database_connection_pools**\ *()*

    Get all instances of each sub-class of *BaseConnectionPool*.

    Return:
        A dictionary, key is the class name and value is the class's instance.


**get_connection_pool**\ *(pool_name)*

    Get the specific instance with the class's name.

    Parameters:
        * *pool_name* (str) : An iterator of *Workers*.
    Return:
        An instance of the class's name, but it would return None if it cannot find the key.


BaseDatabaseConnection
------------------------

*class* multirunnable.persistence.database.strategy.\ **BaseDatabaseConnection**\ *(**kwargs)*

    This is the base class rules which methods you should implement.
    It would initial database configuration first if it be instantiated.

    This class also be implemented with Singleton Pattern for keeping same database configuration and
    connection instance(s). The reasons are:

        1. Save database configuration to avoid to it need to set it before use it every time.
        2. Keep using the same database connection instance to avoid to instantiate it every time.
        3. Share the same connection pool instance to each workers so that they could get connection instance from it.

    Therefore, it would guarantee the instance of class *BaseDatabaseConnection* or its sub-classes be used from
    the same one with current instance name.

    Parameters:
        * *kwargs* (Dict) : The configuration of database.
    Return:
        *BaseDatabaseConnection* object.


    *abstractmethod* **_initial_database_config**\ *()*

        Initial database configuration with default settings and save it into a global variable which is *dict* type.
        The key would be the currently instance name.

        Return:
            None.


    *abstractmethod* **_update_database_config**\ *(db_config)*

        Update the database configuration with argument *db_config*.

        Parameters:
            * *db_config* (dict) : One or more settings of database configuration.
        Return:
            None.


    *property* *abstractmethod* **database_config**\ *()*

        Operate with database configuration as property of instance. It has getter and setter.
        Getter would return *dict* type value and setter should entry *dict* type value.


    *abstractmethod* **update_database_config**\ *(key, value)*

        Update the value of database configuration with target key.

        Parameters:
            * *key* (str) : The setting name.
            * *value* (Any) : The setting value.
        Return:
            None.


    **_get_instance_name**\ *()*

        Get the current instance name.

        Return:
            A str value, returns the current instance name.


    *abstractmethod* **get_all_database_configs**\ *()*

        Get all the database configurations of each instances.

        Return:
            A dictionary value.


    *property* *abstractmethod* **current_connection**\ *()*

        Return the database connection instance with current instance name.

        * For object *BaseSingleConnection*, it would return the current connection instance by instance name.
        * For object *BaseConnectionPool*, it would return the current connection instance by worker name.


    *abstractmethod* **initial**\ *(**kwargs)*

        Initial processing of this object. It would connect to database and instantiate an connection instance.

        * For object *BaseSingleConnection*, it would connect to database and get the connection instance.
        * For object *BaseConnectionPool*, it would connect to database and get the connection pool instance. Finally, it would save the pool instance as global variable.

        Return:
            None.


    *abstractmethod* **connect_database**\ *(**kwargs)*

        Connect to database with configuration.

        * For object *BaseSingleConnection*, it would connect to database and get the connection instance.
        * For object *BaseConnectionPool*, it would connect to database and get the connection pool instance.

        Return:
            Return a database connection instance (sub-class which extends *BaseSingleConnection*) or a database connection pool instance (sub-class which extends *BaseConnectionPool*).

.. _BaseDatabaseConnection.reconnect:

    *abstractmethod* **reconnect**\ *(timeout=3, force=False)*

        Reconnect to database. Argument *timeout* control how many times it would retry timeout.
        It would force to reconnect to database (no matter the connection instance still is connected or not)
        if argument *force* is *True*, or it doesn't if session is connected if *force* is *False*.

        Parameters:
            * *timeout* (int) : The number of seconds it would timeout to raise an exception when it try to connect to database to get connection instance.
            * *force* (bool) : It would force to connect to database again and get a new database connection instance if *force* is True, or it may be return existed connection instance event it maybe not connected.
        Return:
            A database connection instance.


    *abstractmethod* **get_one_connection**\ *(**kwargs)*

        Get a database connection instance.

        * For object *BaseSingleConnection*, it returns connection instance directly if it exists and still is connected, or it would connect to database first, get the connection instance and return it.
        * For object *BaseConnectionPool*, it would try to get one connection from pool with argument *pool_name* and return it.

        Return:
            A database connection instance.


    **is_connected**\ *(**kwargs)*

        Return *True* if current database connection session still is connected, or it would return *False*.

        Return:
            Return a boolean value. It's True if instance state is connected, or it's False.

.. _BaseDatabaseConnection.commit:

    *abstractmethod* **commit**\ *(**kwargs)*

        Commit the SQL execution to database.

        Return:
            None.

.. _BaseDatabaseConnection.close_connection:

    *abstractmethod* **close_connection**\ *(**kwargs)*

        Close the database connection instance.

        Return:
            None.


BaseSingleConnection
----------------------

*class* multirunnable.persistence.database.strategy.\ **BaseSingleConnection**\ *(initial=True, **kwargs)*

    It would run *initial* first if the option *initial* is True (default is True).

    Parameters:
        * *initial* (bool) : it would get connection instance in instantiate this object process.
        * *kwargs* (Dict) : The configuration of database.
    Return:
        *BaseDatabaseConnection* object.


    **initial**\ *(**kwargs)*

        Implement *abstractmethod* **initial**. It would initial database configuration and use it to
        connect to database to get session instance.

        Return:
            None.


    *abstractmethod* **_connect_database**\ *(**kwargs)*

        Truly run the implementation about connecting to database and get session instance.

        Sub-class must to implement.

        Parameters:
            * *kwargs* (dict) : The configuration of database.
        Return:
            A database connection instance.


    **get_one_connection**\ *()*

        Implement *abstractmethod* *get_one_connection*. Return the current database connection instance. It would connect to database to initial
        instance if it doesn't exist or be disconnected.

        Return:
            A database connection instance.


    *abstractmethod* **commit**\ *()*

        Commit the SQL execution to database.

        Sub-class must to implement.

        Return:
            None.


    *abstractmethod* **_close_connection**\ *()*

        Truly run the implementation about closing database connection instance.

        Sub-class must to implement.

        Return:
            None.


BaseConnectionPool
--------------------

*class* multirunnable.persistence.database.strategy.\ **BaseConnectionPool**\ *(initial=True)*

    It would run *initial* first if the option *initial* is True (default is True).

    Parameters:
        * *initial* (bool) : it would connect to database in instantiate this object process.
        * *kwargs* (Dict) : The configuration of database.
    Return:
        *BaseDatabaseConnection* object.


    **initial**\ *(**kwargs)*

        Initial processing of this object. It would connect to database to instantiate a connection pool
        and set it into a *dict* type global variable with key which is *pool_name*.

        Parameters:
            * *kwargs* (dict) : The configuration of database.
        Return:
            None.


    *property* **current_pool_name**\ *()*

        Return pool name of connection pool we're using currently. It could use *getting* and *setting* of this property.


    *property* **pool_size**\ *()*

        Return pool size of connection pool we're using currently. It could use *getting* and *setting* of this property.


    **get_one_connection**\ *(pool_name="", **kwargs)*

        Implement *abstractmethod* *get_one_connection*. Return a connection which be get from connection pool instance.

        Parameters:
            * *pool_name* (str) : The connection pool name.
            * *kwargs* (dict) : The configuration of database.
        Return:
            A database connection instance.


    *abstractmethod* **_get_one_connection**\ *(pool_name="", **kwargs)*

        Truly run the implementation about getting connection instance from connection pool.

        Sub-class must to implement.

        Parameters:
            * *pool_name* (str) : The connection pool name.
            * *kwargs* (dict) : The configuration of database.
        Return:
            A database connection instance.


    *abstractmethod* **_commit**\ *(conn)*

        Commit the SQL execution to database with the connection instance from argument *conn*.

        Sub-class must to implement.

        Parameters:
            * *conn* (Any) : Database connection instance.
        Return:
            None.


    *abstractmethod* **_close_connection**\ *(conn)*

        Truly run the implementation about closing the connection resource of pool instance with the
        connection instance from argument *conn*.

        Sub-class must to implement.

        Parameters:
            * *conn* (Any) : Database connection instance.
        Return:
            None.



Operator Objects
===================

*module* multirunnable.persistence.database.operator

It responses of all operators with database, it including generating database cursor
instance from the connection instance which be get by **BaseDatabaseConnection** object.

BaseDatabaseOperator
----------------------

*class* multirunnable.persistence.database.operator.\ **BaseDatabaseOperator**\ *(conn_strategy, db_config={}, timeout=1)*

    Some basic operator with database. Option *conn_strategy* receives **BaseSingleConnection** or **BaseConnectionPool** object. It decides how to get connection instance.
    Option *db_config* receives dict type data, it's the configuration to connect to database.

    Parameters:
        * *conn_strategy* (BaseDatabaseConnection) : The database connection strategy object.
        * *db_config* (Dict) : The configuration of database.
        * *timeout* (int) : The timeout of connecting database.
    Return:
        *BaseDatabaseOperator* object.


    *property* **_connection**\ *()*

        Return database connection instance. It would reconnect by itself if connection is None.
        It only be permitted to use *getting* of this property.


    *property* **_cursor**\ *()*

        Return database cursor instance by connection instance with *_connection*.
        It only be permitted to use *getting* of this property.


    *abstractmethod* **reconnect**\ *(timeout=1, force=False)*

        Reconnect to database. This function working is same as :ref:`BaseDatabaseConnection.reconnect<BaseDatabaseConnection.reconnect>`.


    *abstractmethod* **commit**\ *(**kwargs)*

        Commit the SQL execution to database. This function working is same as :ref:`BaseDatabaseConnection.commit<BaseDatabaseConnection.commit>`.


    *abstractmethod* **close_connection**\ *(**kwargs)*

        Close the connection of database. This function working is same as :ref:`BaseDatabaseConnection.close_connection<BaseDatabaseConnection.close_connection>`.


    *abstractmethod* **initial_cursor**\ *(connection: Generic[T])*

        Initial and return a database cursor instance.

        Parameters:
            * *connection* (Generic[T]) : Database connection instance.
        Return:
            A database cursor instance.

.. _BaseDatabaseOperator.execute:

    *abstractmethod* **execute**\ *(operator, params=None, multi=False)*

        Execute SQL query.

        Parameters:
            * *operator* (str) : The SQL query.
            * *params* (Tuple) : The arguments of SQL.
            * *multi* (bool) : It could run multiple queries and return an iterator.
        Return:
            None. But it would return an iterator if *multi* is True.

.. _BaseDatabaseOperator.execute_many:

    **execute_many**\ *(operator, seq_params)*

        Execute SQL queries via batch.

        Parameters:
            * *operator* (Any) : The SQL query.
            * *seq_params* (Any) : An iterator of SQL arguments.
        Return:
            None.

.. _BaseDatabaseOperator.fetch_one:

    **fetch_one**\ *()*

        Get only one data row of query result.

        Return:
            A list type value.

.. _BaseDatabaseOperator.fetch_many:

    *abstractmethod* **fetch_many**\ *(size=None)*

        Get the size of data rows of query result.

        Parameters:
            * *size* (int) : The size of data rows.
        Return:
            A list type value.

.. _BaseDatabaseOperator.fetch_all:

    **fetch_all**\ *()*

        Get all data rows of query result.

        Return:
            A list type value.

.. _BaseDatabaseOperator.close_cursor:

    *abstractmethod* **close_cursor**\ *()*

        Close the database cursor instance.

        Return:
            None.


DatabaseOperator
------------------

*class* multirunnable.persistence.database.operator.\ **DatabaseOperator**\ *(conn_strategy, db_config={}, timeout=1)*

    This object implements all the *abstractmethod* which is related with *BaseDatabaseConnection* includes *reconnect*, *commit* and *close_connection*.



Persistence Layer Objects
==========================

*module* multirunnable.persistence.database.layer

It's a DAO (Database Access Object) role to let client site operating database.
It annotates some templated methods which could be used directly by subclass.
So the business logic which related with SQL should be implemented here but never
implement any operator detail with database like how to execute SQL or fetch data row.

BaseDao
--------

*class* multirunnable.persistence.database.layer.\ **BaseDao**\ *()*

    The base class to let all subclass to inherit it.

    Return:
        A database access object object *BaseDao*.


    *property* *abstractmethod* **database_opt**\ *()*

        Return *BaseDatabaseOperator* type instance to let template methods to use it.
        It's an abstracted method so developers should implement what *BaseDatabaseOperator* type instance it returns.

        Return:
            A list type value.


    *abstractmethod* **_instantiate_strategy**\ *()*

        Return *BaseDatabaseConnection* type instance to let template methods to use it.

        Return:
            A database connection strategy object *BaseDatabaseConnection*.


    *abstractmethod* **_instantiate_database_opts**\ *(strategy)*

        Return *BaseDatabaseOperator* type instance to let template methods to use it.

        Parameters:
            * *strategy* (BaseDatabaseConnection) : The database connection strategy.
        Return:
            A database operator object *DatabaseOperator*.


    **reconnect**\ *(timeout: int = 1, force: bool = False)*

        Reconnect to database. This function working is same as :ref:`BaseDatabaseConnection.reconnect<BaseDatabaseConnection.reconnect>`.


    **commit**\ *()*

        Commit the SQL execution to database. This function working is same as :ref:`BaseDatabaseConnection.commit<BaseDatabaseConnection.commit>`.


    **execute**\ *(operator: Any, params: Tuple = None, multi: bool = False)*

        Execute SQL query. It's same as :ref:`BaseDatabaseOperator.execute<BaseDatabaseOperator.execute>`.


    **execute_many**\ *(operator: Any, seq_params: Tuple = None)*

        Execute SQL queries via batch. It's same as :ref:`BaseDatabaseOperator.execute_many<BaseDatabaseOperator.execute_many>`.


    **fetch_one**\ *()*

        Get only one data row of query result. It's same as :ref:`BaseDatabaseOperator.fetch_one<BaseDatabaseOperator.fetch_one>`.


    **fetch_many**\ *(size: int = None)*

        Execute SQL queries via batch. It's same as :ref:`BaseDatabaseOperator.fetch_many<BaseDatabaseOperator.fetch_many>`.


    **fetch_all**\ *()*

        Get all data rows of query result. It's same as :ref:`BaseDatabaseOperator.fetch_all<BaseDatabaseOperator.fetch_all>`.


    **close_cursor**\ *()*

        Close the database cursor instance. It's same as :ref:`BaseDatabaseOperator.close_cursor<BaseDatabaseOperator.close_cursor>`.


    **close_connection**\ *()*

        Close the database connection instance. It's same as :ref:`BaseDatabaseConnection.close_connection<BaseDatabaseConnection.close_connection>`.



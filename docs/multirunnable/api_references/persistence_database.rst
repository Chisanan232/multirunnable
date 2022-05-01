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

BaseDatabaseConnection
------------------------

*class* multirunnable.persistence.database.strategy.\ **BaseDatabaseConnection**\ *([str, Any])*

    This is the base class rules which methods you should implement.
    It would initial database configuration first if it be instantiated.

    This class also be implemented with Singleton Pattern for keeping same database configuration and
    connection instance(s). The reasons are:

        1. Save database configuration to avoid to it need to set it before use it every time.
        2. Keep using the same database connection instance to avoid to instantiate it every time.
        3. Share the same connection pool instance to each workers so that they could get connection instance from it.

    Therefore, it would guarantee the instance of class *BaseDatabaseConnection* or its sub-classes be used from
    the same one with current instance name.


*abstractmethod* **_initial_database_config**\ *()*

    Initial database configuration with default settings and save it into a global variable which is *dict* type.
    The key would be the currently instance name.


*abstractmethod* **_update_database_config**\ *(db_config: dict)*

    Update the database configuration with argument *db_config*.


*property* *abstractmethod* **database_config**\ *()*

    Operate with database configuration as property of instance. It has getter and setter.
    Getter would return *dict* type value and setter should entry *dict* type value.


*abstractmethod* **update_database_config**\ *(key: str, value: Any)*

    Update the value of database configuration with target key.


**_get_instance_name**\ *()*

    Get the current instance name.


*abstractmethod* **get_all_database_configs**\ *()*

    Get all the database configurations of each instances.


*property* *abstractmethod* **current_connection**\ *()*

    Return the database connection instance with current instance name.

    * For object *BaseSingleConnection*, it would return the current connection instance by instance name.
    * For object *BaseConnectionPool*, it would return the current connection instance by worker name.


*abstractmethod* **initial**\ *(**kwargs)*

    Initial processing of this object. It would connect to database and instantiate an connection instance.

    * For object *BaseSingleConnection*, it would connect to database and get the connection instance.
    * For object *BaseConnectionPool*, it would connect to database and get the connection pool instance. Finally, it would save the pool instance as global variable.


*abstractmethod* **connect_database**\ *(**kwargs)*

    Connect to database with configuration.

    * For object *BaseSingleConnection*, it would connect to database and get the connection instance.
    * For object *BaseConnectionPool*, it would connect to database and get the connection pool instance.


*abstractmethod* **reconnect**\ *(timeout: int = 3, force: bool = False)*

    Reconnect to database. Argument *timeout* control how many times it would retry timeout.
    It would force to reconnect to database (no matter the connection instance still is connected or not)
    if argument *force* is *True*, or it doesn't if session is connected if *force* is *False*.


*abstractmethod* **get_one_connection**\ *(**kwargs)*

    Get a database connection instance.

    * For object *BaseSingleConnection*, it returns connection instance directly if it exists and still is connected, or it would connect to database first, get the connection instance and return it.
    * For object *BaseConnectionPool*, it would try to get one connection from pool with argument *pool_name* and return it.


**is_connected**\ *()*

    Return *True* if current database connection session still is connected, or it would return *False*.


*abstractmethod* **commit**\ *(**kwargs)*

    Commit the SQL execution to database.


*abstractmethod* **close_connection**\ *()*

    Close the database connection instance.


BaseSingleConnection
----------------------

*class* multirunnable.persistence.database.strategy.\ **BaseSingleConnection**\ *(initial=True, [str, Any])*

    It would run *initial* first if the option *initial* is True (default is True).


**initial**\ *(**kwargs)*

    Implement *abstractmethod* **initial**. It would initial database configuration and use it to
    connect to database to get session instance.


*abstractmethod* **_connect_database**\ *(**kwargs)*

    Truly run the implementation about connecting to database and get session instance.

    Sub-class must to implement.


*abstractmethod* **_is_connected**\ *()*

    Truly run the implementation about checking whether current session instance is connected or not.

    Sub-class must to implement.


**get_one_connection**\ *()*

    Implement *abstractmethod* *get_one_connection*. Return the current database connection instance. It would connect to database to initial
    instance if it doesn't exist or be disconnected.


*abstractmethod* **commit**\ *()*

    Commit the SQL execution to database.

    Sub-class must to implement.


*abstractmethod* **_close_connection**\ *()*

    Truly run the implementation about closing database connection instance.

    Sub-class must to implement.


BaseConnectionPool
--------------------

*class* multirunnable.persistence.database.strategy.\ **BaseConnectionPool**\ *(initial=True)*

    It would run *initial* first if the option *initial* is True (default is True).


**initial**\ *(**kwargs)*

    Initial processing of this object. It would connect to database to instantiate a connection pool
    and set it into a *dict* type global variable with key which is *pool_name*.


*property* **current_pool_name**\ *()*

    Return pool name of connection pool we're using currently. It could use *getting* and *setting* of this property.


*property* **pool_size**\ *()*

    Return pool size of connection pool we're using currently. It could use *getting* and *setting* of this property.


**get_one_connection**\ *()*

    Implement *abstractmethod* *get_one_connection*. Return a connection which be get from connection pool instance.


*abstractmethod* **_get_one_connection**\ *()*

    Truly run the implementation about getting connection instance from connection pool.

    Sub-class must to implement.


*abstractmethod* **_commit**\ *(conn: Any = None)*

    Commit the SQL execution to database with the connection instance from argument *conn*.

    Sub-class must to implement.


*abstractmethod* **_close_connection**\ *(conn: Any = None)*

    Truly run the implementation about closing the connection resource of pool instance with the
    connection instance from argument *conn*.

    Sub-class must to implement.



Operator Objects
===================

*module* multirunnable.persistence.database.operator

It responses of all operators with database, it including generating database cursor
instance from the connection instance which be get by **BaseDatabaseConnection** object.

BaseDatabaseOperator
----------------------

*class* multirunnable.persistence.database.operator.\ **BaseDatabaseOperator**\ *(conn_strategy: BaseDatabaseConnection, db_config: Dict = {}, timeout: int = 1)*

    Some basic operator with database. Option *conn_strategy* receives **BaseSingleConnection** or **BaseConnectionPool** object. It decides how to get connection instance.
    Option *db_config* receives dict type data, it's the configuration to connect to database.


*property* **_connection**\ *()*

    Return database connection instance. It would reconnect by itself if connection is None.
    It only be permitted to use *getting* of this property.


*property* **_cursor**\ *()*

    Return database cursor instance by connection instance with *_connection*.
    It only be permitted to use *getting* of this property.


*abstractmethod* **reconnect**\ *(timeout: int = 1, force: bool = False)*

    Reconnect to database. This function working is same as *BaseDatabaseConnection.reconnect*.


*abstractmethod* **commit**\ *(**kwargs)*

    Commit the SQL execution to database. This function working is same as *BaseDatabaseConnection.commit*.


*abstractmethod* **close_connection**\ *(**kwargs)*

    Close the connection of database. This function working is same as *BaseDatabaseConnection.close_connection*.


*abstractmethod* **initial_cursor**\ *()*

    Initial and return a database cursor instance.


*abstractmethod* **execute**\ *(operator: Any, params: Tuple = None, multi: bool = False)*

    Execute SQL query.


**execute_many**\ *(operator: Any, seq_params=None)*

    Execute SQL queries via batch.


**fetch**\ *()*

    Get result of query.


**fetch_one**\ *()*

    Get only one data row of query result.


*abstractmethod* **fetch_many**\ *(size: int = None)*

    Get the size of data rows of query result.


**fetch_all**\ *()*

    Get all data rows of query result.


*abstractmethod* **close**\ *()*

    Close the database cursor instance.


DatabaseOperator
------------------

*class* multirunnable.persistence.database.operator.\ **DatabaseOperator**\ *(conn_strategy: BaseDatabaseConnection, db_config: Dict = {}, timeout: int = 1)*

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


*property* *abstractmethod* **database_opt**\ *()*

    Return *BaseDatabaseOperator* type instance to let template methods to use it.
    It's an abstracted method so developers should implement what *BaseDatabaseOperator* type instance it returns.


*abstractmethod* **_instantiate_strategy**\ *()*

    Return *BaseDatabaseConnection* type instance to let template methods to use it.


*abstractmethod* **_instantiate_database_opts**\ *(strategy: BaseDatabaseConnection)*

    Return *BaseDatabaseOperator* type instance to let template methods to use it.


**reconnect**\ *(timeout: int = 1, force: bool = False)*

    Reconnect to database. This function working is same as *BaseDatabaseConnection.reconnect*.


**commit**\ *()*

    Commit the SQL execution to database. This function working is same as *BaseDatabaseConnection.commit*.


**execute**\ *(operator: Any, params: Tuple = None, multi: bool = False)*

    Execute SQL query. It's same as *BaseDatabaseOperator.execute*.


**execute_many**\ *(operator: Any, seq_params: Tuple = None)*

    Execute SQL queries via batch. It's same as *BaseDatabaseOperator.execute_many*.


**fetch_one**\ *()*

    Get only one data row of query result. It's same as *BaseDatabaseOperator.fetch_one*.


**fetch_many**\ *(size: int = None)*

    Execute SQL queries via batch. It's same as *BaseDatabaseOperator.fetch_many*.


**fetch_all**\ *()*

    Get all data rows of query result. It's same as *BaseDatabaseOperator.fetch_all*.


**close_cursor**\ *()*

    Close the database cursor instance. It's same as *BaseDatabaseOperator.close_cursor*.


**close_connection**\ *()*

    Close the database connection instance. It's same as *BaseDatabaseConnection.close_connection*.



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


Strategy Objects
===================

*module* multirunnable.persistence.database.strategy

About strategy module, it has 2 objects *BaseSingleConnection* and *BaseConnectionPool*.
Literally, one for using single database connection instance which would be
initialed, instantiated, executed and closed every using time. Another one
would initial pool once and get the connection instance from the pool every time.

BaseSingleConnection
----------------------

*class* multirunnable.persistence.database.strategy.\ **BaseSingleConnection**\ *(initial=True, [str, Any])*
    It would run *initial* first if the option *initial* is True (default is True).

**initial**\ *(**kwargs)*
    Initial processing of this object. It would connect to database and instantiate an connection instance.

*abstractmethod and property* **connection**\ *()*
    Return the current database connection instance.

*abstractmethod* **connect_database**\ *(**kwargs)*
    Connect to database and instantiate connection instance. Arguments are the options of Python package of database.

**reconnect**\ *(timeout)*
    Reconnect to database until it timeout of connect to database. Option *timeout*
    control how many timeout it could occur. Default value is 3.

**get_one_connection**\ *()*
    Return the current database connection instance. It would connect to database to initial
    instance if it doesn't have.

*abstractmethod* **commit**\ *()*
    Commit database connection.

*abstractmethod* **close**\ *()*
    Close the database instance.


BaseConnectionPool
--------------------

*class* multirunnable.persistence.database.strategy.\ **BaseConnectionPool**\ *(initial=True)*
    It would run *initial* first if the option *initial* is True (default is True).

**initial**\ *(**kwargs)*
    Initial processing of this object. It would connect to database to instantiate a connection pool
    and set it into a dict type global variable with key which is *pool_name* of it.

*property* **current_pool_name**\ *()*
    Return pool name of connection pool we're using currently. It could use *getting* and *setting* of this property.

*property* **connection**\ *()*
    Return a connection instance which be get from connection pool. It only be permitted to use *getting* of this property.

*property* **pool_size**\ *()*
    Return pool size of connection pool we're using currently. It could use *getting* and *setting* of this property.

**reconnect**\ *(timeout)*
    Reconnect to database and instantiate a pool instance.
    It would set it to a global variable (dict type) with pool name as key and return a connection instance if it reconnect successfully.

*abstractmethod* **get_one_connection**\ *()*
    Return a connection which be get from connection pool instance. This is a abstract method.

*abstractmethod* **commit**\ *()*
    Commit database connection.

*abstractmethod* **close_pool**\ *()*
    Close the connection pool with the pool name.



Operator Objects
===================

*module* multirunnable.persistence.database.operator

It responses of all operators with database, it including generating database cursor
instance from the connection instance which be get by **Strategy Objects**.

BaseDatabaseOperator
----------------------

*class* multirunnable.persistence.database.strategy.\ **BaseDatabaseOperator**\ *(conn_strategy, db_config)*
    Some basic operator with database. Option *conn_strategy* receives **BaseSingleConnection** or **BaseConnectionPool** object. It decides how to get connection instance.
    Option *db_config* receives dict type data, it's the configuration to connect to database.

*property* **_connection**\ *()*
    Return database connection instance. It would reconnect by itself if connection is None.
    It only be permitted to use *getting* of this property.

*property* **_cursor**\ *()*
    Return database cursor instance by connection instance with *_connection*.
    It only be permitted to use *getting* of this property.

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



Persistence Layer Objects
==========================

*module* multirunnable.persistence.database.operator

It's a DAO (Database Access Object) role to let client site operating database.
It annotates some templated methods which could be used directly by subclass.
So the business logic which related with SQL should be implemented here but never
implement any operator detail with database like how to execute SQL or fetch data row.

BaseDao
--------

*class* multirunnable.persistence.database.layer.\ **BaseDao**\ *()*
    The base class to let all subclass to inherit it.

*abstractmethod* **database_opt**\ *()*
    Return *BaseDatabaseOperator* type instance to let template methods to use it.
    It's an abstracted method so developers should implement what *BaseDatabaseOperator* type instance it returns.

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

**close**\ *()*
    Close the database cursor instance.



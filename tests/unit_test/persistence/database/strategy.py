import traceback
import pytest
import re

from multirunnable.persistence.database.strategy import get_connection_pool, database_connection_pools, Globalize
from multirunnable.exceptions import GlobalizeObjectError
from multirunnable import set_mode, RunningMode

from ....test_config import (
    Under_Test_RunningModes, Test_Pool_Name, Test_Pool_Size, database_host, Database_Config, Database_Pool_Config,
    SELECT_TEST_DATA_SQL, INSERT_TEST_DATA_SQL, DELETE_TEST_DATA_SQL
)
from ._test_db_implement import MySQLSingleConnection, MySQLDriverConnectionPool, ErrorConfigConnectionPool



@pytest.fixture(scope="function")
def single_connection_strategy():
    return MySQLSingleConnection(**Database_Config)


@pytest.fixture(scope="function")
def connection_pool_strategy():
    return MySQLDriverConnectionPool(**Database_Pool_Config)


ErrorConfigConnectionPoolObj = ErrorConfigConnectionPool
ErrorConfigConnectionPoolInstance: ErrorConfigConnectionPool = None


def _select_data(_cursor) -> list:
    _cursor.execute(SELECT_TEST_DATA_SQL)
    _data = _cursor.fetchall()
    return _data



class TestPersistenceDatabaseOneConnection:

    def test_repr(self, single_connection_strategy: MySQLSingleConnection):
        _strategy_inst_repr = repr(single_connection_strategy)
        _chksum = re.search(
            re.escape(single_connection_strategy.__class__.__name__) +
            r"\(" + re.escape(str(single_connection_strategy.database_config)) + r"\)" ,
            str(_strategy_inst_repr))

        assert _chksum is not None, "The __repr__ info should be map to the format."


    def test_connect_database(self, single_connection_strategy: MySQLSingleConnection):
        # _connection = single_connection_strategy.current_connection
        _connection = single_connection_strategy.get_one_connection()
        assert _connection is not None, "It should return a database connection instance."
        assert single_connection_strategy.is_connected() is True, "The connection instance should be connected."
        assert _connection.is_connected() is True, "The connection instance should be connected."

        _get_connection = single_connection_strategy.get_one_connection()
        assert _get_connection is _connection is not None, "These values should be the same."


    def test_database_config(self, single_connection_strategy: MySQLSingleConnection):
        _db_config = single_connection_strategy.database_config
        assert _db_config == Database_Config, "It should return the database configuration back to us which we set."


    def test_update_database_config(self, single_connection_strategy: MySQLSingleConnection):
        single_connection_strategy.update_database_config(key="host", value="localhost")
        assert "host" in single_connection_strategy.database_config.keys(), "The key 'host' should be set in keys of database configuration."
        assert "localhost" in single_connection_strategy.database_config.values(), "The value of key 'host' should be 'localhost'."
        single_connection_strategy.update_database_config(key="host", value=database_host)


    def test_reconnect(self, single_connection_strategy: MySQLSingleConnection):
        single_connection_strategy.close_connection()

        try:
            single_connection_strategy.update_database_config(key="host", value="1.1.1.1")
            try:
                _connection = single_connection_strategy.reconnect(timeout=1)
            except ConnectionError as ce:
                assert "It's timeout to retry" in str(ce) and "Cannot reconnect to database" in str(ce), "It should raise an exception about retry timeout."
            except Exception as ce:
                assert "Can't connect to MySQL server on '1.1.1.1:3306'" in str(ce), "It should raise some exceptions which be annotated by database package."
            else:
                assert False, "It should raise something exceptions because the IP is invalid."

        except Exception as e:
            raise e

        finally:
            single_connection_strategy.update_database_config(key="host", value=database_host)

        _connection = single_connection_strategy.reconnect()
        assert _connection is not None, "It should return a database connection instance."


    def test_commit(self, single_connection_strategy: MySQLSingleConnection):
        # # Insert data but doesn't commit it and close cursor and connection.
        _connection = single_connection_strategy.connect_database()
        _connection = single_connection_strategy.current_connection
        _cursor = _connection.cursor()

        TestPersistenceDatabaseOneConnection._insert_data(cursor=_cursor, commit=False)
        TestPersistenceDatabaseOneConnection._close_instance(_strategy=single_connection_strategy, _cursor=_cursor)

        # # Select data to check. Insert data and commit it.
        _new_connection = single_connection_strategy.reconnect()
        _new_cursor = _new_connection.cursor()

        _data = _select_data(_cursor=_new_cursor)
        assert _data == [], "It should get an empty dataset right now."
        TestPersistenceDatabaseOneConnection._insert_data(cursor=_new_cursor, commit=True, connection_strategy=single_connection_strategy)
        TestPersistenceDatabaseOneConnection._close_instance(_strategy=single_connection_strategy, _cursor=_new_cursor)

        # # Select data to check. Delete testing data and commit it.
        _latest_connection = single_connection_strategy.reconnect()
        _latest_cursor = _latest_connection.cursor()

        _data = _select_data(_cursor=_latest_cursor)
        assert _data != [] and len(_data) == 1, "It should get an empty dataset right now."
        TestPersistenceDatabaseOneConnection._delete_data(cursor=_latest_cursor, connection_strategy=single_connection_strategy)
        TestPersistenceDatabaseOneConnection._close_instance(_strategy=single_connection_strategy, _cursor=_latest_cursor)


    @staticmethod
    def _delete_data(cursor, connection_strategy) -> None:
        cursor.execute(DELETE_TEST_DATA_SQL)
        connection_strategy.commit()
        cursor.execute(SELECT_TEST_DATA_SQL)
        _data = cursor.fetchall()
        assert _data == [], ""


    @staticmethod
    def _insert_data(cursor, commit: bool, connection_strategy=None) -> None:
        cursor.execute(INSERT_TEST_DATA_SQL)

        if commit is True:
            if connection_strategy is None:
                raise ValueError("ConnectionStrategy cannot be empty if option *commit* is True.")
            connection_strategy.commit()


    @staticmethod
    def _close_instance(_strategy: MySQLSingleConnection, _cursor):
        _cursor.close()
        _strategy.close_connection()


    def test_close_connection(self, single_connection_strategy: MySQLSingleConnection):
        _connection = single_connection_strategy.reconnect()
        _is_connected = _connection.is_connected()
        assert _is_connected is True, "The database connection instance should be connected."

        try:
            single_connection_strategy.close_connection()
        except Exception:
            assert False, f"It should close the database connection and cursor instances normally.\n Error: {traceback.format_exc()}"
        else:
            assert True, "It closes the database connection and cursor instances normally."

        _connection = single_connection_strategy.current_connection
        assert _connection is not None, "The database connection instance should not be None object."
        _is_connected = _connection.is_connected()
        assert _is_connected is False, "The database connection instance should be closed."



class TestPersistenceDatabaseConnectionPool:

    def instantiate_with_error_pool_size(self):
        Database_Pool_Config.update({
            "pool_name": "error_pool_size",
            "pool_size": -10
        })
        try:
            ErrorConfigConnectionPoolObj(initial=False, **Database_Pool_Config)
        except ValueError as ve:
            assert "The database connection pool size cannot less than 0" in str(ve), "It should raise an exception about pool size cannot less than 0."
        else:
            assert False, "It should raise an exception about pool size cannot less than 0."


    def test_repr(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _strategy_inst_repr = repr(connection_pool_strategy)
        _chksum = re.search(
            re.escape(connection_pool_strategy.__class__.__name__) +
            r"\(" + re.escape(str(connection_pool_strategy.database_config)) + r"\)" ,
            str(_strategy_inst_repr))

        assert _chksum is not None, "The __repr__ info should be map to the format."


    def test_connect_database(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _conn_pool = get_connection_pool(pool_name=Test_Pool_Name)
        assert _conn_pool is not None, f"It should return a connection pool object back with the pool name {Test_Pool_Name}."
        assert _conn_pool.pool_name == Test_Pool_Name, f"The pool name we get from the connection pool instance should be equal to the name we set '{Test_Pool_Name}' before."
        assert int(_conn_pool.pool_size) == int(Test_Pool_Size), f"The pool size we get from the connection pool instance should be equal to the number we set '{Test_Pool_Size}' before."

        _all_pools = database_connection_pools()
        assert len(_all_pools) != 0, "The length should not be '0' because we only instantiate one database connection pool object."
        assert Test_Pool_Name in _all_pools.keys(), f"The pool name '{Test_Pool_Name} should be in the keys of {_all_pools}.'"
        assert _all_pools[Test_Pool_Name] is _conn_pool, f"The instances '{_all_pools[Test_Pool_Name]}' and '{_conn_pool}' should be the same."


    def test_database_config(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _db_config = connection_pool_strategy.database_config
        assert _db_config == Database_Pool_Config, "It should return the database configuration back to us which we set."


    def test_update_database_config(self, connection_pool_strategy: MySQLDriverConnectionPool):
        connection_pool_strategy.update_database_config(key="host", value="localhost")
        assert "host" in connection_pool_strategy.database_config.keys(), ""
        assert "localhost" in connection_pool_strategy.database_config.values(), ""
        connection_pool_strategy.update_database_config(key="host", value=database_host)


    def test_get_current_pool_name(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _current_pool_name = connection_pool_strategy.current_pool_name
        assert _current_pool_name == Test_Pool_Name, f"It should return the pool name of database configuration back to us which we set '{Test_Pool_Name}'."


    def test_set_current_pool_name(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _test_name = "test_pool_name"
        connection_pool_strategy.current_pool_name = _test_name
        assert connection_pool_strategy.current_pool_name == _test_name, f"It should return the pool name of database configuration back to us which we set '{_test_name}'."
        connection_pool_strategy.current_pool_name = Test_Pool_Name


    def test_get_pool_size(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _pool_size = connection_pool_strategy.pool_size
        assert _pool_size == Test_Pool_Size, f"It should return the pool size of database configuration back to us which we set '{Test_Pool_Size}'."


    def test_get_pool_size_with_zero_size_value(self):
        Database_Pool_Config.update({
            "pool_name": "no_pool_size"
        })
        global ErrorConfigConnectionPoolInstance
        ErrorConfigConnectionPoolInstance = ErrorConfigConnectionPool(pool_name="error_config", initial=False)
        _pool_size = ErrorConfigConnectionPoolInstance.pool_size
        from multiprocessing import cpu_count
        assert _pool_size == cpu_count(), "It should return the pool size which is equal to the count of CPU."


    def test_get_pool_size_with_invalid_value(self):
        global ErrorConfigConnectionPoolInstance
        ErrorConfigConnectionPoolInstance.update_database_config(key="pool_size", value=-10)
        try:
            _pool_size = ErrorConfigConnectionPoolInstance.pool_size
        except ValueError as ve:
            assert "The database connection pool size cannot less than 0" in str(ve), "It should raise an exception about pool size cannot less than 0."
        else:
            assert False, "It should raise an exception about pool size cannot less than 0."


    def test_get_pool_size_with_no_size_value(self):
        global ErrorConfigConnectionPoolInstance
        ErrorConfigConnectionPoolInstance.pool_size = 0
        _pool_size = ErrorConfigConnectionPoolInstance.pool_size
        from multiprocessing import cpu_count
        assert _pool_size == cpu_count(), "It should return the pool size which is equal to the count of CPU."


    def test_get_pool_size_with_exceed_size_value(self):
        global ErrorConfigConnectionPoolInstance
        ErrorConfigConnectionPoolInstance.pool_size = 100
        _pool_size = ErrorConfigConnectionPoolInstance.pool_size
        assert _pool_size == 100, "It should return the pool size which you set but log a warning message."


    def test_set_pool_size(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _test_size = 10
        connection_pool_strategy.pool_size = _test_size
        assert connection_pool_strategy.pool_size == _test_size, f"It should return the pool size of database configuration back to us which we set '{_test_size}'."
        try:
            connection_pool_strategy.pool_size = -10
        except ValueError as ve:
            assert "The database connection pool size cannot less than 0" in str(ve), "It should raise an exception about the pool size value is invalid."
        else:
            assert False, "It should raise an exception about the pool size value is invalid."
        connection_pool_strategy.pool_size = Test_Pool_Size


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_reconnect(self, mode: RunningMode, connection_pool_strategy: MySQLDriverConnectionPool):
        set_mode(mode=mode)

        try:
            connection_pool_strategy.current_pool_name = Test_Pool_Name
            connection_pool_strategy.update_database_config(key="host", value="1.1.1.1")
            connection_pool_strategy.update_database_config(key="port", value=3306)
            try:
                _connection = connection_pool_strategy.reconnect(timeout=1)
            except ConnectionError as ce:
                assert "Cannot reconnect to database" in str(ce), "It should raise an exception about retry timeout."
            except Exception as ce:
                assert "Can't connect to MySQL server on '1.1.1.1:3306'" in str(ce), "It should raise some exceptions which be annotated by database package."
            else:
                assert False, "It should raise something exceptions because the IP is invalid."

        except Exception as e:
            raise e

        finally:
            connection_pool_strategy.update_database_configs(config=Database_Config)

        _connection = connection_pool_strategy.reconnect()
        assert _connection is not None, "It should return a database connection instance."
        connection_pool_strategy.close_connection(conn=_connection)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_get_one_connection(self, mode: RunningMode, connection_pool_strategy: MySQLDriverConnectionPool):
        set_mode(mode=mode)

        _pools = database_connection_pools()

        try:
            _conn = connection_pool_strategy.get_one_connection()
        except ValueError as ce:
            assert "Cannot get the one connection instance from connection pool because it doesn't exist the connection pool with the name" in str(ce), \
                "It should raise an exception about cannot find the connection pool with the target pool name."
        else:
            assert False, "It should find nothing by the pool name ''."

        _conn = connection_pool_strategy.get_one_connection(pool_name=Test_Pool_Name)
        assert _conn is not None, f"It should get a connection instance from the pool with pool name '{Test_Pool_Name}'."
        # # Release connection instance back to pool
        connection_pool_strategy.close_connection(conn=_conn)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_commit(self, mode: RunningMode, connection_pool_strategy: MySQLDriverConnectionPool):
        set_mode(mode=mode)

        # # Insert data but doesn't commit it and close cursor and connection.
        _connection = connection_pool_strategy.get_one_connection(pool_name=Test_Pool_Name)
        _cursor = _connection.cursor()

        TestPersistenceDatabaseConnectionPool._insert_data(conn=_connection, cursor=_cursor, commit=False)
        TestPersistenceDatabaseConnectionPool._close_instance(_strategy=connection_pool_strategy, _conn=_connection, _cursor=_cursor)

        # # Select data to check. Insert data and commit it.
        _new_connection = connection_pool_strategy.reconnect()
        _new_cursor = _new_connection.cursor()

        _data = _select_data(_cursor=_new_cursor)
        assert _data == [], "It should get an empty dataset right now."
        TestPersistenceDatabaseConnectionPool._insert_data(conn=_new_connection, cursor=_new_cursor, commit=True, connection_strategy=connection_pool_strategy)
        TestPersistenceDatabaseConnectionPool._close_instance(_strategy=connection_pool_strategy, _conn=_new_connection, _cursor=_new_cursor)

        # # Select data to check. Delete testing data and commit it.
        _latest_connection = connection_pool_strategy.reconnect()
        _latest_cursor = _latest_connection.cursor()

        _data = _select_data(_cursor=_latest_cursor)
        assert _data != [] and len(_data) == 1, "It should get an empty dataset right now."
        TestPersistenceDatabaseConnectionPool._delete_data(conn=_latest_connection, cursor=_latest_cursor, connection_strategy=connection_pool_strategy)
        TestPersistenceDatabaseConnectionPool._close_instance(_strategy=connection_pool_strategy, _conn=_latest_connection, _cursor=_latest_cursor)


    @staticmethod
    def _delete_data(conn, cursor, connection_strategy) -> None:
        cursor.execute(DELETE_TEST_DATA_SQL)
        connection_strategy.commit(conn=conn)
        cursor.execute(SELECT_TEST_DATA_SQL)
        _data = cursor.fetchall()
        assert _data == [], ""


    @staticmethod
    def _insert_data(conn, cursor, commit: bool, connection_strategy=None) -> None:
        cursor.execute(INSERT_TEST_DATA_SQL)

        if commit is True:
            if connection_strategy is None:
                raise ValueError("ConnectionStrategy cannot be empty if option *commit* is True.")
            connection_strategy.commit(conn=conn)


    @staticmethod
    def _close_instance(_strategy: MySQLDriverConnectionPool, _conn, _cursor):
        _cursor.close()
        _strategy.close_connection(conn=_conn)


    @pytest.mark.parametrize("mode", Under_Test_RunningModes)
    def test_close_connection(self, mode: RunningMode, connection_pool_strategy: MySQLDriverConnectionPool):
        set_mode(mode=mode)

        _conn = connection_pool_strategy.get_one_connection(pool_name=Test_Pool_Name)
        _cursor = _conn.cursor()
        assert _cursor is not None, "It should get the cursor instance without any issue."

        _cursor.close()
        connection_pool_strategy.close_connection(conn=_conn)

        try:
            _cursor = _conn.cursor()
        except AttributeError as ae:
            assert "'NoneType' object has no attribute 'cursor'" in str(ae), ""



class TestGlobalize:

    def test_connection_pool_with_invalid_argument(self):
        try:
            Globalize.connection_pool(name="test", pool=None)
        except GlobalizeObjectError as ge:
            assert str(ge), ""
        else:
            assert False, "It should raise an exception about target object of option *pool* cannot be a None type object."


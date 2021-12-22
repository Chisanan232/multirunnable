from multirunnable.persistence.database.strategy import get_connection_pool

from ...test_config import Test_Pool_Name, Test_Pool_Size,Database_Config, Database_Pool_Config
from ._test_db_implement import MySQLSingleConnection, MySQLDriverConnectionPool

import pytest



@pytest.fixture(scope="function")
def single_connection_strategy():
    return MySQLSingleConnection(**Database_Config)


@pytest.fixture(scope="function")
def connection_pool_strategy():
    Database_Pool_Config.update({
        "pool_name": Test_Pool_Name,
        "pool_size": Test_Pool_Size
    })
    return MySQLDriverConnectionPool(**Database_Pool_Config)


class TestPersistenceDatabaseOneConnection:

    def test_connect_database(self, single_connection_strategy: MySQLSingleConnection):
        _connection = single_connection_strategy.connection
        assert _connection is not None, f"It should return a database connection instance."


    def test_database_config(self, single_connection_strategy: MySQLSingleConnection):
        _db_config = single_connection_strategy.database_config
        assert _db_config == Database_Config, f"It should return the database configuration back to us which we set."


    def test_update_database_config(self, single_connection_strategy: MySQLSingleConnection):
        single_connection_strategy.update_database_config(key="host", value="localhost")
        assert "host" in single_connection_strategy.database_config.keys(), f"The key 'host' should be set in keys of database configuration."
        assert "localhost" in single_connection_strategy.database_config.values(), f"The value of key 'host' should be 'localhost'."


    def test_reconnect(self, single_connection_strategy: MySQLSingleConnection):
        single_connection_strategy.update_database_config(key="host", value="1.1.1.1")
        try:
            _connection = single_connection_strategy.reconnect(timeout=1)
        except ConnectionError as ce:
            assert "It's timeout to retry" in str(ce) and "Cannot reconnect to database" in str(ce), f"It should raise an exception about retry timeout."
        except Exception as ce:
            assert True, f"It should raise some exceptions which be annotated by database package."
        else:
            assert False, f"It should raise something exceptions because the IP is invalid."

        single_connection_strategy.update_database_config(key="host", value="127.0.0.1")
        _connection = single_connection_strategy.reconnect()
        assert _connection is not None, f"It should return a database connection instance."


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_commit(self, single_connection_strategy: MySQLSingleConnection):
        single_connection_strategy.commit()


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_close(self, single_connection_strategy: MySQLSingleConnection):
        try:
            single_connection_strategy.close()
        except Exception as e:
            assert False, f"It should close the database connection and cursor instances normally."
        else:
            assert True, f"It closes the database connection and cursor instances normally."



class TestPersistenceDatabaseConnectionPool:

    def test_connect_database(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _conn_pool = get_connection_pool(pool_name=Test_Pool_Name)
        assert _conn_pool is not None, f"It should return a connection pool object back with the pool name {Test_Pool_Name}."
        assert _conn_pool.pool_name == Test_Pool_Name, f"The pool name we get from the connection pool instance should be equal to the name we set '{Test_Pool_Name}' before."
        assert int(_conn_pool.pool_size) == int(Test_Pool_Size), f"The pool size we get from the connection pool instance should be equal to the number we set '{Test_Pool_Size}' before."


    def test_database_config(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _db_config = connection_pool_strategy.database_config
        assert _db_config == Database_Pool_Config, f"It should return the database configuration back to us which we set."


    def test_update_database_config(self, connection_pool_strategy: MySQLDriverConnectionPool):
        connection_pool_strategy.update_database_config(key="host", value="localhost")
        assert "host" in connection_pool_strategy.database_config.keys(), f""
        assert "localhost" in connection_pool_strategy.database_config.values(), f""


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


    def test_set_pool_size(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _test_size = 10
        connection_pool_strategy.pool_size = _test_size
        assert connection_pool_strategy.pool_size == _test_size, f"It should return the pool size of database configuration back to us which we set '{_test_size}'."
        try:
            connection_pool_strategy.pool_size = -10
        except ValueError as ve:
            assert "The database connection pool size cannot less than 0" in str(ve), f"It should raise an exception about the pool size value is invalid."
        else:
            assert False, f"It should raise an exception about the pool size value is invalid."
        connection_pool_strategy.pool_size = Test_Pool_Size


    def test_reconnect(self, connection_pool_strategy: MySQLDriverConnectionPool):
        connection_pool_strategy.update_database_config(key="host", value="1.1.1.1")
        try:
            _connection = connection_pool_strategy.reconnect(timeout=1)
        except ConnectionError as ce:
            assert "Cannot reconnect to database" in str(ce), f"It should raise an exception about retry timeout."
        except Exception as ce:
            assert True, f"It should raise some exceptions which be annotated by database package."
        else:
            assert False, f"It should raise something exceptions because the IP is invalid."

        connection_pool_strategy.update_database_config(key="host", value="127.0.0.1")
        _connection = connection_pool_strategy.reconnect()
        assert _connection is not None, f"It should return a database connection instance."


    def test_get_one_connection(self, connection_pool_strategy: MySQLDriverConnectionPool):
        try:
            _conn = connection_pool_strategy.get_one_connection()
        except ConnectionError as ce:
            assert "Cannot get the one connection instance from connection pool because it doesn't exist the connection pool with the name" in str(ce), \
                f"It should raise an exception about cannot find the connection pool with the target pool name."
        else:
            assert False, f"It should find nothing by the pool name ''."

        _conn = connection_pool_strategy.get_one_connection(pool_name=Test_Pool_Name)
        assert _conn is not None, f"It should get a connection instance from the pool with pool name '{Test_Pool_Name}'."


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_commit(self, connection_pool_strategy: MySQLDriverConnectionPool):
        connection_pool_strategy.commit()


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_close(self, connection_pool_strategy: MySQLDriverConnectionPool):
        _conn = connection_pool_strategy.get_one_connection(pool_name=Test_Pool_Name)
        connection_pool_strategy.current_pool_name = Test_Pool_Name
        connection_pool_strategy.close()


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_close_pool(self, connection_pool_strategy: MySQLDriverConnectionPool):
        # connection_pool_strategy.current_pool_name = Test_Pool_Name
        connection_pool_strategy.close_pool()


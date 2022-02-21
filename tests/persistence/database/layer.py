from multirunnable.persistence.database.layer import BaseDao

from ...test_config import Test_Pool_Name, Test_Pool_Size,Database_Config, Database_Pool_Config
from ._test_db_implement import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator

import traceback
import pytest


_Data_Row_Number = 3
_Test_SQL_Fetch_Size = 2
_Test_SQL = f"select * from stock_data_2330 limit {_Data_Row_Number};"


class TargetSingleDao(BaseDao):

    def _instantiate_strategy(self) -> MySQLSingleConnection:
        _strategy = MySQLSingleConnection(**Database_Config)
        return _strategy


    def _instantiate_database_opts(self, strategy: MySQLSingleConnection) -> MySQLOperator:
        return MySQLOperator(conn_strategy=strategy)



class TargetPoolDao(BaseDao):

    def _instantiate_strategy(self) -> MySQLDriverConnectionPool:
        Database_Pool_Config.update({
            "pool_name": Test_Pool_Name,
            "pool_size": Test_Pool_Size
        })
        _strategy = MySQLDriverConnectionPool(**Database_Pool_Config)
        _strategy.current_pool_name = Test_Pool_Name
        return _strategy


    def _instantiate_database_opts(self, strategy: MySQLDriverConnectionPool) -> MySQLOperator:
        return MySQLOperator(conn_strategy=strategy)


@pytest.fixture(scope="function")
def db_opt_single() -> TargetSingleDao:
    return TargetSingleDao()


@pytest.fixture(scope="function")
def db_opt_pool() -> TargetPoolDao:
    return TargetPoolDao()


class TestDaoWithSingleConnection:

    def test_database_opt(self, db_opt_single: TargetSingleDao):
        _db_opt = db_opt_single.database_opts
        assert isinstance(_db_opt, MySQLOperator) is True, "The return value we get should be an object which is sub-instance of 'MySQLOperator'."


    def test__instantiate_strategy(self, db_opt_single: TargetSingleDao):
        _db_conn_strategy = db_opt_single._instantiate_strategy()
        assert isinstance(_db_conn_strategy, MySQLSingleConnection) is True, "The return value we get should be an object which is sub-instance of 'MySQLSingleConnection'."


    def test__instantiate_database_opts(self, db_opt_single: TargetSingleDao):
        _db_conn_strategy = db_opt_single._instantiate_strategy()
        _db_opt = db_opt_single._instantiate_database_opts(strategy=_db_conn_strategy)
        assert isinstance(_db_opt, MySQLOperator) is True, "The return value we get should be an object which is sub-instance of 'MySQLOperator'."


    def test_reconnect(self, db_opt_single: TargetSingleDao):
        _opts = db_opt_single.database_opts
        assert _opts is not None, "This step to ensure that the protected variable '_Database_Connection_Strategy' is not None."

        _conn_opts = getattr(db_opt_single, "_Database_Opts_Instance")
        _db_connection = getattr(_conn_opts, "_connection")
        _db_cursor = getattr(_conn_opts, "_cursor")
        assert _db_connection is not None, "Database connection instance should not be None."
        assert _db_cursor is not None, "Database cursor instance should not be None."

        _db_connection_id = id(_db_connection)
        _db_cursor_id = id(_db_cursor)

        db_opt_single.reconnect()

        _new_db_connection = getattr(_conn_opts, "_connection")
        _new_db_cursor = getattr(_conn_opts, "_cursor")
        assert _new_db_connection is not None, "Database connection instance should not be None."
        assert _new_db_cursor is not None, "Database cursor instance should not be None."

        _new_db_connection_id = id(_new_db_connection)
        _new_db_cursor_id = id(_new_db_cursor)

        assert _db_connection_id != _new_db_connection_id, "The memory store places of database connection instance should be different."
        assert _db_cursor_id != _new_db_cursor_id, "The memory store places of database cursor instance should be different."


    def test_commit(self, db_opt_single: TargetSingleDao):
        try:
            db_opt_single.commit()
        except Exception as e:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It works finely."


    def test_execute(self, db_opt_single: TargetSingleDao):
        try:
            db_opt_single.execute(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely!"

        _data = db_opt_single.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_execute_many(self, db_opt_single: TargetSingleDao):
        try:
            db_opt_single.execute_many(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely!"


    def test_fetch_one(self, db_opt_single: TargetSingleDao):
        _row_number = 0

        db_opt_single.execute(_Test_SQL)
        _data = db_opt_single.fetch_one()
        assert _data is not None and _data != [], "It should get the data row (only one) from the cursor instance with target SQL."
        _row_number += 1

        while _data is not None or _data != []:
            _data = db_opt_single.fetch_one()
            if _row_number == _Data_Row_Number and (_data == [] or _data is None):
                break
            _row_number += 1

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_many(self, db_opt_single: TargetSingleDao):
        _row_number = 0

        db_opt_single.execute(_Test_SQL)
        _data = db_opt_single.fetch_many(size=_Test_SQL_Fetch_Size)
        assert _data is not None and _data != [], f"It should get the data row (row number as '{_Test_SQL_Fetch_Size}') from the cursor instance with target SQL."
        if _Test_SQL_Fetch_Size < _Data_Row_Number and _Data_Row_Number > 1:
            assert len(_data) < _Data_Row_Number and len(_data) == _Test_SQL_Fetch_Size, "The data row number should be equal to fetch size and less than the limit data row number."
        _row_number += len(_data)

        while _data is not None or _data != []:
            _data = db_opt_single.fetch_many(size=_Test_SQL_Fetch_Size)
            if _row_number == _Data_Row_Number and _data == []:
                break
            _row_number += len(_data)

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_all(self, db_opt_single: TargetSingleDao):
        db_opt_single.execute(_Test_SQL)
        _data = db_opt_single.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_close_cursor(self, db_opt_single: TargetSingleDao):
        db_opt_single.close_cursor()

        try:
            db_opt_single.execute(_Test_SQL)
        except Exception as e:
            assert "Cursor is not connected" in str(e), "It should raise an exception about cursor is not connected."


    def test_close_connection(self, db_opt_single: TargetSingleDao):
        db_opt_single.close_connection()

        try:
            db_opt_single.execute(_Test_SQL)
        except Exception as e:
            assert "Lost connection to MySQL server at '127.0.0.1:3306', system error: 9 Bad file descriptor" in str(e), "It should raise an exception about it lose connection."



class TestDaoWithConnectionPool:

    def test_database_opt(self, db_opt_pool: TargetPoolDao):
        _db_opt = db_opt_pool.database_opts
        assert isinstance(_db_opt, MySQLOperator) is True, "The return value we get should be an object which is sub-instance of 'MySQLOperator'."


    def test__instantiate_strategy(self, db_opt_pool: TargetPoolDao):
        _db_conn_strategy = db_opt_pool._instantiate_strategy()
        assert isinstance(_db_conn_strategy, MySQLDriverConnectionPool) is True, "The return value we get should be an object which is sub-instance of 'MySQLDriverConnectionPool'."


    def test__instantiate_database_opts(self, db_opt_pool: TargetPoolDao):
        _db_conn_strategy = db_opt_pool._instantiate_strategy()
        _db_opt = db_opt_pool._instantiate_database_opts(strategy=_db_conn_strategy)
        assert isinstance(_db_opt, MySQLOperator) is True, "The return value we get should be an object which is sub-instance of 'MySQLOperator'."


    def test_reconnect(self, db_opt_pool: TargetPoolDao):
        _opts = db_opt_pool.database_opts
        assert _opts is not None, "This step to ensure that the protected variable '_Database_Connection_Strategy' is not None."

        _conn_opts = getattr(db_opt_pool, "_Database_Opts_Instance")
        _db_connection = getattr(_conn_opts, "_connection")
        _db_cursor = getattr(_conn_opts, "_cursor")
        assert _db_connection is not None, "Database connection instance should not be None."
        assert _db_cursor is not None, "Database cursor instance should not be None."

        _db_connection_id = id(_db_connection)
        _db_cursor_id = id(_db_cursor)

        db_opt_pool.reconnect()

        _new_db_connection = getattr(_conn_opts, "_connection")
        _new_db_cursor = getattr(_conn_opts, "_cursor")
        assert _new_db_connection is not None, "Database connection instance should not be None."
        assert _new_db_cursor is not None, "Database cursor instance should not be None."

        _new_db_connection_id = id(_new_db_connection)
        _new_db_cursor_id = id(_new_db_cursor)

        assert _db_connection_id != _new_db_connection_id, "The memory store places of database connection instance should be different."
        assert _db_cursor_id != _new_db_cursor_id, "The memory store places of database cursor instance should be different."


    def test_commit(self, db_opt_pool: TargetSingleDao):
        try:
            db_opt_pool.commit()
        except Exception as e:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It works finely."


    def test_execute(self, db_opt_pool: TargetPoolDao):
        try:
            db_opt_pool.execute(_Test_SQL)
        except Exception as e:
            assert False, ""
        else:
            assert True, ""


    def test_execute_many(self, db_opt_pool: TargetPoolDao):
        try:
            db_opt_pool.execute_many(_Test_SQL)
        except Exception as e:
            assert False, ""
        else:
            assert True, ""


    def test_fetch_one(self, db_opt_pool: TargetPoolDao):
        _row_number = 0

        db_opt_pool.execute(_Test_SQL)
        _data = db_opt_pool.fetch_one()
        assert _data is not None and _data != [], "It should get the data row (only one) from the cursor instance with target SQL."
        _row_number += 1

        while _data is not None or _data != []:
            _data = db_opt_pool.fetch_one()
            if _row_number == _Data_Row_Number and (_data == [] or _data is None):
                break
            _row_number += 1

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_many(self, db_opt_pool: TargetPoolDao):
        _row_number = 0

        db_opt_pool.execute(_Test_SQL)
        _data = db_opt_pool.fetch_many(size=_Test_SQL_Fetch_Size)
        assert _data is not None and _data != [], f"It should get the data row (row number as '{_Test_SQL_Fetch_Size}') from the cursor instance with target SQL."
        if _Test_SQL_Fetch_Size < _Data_Row_Number and _Data_Row_Number > 1:
            assert len(_data) < _Data_Row_Number and len(_data) == _Test_SQL_Fetch_Size, "The data row number should be equal to fetch size and less than the limit data row number."
        _row_number += len(_data)

        while _data is not None or _data != []:
            _data = db_opt_pool.fetch_many(size=_Test_SQL_Fetch_Size)
            if _row_number == _Data_Row_Number and _data == []:
                break
            _row_number += len(_data)

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_all(self, db_opt_pool: TargetPoolDao):
        db_opt_pool.execute(_Test_SQL)
        _data = db_opt_pool.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_close_cursor(self, db_opt_pool: TargetPoolDao):
        db_opt_pool.close_cursor()

        try:
            db_opt_pool.execute(_Test_SQL)
        except Exception as e:
            assert "Cursor is not connected" in str(e), "It should raise an exception about cursor is not connected."


    def test_close_connection(self, db_opt_pool: TargetPoolDao):
        db_opt_pool.close_connection()

        try:
            db_opt_pool.execute(_Test_SQL)
        except Exception as e:
            assert "MySQL Connection not available." in str(e), "It should raise an exception about it lose connection."



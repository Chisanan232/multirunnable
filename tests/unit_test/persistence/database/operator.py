import traceback
import datetime
import pytest

from multirunnable import set_mode

from ....test_config import (
    Under_Test_RunningModes, Under_Test_RunningModes_Without_Greenlet, Database_Config, Database_Pool_Config,
    Table_Columns, TEST_DATA_ROWS, SELECT_TEST_DATA_SQL_WITH_OPTION, INSERT_TEST_DATA_SQL_WITH_OPTION, DELETE_TEST_DATA_SQL_WITH_OPTION
)
from ._test_db_implement import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator


_Single_Strategy: MySQLSingleConnection
_Pool_Strategy: MySQLDriverConnectionPool

_Data_Row_Number = 3
_Fetch_Size = 2
_Test_SQL = f"select * from stock_data_2330 limit {_Data_Row_Number};"


@pytest.fixture(scope="function")
def opts_with_single_conn_strategy() -> MySQLOperator:
    global _Single_Strategy
    _Single_Strategy = MySQLSingleConnection(initial=False, **Database_Config)
    return MySQLOperator(conn_strategy=_Single_Strategy, db_config=Database_Config)



@pytest.fixture(scope="function")
def opts_with_conn_pool_strategy(request) -> MySQLOperator:
    global _Pool_Strategy
    _Pool_Strategy = MySQLDriverConnectionPool(initial=False, **Database_Pool_Config)

    set_mode(mode=request.param)

    return MySQLOperator(conn_strategy=_Pool_Strategy, db_config=Database_Pool_Config)



class TestPersistenceDatabaseOperatorWithSingleConnection:

    def test__connection(self, opts_with_single_conn_strategy: MySQLOperator):
        assert opts_with_single_conn_strategy._connection is _Single_Strategy.current_connection, "For SingleConnection strategy, it shuold initial a database connection instance after we instantiate it."
        assert opts_with_single_conn_strategy._connection is _Single_Strategy.current_connection, "For SingleConnection strategy, it shuold initial a database connection instance after we instantiate it."

        setattr(opts_with_single_conn_strategy, "_db_connection", None)
        assert opts_with_single_conn_strategy._connection is not None, "The database connection should be instantiate."


    def test_initial_cursor(self, opts_with_single_conn_strategy: MySQLOperator):
        _conn = opts_with_single_conn_strategy._db_connection
        _cursor = opts_with_single_conn_strategy.initial_cursor(connection=_conn)
        assert _cursor is not None, "For SingleConnection strategy, it shuold initial a database cursor instance after we instantiate strategy."


    def test__cursor(self, opts_with_single_conn_strategy: MySQLOperator):
        assert opts_with_single_conn_strategy._cursor is not None, "For SingleConnection strategy, it shuold initial a database cursor instance when we call the '_cursor' property."

        setattr(opts_with_single_conn_strategy, "_db_cursor", None)
        assert opts_with_single_conn_strategy._cursor is not None, "The database connection should be instantiate."


    def test_reconnect(self, opts_with_single_conn_strategy: MySQLOperator):
        _db_connection = getattr(opts_with_single_conn_strategy, "_db_connection")
        _db_cursor = getattr(opts_with_single_conn_strategy, "_db_cursor")
        assert _db_connection is not None, "Database connection instance should not be None."
        assert _db_cursor is not None, "Database cursor instance should not be None."

        _db_connection_id = id(_db_connection)
        _db_cursor_id = id(_db_cursor)

        opts_with_single_conn_strategy.reconnect(force=True)

        _new_db_connection = getattr(opts_with_single_conn_strategy, "_db_connection")
        _new_db_cursor = getattr(opts_with_single_conn_strategy, "_db_cursor")
        assert _new_db_connection is not None, "Database connection instance should not be None."
        assert _new_db_cursor is not None, "Database cursor instance should not be None."

        _new_db_connection_id = id(_new_db_connection)
        _new_db_cursor_id = id(_new_db_cursor)

        assert _db_connection_id != _new_db_connection_id, "The memory store places of database connection instance should be different."
        assert _db_cursor_id != _new_db_cursor_id, "The memory store places of database cursor instance should be different."


    def test_commit(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.commit()
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It works finely."


    def test_column_names(self, opts_with_single_conn_strategy: MySQLOperator):
        opts_with_single_conn_strategy.execute(_Test_SQL)
        _column_names = opts_with_single_conn_strategy.column_names
        assert _column_names == Table_Columns, \
            f"These collections which saves column names should be the same. It should be like {Table_Columns}, but we got {_column_names}."


    def test_row_count(self, opts_with_single_conn_strategy: MySQLOperator):
        opts_with_single_conn_strategy.execute(_Test_SQL)
        _row_count = opts_with_single_conn_strategy.row_count
        assert _row_count == _Data_Row_Number, f"The data rows count should be {_Data_Row_Number}. But we got {_row_count}."


    def test_execute(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.execute(_Test_SQL)
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely!"

        _data = opts_with_single_conn_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_execute_many(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.execute_many(INSERT_TEST_DATA_SQL_WITH_OPTION, TEST_DATA_ROWS)
            opts_with_single_conn_strategy.commit()
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely!"

        opts_with_single_conn_strategy.execute(SELECT_TEST_DATA_SQL_WITH_OPTION)
        _data = opts_with_single_conn_strategy.fetch_all()
        assert _data is not None and len(_data) == len(TEST_DATA_ROWS), f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."
        try:
            for _datarow, testing_datarow in zip(_data, TEST_DATA_ROWS):
                for _d, _td in zip(_datarow, testing_datarow):
                    if isinstance(_d, datetime.datetime):
                        _datetime = datetime.datetime.strptime(_td, '%Y-%m-%d %H:%M:%S')
                        assert _d == _datetime, "Datetime value should be the same."
                    elif isinstance(_d, str):
                        assert _d == str(_td), "String value should be the same."
                    else:
                        assert float(_d) == float(_td), "Float value should be the same."
        finally:
            opts_with_single_conn_strategy.execute(DELETE_TEST_DATA_SQL_WITH_OPTION)
            opts_with_single_conn_strategy.commit()


    def test_fetch_one(self, opts_with_single_conn_strategy: MySQLOperator):
        _row_number = 0

        opts_with_single_conn_strategy.execute(_Test_SQL)
        _data = opts_with_single_conn_strategy.fetch_one()
        assert _data is not None and _data != [], "It should get the data row (only one) from the cursor instance with target SQL."
        _row_number += 1

        while _data is not None or _data != []:
            _data = opts_with_single_conn_strategy.fetch_one()
            if _row_number == _Data_Row_Number and (_data == [] or _data is None):
                break
            _row_number += 1

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_many(self, opts_with_single_conn_strategy: MySQLOperator):
        _row_number = 0

        opts_with_single_conn_strategy.execute(_Test_SQL)
        _data = opts_with_single_conn_strategy.fetch_many(size=_Fetch_Size)
        assert _data is not None and _data != [], f"It should get the data row (row number as '{_Fetch_Size}') from the cursor instance with target SQL."
        if _Fetch_Size < _Data_Row_Number and _Data_Row_Number > 1:
            assert len(_data) < _Data_Row_Number and len(_data) == _Fetch_Size, "The data row number should be equal to fetch size and less than the limit data row number."
        _row_number += len(_data)

        while _data is not None or _data != []:
            _data = opts_with_single_conn_strategy.fetch_many(size=_Fetch_Size)
            if _row_number == _Data_Row_Number and _data == []:
                break
            _row_number += len(_data)

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_all(self, opts_with_single_conn_strategy: MySQLOperator):
        opts_with_single_conn_strategy.execute(_Test_SQL)
        _data = opts_with_single_conn_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_close_cursor(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.close_cursor()
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely."

        _cursor = getattr(opts_with_single_conn_strategy, "_db_cursor")
        assert _cursor is not None, "Cursor just be closed but instance should be still exist."
        try:
            opts_with_single_conn_strategy.execute(_Test_SQL)
        except Exception as e:
            assert "Cursor is not connected" in str(e), "It should raise an exception about cursor is not connected."
        else:
            assert False, "It should raise an exception about cursor is not connected."


    def test_close_connection(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.close_connection()
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely."

        _db_connection = opts_with_single_conn_strategy._connection
        assert _db_connection is not None, ""
        _is_connected = _db_connection.is_connected()
        assert _is_connected is False, ""



class TestPersistenceDatabaseOperatorWithConnectionPool:

    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes_Without_Greenlet,
        indirect=True
    )
    def test__connection(self, opts_with_conn_pool_strategy: MySQLOperator):
        assert opts_with_conn_pool_strategy._connection is not None, "The database connection should be instantiate."
        assert opts_with_conn_pool_strategy._connection is _Pool_Strategy.current_connection, "For PoolConnection strategy, it shuold initial a database connection instance after we instantiate it."

        opts_with_conn_pool_strategy.close_connection()
        setattr(opts_with_conn_pool_strategy, "_db_connection", None)
        assert opts_with_conn_pool_strategy._connection is not None, "The database connection should be instantiate."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test__cursor(self, opts_with_conn_pool_strategy: MySQLOperator):
        assert opts_with_conn_pool_strategy._cursor is not None, "The database cursor should be instantiate."

        setattr(opts_with_conn_pool_strategy, "_db_cursor", None)
        assert opts_with_conn_pool_strategy._cursor is not None, "The database cursor should be instantiate."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_reconnect(self, opts_with_conn_pool_strategy: MySQLOperator):
        _db_connection = getattr(opts_with_conn_pool_strategy, "_db_connection")
        _db_cursor = getattr(opts_with_conn_pool_strategy, "_db_cursor")
        assert _db_connection is not None, "Database connection instance should not be None."
        assert _db_cursor is not None, "Database cursor instance should not be None."

        _db_connection_id = id(_db_connection)
        _db_cursor_id = id(_db_cursor)

        opts_with_conn_pool_strategy.reconnect(force=True)

        _new_db_connection = getattr(opts_with_conn_pool_strategy, "_db_connection")
        _new_db_cursor = getattr(opts_with_conn_pool_strategy, "_db_cursor")
        assert _new_db_connection is not None, "Database connection instance should not be None."
        assert _new_db_cursor is not None, "Database cursor instance should not be None."

        _new_db_connection_id = id(_new_db_connection)
        _new_db_cursor_id = id(_new_db_cursor)

        assert _db_connection_id != _new_db_connection_id, "The memory store places of database connection instance should be different."
        assert _db_cursor_id != _new_db_cursor_id, "The memory store places of database cursor instance should be different."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_commit(self, opts_with_conn_pool_strategy: MySQLOperator):
        _db_connection = getattr(opts_with_conn_pool_strategy, "_db_connection")
        try:
            opts_with_conn_pool_strategy.commit(conn=_db_connection)
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It works finely."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_commit_without_option(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.commit()
        except ValueError as ve:
            assert "Option *conn* cannot be None object if connection strategy is BaseConnectionPool type" in str(ve), "It should raise an exception about option *conn* cannot be None type."
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It still could work finely even it works with option *conn* as a None type."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_column_names(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _column_names = opts_with_conn_pool_strategy.column_names
        assert _column_names == Table_Columns, \
            f"These collections which saves column names should be the same. It should be like {Table_Columns}, but we got {_column_names}."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_row_count(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _row_count = opts_with_conn_pool_strategy.row_count
        assert _row_count == _Data_Row_Number, f"The data rows count should be {_Data_Row_Number}. But we got {_row_count}."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_execute(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.execute(_Test_SQL)
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely!"

        _data = opts_with_conn_pool_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_execute_many(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.execute_many(INSERT_TEST_DATA_SQL_WITH_OPTION, TEST_DATA_ROWS)
            opts_with_conn_pool_strategy.commit()
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely!"

        opts_with_conn_pool_strategy.execute(SELECT_TEST_DATA_SQL_WITH_OPTION)
        _data = opts_with_conn_pool_strategy.fetch_all()
        assert _data is not None and len(_data) == len(TEST_DATA_ROWS), f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."
        try:
            for _datarow, testing_datarow in zip(_data, TEST_DATA_ROWS):
                for _d, _td in zip(_datarow, testing_datarow):
                    if isinstance(_d, datetime.datetime):
                        _datetime = datetime.datetime.strptime(_td, '%Y-%m-%d %H:%M:%S')
                        assert _d == _datetime, "Datetime value should be the same."
                    elif isinstance(_d, str):
                        assert _d == str(_td), "String value should be the same."
                    else:
                        assert float(_d) == float(_td), "Float value should be the same."
        finally:
            opts_with_conn_pool_strategy.execute(DELETE_TEST_DATA_SQL_WITH_OPTION)
            opts_with_conn_pool_strategy.commit()


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_fetch_one(self, opts_with_conn_pool_strategy: MySQLOperator):
        _row_number = 0

        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch_one()
        assert _data is not None and _data != [], "It should get the data row (only one) from the cursor instance with target SQL."
        _row_number += 1

        while _data is not None or _data != []:
            _data = opts_with_conn_pool_strategy.fetch_one()
            if _row_number == _Data_Row_Number and (_data == [] or _data is None):
                break
            _row_number += 1

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_fetch_many(self, opts_with_conn_pool_strategy: MySQLOperator):
        _row_number = 0

        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch_many(size=_Fetch_Size)
        assert _data is not None and _data != [], f"It should get the data row (row number as '{_Fetch_Size}') from the cursor instance with target SQL."
        if _Fetch_Size < _Data_Row_Number and _Data_Row_Number > 1:
            assert len(_data) < _Data_Row_Number and len(_data) == _Fetch_Size, "The data row number should be equal to fetch size and less than the limit data row number."
        _row_number += len(_data)

        while _data is not None or _data != []:
            _data = opts_with_conn_pool_strategy.fetch_many(size=_Fetch_Size)
            if _row_number == _Data_Row_Number and _data == []:
                break
            _row_number += len(_data)

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_fetch_all(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_close_cursor(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.close_cursor()
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely."

        _cursor = getattr(opts_with_conn_pool_strategy, "_db_cursor")
        assert _cursor is not None, "Cursor just be closed but instance should be still exist."
        try:
            opts_with_conn_pool_strategy.execute(_Test_SQL)
        except Exception as e:
            assert f"Cursor is not connected" in str(e), "It should raise an exception about cursor is not connected. \nThe exception message is {traceback.format_exc()}"
        else:
            assert False, "It should raise an exception about cursor is not connected."


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_close_connection(self, opts_with_conn_pool_strategy: MySQLOperator):
        _db_connection = getattr(opts_with_conn_pool_strategy, "_db_connection")
        try:
            opts_with_conn_pool_strategy.close_connection(conn=_db_connection)
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It work finely."

        try:
            _cursor = _db_connection.cursor()
        except AttributeError as ae:
            assert "'NoneType' object has no attribute 'cursor'" in str(ae), f""


    @pytest.mark.parametrize(
        argnames="opts_with_conn_pool_strategy",
        argvalues=Under_Test_RunningModes,
        indirect=True
    )
    def test_close_connection_without_option(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.close_connection()
        except ValueError as ve:
            assert "Option *conn* cannot be None object if connection strategy is BaseConnectionPool type" in str(ve), "It should raise an exception about option *conn* cannot be None type."
        except Exception:
            assert False, f"It should work finely without any issue. \nThe exception message is {traceback.format_exc()}"
        else:
            assert True, "It still could work finely even it works with option *conn* as a None type."


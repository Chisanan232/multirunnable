from multirunnable.persistence.database.strategy import database_connection_pools, get_connection_pool

from ...test_config import Test_Pool_Name, Test_Pool_Size,Database_Config, Database_Pool_Config
from ._test_db_implement import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator

import pytest


_Single_Strategy: MySQLSingleConnection
_Pool_Strategy: MySQLDriverConnectionPool

_Data_Row_Number = 3
_Fetch_Size = 2
_Test_SQL = f"select * from stock_data_2330 limit {_Data_Row_Number};"


@pytest.fixture(scope="function")
def opts_with_single_conn_strategy() -> MySQLOperator:
    global _Single_Strategy
    _Single_Strategy = MySQLSingleConnection(**Database_Config)
    return MySQLOperator(conn_strategy=_Single_Strategy)



@pytest.fixture(scope="function")
def opts_with_conn_pool_strategy() -> MySQLOperator:
    global _Pool_Strategy
    Database_Pool_Config.update({
        "pool_name": Test_Pool_Name,
        "pool_size": Test_Pool_Size
    })
    _Pool_Strategy = MySQLDriverConnectionPool(**Database_Pool_Config)
    _Pool_Strategy.current_pool_name = Test_Pool_Name
    return MySQLOperator(conn_strategy=_Pool_Strategy)



class TestPersistenceDatabaseOperatorWithSingleConnection:

    def test__connection(self, opts_with_single_conn_strategy: MySQLOperator):
        assert opts_with_single_conn_strategy._connection is _Single_Strategy.connection, f"For SingleConnection strategy, it shuold initial a database connection instance after we instantiate it."


    def test_initial_cursor(self, opts_with_single_conn_strategy: MySQLOperator):
        _conn = opts_with_single_conn_strategy._db_connection
        _cursor = opts_with_single_conn_strategy.initial_cursor(connection=_conn)
        assert _cursor is not None, f"For SingleConnection strategy, it shuold initial a database cursor instance after we instantiate strategy."


    def test__cursor(self, opts_with_single_conn_strategy: MySQLOperator):
        assert opts_with_single_conn_strategy._db_cursor is not None, f"For SingleConnection strategy, it shuold initial a database cursor instance when we call the '_cursor' property."


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_column_names(self, opts_with_single_conn_strategy: MySQLOperator):
        _column_names = opts_with_single_conn_strategy.column_names


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_row_count(self, opts_with_single_conn_strategy: MySQLOperator):
        _row_count = opts_with_single_conn_strategy.row_count


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_next(self, opts_with_single_conn_strategy: MySQLOperator):
        opts_with_single_conn_strategy.next()


    def test_execute(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.execute(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue."
        else:
            assert True, f"It work finely!"

        _data = opts_with_single_conn_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.skip(reason="Not finish this feature testing yet.")
    def test_execute_many(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.execute_many(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue."
        else:
            assert True, f"It work finely!"

        _data = opts_with_single_conn_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.skip(reason="This feature not support in MySQL of Python library..")
    def test_fetch(self, opts_with_single_conn_strategy: MySQLOperator):
        opts_with_single_conn_strategy.execute(_Test_SQL)
        _data = opts_with_single_conn_strategy.fetch()
        assert _data is not None, f""


    def test_fetch_one(self, opts_with_single_conn_strategy: MySQLOperator):
        _row_number = 0

        opts_with_single_conn_strategy.execute(_Test_SQL)
        _data = opts_with_single_conn_strategy.fetch_one()
        assert _data is not None and _data != [], f"It should get the data row (only one) from the cursor instance with target SQL."
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
            assert len(_data) < _Data_Row_Number and len(_data) == _Fetch_Size, f"The data row number should be equal to fetch size and less than the limit data row number."
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


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_reset(self, opts_with_single_conn_strategy: MySQLOperator):
        opts_with_single_conn_strategy.reset()


    @pytest.mark.skip(reason="For debug the testing code.")
    def test_close(self, opts_with_single_conn_strategy: MySQLOperator):
        try:
            opts_with_single_conn_strategy.close()
        except Exception as e:
            assert False, f""
        else:
            assert True, f""



class TestPersistenceDatabaseOperatorWithConnectionPool:

    def test_initial(self, opts_with_conn_pool_strategy: MySQLOperator):
        _all_conn_pools = database_connection_pools()
        assert _all_conn_pools != {}, f"The database connection pools should not be empty."
        assert Test_Pool_Name in _all_conn_pools.keys(), f"The pool name should be in the database connection pools."
        assert _all_conn_pools[Test_Pool_Name] is not None, f"The database connection pool should exist with the pool name (from database_connection_pools)."
        assert get_connection_pool(pool_name=Test_Pool_Name) is not None, f"The database connection pool should exist with the pool name (from get_connection_pool)."


    def test__connection(self, opts_with_conn_pool_strategy: MySQLOperator):
        assert opts_with_conn_pool_strategy._connection is not None, f"The database connection should be instantiate."


    def test__cursor(self, opts_with_conn_pool_strategy: MySQLOperator):
        assert opts_with_conn_pool_strategy._cursor is not None, f"The database cursor should be instantiate."


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_column_names(self, opts_with_conn_pool_strategy: MySQLOperator):
        _column_names = opts_with_conn_pool_strategy.column_names


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_row_count(self, opts_with_conn_pool_strategy: MySQLOperator):
        _row_count = opts_with_conn_pool_strategy.row_count


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_next(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.next()


    def test_execute(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.execute(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue."
        else:
            assert True, f"It work finely!"

        _data = opts_with_conn_pool_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.skip(reason="Not finish this feature testing yet.")
    def test_execute_many(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.execute_many(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue."
        else:
            assert True, f"It work finely!"

        _data = opts_with_conn_pool_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.skip(reason="This feature not support in MySQL of Python library..")
    def test_fetch(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch()
        assert _data is not None, f""


    def test_fetch_one(self, opts_with_conn_pool_strategy: MySQLOperator):
        _row_number = 0

        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch_one()
        assert _data is not None and _data != [], f"It should get the data row (only one) from the cursor instance with target SQL."
        _row_number += 1

        while _data is not None or _data != []:
            _data = opts_with_conn_pool_strategy.fetch_one()
            if _row_number == _Data_Row_Number and (_data == [] or _data is None):
                break
            _row_number += 1

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_many(self, opts_with_conn_pool_strategy: MySQLOperator):
        _row_number = 0

        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch_many(size=_Fetch_Size)
        assert _data is not None and _data != [], f"It should get the data row (row number as '{_Fetch_Size}') from the cursor instance with target SQL."
        if _Fetch_Size < _Data_Row_Number and _Data_Row_Number > 1:
            assert len(_data) < _Data_Row_Number and len(_data) == _Fetch_Size, f"The data row number should be equal to fetch size and less than the limit data row number."
        _row_number += len(_data)

        while _data is not None or _data != []:
            _data = opts_with_conn_pool_strategy.fetch_many(size=_Fetch_Size)
            if _row_number == _Data_Row_Number and _data == []:
                break
            _row_number += len(_data)

        assert _row_number == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_fetch_all(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.execute(_Test_SQL)
        _data = opts_with_conn_pool_strategy.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    @pytest.mark.skip(reason="Not implement testing logic. Consider about the feature's necessary.")
    def test_reset(self, opts_with_conn_pool_strategy: MySQLOperator):
        opts_with_conn_pool_strategy.reset()


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_close(self, opts_with_conn_pool_strategy: MySQLOperator):
        try:
            opts_with_conn_pool_strategy.close()
        except Exception as e:
            assert False, f""
        else:
            assert True, f""


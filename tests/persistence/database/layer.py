from multirunnable.persistence.database.layer import BaseDao

from ...test_config import Test_Pool_Name, Test_Pool_Size,Database_Config, Database_Pool_Config
from ._test_db_implement import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator

import pytest


_Data_Row_Number = 3
_Test_SQL_Fetch_Size = 2
_Test_SQL = f"select * from stock_data_2330 limit {_Data_Row_Number};"


class TargetSingleDao(BaseDao):

    @property
    def database_opt(self) -> MySQLOperator:
        _strategy = MySQLSingleConnection(**Database_Config)
        return MySQLOperator(conn_strategy=_strategy)



class TargetPoolDao(BaseDao):

    @property
    def database_opt(self) -> MySQLOperator:
        Database_Pool_Config.update({
            "pool_name": Test_Pool_Name,
            "pool_size": Test_Pool_Size
        })
        _strategy = MySQLDriverConnectionPool(**Database_Pool_Config)
        _strategy.current_pool_name = Test_Pool_Name
        return MySQLOperator(conn_strategy=_strategy)


@pytest.fixture(scope="function")
def db_opt_single() -> TargetSingleDao:
    return TargetSingleDao()


@pytest.fixture(scope="function")
def db_opt_pool() -> TargetPoolDao:
    return TargetPoolDao()


class TestDaoWithSingleConnection:

    def test_database_opt(self, db_opt_single: TargetSingleDao):
        _db_opt = db_opt_single.database_opt
        assert isinstance(_db_opt, MySQLOperator) is True, f""


    def test_execute(self, db_opt_single: TargetSingleDao):
        try:
            db_opt_single.execute(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue."
        else:
            assert True, f"It work finely!"

        _data = db_opt_single.fetch_all()
        assert _data is not None and len(_data) == _Data_Row_Number, f"It should get the data from the cursor instance with target SQL and the data row number should be '{_Data_Row_Number}'."


    def test_execute_many(self, db_opt_single: TargetSingleDao):
        try:
            db_opt_single.execute_many(_Test_SQL)
        except Exception as e:
            assert False, f"It should work finely without any issue."
        else:
            assert True, f"It work finely!"


    def test_fetch_one(self, db_opt_single: TargetSingleDao):
        _row_number = 0

        db_opt_single.execute(_Test_SQL)
        _data = db_opt_single.fetch_one()
        assert _data is not None and _data != [], f"It should get the data row (only one) from the cursor instance with target SQL."
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
            assert len(_data) < _Data_Row_Number and len(_data) == _Test_SQL_Fetch_Size, f"The data row number should be equal to fetch size and less than the limit data row number."
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


    @pytest.mark.skip(reason="Avoid for raising an exception about ConnectionError.")
    def test_close(self, db_opt_single: TargetSingleDao):
        db_opt_single.close()



class TestDaoWithConnectionPool:

    def test_database_opt(self, db_opt_pool: TargetPoolDao):
        _db_opt = db_opt_pool.database_opt
        assert isinstance(_db_opt, MySQLOperator) is True, f""


    def test_execute(self, db_opt_pool: TargetPoolDao):
        try:
            db_opt_pool.execute(_Test_SQL)
        except Exception as e:
            assert False, f""
        else:
            assert True, f""


    def test_execute_many(self, db_opt_pool: TargetPoolDao):
        try:
            db_opt_pool.execute_many(_Test_SQL)
        except Exception as e:
            assert False, f""
        else:
            assert True, f""


    def test_fetch_one(self, db_opt_pool: TargetPoolDao):
        _row_number = 0

        db_opt_pool.execute(_Test_SQL)
        _data = db_opt_pool.fetch_one()
        assert _data is not None and _data != [], f"It should get the data row (only one) from the cursor instance with target SQL."
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
            assert len(_data) < _Data_Row_Number and len(_data) == _Test_SQL_Fetch_Size, f"The data row number should be equal to fetch size and less than the limit data row number."
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


    @pytest.mark.skip(reason="Consider this feature testing logic.")
    def test_close(self, db_opt_pool: TargetPoolDao):
        db_opt_pool.close()



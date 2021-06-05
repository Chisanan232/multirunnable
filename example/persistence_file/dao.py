from pyocean.operator import MultiRunnableOperator, AsyncRunnableOperator
from pyocean.persistence import OceanPersistence
from pyocean.persistence.database import BaseDao, BaseConnection, SingleConnection, MultiConnections
from pyocean.logger import ocean_logger

from mysql.connector import Error
from mysql.connector.cursor import MySQLCursor
from typing import Dict, Tuple, Iterable, Callable, Union
import datetime
import decimal
import os



class TestDao(BaseDao):

    def __init__(self, connection_strategy: OceanPersistence):
        super().__init__(connection_strategy=connection_strategy)
        self._logger = ocean_logger


    def get_test_data(self, *args, **kwargs) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        # Running directly
        if isinstance(self._Connection_Strategy, MultiConnections):
            self._logger.debug("Running all things with Bounded Semaphore.")
            # data = MultiRunnableOperator.run_with_semaphore(function=self.sql_process_new)
            data = MultiRunnableOperator.run_with_bounded_semaphore(function=self.sql_process_new)
            self._logger.debug(f"at fun 'run': {data}")
            return data
        elif isinstance(self._Connection_Strategy, SingleConnection):
            self._logger.debug("Running all things with Lock.")
            return MultiRunnableOperator.run_with_lock(function=self.sql_process_new)
        else:
            pass


    def sql_process_new(self):
        sql_tasks = self.get_all_sql_tasks()
        self._logger.debug(f"SQL tasks: {sql_tasks}")
        sql_query = sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {sql_query}")
        data = self.running_sql_query_process(sql_query=sql_query)
        return data


    def execute_sql(self, cursor: MySQLCursor, query: str) -> object:
        cursor.execute(query)
        return cursor


    def fetch_all(self, cursor: MySQLCursor) -> Union[object, None]:
        return cursor.fetchall()


    def error_handling(self, error: Error) -> Union[object, None]:
        # Print error message
        self._logger.error(f"Got an error! ")
        self._logger.error(f"error: {error}")
        self._logger.error(f"e.sqlstate: {error.sqlstate}")
        self._logger.error(f"e.errno: {error.errno}")
        self._logger.error(f"e.msg: {error.msg}")
        return None


    def executing_result(self, running_state, data, exception_info) -> Dict[str, object]:
        self._logger.debug(f"SQL result data: {data}")
        __handled_data = data
        if __handled_data is not None:
            __handled_data = self.iterate_data_rows(data=data)
        self._logger.debug(f"Handling finish and final data is: {__handled_data}")
        return {
            "pid": os.getpid(),
            "state": running_state,
            "data": __handled_data,
            "exception_info": exception_info
        }


    def iterate_data_rows(self, data: Tuple[Tuple]):
        new_data = map(self.__data_type_handling, data)
        return list(new_data)


    def __data_type_handling(self, data: Iterable):
        new_data = []
        for d in data:
            if isinstance(d, datetime.datetime):
                f = '%Y-%m-%d %H:%M:%S'
                new_d = datetime.datetime.strftime(d, f)
                new_data.append(new_d)
            if isinstance(d, decimal.Decimal):
                new_d = float(d)
                new_data.append(new_d)
        return new_data



class AsyncTestDao(BaseDao):

    def __init__(self, connection_strategy: OceanPersistence):
        super().__init__(connection_strategy=connection_strategy)
        self._logger = ocean_logger


    async def get_test_data(self, *args, **kwargs) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        # Running directly
        if isinstance(self._Connection_Strategy, MultiConnections):
            self._logger.debug("Running all things with Bounded Semaphore.")
            # data = await AsyncRunnableOperator.run_with_semaphore(function=self.sql_process_new)
            data = await AsyncRunnableOperator.run_with_bounded_semaphore(function=self.sql_process_new)
            self._logger.debug(f"at fun 'run': {data}")
            return data
        elif isinstance(self._Connection_Strategy, SingleConnection):
            self._logger.debug("Running all things with Lock.")
            return AsyncRunnableOperator.run_with_lock(function=self.sql_process_new)
        else:
            pass


    async def sql_process_new(self):
        sql_tasks = self.get_all_sql_tasks()
        self._logger.debug(f"SQL tasks: {sql_tasks}")
        sql_query = await sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {sql_query}")
        data = self.running_sql_query_process(sql_query=sql_query)
        return data


    def execute_sql(self, cursor: MySQLCursor, query: str) -> object:
        cursor.execute(query)
        return cursor


    def fetch_all(self, cursor: MySQLCursor) -> Union[object, None]:
        return cursor.fetchall()


    def error_handling(self, error: Error) -> Union[object, None]:
        # Print error message
        self._logger.error(f"Got an error! ")
        self._logger.error(f"error: {error}")
        self._logger.error(f"e.sqlstate: {error.sqlstate}")
        self._logger.error(f"e.errno: {error.errno}")
        self._logger.error(f"e.msg: {error.msg}")
        return None


    def executing_result(self, running_state, data, exception_info) -> Dict[str, object]:
        return {"pid": os.getpid(), "state": running_state, "data": data, "exception_info": exception_info}


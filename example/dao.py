from pyocean.framework.builder import RunnableBuilder
from pyocean.persistence.database.connection import BaseConnection
from pyocean.persistence.database.single_connection import SingleConnection
from pyocean.persistence.database.multi_connections import MultiConnections
from pyocean.persistence.database.access_object import BaseDao
from pyocean.logging.level import Logger

from mysql.connector import Error
from mysql.connector.cursor import MySQLCursor
from typing import Dict, Callable, Union
import os



class TestDao(BaseDao):

    def __init__(self, connection_strategy: BaseConnection, logger: Logger):
        super().__init__(connection_strategy=connection_strategy)


    def run(self) -> object:
        """
        Note (?) need to consider:
            How to abstractilize the logic or how to be more clear ?
        :return:
        """
        # Running directly
        if isinstance(self._Connection_Strategy, MultiConnections):
            self._logger.debug("Running all things with Bounded Semaphore.")
            # data = RunnableBuilder.run_with_semaphore(function=self.sql_process_new)
            data = RunnableBuilder.run_with_bounded_semaphore(function=self.sql_process_new)
            print("[DEBUG] at fun 'run': ", data)
            return data
        else:
            self._logger.debug("Running all things with Lock.")
            return RunnableBuilder.run_with_lock(function=self.sql_process_new)


    def sql_process_new(self):
        sql_tasks = self.get_all_sql_tasks()
        self._logger.debug(f"SQL tasks: {sql_tasks}")
        sql_query = sql_tasks.get()
        self._logger.debug(f"SQL tasks query: {sql_query}")
        data = self.running_sql_query_process(sql_query=sql_query)
        self._logger.debug(f"at fun 'sql_process_new': {data}")
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

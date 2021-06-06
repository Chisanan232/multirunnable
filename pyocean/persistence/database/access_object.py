from pyocean.operator import MultiRunnableOperator, AsyncRunnableOperator
from pyocean.persistence.interface import OceanPersistence, OceanDao
from pyocean.persistence.mode import PersistenceMode
from pyocean.persistence.database.connection import BaseConnection
from pyocean.persistence.database.exceptions import PersistenceModeIsInvalid

from abc import ABC, abstractmethod
from typing import Dict, Union
import os



class BaseDao(OceanDao):

    _Connection_Strategy: BaseConnection = None

    def __init__(self, connection_strategy: OceanPersistence):
        self._Connection_Strategy = connection_strategy


    def get_connection(self) -> object:
        """
        Description:
            Get one connection instance.
        :return:
        """
        return self._Connection_Strategy.get_one_connection()


    def get_cursor(self, connection: object) -> object:
        """
        Description:
            Get cursor of one specific connection instance.
        :param connection:
        :return:
        """
        return self._Connection_Strategy.build_cursor(connection=connection)


    def close_connection_instance(self, connection: object, cursor: object) -> None:
        """
        Description:
            Close the database instance including connection (session) or cursor of it.
        :param connection:
        :param cursor:
        :return:
        """
        self._Connection_Strategy.close_instance(connection=connection, cursor=cursor)


    def get_one_sql_task(self) -> object:
        """
        Description: (is it used ?)
            Get one task from Queue.
        :return:
        """
        return MultiRunnableOperator.get_one_value_of_queue()


    def get_all_sql_tasks(self) -> object:
        """
        Description: (is it used ?)
            Get all tasks (Queue).
        :return:
        """
        return MultiRunnableOperator.get_queue()


    def running_sql_query_process(self, sql_query: str) -> Dict[str, object]:
        """
        Description:
            Running a SQL query process.
            The procedure is get instance (connection and cursor) -> execute query
            (if occur error -> catch the exception and do something) -> close instance.
        :param sql_query:
        :return:
        """
        connection = None
        cursor = None
        data = None
        exception_info = None

        try:
            connection = self.get_connection()
            cursor = self.get_cursor(connection=connection)
            print(f"[DEBUG] connection: {connection} - {os.getpid()}")
            print(f"[DEBUG] cursor: {cursor} - {os.getpid()}")
        except Exception as e:
            exception_info = e
            self.error_handling(error=e)
            running_state = False
        else:
            cursor = self.execute_sql(cursor=cursor, query=sql_query)
            data = self.fetch_all(cursor=cursor)
            running_state = True
        finally:
            self.close_connection_instance(connection=connection, cursor=cursor)

        return self.executing_result(running_state=running_state, data=data, exception_info=exception_info)


    @abstractmethod
    def execute_sql(self, cursor: object, query: str) -> object:
        """
        Description:
            Execute SQL query.
        :param cursor:
        :param query:
        :return:
        """
        pass


    @abstractmethod
    def fetch_all(self, cursor: object) -> Union[object, None]:
        """
        Description: (is it used?)
            Get the query result.
        :param cursor:
        :return:
        """
        pass


    @abstractmethod
    def error_handling(self, error: Exception) -> Union[object, None]:
        """
        Description:
            Do something if occur any exception.
        :param error:
        :return:
        """
        pass


    @abstractmethod
    def executing_result(self, running_state, data, exception_info) -> Dict[str, object]:
        """
        Description:
            Handling to be final data result.
            Like below:
              pass {"pid": os.getpid(), "state": running_state}
        :return:
        """
        pass



class AbstractedMultiWorkBaseDao(BaseDao):

    @abstractmethod
    def query_with_lock(self, sql_query: str):
        pass


    @abstractmethod
    def query_with_rlock(self, sql_query: str):
        pass


    @abstractmethod
    def query_with_semaphore(self, sql_query: str):
        pass


    @abstractmethod
    def query_with_bounded_semaphore(self, sql_query: str):
        pass



class AbstractedAsyncBaseDao(BaseDao):

    @abstractmethod
    async def query_with_lock(self, sql_query: str):
        pass


    @abstractmethod
    async def query_with_rlock(self, sql_query: str):
        pass


    @abstractmethod
    async def query_with_semaphore(self, sql_query: str):
        pass


    @abstractmethod
    async def query_with_bounded_semaphore(self, sql_query: str):
        pass



class MultiWorkBaseDao(AbstractedMultiWorkBaseDao, ABC):

    def get_one_sql_task(self) -> object:
        """
        Description: (is it used ?)
            Get one task from Queue.
        :return:
        """
        return MultiRunnableOperator.get_one_value_of_queue()


    def get_all_sql_tasks(self) -> object:
        """
        Description: (is it used ?)
            Get all tasks (Queue).
        :return:
        """
        return MultiRunnableOperator.get_queue()


    def query_with_lock(self, sql_query: str):
        data = MultiRunnableOperator.run_with_lock(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        return data


    def query_with_rlock(self, sql_query: str):
        data = MultiRunnableOperator.run_with_lock(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        return data


    def query_with_semaphore(self, sql_query: str):
        data = MultiRunnableOperator.run_with_semaphore(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        print(f"at fun 'run': {data}")
        return data


    def query_with_bounded_semaphore(self, sql_query: str):
        data = MultiRunnableOperator.run_with_bounded_semaphore(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        print(f"at fun 'run': {data}")
        return data


    def run_with_mode(self, mode: PersistenceMode, sql_query: str):
        if mode is PersistenceMode.SINGLE_DATABASE_CONNECTION:
            data = MultiRunnableOperator.run_with_lock(
                function=self.running_sql_query_process,
                kwarg={"sql_query": sql_query}
            )
        elif mode is PersistenceMode.MULTI_DATABASE_CONNECTION:
            data = MultiRunnableOperator.run_with_bounded_semaphore(
                function=self.running_sql_query_process,
                kwarg={"sql_query": sql_query}
            )
        else:
            raise PersistenceModeIsInvalid

        return data



class AsyncBaseDao(AbstractedAsyncBaseDao, ABC):

    async def get_one_sql_task(self) -> object:
        """
        Description: (is it used ?)
            Get one task from Queue.
        :return:
        """
        return await AsyncRunnableOperator.get_one_value_of_queue()


    def get_all_sql_tasks(self) -> object:
        """
        Description: (is it used ?)
            Get all tasks (Queue).
        :return:
        """
        return AsyncRunnableOperator.get_queue()


    async def query_with_lock(self, sql_query: str):
        data = await AsyncRunnableOperator.run_with_lock(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        return data


    async def query_with_rlock(self, sql_query: str):
        data = await AsyncRunnableOperator.run_with_lock(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        return data


    async def query_with_semaphore(self, sql_query: str):
        data = await AsyncRunnableOperator.run_with_semaphore(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        print(f"at fun 'run': {data}")
        return data


    async def query_with_bounded_semaphore(self, sql_query: str):
        data = await AsyncRunnableOperator.run_with_bounded_semaphore(
            function=self.running_sql_query_process,
            kwarg={"sql_query": sql_query}
        )
        print(f"at fun 'run': {data}")
        return data


    async def run_with_mode(self, mode: PersistenceMode, sql_query: str):
        if mode is PersistenceMode.SINGLE_DATABASE_CONNECTION:
            data = await AsyncRunnableOperator.run_with_lock(
                function=self.running_sql_query_process,
                kwarg={"sql_query": sql_query}
            )
        elif mode is PersistenceMode.MULTI_DATABASE_CONNECTION:
            data = await AsyncRunnableOperator.run_with_bounded_semaphore(
                function=self.running_sql_query_process,
                kwarg={"sql_query": sql_query}
            )
        else:
            raise PersistenceModeIsInvalid

        return data


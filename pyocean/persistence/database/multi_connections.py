from pyocean.framework.strategy import Globalize as RunningGlobalize
from pyocean.api.features_adapter import RunningMode, RunningStrategyAPI
from pyocean.persistence.database.connection import BaseConnection
from pyocean.exceptions import GlobalizeObjectError

from abc import abstractmethod
from typing import Callable, Union, cast

from deprecation import deprecated


Database_Connection_Pool: object = None


class MultiConnections(BaseConnection):

    __Connection_Pool_Name: str = "stock_crawler"


    def initialize(self, mode: RunningMode, **kwargs) -> None:
        """
        Description:
            Target to initialize Process Semaphore and Database connection pool object, and globalize them to let
            processes to use.
        Note:
            RLock mostly like Semaphore, so doesn't do anything with RLock currently.
        :param mode:
        :param kwargs:
        :return:
        """
        # # Get value
        __db_connection_instances_number = cast(int, kwargs["db_conn_instances_num"])
        __pool_name = kwargs.get("pool_name", self.__Connection_Pool_Name)

        __running_feature_api = RunningStrategyAPI(mode=mode)
        # # Semaphore part (Limitation)
        __bounded_semaphore = __running_feature_api.bounded_semaphore(value=__db_connection_instances_number)
        RunningGlobalize.bounded_semaphore(bsmp=__bounded_semaphore)

        # # Database Connections Pool part
        # Initialize the Database Connection Instances Pool.
        database_connections_pool = self.connect_database(pool_name=__pool_name, pool_size=__db_connection_instances_number)
        # Globalize object to share between different multiple processes
        Globalize.connection_pool(pool=database_connections_pool)


    @property
    def database_connection_pool(self) -> object:
        """
        Description:
            Get the database connection pool which has been globalized.
        :return:
        """
        return Database_Connection_Pool


    @abstractmethod
    def set_pool_size(self, pool_size: int) -> None:
        """
        Description:
            Set the database connection pool size.
        :return:
        """
        pass


    @abstractmethod
    def close_pool(self) -> None:
        """
        Description:
            Close the database connection pool instance.
        :return:
        """
        pass



class Globalize:

    @staticmethod
    def connection_pool(pool):
        if pool is not None:
            global Database_Connection_Pool
            Database_Connection_Pool = pool
        else:
            raise GlobalizeObjectError


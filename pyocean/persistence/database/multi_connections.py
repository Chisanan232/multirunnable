from pyocean.framework.strategy import Globalize as RunningGlobalize
from pyocean.framework.features import BaseQueueType
from pyocean.api.features_adapter import RunningMode, RunningStrategyAPI
from pyocean.persistence.database.connection import BaseConnection
from pyocean.exceptions import GlobalizeObjectError

from abc import abstractmethod
from typing import List, Tuple, Dict, Iterable, Callable, Union, cast
import re

from deprecation import deprecated


Database_Connection_Pool: object = None


class MultiConnections(BaseConnection):

    __Connection_Pool_Name: str = "stock_crawler"


    def initialize(self, mode: RunningMode, queue_type: BaseQueueType, **kwargs) -> None:
        """
        Description:
            Target to initialize Process Semaphore and Database connection pool object, and globalize them to let
            processes to use.
        Note:
            RLock mostly like Semaphore, so doesn't do anything with RLock currently.
        :param queue_type:
        :param mode:
        :param kwargs:
        :return:
        """
        # Get value
        # tasks_queue = self.__get_value(param=kwargs.get("tasks_queue", None))
        db_connection_instances_number = cast(int, self.__get_value(param=kwargs.get("db_connection_instances_number", None)))
        # limited_obj = self.__get_value(param=kwargs.get("limited_obj", None))
        pool_name = kwargs.get("pool_name", self.__Connection_Pool_Name)

        # # # Older version written (version 0.6)
        # # Initialize process semaphore
        # limitation_obj = getattr(limitation, mode.value)(value=db_connection_instances_number)
        # # Globalize object to share between different multiple processes
        # globalize_fun = getattr(limitation, "Globalize")
        # globalize_fun(limitation_obj)

        # # # Latest version written (version 0.7)
        # # Queue part (Limitation)
        __running_feature_api = RunningStrategyAPI(mode=mode)
        __queue = __running_feature_api.queue(qtype=queue_type)
        RunningGlobalize.queue(queue=__queue)

        # # Semaphore part (Limitation)
        __running_feature_api = RunningStrategyAPI(mode=mode)
        __bounded_semaphore = __running_feature_api.bounded_semaphore(value=db_connection_instances_number)
        RunningGlobalize.bounded_semaphore(bsmp=__bounded_semaphore)

        # # Database Connections Pool part
        # Initialize the Database Connection Instances Pool.
        database_connections_pool = self.connect_database(pool_name=pool_name, pool_size=db_connection_instances_number)
        # Globalize object to share between different multiple processes
        Globalize.connection_pool(pool=database_connections_pool)


    @deprecated(deprecated_in="0.6", removed_in="0.8", details="Adjust the software architecture")
    def __get_value(self, param: object) -> Union[object, Callable]:
        if param is None:
            raise Exception("Parameter object shouldn't be empty.")
        else:
            return param


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


    @deprecated(deprecated_in="0.2", removed_in="0.7", details="Move the abstracted method up to parent class.")
    @abstractmethod
    def get_one_connection(self) -> object:
        """
        Description:
            Get one database connection instance.
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


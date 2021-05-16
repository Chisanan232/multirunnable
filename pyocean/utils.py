import re



class Utils:

    @staticmethod
    def parse_class_name(object_char: object) -> str:
        """
        Description:
            Parse the object package and class name.
        :param object_char:
        :return:
        """

        if re.search(r"<class \'\w{0,64}\.\w{0,64}\'>", str(object_char), re.IGNORECASE) is not None:
            return str(object_char).split(".")[-1].split("'>")[0]
        else:
            raise Exception("Cannot parse the class instance string")


    @staticmethod
    def is_queue_obj(obj: object) -> bool:
        """
        Description:
             Return True if object type is Queue.
        :param obj:
        :return:
        """
        return re.search(r"queue", repr(obj), re.IGNORECASE) is not None


    @staticmethod
    def is_lock_obj(obj: object) -> bool:
        """
        Description:
             Return True if object type is Lock.
        :param obj:
        :return:
        """
        return re.search(r"lock", repr(obj), re.IGNORECASE) is not None


    @staticmethod
    def is_semaphore_obj(obj: object) -> bool:
        """
        Description:
             Return True if object type is Semaphore.
        :param obj:
        :return:
        """
        return re.search(r"semaphore", repr(obj), re.IGNORECASE) is not None


    @staticmethod
    def is_connection_obj(obj: object) -> bool:
        """
        Description:
             Return True if object type is Database Connection.
        :param obj:
        :return:
        """
        return re.search(r"connection", repr(obj), re.IGNORECASE) is not None


    @staticmethod
    def is_pool_obj(obj: object) -> bool:
        """
        Description:
             Return True if object type is Connection Pool.
        :param obj:
        :return:
        """
        return re.search(r"pool", repr(obj), re.IGNORECASE) is not None


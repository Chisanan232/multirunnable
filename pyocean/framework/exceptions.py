
class ParameterCannotBeEmpty(Exception):

    def __init__(self, param: str):
        self.__param = param


    def __str__(self):
        return f"The parameter '{self.__param} shouldn't be empty.'"

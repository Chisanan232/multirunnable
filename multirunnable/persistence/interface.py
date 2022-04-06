from abc import ABCMeta

from .._singletons import NamedSingletonABCMeta



class BasePersistence(metaclass=NamedSingletonABCMeta):
    pass



class DataPersistenceLayer(metaclass=ABCMeta):
    pass

